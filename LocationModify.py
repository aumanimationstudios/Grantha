#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import time
from colours import *

db = MySQLdb.connect("localhost","test","test123","INVENTORY")
db.autocommit(1)

print CGREEN + "Enter location to change its Primary location" + CEND

loc = str(raw_input("location[BLUE0001-0666]: "))

cursor = db.cursor()
cursor.execute(""" SELECT parent_location FROM LOCATION WHERE location="%s" """ %(loc))
results = cursor.fetchall()
for row in results:
    parent_loc = row[0]
    print("Current Parent location is "+ '%s' ) %(parent_loc)

parent_location = str(raw_input("New Parent Location[WORKSPACE1-35]: "))

sql = """ UPDATE LOCATION SET parent_location = '%s' WHERE location = '%s' """ %(parent_location, loc)

try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    print("Parent location changed to "+ parent_location)
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())
db.close()

