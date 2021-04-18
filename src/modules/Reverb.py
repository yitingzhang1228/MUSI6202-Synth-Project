import numpy as np
import soundfile as sf


class Reverb(object):
  def __init__(self, bufSize, type, BL=0.3):
    # inFile = '../audio/input/impulse-response.wav'
    if type == 'Cathedral':
      inFile = '../audio/IR/cathedral_48k.wav'
    elif type == 'Hall':
      inFile = '../audio/IR/hall_48k.wav'
    elif type == 'Plate':
      inFile = '../audio/IR/plate_48k.wav'
    elif type == 'Room':
      inFile = '../audio/IR/room_48k.wav'
    elif type == 'Tunnel':
      inFile = '../audio/IR/tunnel_48k.wav'
    else:
      raise RuntimeError("Undefined reverb type")
    h, sr = sf.read(inFile)
    self.L = bufSize
    self.M = len(h)
    self.N = self.L + self.M - 1
    h_pad = np.pad(h, (0, self.L - 1), 'constant', constant_values=(0, 0))
    self.H_n = np.fft.fft(h_pad)
    self.x_n = np.zeros(self.N)
    self.BL = BL

  def render(self, buffer):
    self.x_n = np.concatenate((self.x_n[- (self.M - 1):], buffer))
    #         print('self.x_n ', len(self.x_n))

    if len(buffer) < self.L:
      last_len = len(buffer)
      if last_len == 0:
        pass
      else:
        self.x_n = np.pad(self.x_n, (0, self.N - len(self.x_n)), 'constant', constant_values=(0, 0))
        X_n = np.fft.fft(self.x_n)
        y_n = (np.fft.ifft((X_n * self.H_n))).real
        y_n_L = y_n[-self.L:][:last_len]

    else:
      X_n = np.fft.fft(self.x_n)
      y_n = (np.fft.ifft((X_n * self.H_n))).real
      y_n_L = y_n[-self.L:]

    for i in range(len(buffer)):
      buffer[i] = buffer[i] + self.BL * y_n_L[i]
