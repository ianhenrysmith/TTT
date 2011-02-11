#! /usr/bin/python

import serial, commands, time, random

usb_dev = commands.getoutput('ls /dev | grep "USB"')
ser = serial.Serial('/dev/%s'%usb_dev, 9600)
if ser.read() is 'X':
  while(True):
    ser.write(chr(13))
    delta = random.randint(0,1000)/1000.0
    time.sleep(delta)
    print delta
