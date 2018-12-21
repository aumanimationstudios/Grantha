#!/usr/bin/python2
# *-* coding: utf-8 *-*

import socket
import sys

def getHostNameIP():
    try:
        hostName = socket.gethostname()
        IP = socket.gethostbyname(hostName)
        # return(hostName,IP)
        print IP
    except:
        print "Unable to get Hostname and IP",str(sys.exc_info())

getHostNameIP()




