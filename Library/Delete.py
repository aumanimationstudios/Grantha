#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import os
import  readchar

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

from colours import *

#usage message
print CGREEN + "Enter the Serial_no of the item to delete " + CEND

#user input
sln = str(raw_input("Serial_no: "))

print "Are You sure to delete the Item? [y/n]"
db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)
cursor = db.cursor()

while True:
    key = readchar.readkey()
    if(key == 'y'):
        try:
            cursor.execute("DELETE FROM ITEMS WHERE serial_no = '%s' " %(sln))
            print("Item with serial_no: "+ sln + " Deleted ")
        except:
            print "Error: unable to fetch data : "+ str(sys.exc_info())
        break
    elif(key == 'n'):
        print "Nothing to do. Exiting..."
        break

    cursor.close()
    db.close()

