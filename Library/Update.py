#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import time
import os
from collections import OrderedDict

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)
from colours import *

libraryPath = os.path.join(progPath,"Library")
sys.path.append(libraryPath)
from ListOptions import readList

#usage message
print CGREEN + "Enter serial_no to change items Location " + CEND

#user input
userInput = OrderedDict()

#present date and time
userInput["date_time"] = time.strftime('%Y-%m-%d %H:%M:%S')

userInput["serial_no"] = str(raw_input("Serial_no: "))

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

#sql query to fetch the present location and user of the item
cursor = db.cursor()
cursor.execute("SELECT serial_no FROM SERIAL_NO")
serial_no = sum(cursor.fetchall(), ())

if userInput["serial_no"] in serial_no:
    cursor.execute(" SELECT location, user FROM ITEMS WHERE serial_no='%s' " %(userInput["serial_no"]))
    results = cursor.fetchall()
    for row in results:
        userInput["location"] = row[0]
        user = row[1]
        print("Item is at "+ '%s' + " User: " + '%s') %(userInput["location"],user)

    #user input for the updated location
    print("Location (Type 'l' to see the list):")
    readList('all_locations')
    userInput["new_location"] = str(raw_input("New_Location: "))

    userInput["updated_by"] = os.environ['USER']

    #sql query to update the location and user of the item
    sql = " UPDATE ITEMS SET location = '%s' \
            WHERE serial_no = '%s' " %(userInput["new_location"], userInput["serial_no"])
    try:
        cursor.execute(sql)
        print("Item location changed to "+ userInput["new_location"])
        print userInput["date_time"]
    except:
        print "Error: unable to fetch data : "+ str(sys.exc_info())

    values = []
    for key in userInput.keys():
        values.append(userInput[key])

    #sql query to store the update details in UPDATE_LOG table
    cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'UPDATE_LOG' \
                    AND COLUMN_NAME NOT IN ('no')")
    col = sum(cursor.fetchall(), ())

    cursor.execute(" INSERT INTO UPDATE_LOG (" + ','.join(col) + ") VALUES %r" %(tuple(values),))
    #cursor.execute(" INSERT INTO UPDATE_LOG (date_time, serial_no, old_location, new_location) VALUES \
                         #('%s', '%s', '%s', '%s') " %(now, sln, location, new_location) )
else:
    print CRED + "Invalid Serial No." + CEND

cursor.close()
db.close()

