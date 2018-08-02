#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse
import sys
import os

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

sl_no_generator = os.path.join(progPath,"Library","SlnoGenerator.py")

from colours import *

adminlist = ("sanath.shetty")
if os.environ['USER'] in adminlist:
    parser = argparse.ArgumentParser(description='Serial number generator')
    parser.add_argument("-g", "--generate", help="Generate a serial number", action="store_true")
    args = parser.parse_args()
    if args.generate:
        execfile(sl_no_generator)
    else:
        print (CYELLOW2 +"Please provide an argument or refer to 'help' with -h argument" + CEND)
else:
    print (CRED + "You Are An Unauthorized User" + CEND)

