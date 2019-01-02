#!/usr/bin/python2
# *-* coding: utf-8 *-*

import threading
import time
import RPi.GPIO as GPIO
import SimpleMFRC522
import sys
import argparse

class reader(threading.Thread):
    def __init__(self,timeout):
        super(reader, self).__init__()
        self._timeout = timeout

    def run(self):
        GPIO.setwarnings(False)
        x = " "
        print "id" + 20 * x + "data"

        idTxt = {}
        timestarted = time.time()
        while True:
            try:
                if ((time.time() - timestarted) >= self._timeout):
                    break

                reader = SimpleMFRC522.SimpleMFRC522()
                id, text = reader.read()
                idTxt[id] = text
                print idTxt[id]

                GPIO.cleanup()

                time.sleep(1)

            except:
                print("trying again : " + str(sys.exc_info()))
                GPIO.cleanup()

        for x in idTxt:
            print(str(x) + " : " + str(idTxt[x]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility to read multiple tags")
    parser.add_argument('timeout', metavar='N', type=int, help='time in seconds')
    args = parser.parse_args()

    Reader = reader(args.timeout)
    Reader.start()



