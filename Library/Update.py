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

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

#present date and time
now = time.strftime('%Y-%m-%d %H:%M:%S')

#usage message
print CGREEN + "Enter serial_no to change items Location and User"
print "Don't leave any area blank"+ CEND

#user input
sln = str(raw_input("Serial_no: "))

#sql query to fetch the present location and user of the item
cursor = db.cursor()
cursor.execute(""" SELECT location, user FROM ITEMS WHERE serial_no="%s" """ %(sln))
results = cursor.fetchall()
for row in results:
    location = row[0]
    user = row[1]
    print("Item is at "+ '%s' + " User: " + '%s') %(location,user)

#user input for the updated location
loc = str(raw_input("Location[aum_r(01-03)_stock01, aum_r01_workspace_(01-09), aum_r02_workspace_M01, "
                    "aum_r02_workspace_(pA1-pA10),aum_r02_workspace_(pB1-pB8), aum_r02_workspace_(pC1-pC9), "
                    "blue(0001-0035)]: "))
usr = str(raw_input("New User: "))

#sql query to update the location and user of the item
sql = """ UPDATE ITEMS SET location = '%s', user= '%s' WHERE serial_no = '%s' """ %(loc, usr, sln)
try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    print("Item location changed to "+ loc +" New User: "+ usr)
    print now
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

#sql query to store the update details in UPDATE_LOG table
cursor = db.cursor()
for row in results:
    location = row[0]
    cursor.execute(""" INSERT INTO UPDATE_LOG (date_time, serial_no, old_location, new_location) VALUES
              ('%s', '%s', '%s', '%s') """ %(now, sln, location, loc) )

db.close()

