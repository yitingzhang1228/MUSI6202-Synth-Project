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
            for filter in filters[0]:
                self.filters.append(BiquadFilter(filter[0], f0=filter[1]))
            self.filterConnection = filters[1]

        self.globalEffects = []
        if effects:
            for effect in effects:
                if effect[0].lower() == 'echo':
                    self.globalEffects.append(Echo(BL=effect[1]))
                elif effect[0].lower() == 'tremolo':
                    self.globalEffects.append(Tremolo(BL=effect[1]))
                elif effect[0].lower() == 'flanger':
                    self.globalEffects.append(FlangerFB(BL=effect[1]))
                elif effect[0].lower() == 'chorus':
                    self.globalEffects.append(SimpleChorus(BL=effect[1]))
                elif effect[0].lower() == 'cathedral' or 'hall' or 'plate' or 'room' or 'tunnel':
                    self.globalEffects.append(Reverb(bufSize=self.bufSize, type=effect[0].lower(), BL=effect[1]))
                else:
                    raise RuntimeError("Invalid effect type")

    def render(self, buffer):
        for instrument in self.instruments:
            instrument.render(buffer)

        if self.filters:
            if self.filterConnection == 'parallel':
                output = np.zeros(len(buffer))
                for filter in self.filters:
                    output += filter.process(buffer)
                for i in range(len(buffer)):
                    buffer[i] = output[i]
            elif self.filterConnection == 'series':
                for filter in self.filters:
                    filter.render(buffer)

        for effect in self.globalEffects:
            effect.render(buffer)


class Score(object):
    def __init__(self, bufSize, synthEngine, notes, filters=None, effects=None):
        self.sr = 48000
        self.orchestra = Orchestra(bufSize, synthEngine, filters, effects)
        self.notes = notes
        self.noteIdx = 0
        self.beatLengthInSamples = int(0.5 * self.sr)
        self.curBeatPos = 0

    def render(self, buffer):
        while self.curBeatPos <= 0:
            for i in range(len(self.orchestra.instruments)):
                self.orchestra.instruments[i].playNote(self.notes[self.noteIdx])
            self.noteIdx = (self.noteIdx + 1) % len(self.notes)
            self.curBeatPos += self.beatLengthInSamples
        self.orchestra.render(buffer)
        self.curBeatPos -= len(buffer)


def SR_convert(inputBuffer, srIn, srOut=44100):
    """
    convert the inputBuffer array to new sampling rate, srOut
    return: numpy array
    """
    ratio = srIn / srOut
    inputBufferLength  = len(inputBuffer)
    outputBufferLength = int(inputBufferLength / ratio)
    outputBuffer = np.zeros(outputBufferLength)
    for i in range(outputBufferLength):
        idx_float = i*ratio  # float location
        idx_int = int(idx_float)  # floor int location
        # avoid bound error
        zero = idx_int - 1
        two = idx_int + 1
        three = idx_int + 2
        if zero < 0:
            zero = 0
        if three > inputBufferLength - 1:
            two = inputBufferLength - 1
            three = inputBufferLength - 1
        if three > inputBufferLength - 2:
            three = inputBufferLength - 1
        y0 = inputBuffer[zero]
        y1 = inputBuffer[idx_int]
        y2 = inputBuffer[two]
        y3 = inputBuffer[three]
        mu = idx_float - idx_int
        # Cubic Interpretation
        mu2 = mu * mu
        a0 = y3 - y2 - y0 + y1
        a1 = y0 - y1 - a0
        a2 = y2 - y0
        a3 = y1
        value = a0 * mu * mu2 + a1 * mu2 + a2 * mu + a3
        outputBuffer[i] = value
    return outputBuffer


def playScore(filename, length, synthEngine, notes, filters, effects, output_samplingRate, bitDepth=24):
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

    outputBuffer = SR_convert(outputBuffer, sr, output_samplingRate)

    #add -80dB triangular noise
    for i in range(len(outputBuffer)):
        outputBuffer[i] = outputBuffer[i] + 0.00001 * np.random.triangular(-1, 0, 1)

    if bitDepth == 24:
        format = 'PCM_24'
    elif bitDepth == 16:
        format = 'PCM_16'
    else:
        print("bitDepth not supported, default PCM_16")
        format = 'PCM_16'

    outputBuffer = outputBuffer / max(outputBuffer)
    with sf.SoundFile(filename, 'wb', output_samplingRate, 1, format) as f:
        f.write(outputBuffer)


def playAudio(inFile, outFile, filters=None, effects=None, output_samplingRate=44100, bitDepth=24):
    x, sr = sf.read(inFile)
    bufSize = 4096
    lengthSamples = len(x)
    numBlocks = int(lengthSamples / bufSize) + 1
    outputBuffer = np.zeros(lengthSamples)

    myFilters = []
    if filters:
        for filter in filters[0]:
            myFilters.append(BiquadFilter(filter[0], f0=filter[1]))

    myEffects = []
    if effects:
        for effect in effects:
            if effect[0].lower() == 'echo':
                myEffects.append(Echo(BL=effect[1]))
            elif effect[0].lower() == 'tremolo':
                myEffects.append(Tremolo(BL=effect[1]))
            elif effect[0].lower() == 'flanger':
                myEffects.append(FlangerFB(BL=effect[1]))
            elif effect[0].lower() == 'chorus':
                myEffects.append(SimpleChorus(BL=effect[1]))
            elif effect[0].lower() == 'cathedral' or 'hall' or 'plate' or 'room' or 'tunnel':
                myEffects.append(Reverb(bufSize=bufSize, type=effect[0].lower(), BL=effect[1]))
            else:
                raise RuntimeError("Invalid effect type")

    for i in range(numBlocks):
        buffer = x[bufSize * i: bufSize * (i + 1)]
        if filters:
            if filters[1] == 'parallel':
                output = np.zeros(len(buffer))
                for filter in myFilters:
                    output += filter.process(buffer)
                for j in range(len(buffer)):
                    buffer[j] = output[j]
            elif filters[1] == 'series':
                for filter in myFilters:
                    filter.render(buffer)
        if effects:
            for effect in myEffects:
                effect.render(buffer)
        outputBuffer[bufSize * i: bufSize * (i + 1)] = buffer

    outputBuffer = SR_convert(outputBuffer, sr, output_samplingRate)

    #add -80dB triangular noise
    for i in range(len(outputBuffer)):
        outputBuffer[i] = outputBuffer[i] + 0.00001 * np.random.triangular(-1, 0, 1)

    if bitDepth == 24:
        format = 'PCM_24'
    elif bitDepth == 16:
        format = 'PCM_16'
    else:
        print("bitDepth not supported, default PCM_16")
        format = 'PCM_16'

    outputBuffer = outputBuffer / max(outputBuffer)
    with sf.SoundFile(outFile, 'wb', output_samplingRate, 1, format) as f:
        f.write(outputBuffer)

    #with sf.SoundFile(outFile, 'wb', 44100, 1, 'PCM_24') as f:
    #    f.write(outputBuffer)
