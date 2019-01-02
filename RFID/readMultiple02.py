#!/usr/bin/python2
# *-* coding: utf-8 *-*

import threading
import time
import RPi.GPIO as GPIO
import SimpleMFRC522
import sys
import argparse
import multiprocessing
import os
import signal
import setproctitle
from tabulate import tabulate

def readInfi(Q):

    def signalHandler(sigNum,frame):
        # print(sigNum,frame)
        global Q
        print("TERMINATING PROCESS : "+ str(os.getpid()))
        Q.put({0:os.getpid()})
        time.sleep(1)
        # return
        os.kill(os.getpid(),9)


    signal.signal(signal.SIGTERM,signalHandler)

    GPIO.setwarnings(False)

    while True:
        try:
            idTxt = {}
            reader = SimpleMFRC522.SimpleMFRC522()
            id, text = reader.read()
            idTxt[id] = text
            os.system("echo 1 | sudo tee /sys/class/leds/led0/brightness")

            GPIO.cleanup()
            Q.put(idTxt)
            time.sleep(0.1)

        except:
            print("trying again : " + str(sys.exc_info()))
            GPIO.cleanup()
            os.system("echo 1 | sudo tee /sys/class/leds/led1/brightness")

def storData(Q):
    data = {}
    while True:
        dictGet = Q.get()
        if(dictGet.has_key(0)):
            print("DONE SCANNING")
            print(data)
            print tabulate(data.items(), headers=('id', 'data'))
            sys.exit(0)
        else:
            data.update(dictGet)



if __name__ == "__main__":
    setproctitle.setproctitle("MULTIREADER")
    Q = multiprocessing.Queue(1000)
    # Q2S = multiprocessing.Queue(1000)
    parser = argparse.ArgumentParser(description="Utility to read multiple tags")
    parser.add_argument('timeout', metavar='N', type=int, help='time in seconds')
    args = parser.parse_args()

    Reader = multiprocessing.Process(target=readInfi, args=(Q,))
    storer = multiprocessing.Process(target=storData, args=(Q,))
    Reader.start()
    storer.start()

    timestared = time.time()
    while(True):
        if((time.time() - timestared) >= args.timeout):
            Reader.terminate()
            # storer.terminate()
            break

    Reader.join()
    storer.join()
    # Q.join_thread()

