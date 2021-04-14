import math
import numpy as np


class BiquadFilter(object):
    def __init__(self, filterType, f0=None):
        self.filterType = filterType  # 'HP' or 'LP'
        self.sr = 48000
        if f0 is None and filterType == 'LP':
            self.f0 = 3000
        elif f0 is None and filterType == 'HP':
            self.f0 = 1000
        else:
            self.f0 = f0  # center frequency
        self.q = 1  # Q factor
        self.xn1 = 0  # x[n-1]
        self.xn2 = 0  # x[n-2]
        self.yn1 = 0  # y[n-1]
        self.yn2 = 0  # y[n-2]

    def calCoeff(self, filterType, f0, q):
        w0 = 2 * math.pi * f0 / self.sr
        alpha = math.sin(w0) / (2 * q)

        if filterType == 'LP':
            b0 = (1 - math.cos(w0)) / 2
            b1 = 1 - math.cos(w0)
            b2 = (1 - math.cos(w0)) / 2
            a0 = 1 + alpha
            a1 = -2 * math.cos(w0)
            a2 = 1 - alpha

        elif filterType == 'HP':
            b0 = (1 + math.cos(w0)) / 2
            b1 = - (1 + math.cos(w0))
            b2 = (1 + math.cos(w0)) / 2
            a0 = 1 + alpha
            a1 = -2 * math.cos(w0)
            a2 = 1 - alpha

        else:
            raise RuntimeError("Undefined filter type")

        return b0, b1, b2, a0, a1, a2

    # modify buffer directly
    def render(self, buffer):
        b0, b1, b2, a0, a1, a2 = self.calCoeff(self.filterType, self.f0, self.q)
        x = buffer

        for i in range(len(buffer)):
            s = x[i]
            buffer[i] = self.yn2
            y = (b0 / a0) * s + (b1 / a0) * self.xn1 + (b2 / a0) * self.xn2 \
                - (a1 / a0) * self.yn1 - (a2 / a0) * self.yn2
            self.xn2 = self.xn1
            self.xn1 = s
            self.yn2 = self.yn1
            self.yn1 = y

    # generate output for parallel processing
    def process(self, buffer):
        b0, b1, b2, a0, a1, a2 = self.calCoeff(self.filterType, self.f0, self.q)
        x = buffer
        output = np.zeros(len(buffer))

        for i in range(len(buffer)):
            s = x[i]
            output[i] = self.yn2
            y = (b0 / a0) * s + (b1 / a0) * self.xn1 + (b2 / a0) * self.xn2 \
                - (a1 / a0) * self.yn1 - (a2 / a0) * self.yn2
            self.xn2 = self.xn1
            self.xn1 = s
            self.yn2 = self.yn1
            self.yn1 = y

        return output