#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--insert", help="Insert an item to the list", action="store_true")

args=parser.parse_args()

if args.insert:
    execfile("Insert.py")

