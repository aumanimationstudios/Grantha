#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--square", help="square the number", action="store_true")
parser.add_argument("-c", "--cube", help="cube the number", action="store_true")
parser.add_argument("number", help="give the number to be squared", type=int)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()

if args.square:
    print(args.number**2)
elif args.cube:
    print(args.number**3)
if args.verbose:
    while args.square:
        print("Square of "+ str(args.number))
        break
    else:
        print("Cube of "+ str(args.number))

