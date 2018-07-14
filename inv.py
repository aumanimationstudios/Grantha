#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--read", help="Read the list for a specific item, location or item type",
                    action="store_true")
parser.add_argument("-a", "--all", help="Read full list for all items", action ="store_true")
parser.add_argument("-i", "--insert", help="Insert an item to the list", action="store_true")
parser.add_argument("-u", "--update", help="Update the location of an item", action="store_true")
parser.add_argument("-d", "--delete", help="Delete an item entry", action="store_true")
parser.add_argument("-l", "--log", help="Read the update log for an item", action="store_true")

args = parser.parse_args()

if args.read:
    execfile("Read.py")
elif args.all:
    execfile("Read_All.py")
elif args.insert:
    execfile("Insert.py")
elif args.update:
    execfile("Update.py")
elif args.delete:
    execfile("Delete.py")
elif args.log:
    execfile("UpdateLog.py")

