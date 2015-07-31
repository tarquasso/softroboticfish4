print "Loading modules (1)..."

from evjs import Joystick
from leds import LEDs

j = Joystick()
leds = LEDs(j)

leds.go(1, color=0xffaa00)
print "Loading modules (2)..."

from rpitx import gettx, oqpsktx, ooktx2, ooktx
import time
import os, sys, select

try:
  # set highest priority
  os.nice(-20)
except OSError:
  # not running as root
  pass 

leds.go(1, color=0xffaa)
print "Initializing hardware..."

#tx = gettx(carrier=32000, bw=100, samp_rate=192000)
#tx = gettx(carrier=32000, bw=1000, samp_rate=192000, block=ooktx2)
tx = gettx(carrier=32000, bw=500, samp_rate=192000, block=oqpsktx)

leds.go(1, color=0xff00)
print "Fish control started."

delay = 0.2
count = 1

try:
  for i in range(255):
    j.scan()
    #print j
    leds.go(count)
    print "Running tx.send()"
    #tx.send('a_h' + chr(count & 0xff) + j.toString() + 'x')
    tx.send(j.toString())
    count += 1
    if select.select([sys.stdin], [], [], 0)[0]:
      break
    #time.sleep(delay)
except KeyboardInterrupt:
  pass

print "Fish control ended."
leds.end()
