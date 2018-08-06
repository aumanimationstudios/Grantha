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

libraryPath = os.path.join(progPath,"Library")
sys.path.append(libraryPath)
from ListOptions import readList

#usage message
print CGREEN + "Enter location to change its Parent location" + CEND

#user input
print("Location (Type 'l' to see the list):")
readList('primary_locations')
location = str(raw_input("Location: "))

#sql query to fetch the current parent_location
db = MySQLdb.connect("localhost","test","test123","INVENTORY")
db.autocommit(1)
cursor = db.cursor()

cursor.execute(" SELECT parent_location FROM LOCATION WHERE location='%s' " %(location))
results = cursor.fetchall()
for row in results:
    parent_location = row[0]
    print("Current Parent location is "+ '%s' ) %(parent_location)

#user input for the updated parent_location
print("New Parent Location (Type 'l' to see the list):")
readList('parent_locations')
new_parent_location = str(raw_input("New Parent Location: "))

#sql query to set the new_parent_location for the user input location
sql = " UPDATE LOCATION SET parent_location = '%s' WHERE location = '%s' " %(new_parent_location, location)
try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    print("Parent location of " + location + " changed to "+ new_parent_location)
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

