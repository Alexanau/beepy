#!/usr/bin/python
import random
import math
import sys
import getopt

BITRATE = 8000
BITDEPTH = 8
SIGNED = False
MAX = (1<<BITDEPTH)-1
MIN = 0
optlist, args = getopt.getopt(sys.argv[1:],'sr:d:')
for opt,arg in optlist:
  if opt == '-d':
    BITDEPTH=int(arg)
  if opt == '-s':
    SIGNED = True
  if opt == '-r':
    BITRATE = int(arg)


if SIGNED:
  MAX=(1<<BITDEPTH-1)-1
  MIN=(-1<<BITDEPTH-1)

quiet = int((MAX+MIN)/2)
sine = []
for x in range(int(BITRATE)):
  scale = (1+math.sin(float(x)/BITRATE * 2.0 * math.pi))/2.0
  sine.append(int(MIN+MAX*scale))


##################################
def writebytes(num,bits):
  while bits >0:
    sys.stdout.write(chr(num&0xFF))
    num = num >> 8
    bits -=8

    
##################################

def tone(freq,length):
  for x in range(int(length*BITRATE)):
    writebytes(sine[(x*freq)%BITRATE],BITDEPTH)

def silence(length):
    for x in range(int(length*BITRATE)):
      writebytes(quiet,BITDEPTH)

def noise(length):
  for x in range(int(length*BITRATE)):
    writebytes(random.randint(MIN,MAX))


####################################

for x in range(5):
  tone(1000,0.5)
  silence(.5)
