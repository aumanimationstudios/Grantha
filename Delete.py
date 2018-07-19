#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
from colours import *

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

#usage message
print CGREEN + "Enter the Item_id to delete " + CEND

#user input
iid = str(raw_input("Item_id: "))

#sql query to delete the item
sql = """DELETE FROM ITEMS WHERE item_id = '%s' """ %(iid)
try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    print("Item No: "+ iid + " Deleted ")
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

