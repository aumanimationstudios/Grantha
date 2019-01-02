#!/usr/bin/python2
# *-* coding: utf-8 *-*

import RPi.GPIO as GPIO

import SimpleMFRC522
import sys

try:
    reader = SimpleMFRC522.SimpleMFRC522()
    print "Place your tag to read"
    id, text = reader.read()
    print "id = %s" %(id)
    print "data = %s" %(text)
    GPIO.cleanup()

except:
    print("trying hard : " + str(sys.exc_info()))
    GPIO.cleanup()

