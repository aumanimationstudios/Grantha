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

libraryPath = os.path.join(progPath,"Library")
sys.path.append(libraryPath)
from ListOptions import readList

#usage message
print (CGREEN + "Read the list for a specific item, location or item type")
print ("Leave the field blank if not applicable" + CEND)

#user input
userInput = {}

userInput["serial_no"] = str(raw_input("Serial_no: "))

print("Location (Type 'l' to see the list):")
readList('location')
userInput["location"] = str(raw_input("Location: "))

print("Item_type (Type 'l' to see the list):")
readList('item_type')
userInput["item_type"] = str(raw_input("Item_type: "))

print("User (Type 'l' to see the list):")
readList('user')
userInput["user"] = str(raw_input("User: "))

whereClause = []
for key in userInput.keys():
    if userInput[key]:
        whereClause.append(key +" = \'" + userInput[key] +"\'")

#sql query to select rows which satisfies the conditions from user input
#sql = """SELECT serial_no, model, make, purchased_on, warranty_valid_till, item_type, location, user FROM ITEMS
         #WHERE serial_no= "%s" OR location= "%s" OR item_type= "%s" OR user= "%s" """ %(sln,loc,it,usr)
if(whereClause):
    db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
    cursor = db.cursor()
    cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
    WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
    col = sum(cursor.fetchall(), ())

    sql = "SELECT " + ','.join(col) + " FROM ITEMS WHERE " + " OR ".join(whereClause)

else:
    print("Nothing to do. Exiting.. ")
    sys.exit(0)

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    #cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
    #WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
    #head = cursor.fetchall()
    #my_head = sum(head,())
    #my_head = [element for x in head for element in x]

    print tabulate(results, headers=col) #headers=['serial_no', 'model', 'make', 'purchased_on', 'warranty_valid_till',
                                     #'item_type', 'location', 'user'])
    #for row in results:
        #item_id = row[0]
        #serial_no = row[1]
        #model = row[2]
        #make = row[3]
        #purchased_on = row[4]
        #warranty_valid_till = row[5]
        #item_type = row[6]
        #location =str(my_head0) row[7]
        #user = row[8]
        #print ("item_id=%s, serial_no=%s, model=%s, make=%s, purchased_on=%s, warranty_valid_till=%s, item_type=%s, " \
              #"location=%s, user=%s" %(item_id,serial_no,model,make,purchased_on,warranty_valid_till,item_type,
                                      #location,user))
except:
    print ("Error: unable to fetch data : "+ str(sys.exc_info()))

cursor.close()
db.close()

