#!/usr/bin/python
import random
import math
import sys
import getopt

BITRATE = 8000
BITDEPTH = 8
SIGNED = False
optlist, args = getopt.getopt(sys.argv[1:],'sr:d:')
for opt,arg in optlist:
  if opt == '-d':
    BITDEPTH = int(arg)
  if opt == '-s':
    SIGNED = True
  if opt == '-r':
    BITRATE = int(arg)

##############
BITDEPTH = 8 #
##############

sine = []
if SIGNED:
  for x in range(int(BITRATE)):
    sine.append(int(((1<<BITDEPTH) -1) * math.sin(float(x)/BITRATE * 2.0 * math.pi)))
else:
  for x in range(int(BITRATE)):
    sine.append(int(((1<<BITDEPTH) -1) * (1+math.sin(float(x)/BITRATE * 2.0 * math.pi))/2.0))

##################################

def tone(freq,length):
  for x in range(int(length*BITRATE)):
    sys.stdout.write(chr(sine[(x*freq)%BITRATE]))
  

def silence(length):
  if SIGNED:
    for x in range(int(length*BITRATE)):
      sys.stdout.write('\0')

  else:
    for x in range(int(length*BITRATE)):
      sys.stdout.write('\x7F')

def noise(length):
  if SIGNED:
    for x in range(int(length*BITRATE)):
      sys.stdout.write(chr(random.randint(0,255)))

  else:
    for x in range(int(length*BITRATE)):
      sys.stdout.write(chr(random.randint(0,255)))

####################################

for x in range(5):
  tone(1000,0.5)
  silence(.5)
