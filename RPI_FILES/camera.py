#!/usr/bin/python3
# *-* coding: utf-8 *-*

### Utility to capture image from camera module on Raspberry pi ###

from picamera import PiCamera
from time import sleep
from datetime import datetime
import os
import argparse
import debug
import sys
import setproctitle


setproctitle.setproctitle("CAMERA")

parser = argparse.ArgumentParser(description="Utility to capture image on PiCamera")
parser.add_argument('filename', metavar='N', type=str, help='file name')
args = parser.parse_args()

camera = PiCamera()
try:
    # camera.resolution = (2048, 1080)
    camera.resolution = (1920, 1080)
    camera.annotate_text = str(datetime.now().replace(microsecond=0))
    # camera.rotation = 90
    camera.awb_mode = 'incandescent'

    i = args.filename
    debug.info(i)
    camera.capture('/home/pi/Pictures/%s.jpg' %i)

    os.system("rsync -av /home/pi/Pictures/%s.jpg bluepixels@blue0030:/blueprod/STOR2/stor2/grantha/share/pics/" %i)

except:
    debug.info(str(sys.exc_info()))

finally:
    camera.close()
