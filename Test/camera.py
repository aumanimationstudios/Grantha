#!/usr/bin/python3
# *-* coding: utf-8 *-*

from picamera import PiCamera
from time import sleep
from datetime import datetime
import os
import argparse
import debug
import sys
import setproctitle

# camera = PiCamera()
# camera.resolution = (2048, 1080)
# #camera.framerate = 15
# #camera.start_preview()
# sleep(0.5)
# i = 1
# while os.path.exists('/home/pi/Pictures/image0%s.jpg' %i):
#     i+=1
# camera.capture('/home/pi/Pictures/image0%s.jpg' %i)
# #camera.stop_preview()

setproctitle.setproctitle("CAMERA")

parser = argparse.ArgumentParser(description="Utility to capture image on PiCamera")
parser.add_argument('filename', metavar='N', type=str, help='file name')
args = parser.parse_args()

# with PiCamera() as camera:
camera = PiCamera()
try:
    # camera.resolution = (2048, 1080)
    camera.resolution = (1920, 1080)
    camera.annotate_text = str(datetime.now().replace(microsecond=0))
    # camera.rotation = 90
    camera.awb_mode = 'incandescent'
    # i = 1
    # while os.path.exists('/home/pi/Pictures/image0%s.jpg' %i):
    #     i+=1
    # camera.capture('/home/pi/Pictures/image0%s.jpg' %i)
    # os.system("rsync -av /home/pi/Pictures/image0%s.jpg bluepixels@blue0030:/crap/crap.server/Sanath_Shetty/piCameraCaptures/" %i)
    i = args.filename
    debug.info(i)
    camera.capture('/home/pi/Pictures/%s.jpg' %i)
    # print("captured")
    os.system("rsync -av /home/pi/Pictures/%s.jpg bluepixels@blue0030:/crap/crap.server/Sanath_Shetty/piCameraCaptures/" %i)
except:
    debug.info(str(sys.exc_info()))
finally:
    camera.close()
