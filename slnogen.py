#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse
import os

adminlist = ("sanath.shetty", "root")
if os.environ['USER'] in adminlist:
    parser = argparse.ArgumentParser(description='Serial number generator')
    parser.add_argument("-g", "--generate", help="Generate a serial number", action="store_true")
    args = parser.parse_args()
    if args.generate:
        execfile("slno_generator.py")
    else:
        print "Please provide an argument or refer to 'help' with -h argument"
else:
    print "You Are An Unauthorized User"

