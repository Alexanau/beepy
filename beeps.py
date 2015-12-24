#!/usr/bin/python
import random
import math
import sys
import getopt

BITRATE = 8000
BITDEPTH = 8
SIGNED = False
STEREO = False

msg = '123'
MAX = (1<<BITDEPTH)-1
MIN = 0
optlist, args = getopt.getopt(sys.argv[1:],'cSsr:d:m:')
for opt,arg in optlist:
  if opt == '-d':
    BITDEPTH=int(arg)
  if opt == '-c':
    STEREO = True
    SIGNED = True
    BITRATE = 44100
    BITDEPTH = 16
  if opt == '-S':
    STEREO = True
  if opt == '-s':
    SIGNED = True
  if opt == '-r':
    BITRATE = int(arg)
  if opt == '-m':
    msg = arg

MAX = (1<<BITDEPTH)-1
MIN = 0

if SIGNED:
  MAX=(1<<BITDEPTH-1)-1
  MIN=(-1<<BITDEPTH-1)

quiet = int((MAX+MIN)/2)
sine = []
for x in range(int(BITRATE)):
  scale = (1+math.sin(float(x)/BITRATE * 2.0 * math.pi))/2.0
  sine.append(int(MIN+(MAX-MIN)*scale))


##################################
def writebytes(num,bits):
  buff = []
  while bits >0:
    try:
      buff.append(chr(num&0xFF))
    except IOError:
      exit(0)
    num = num >> 8
    bits -=8
  sys.stdout.write(''.join(buff))
  if STEREO:
    sys.stdout.write(''.join(buff))

    
##################################

def tone(freq,length):
  for x in range(int(length*BITRATE)):
    writebytes(sine[(x*freq)%BITRATE],BITDEPTH)

def silence(length):
    for x in range(int(length*BITRATE)):
      writebytes(quiet,BITDEPTH)

def noise(length):
  for x in range(int(length*BITRATE)):
    writebytes(random.randint(MIN,MAX), BITDEPTH)


####################################


for c in msg:
  noise(.5)
  silence(1)
  for x in range(int(c)):
    tone(800,.6)
    silence(1)
  noise(.5)
