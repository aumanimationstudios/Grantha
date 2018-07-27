#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import argparse
import sys
import os

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

from colours import *

read_py = os.path.join(progPath,"Library","Read.py")
read_all_py = os.path.join(progPath,"Library","Read_All.py")
insert_py = os.path.join(progPath,"Library","Insert.py")
update_py = os.path.join(progPath,"Library","Update.py")
location_modify_py = os.path.join(progPath,"Library","LocationModify.py")
delete_py = os.path.join(progPath,"Library","Delete.py")
update_log_py = os.path.join(progPath,"Library", "UpdateLog.py")


adminlist = ("sanath.shetty")
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
        execfile(read_py)
    elif args.all:
        execfile(read_all_py)
    elif args.insert:
        execfile(insert_py)
    elif args.update:
        execfile(update_py)
    elif args.modify:
        execfile(location_modify_py)
    elif args.delete:
        execfile(delete_py)
    elif args.log:
        execfile(update_log_py)
    else:
        print (CYELLOW2 + "Please provide an argument or refer to 'help' with -h argument" + CEND)
else:
    print (CRED +"You Are An Unauthorized User" + CEND)

