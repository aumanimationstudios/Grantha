#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-u", "--update", help="Update location of an item", action="store_true")

args=parser.parse_args()

if args.update:
    execfile("Update.py")


