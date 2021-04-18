import math

from .RingBuffer import RingBuffer, LinearWrap, LinearRingBuffer


class Echo(object):
    def __init__(self, BL=0.5):
        self.sr = 48000
        self.BL = BL
        self.delayTime = 0.25
        self.delaySamps = int(self.delayTime * self.sr)
        self.ringBuf = RingBuffer(self.delaySamps)

    def render(self, buffer):
        for i in range(len(buffer)):
            s = buffer[i]
            self.ringBuf.pushSample(s)
            buffer[i] = s * self.BL + self.ringBuf.delayedSample(self.delaySamps) * 0.5


class Tremolo(object):
    def __init__(self, BL=0.5):
        self.sr = 48000
        self.fmod = 5
        self.alpha = 0.5
        self.BL = BL
        self.phi = 0

    def render(self, buffer):
        x = LinearWrap(buffer)
        deltaPhi = self.fmod / self.sr

        for i in range(len(buffer)):
            s = x[i]
            trem = 1 + self.alpha * math.sin(2 * math.pi * self.phi)
            buffer[i] = s * self.BL + s * trem

            self.phi = self.phi + deltaPhi
            while self.phi >= 1:
                self.phi -= 1


class SimpleChorus(object):
    def __init__(self, BL=1):
        self.sr = 48000
        self.fmod = 1.5
        self.A = int(0.002 * self.sr)
        self.M = int(0.002 * self.sr)
        self.BL = BL
        self.FF = 0.7
        self.maxDelaySamps = self.M + self.A + 2
        self.ringBuf = LinearRingBuffer(self.maxDelaySamps)
        self.phi = 0

    def render(self, buffer):
        x = LinearWrap(buffer)
        deltaPhi = self.fmod / self.sr

        for i in range(len(buffer)):
            s = x[i]
            self.ringBuf.pushSample(s)
            delaySamps = math.sin(2 * math.pi * self.phi) * self.maxDelaySamps
            buffer[i] = s * self.BL + self.ringBuf.delayedSample(delaySamps) * self.FF

            self.phi = self.phi + deltaPhi
            while self.phi >= 1:
                self.phi -= 1


class FlangerFB(object):
    def __init__(self, BL=0.7):
        self.sr = 48000
        self.fmod = 0.1
        self.A = int(0.005 * self.sr)
        self.M = int(0.005 * self.sr)
        self.BL = BL
        self.FF = 0.7
        self.FB = -0.7
        self.maxDelaySamps = self.M + self.A + 2
        self.ringBuf = LinearRingBuffer(self.maxDelaySamps)
        self.prevDelaySamp = 0
        self.phi = 0

    def render(self, buffer):
        x = LinearWrap(buffer)
        deltaPhi = self.fmod / self.sr

        for i in range(len(buffer)):
            s = x[i] + self.prevDelaySamp * self.FB
            self.ringBuf.pushSample(s)
            delaySamps = self.M + math.sin(2 * math.pi * self.phi) * self.A
            self.prevDelaySamp = self.ringBuf.delayedSample(delaySamps)
            buffer[i] = s * self.BL + self.prevDelaySamp * self.FF

            self.phi = self.phi + deltaPhi
            while self.phi >= 1:
                self.phi -= 1
