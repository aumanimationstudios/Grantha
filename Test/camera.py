#!/usr/bin/python3
# *-* coding: utf-8 *-*

from picamera import PiCamera
from time import sleep
from datetime import datetime
import os

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

with PiCamera() as camera:
    try:
        # camera.resolution = (2048, 1080)
        camera.annotate_text = str(datetime.now().replace(microsecond=0))
        camera.rotation = 180
        camera.awb_mode = 'incandescent'
        i = 1
        while os.path.exists('/home/pi/Pictures/image0%s.jpg' %i):
            i+=1
        camera.capture('/home/pi/Pictures/image0%s.jpg' %i)
        os.system("rsync -av /home/pi/Pictures/image0%s.jpg bluepixels@blue0030:/crap/crap.server/Sanath_Shetty/piCameraCaptures/" %i)
        print("captured")
    finally:
        camera.close()
