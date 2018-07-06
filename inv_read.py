#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--read", help="Read the items list", action="store_true")

args=parser.parse_args()

if args.read:
    execfile("Read.py")

