#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
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
print CGREEN + "Insert Details of the Item" + CEND

#user input
userInput = OrderedDict()

userInput["serial_no"] = str(raw_input("Serial_No: "))

print("Item_type (Type 'l' to see the list):")
readList('item_type')
userInput["item_type"] = str(raw_input("Item_type: "))

userInput["make"] = str(raw_input("Make: "))

userInput["model"] = str(raw_input("Model: "))

userInput["price"] = str(raw_input("Price: "))

userInput["purchased_on"] = str(raw_input("Purchase_Date[YYYY-MM-DD]: "))

userInput["warranty_till"] = str(raw_input("Warranty_Till[YYYY-MM-DD]: "))

print("Location (Type 'l' to see the list):")
readList('location')
userInput["location"] = str(raw_input("Location: "))

print("User (Type 'l' to see the list):")
readList('user')
userInput["user"] = str(raw_input("User: "))

values = []
for key in userInput.keys():
    values.append(userInput[key])
#print values

#user input
#sl = str(raw_input("Serial_No: "))
#mdl = str(raw_input("Model: "))
#mk = str(raw_input("Make: "))
#po = str(raw_input("Purchase_Date[YYYY-MM-DD]: "))
#wt = str(raw_input("Warranty_Till[YYYY-MM-DD]: "))

#print("Item_type (Type 'l' to see the list):")
#readList('item_type')

#it = str(raw_input("Item_type: "))

#print("Location (Type 'l' to see the list):")
#readList('location')

#loc = str(raw_input("Location: "))

#print("User (Type 'l' to see the list):")
#readList('user')

#usr = str(raw_input("User: "))

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)
cursor = db.cursor()

cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
col = sum(cursor.fetchall(), ())

#sql query to insert an item to the ITEMS table with user input data

sql = "INSERT INTO ITEMS (" + ','.join(col) + ") VALUES %r" %(tuple(values),)
#sql = "INSERT INTO ITEMS (serial_no, model, make, purchased_on, warranty_valid_till, item_type, location, user) \
       #VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(sl, mdl, mk, po, wt, it, loc, usr)
#print sql
try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.execute("INSERT INTO SERIAL_NO (serial_no) VALUES ('%s') " %(userInput["serial_no"]))
    cursor.close()
    print("Item added to the list")
    #print("Item added, Item_id: "+ str(db.insert_id()))
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

