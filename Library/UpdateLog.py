#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import os

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

from colours import *
from tabulate import tabulate

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
cursor = db.cursor()

#usage message
print CGREEN + "Enter Serial_no of the Item to view Log" + CEND

#user input
sln = str(raw_input("Serial_no: "))

#sql query to fetch the entries from the UPDATE_LOG table
sql = """ SELECT * FROM UPDATE_LOG WHERE serial_no ="%s" """ %(sln)
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    print tabulate(results, headers=['Date_time', 'Serial_no', 'Old_location', 'New_location'])
    #for row in results:
        #date_time = row[0]
        #item_id = row[1]
        #old_location = row[2]
        #new_location = row[3]
        #print "Date_Time=%s, Item_id=%s, Old_location=%s, New_location=%s" \
              #%(date_time, item_id, old_location, new_location)
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

cursor.close()
db.close()

