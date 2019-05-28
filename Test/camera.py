#!/usr/bin/python3
# *-* coding: utf-8 *-*

from picamera import PiCamera
from time import sleep
from datetime import datetime
import os
import argparse

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

parser = argparse.ArgumentParser(description="Utility to capture image on PiCamera")
parser.add_argument('filename', metavar='N', type=str, help='file name')
args = parser.parse_args()

with PiCamera() as camera:
    try:
        # camera.resolution = (2048, 1080)
        camera.annotate_text = str(datetime.now().replace(microsecond=0))
        camera.rotation = 180
        camera.awb_mode = 'incandescent'
        # i = 1
        # while os.path.exists('/home/pi/Pictures/image0%s.jpg' %i):
        #     i+=1
        # camera.capture('/home/pi/Pictures/image0%s.jpg' %i)
        # os.system("rsync -av /home/pi/Pictures/image0%s.jpg bluepixels@blue0030:/crap/crap.server/Sanath_Shetty/piCameraCaptures/" %i)
        i = args.filename
        camera.capture('/home/pi/Pictures/%s.jpg' %i)
        print("captured")
    finally:
        camera.close()
