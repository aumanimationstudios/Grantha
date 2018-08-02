#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import time
import os

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

from colours import *

db = MySQLdb.connect("localhost","test","test123","INVENTORY")
db.autocommit(1)

#usage message
print CGREEN + "Enter location to change its Primary location" + CEND

#user input
loc = str(raw_input("location[BLUE0001-0666]: "))

#sql query to fetch the current parent_location
cursor = db.cursor()
cursor.execute(" SELECT parent_location FROM LOCATION WHERE location='%s' " %(loc))
results = cursor.fetchall()
for row in results:
    parent_loc = row[0]
    print("Current Parent location is "+ '%s' ) %(parent_loc)

#user input for the updated parent_location
parent_location = str(raw_input("New Parent Location[WORKSPACE1-35]: "))

#sql query to set the parent_location for the user input location
sql = " UPDATE LOCATION SET parent_location = '%s' WHERE location = '%s' " %(parent_location, loc)
try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    print("Parent location changed to "+ parent_location)
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

