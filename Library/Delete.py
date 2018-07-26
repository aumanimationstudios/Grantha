#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
from colours import *

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

#usage message
print CGREEN + "Enter the Serial_no of the item to delete " + CEND

#user input
sln = str(raw_input("Serial_no: "))

#sql query to delete the item
sql = """DELETE FROM ITEMS WHERE serial_no = '%s' """ %(sln)
try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    print("Item with serial_no: "+ sln + " Deleted ")
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

