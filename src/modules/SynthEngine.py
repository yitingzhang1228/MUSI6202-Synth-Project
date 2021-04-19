import math
import numpy as np


class SineWaveNaive(object):
    def __init__(self, freq, sr=48000):
        self.freq = freq
        self.phi = 0
        self.sr = sr

    def render(self, buffer):
        for i in range(len(buffer)):
            buffer[i] = math.sin(self.phi * 2 * math.pi)
            self.phi += float(self.freq) / float(self.sr)
            while self.phi > 1.0:
                self.phi -= 1.0


class SquareWaveAdditive(object):
    def __init__(self, freq, numHarmonics=20, amp=1, sr=48000):
        self.freq = freq
        self.numHarmonics = numHarmonics
        self.phis = np.zeros(self.numHarmonics)
        self.amp = amp * 4 / math.pi
        self.phiDeltas = np.zeros(self.numHarmonics)

        for i in range(self.numHarmonics):
            harmonicFreq = float(self.freq) * (float(i) * 2 + 1)
            self.phiDeltas[i] = harmonicFreq / float(sr)

    def render(self, buffer):
        for i in range(len(buffer)):
            for j in range(self.numHarmonics):
                buffer[i] += math.sin(2 * math.pi * self.phis[j]) * self.amp / (float(j) * 2 + 1)
                self.phis[j] += self.phiDeltas[j]
                while self.phis[j] >= 1:
                    self.phis[j] -= 1


class SawWaveAdditive(object):
    def __init__(self, freq, numHarmonics=20, amp=1, sr=48000):
        self.freq = freq
        self.numHarmonics = numHarmonics
        self.phis = np.zeros(self.numHarmonics)
        self.amp = amp / math.pi
        self.phiDeltas = np.zeros(self.numHarmonics)

        for i in range(self.numHarmonics):
            harmonicFreq = float(self.freq) * (float(i) + 1)
            self.phiDeltas[i] = harmonicFreq / float(sr)

    def render(self, buffer):
        for i in range(len(buffer)):
            for j in range(self.numHarmonics):
                buffer[i] += math.sin(2 * math.pi * self.phis[j]) * self.amp / (float(j) + 1)
                self.phis[j] += self.phiDeltas[j]
                while self.phis[j] >= 1:
                    self.phis[j] -= 1


class SineWaveWavetable(object):
    def __init__(self, freq, sr=48000):
        self.freq = freq
        self.phi = 0
        self.table_size = 24000
        self.sr = sr

        empty_table = np.zeros(self.table_size)  # a single sine wave cycle in 24000 samples
        for i in range(self.table_size):
            empty_table[i] += math.sin(2 * math.pi * i / self.table_size)
        self.table = empty_table

    def render(self, buffer):
        rate = self.freq * self.table_size / self.sr  # reading rate of the table calculated with the sample rate
        for i in range(len(buffer)):
            idx_float = (rate * self.phi) % self.table_size  # float location
            idx_int = int(idx_float)  # floor int location

            # avoid bound error
            zero = idx_int - 1
            two = idx_int + 1
            three = idx_int + 2
            if zero < 0:
                zero = 0
            if three > self.table_size - 1:
                two = self.table_size - 1
                three = self.table_size - 1
            if three > self.table_size - 2:
                three = self.table_size - 1

            y0 = self.table[zero]
            y1 = self.table[idx_int]
            y2 = self.table[two]
            y3 = self.table[three]
            mu = idx_float - idx_int
            # Cubic Interpretation
            mu2 = mu * mu
            a0 = y3 - y2 - y0 + y1
            a1 = y0 - y1 - a0
            a2 = y2 - y0
            a3 = y1

            value = a0 * mu * mu2 + a1 * mu2 + a2 * mu + a3
            buffer[i] = value

            self.phi += 1  # phi keeps adding up as long as the audio is rendering. Should it be reset at all?


class SquareWaveWavetable(object):
    def __init__(self, freq, sr=48000):
        self.freq = freq
        self.phi = 0
        self.table_size = 24000
        self.sr = sr

        empty_table = np.zeros(self.table_size)  # a single sine wave cycle in 24000 samples
        for n in range(20):  # 20 harmonics
            for i in range(self.table_size):
                empty_table[i] += math.sin(2 * (2 * n + 1) * math.pi * i / self.table_size) * (4 / math.pi) / (2 * n + 1)
        self.table = empty_table

    def render(self, buffer):
        rate = self.freq * self.table_size / self.sr  # reading rate of the table calculated with the sample rate
        for i in range(len(buffer)):
            idx_float = (rate * self.phi) % self.table_size  # float location
            idx_int = int(idx_float)  # floor int location

            # avoid bound error
            zero = idx_int - 1
            two = idx_int + 1
            three = idx_int + 2
            if zero < 0:
                zero = 0
            if three > self.table_size - 1:
                two = self.table_size - 1
                three = self.table_size - 1
            if three > self.table_size - 2:
                three = self.table_size - 1

            y0 = self.table[zero]
            y1 = self.table[idx_int]
            y2 = self.table[two]
            y3 = self.table[three]
            mu = idx_float - idx_int
            # Cubic Interpretation
            mu2 = mu * mu
            a0 = y3 - y2 - y0 + y1
            a1 = y0 - y1 - a0
            a2 = y2 - y0
            a3 = y1

            value = a0 * mu * mu2 + a1 * mu2 + a2 * mu + a3
            buffer[i] = value

            self.phi += 1  # phi keeps adding up as long as the audio is rendering. Should it be reset at all?


class SawWaveWavetable(object):
    def __init__(self, freq, sr=48000):
        self.freq = freq
        self.phi = 0
        self.table_size = 24000
        self.sr = sr

        empty_table = np.zeros(self.table_size)  # a single sine wave cycle in 24000 samples
        for n in range(20):  # 20 harmonics
            n += 1
            for i in range(self.table_size):
                empty_table[i] += (1 / math.pi) * (1 / n) * math.sin(2 * n * math.pi * i / self.table_size)
        self.table = empty_table

    def render(self, buffer):
        rate = self.freq * self.table_size / self.sr  # reading rate of the table calculated with the sample rate
        for i in range(len(buffer)):
            idx_float = (rate * self.phi) % self.table_size  # float location
            idx_int = int(idx_float)  # floor int location

            # avoid bound error
            zero = idx_int - 1
            two = idx_int + 1
            three = idx_int + 2
            if zero < 0:
                zero = 0
            if three > self.table_size - 1:
                two = self.table_size - 1
                three = self.table_size - 1
            if three > self.table_size - 2:
                three = self.table_size - 1

            y0 = self.table[zero]
            y1 = self.table[idx_int]
            y2 = self.table[two]
            y3 = self.table[three]
            mu = idx_float - idx_int
            # Cubic Interpretation
            mu2 = mu * mu
            a0 = y3 - y2 - y0 + y1
            a1 = y0 - y1 - a0
            a2 = y2 - y0
            a3 = y1

            value = a0 * mu * mu2 + a1 * mu2 + a2 * mu + a3
            buffer[i] = value

            self.phi += 1  # phi keeps adding up as long as the audio is rendering. Should it be reset at all?