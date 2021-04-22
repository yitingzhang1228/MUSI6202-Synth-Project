import numpy as np
import math

from .SynthEngine import SineWaveNaive, SquareWaveAdditive, SawWaveAdditive, \
    SineWaveWavetable, SquareWaveWavetable, SawWaveWavetable

noteMap = {
    'Ab': -11,
    'A': 12,
    'A#': 13,
    'Bb': 13,
    'B': 14,
    'C': 3,
    'C#': 4,
    'Db': 4,
    'D': 5,
    'D#': 6,
    'Eb': 6,
    'E': 7,
    'F': 8,
    'F#': 9,
    'Gb': 9,
    'G': 10,
    'G#': 11,
}


# Pass in tuple, for example ('A', 4)
def noteToHz(note):
    halfNotes = noteMap.get(note[0], None)
    if halfNotes is None:
        raise RuntimeError("Invalid note entered")
    midiNote = 21 + halfNotes + (12 * note[1])
    return math.pow(2, float(midiNote-69) / 12.0) * 440.0


# Attack, Decay, Release
class ADSR(object):
    def __init__(self, atk, dec, sus, rel):
        self.sr = 48000
        self.atk = int(atk * self.sr)
        self.dec = int(dec * self.sr)
        self.sus = sus
        self.rel = int(rel * self.sr)
        self.pos = 0
        self.lastVal = 0
        self.isNoteOn = True

    def noteOff(self):
        if self.isNoteOn:
            self.isNoteOn = False
            self.pos = 0

    def hasEnded(self):
        return not self.isNoteOn and self.pos > self.rel

    def render(self, buffer):
        for i in range(len(buffer)):
            val = 0
            if self.isNoteOn:
                if self.pos < self.atk:
                    val = float(self.pos) / float(self.atk)
                elif self.pos < (self.atk + self.dec):
                    a = float(self.pos - self.atk) / self.dec
                    val = (1 - a) + self.sus * a
                else:
                    val = self.sus
                self.lastVal = val
            else:
                if self.pos < self.rel:
                    a = float(self.pos) / float(self.rel)
                    val = (1 - a) * self.lastVal
            buffer[i] = buffer[i] * val
            self.pos += 1


class PlayingNote(object):
    def __init__(self, note, noteLength, amp, synth):
        self.sr = 48000
        self.effects = []
        self.amp = amp
        self.lifetimeSamples = noteLength * self.sr
        # self.envelope = ADSR(0.1, 0.1, 0.4, 0.1)
        self.envelope = ADSR(0.02, 0.05, 0.2, 0.3)
        if synth == 'SineWaveNaive':
            self.source = SineWaveNaive(noteToHz(note))
        elif synth == 'SquareWaveAdditive':
            self.source = SquareWaveAdditive(noteToHz(note))
        elif synth == 'SawWaveAdditive':
            self.source = SawWaveAdditive(noteToHz(note))
        elif synth == 'SineWaveWavetable':
            self.source = SineWaveWavetable(noteToHz(note))
        elif synth == 'SquareWaveWavetable':
            self.source = SquareWaveWavetable(noteToHz(note))
        elif synth == 'SawWaveWavetable':
            self.source = SawWaveWavetable(noteToHz(note))
        else:
            raise RuntimeError("Invalid synth name")

    def hasEnded(self):
        return self.envelope.hasEnded()

    def render(self, buffer):
        outBuffer = np.zeros(len(buffer))
        self.source.render(outBuffer)
        outBuffer *= self.amp
        self.envelope.render(outBuffer)

        if self.lifetimeSamples > 0:
            self.lifetimeSamples -= len(buffer)
            if self.lifetimeSamples <= 0:
                self.envelope.noteOff()

        for effect in self.effects:
            effect.render(outBuffer)

        buffer += outBuffer


class Instrument(object):
    def __init__(self, synth):
        self.synth = synth
        self.playingNotes = []
        self.instrumentEffects = []

    def makePlayingNote(self, note):
        return PlayingNote(note, 1, 0.25, self.synth)

    def playNote(self, note):
        self.playingNotes.append(self.makePlayingNote(note))

    def render(self, buffer):
        for playingNote in self.playingNotes:
            playingNote.render(buffer)
        for effect in self.instrumentEffects:
            effect.render(buffer)

        # Cleanup finished notes
        self.playingNotes = list(filter(lambda playingNote: not playingNote.hasEnded(),
                                        self.playingNotes))
