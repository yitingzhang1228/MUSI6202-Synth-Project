import numpy as np
import soundfile as sf

from .PlayingNotes import Instrument
from .BiquadFilters import BiquadFilter
from .ModulatedEffects import Echo, Tremolo, FlangerFB, SimpleChorus
from. Reverb import Reverb


class Orchestra(object):
    def __init__(self, bufSize, synthEngine, filters=None, effects=None):
        self.bufSize = bufSize
        self.instruments = []
        for synth in synthEngine:
            self.instruments.append(Instrument(synth))

        self.filters = []
        if filters:
            for filter in filters:
                self.filters.append(BiquadFilter(filter[0], f0=filter[1]))

        self.globalEffects = []
        if effects:
            for effect in effects:
                if effect == 'Echo':
                    self.globalEffects.append(Echo())
                elif effect == 'Tremolo':
                    self.globalEffects.append(Tremolo())
                elif effect == 'Flanger':
                    self.globalEffects.append(FlangerFB())
                elif effect == 'Chorus':
                    self.globalEffects.append(SimpleChorus())
                elif effect == 'Cathedral' or 'Hall' or 'Plate' or 'Room' or 'Tunnel':
                    self.globalEffects.append(Reverb(self.bufSize, effect))
                else:
                    raise RuntimeError("Invalid effect type")
        self.globalEffects.append(BiquadFilter('LP'))
        self.globalEffects.append(BiquadFilter('HP'))

    def render(self, buffer):
        for instrument in self.instruments:
            instrument.render(buffer)

        if self.filters:
            output = np.zeros(len(buffer))
            for filter in self.filters:
                output += filter.process(buffer)
            for i in range(len(buffer)):
                buffer[i] = output[i]

        for effect in self.globalEffects:
            effect.render(buffer)


class Score(object):
    def __init__(self, bufSize, synthEngine, notes, filters=None, effects=None):
        self.sr = 48000
        self.orchestra = Orchestra(bufSize, synthEngine, filters, effects)
        self.notes = notes
        self.noteIdx = 0
        self.beatLengthInSamples = int(0.75 * self.sr)
        self.curBeatPos = 0

    def render(self, buffer):
        while self.curBeatPos <= 0:
            for i in range(len(self.orchestra.instruments)):
                self.orchestra.instruments[i].playNote(self.notes[self.noteIdx])
            self.noteIdx = (self.noteIdx + 1) % len(self.notes)
            self.curBeatPos += self.beatLengthInSamples
        self.orchestra.render(buffer)
        self.curBeatPos -= len(buffer)


def playScore(filename, length, synthEngine, notes, filters, effects):
    sr = 48000
    bufSize = 4096
    buffer = np.zeros(bufSize)
    lengthSamples = int(length * sr)
    numBlocks = int(lengthSamples / bufSize) + 1
    outputBuffer = np.zeros(lengthSamples)
    score = Score(bufSize=bufSize, synthEngine=synthEngine, notes=notes, filters=filters, effects=effects)

    for i in range(numBlocks):
        buffer *= 0
        if i == numBlocks - 1:
            buffer = np.zeros(lengthSamples - (numBlocks - 1) * bufSize)
        score.render(buffer)
        outputBuffer[bufSize * i: bufSize * (i + 1)] = buffer
    outputBuffer = outputBuffer / max(outputBuffer)

    with sf.SoundFile(filename, 'wb', sr, 1) as f:
        f.write(outputBuffer)


def playAudio(inFile, outFile, filters=None, effects=None):
    x, sr = sf.read(inFile)
    bufSize = 4096
    lengthSamples = len(x)
    numBlocks = int(lengthSamples / bufSize) + 1
    outputBuffer = np.zeros(lengthSamples)

    myFilters = []
    if filters:
        for filter in filters:
            myFilters.append(BiquadFilter(filter[0], f0=filter[1]))

    myEffects = []
    if effects:
        for effect in effects:
            if effect == 'Echo':
                myEffects.append(Echo())
            elif effect == 'Tremolo':
                myEffects.append(Tremolo())
            elif effect == 'Flanger':
                myEffects.append(FlangerFB())
            elif effect == 'Chorus':
                myEffects.append(SimpleChorus())
            elif effect == 'Cathedral' or 'Hall' or 'Plate' or 'Room' or 'Tunnel':
                myEffects.append(Reverb(bufSize, effect))
            else:
                raise RuntimeError("Invalid effect type")

    for i in range(numBlocks):
        buffer = x[bufSize * i: bufSize * (i + 1)]
        if filters:
            output = np.zeros(len(buffer))
            for filter in myFilters:
                output += filter.process(buffer)
            for j in range(len(buffer)):
                buffer[j] = output[j]
        if effects:
            for effect in myEffects:
                effect.render(buffer)
        outputBuffer[bufSize * i: bufSize * (i + 1)] = buffer
    outputBuffer = outputBuffer / max(outputBuffer)

    with sf.SoundFile(outFile, 'wb', sr, 1) as f:
        f.write(outputBuffer)
