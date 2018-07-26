#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--delete", help="Delete an item", action="store_true")

args=parser.parse_args()

if args.delete:
    execfile("Delete.py")

