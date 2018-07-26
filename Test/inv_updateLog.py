#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-l", "--log", help="Read the log list", action="store_true")

args=parser.parse_args()

if args.log:
    execfile("updateLog.py")

