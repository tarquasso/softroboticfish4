#!/bin/python

import numpy as np
from scipy.signal import decimate
from rtlsdr import RtlSdr, limit_calls
from codes import manchester, codes154, codes2corr
import matplotlib.pyplot as plt

import sys, select

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

Mods = enum("MAGNITUDE", "PHASE", "DPHASE")

HEADER = '00011011111010'
FOOTER = '0001111'
PKTLEN = 8*4 + len(FOOTER)

class Demod:
  SAMP_RATE = 256000.
  SAMP_WINDOW = 1024*40

  def __init__(self, carrier=32000, bw=1000, sps=8, codes=manchester, mod=Mods.MAGNITUDE):
    self.mod = mod

    decim = Demod.SAMP_RATE/bw/sps
    assert decim == int(decim)
    self.decim = int(decim)
    assert Demod.SAMP_WINDOW % self.decim == 0

    self.sampchips = Demod.SAMP_WINDOW / self.decim 
    self.corr = codes2corr(codes, sps)
    self.codelen = len(self.corr[0])

    self.sdr = RtlSdr()
    # Sampling rate
    self.sdr.rs = Demod.SAMP_RATE
    # Pins 4 and 5
    self.sdr.set_direct_sampling(2)
    # Center frequency
    self.sdr.fc = carrier
    # I don't think this is used?
    self.sdr.gain = 1

  def bb2c(self, baseband):
    mag = np.abs(baseband)
    phase = np.angle(baseband)
    dp = np.mod(np.ediff1d(phase)+np.pi, 2*np.pi)-np.pi
    return mag[1:], phase[1:], dp

  def decode(self, chips):
    corrs = []
    for c in self.corr:
      corrs.append(np.correlate(chips, c))
    maxes = np.max(np.array(corrs), 0)
    codes = np.argmax(np.array(corrs), 0)
    return maxes, codes

  def extract(self, nc):
    for codeoffset in range(self.codelen):
      pkts = []
      codestr = "".join(map(repr, map(int, nc[codeoffset::self.codelen])))

      for p in self.tocheck[codeoffset]['pkts']:
        pkt = p + codestr[0:PKTLEN-len(p)]
        if len(pkt) < PKTLEN:
          pkts.append(pkt)
        elif pkt[-len(FOOTER):] == FOOTER:
          str = ""
          for j in range(0,len(pkt)-1,8):
            str += chr(int(pkt[j:j+8][::-1], 2))
          print str
          sys.stdout.flush()

      codestr = self.tocheck[codeoffset]['last'] + codestr
      for ind in find_all(codestr, HEADER):
        pkt = codestr[ind+len(HEADER):ind+len(HEADER)+PKTLEN]
        if len(pkt) < PKTLEN:
          pkts.append(pkt)
        elif pkt[-len(FOOTER):] == FOOTER:
          str = ""
          for j in range(0,len(pkt)-1,8):
            str += chr(int(pkt[j:j+8][::-1], 2))
          print str
          sys.stdout.flush()
      self.tocheck[codeoffset]['pkts'] = [] + pkts
      self.tocheck[codeoffset]['last'] = "" + codestr[-len(HEADER)+1:]

  def ddc(self, samp, sdr):
    iq = np.empty(len(samp)//2, 'complex')
    iq.real, iq.imag = samp[::2], samp[1::2]
    iq /= (255/2)
    iq -= (1 + 1j)

    extsamp = np.concatenate((self.last, iq))
    self.last = iq
    #baseband = decimate(extsamp * self.mixer, self.decim, ftype='fir')
    #baseband = decimate(extsamp, self.decim, ftype='fir')
    baseband = np.mean(np.reshape(extsamp, (-1,self.decim)), 1) # poor man's decimation
    mag, phase, dp  = self.bb2c(baseband)
    if self.mod == Mods.PHASE:
      sig = phase
    elif self.mod == Mods.DPHASE:
      sig = dp
    else:
      sig = mag
    corrs, codes = self.decode(sig)

    nc = codes[self.codelen:self.codelen+self.sampchips]
    self.extract(nc)

    if self.index is not None:
      self.chips[self.index*self.sampchips:(self.index+1)*self.sampchips] = sig[self.codelen:self.codelen+self.sampchips]
      self.corrs[self.index*self.sampchips:(self.index+1)*self.sampchips] = corrs[self.codelen:self.codelen+self.sampchips]
      self.demod[self.index*self.sampchips:(self.index+1)*self.sampchips] = nc #codes[self.codelen:self.codelen+self.sampchips]
      self.index += 1

  def end(self):
    self.sdr.close()

  def run(self, limit=None):
    self.last = np.zeros(Demod.SAMP_WINDOW)
    if limit:
      self.chips = np.zeros(limit * Demod.SAMP_WINDOW / self.decim)
      self.corrs = np.zeros(limit * Demod.SAMP_WINDOW / self.decim)
      self.demod = np.zeros(limit * Demod.SAMP_WINDOW / self.decim)
      self.index = 0
    else:
      self.index = None

    self.tocheck = [None] * self.codelen
    for i in range(self.codelen):
      self.tocheck[i] = dict()
      self.tocheck[i]['last'] = ''.join(range(0))
      self.tocheck[i]['pkts'] = range(0)

    if limit is None:
      def callback(samp, sdr):
        if select.select([sys.stdin], [], [], 0)[0]:
          sdr.cancel_read_async()
        self.ddc(samp, sdr)
    else:
      @limit_calls(limit)
      def callback(samp, sdr):
        if select.select([sys.stdin], [], [], 0)[0]:
          sdr.cancel_read_async()
        self.ddc(samp, sdr)

    self.sdr.read_bytes_async(callback, Demod.SAMP_WINDOW*2)
    print self.index, "samples read"
    sys.stdout.flush()

  def plot(self):
    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax1.plot(self.chips)
    ax2 = fig.add_subplot(312, sharex=ax1)
    ax2.plot(self.corrs)
    ax3 = fig.add_subplot(313, sharex=ax1)
    ax3.plot(self.demod)
    plt.show()

  def checkdemod(self, index, demod=None, packetlen=5):
    if demod is None:
      demod = self.demod
    l = packetlen*8+6+7
    b = self.demod[index:index+l*self.codelen:self.codelen]
    return chipsToString(np.concatenate(([1,0], b, [0])))

  def findstring(self, demod = None, packetlen=5):
    if demod is None:
      demod = self.demod
    find = []
    for i in range(len(demod)):
      s, c = self.checkdemod(i, demod, packetlen)
      if len(s) and s[0] == 'a' and s[-1] == 'x':
        find.append((i, s[1:-1]))
    return find

def chipsToString(bits):
  char = 0
  rxstr = ""
  for i, b in enumerate(bits):
    char += (1 << (i%8)) if b else 0
    if i % 8 == 7:
      rxstr += chr(char)
      char = 0
  return rxstr, char
  
if __name__ == "__main__":
  d = Demod(carrier=32000, bw=1000, sps=1, codes=manchester)
  d.run()