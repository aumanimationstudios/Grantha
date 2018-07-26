#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse
import os

adminlist = ("sanath.shetty", "root")
if os.environ['USER'] in adminlist:
    parser = argparse.ArgumentParser(description = 'Inventory Management Tool')

    parser.add_argument("-r", "--read", help="Read the list for a specific item, location, item type, user",
                        action="store_true")
    parser.add_argument("-a", "--all", help="Read full list for all items", action ="store_true")
    parser.add_argument("-i", "--insert", help="Insert an item to the list", action="store_true")
    parser.add_argument("-u", "--update", help="Update the location and user of an item", action="store_true")
    parser.add_argument("-m", "--modify", help="Modify the parent_location of a location", action="store_true")
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
    elif args.modify:
        execfile("LocationModify.py")
    elif args.delete:
        execfile("Delete.py")
    elif args.log:
        execfile("UpdateLog.py")
    else:
        print "Please provide an argument or refer to 'help' with -h argument"
else:
    print "You Are An Unauthorized User"

