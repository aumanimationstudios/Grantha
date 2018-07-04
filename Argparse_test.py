#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("echo", help="echo the string you see here")
parser.add_argument("square", help="display square of a given number", type=int)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()
print(args.echo)
print(args.square**2)
if args.verbose:
    print("verbosity turned on")

