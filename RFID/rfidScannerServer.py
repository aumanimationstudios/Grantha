#!/usr/bin/python2
# *-* coding: utf-8 *-*

import zmq
import SimpleMFRC522
import RPi.GPIO as GPIO
import sys

class Server:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://192.168.1.183:4689")

        while True:
            msgFrmCli = self.socket.recv()
            print "Message from Client: " + msgFrmCli

            if (msgFrmCli == "WRITE"):
                self.WRITE()

            if (msgFrmCli == "READ"):
                self.READ()

            if (msgFrmCli == "WRITE_TAG"):
                self.WRITE_TAG()


    def WRITE(self):
        print "Sending Reply"
        self.socket.send("INPUT")

        serialNo = self.socket.recv()
        print "Message from Client: " + serialNo
        print("Now place your tag to write")

        while True:
            try:
                reader = SimpleMFRC522.SimpleMFRC522()
                msg = reader.write(serialNo)
                if (msg):
                    print("Written")
                GPIO.cleanup()
                break

            except:
                print("trying to screw harder : " + str(sys.exc_info()))
                GPIO.cleanup()

        self.socket.send("Data Written to Tag")

    def READ(self):
        print "Now place your tag to read"
        try:
            reader = SimpleMFRC522.SimpleMFRC522()
            id, text = reader.read()
            slNo = text.strip()
            self.socket.send(slNo)
            print "message sent"
            GPIO.cleanup()

        except:
            print("trying hard : " + str(sys.exc_info()))
            GPIO.cleanup()

    def WRITE_TAG(self):
        print "Sending Reply"
        self.socket.send("INPUT")

        serialNo = self.socket.recv()
        print "Message from Client: " + serialNo
        print("Now place your tag to write")

        while True:
            try:
                reader = SimpleMFRC522.SimpleMFRC522()
                msg = reader.write(serialNo)
                if (msg):
                    print("Written")
                GPIO.cleanup()
                break

            except:
                print("trying to screw harder : " + str(sys.exc_info()))
                GPIO.cleanup()

        self.socket.send("Data Written to Tag")


if __name__ == "__main__":
    Server()

