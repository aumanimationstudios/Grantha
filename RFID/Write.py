#!/usr/bin/python2
# *-* coding: utf-8 *-*

# import RPi.GPIO as GPIO
#
# import SimpleMFRC522
# import sys

class write:
    def __init__(self):
        # import SimpleMFRC522

        # self.reader = SimpleMFRC522.SimpleMFRC522()

        self.askInput()


    def askInput(self):
        self.text = raw_input('New data:')
        print("Now place your tag to write")
        if (self.text):
            self.writeToTag()

    def writeToTag(self):
        import SimpleMFRC522
        import RPi.GPIO as GPIO
        import sys

        while(True):
            try:
                reader = SimpleMFRC522.SimpleMFRC522()
                msg = reader.write(self.text)
                if (msg):
                    print("Written")
                    # return msg
                    # print msg

                GPIO.cleanup()
                break
            except:
                print("trying to screw harder : " + str(sys.exc_info()))
                GPIO.cleanup()

if __name__ == "__main__":
    write()

