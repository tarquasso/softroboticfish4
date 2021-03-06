import rx, codes, hamming

import evjs
j = evjs.Joystick(fake=True)

try:
  import leds
  l = leds.LEDs(j)
except:
  l = None

def callback(rxstr):
  count = ord(rxstr[0])
  b1 = "{:08b}".format(ord(rxstr[1]))
  b2 = "{:08b}".format(ord(rxstr[2]))
  bits = map(int, b1+b2)
  parity = sum(bits) % 2
  data, error = hamming.decode(bits[:-1])

  j.setBits(data)
  if l is None:
    print count, j, error, parity
  else:
    if parity == 0 and error == 0:
      color = 0xffffff
    elif parity > 0 and error > 0:
      color = 0xffff00
    else:
      color = 0xff0000

    l.go(count, color)
  
d = rx.Demod()
#d.run(carrier=32000, bw=100, sps=1, mod=rx.Mods.MAGNITUDE, codes=codes.manchester, callback=callback)
#d.run(carrier=32000, bw=1000, sps=1, mod=rx.Mods.MAGNITUDE, codes=codes.mycode, callback=callback)
d.run(carrier=32000, bw=500, sps=1, mod=rx.Mods.DPHASE, codes=codes.mycode, callback=callback)

if l is not None:
  l.end()
