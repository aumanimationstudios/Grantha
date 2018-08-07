#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import os

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath, "Library")
sys.path.append(libraryPath)

from ListOptions import readList

db = MySQLdb.connect("localhost","test","test123","INVENTORY")
cursor = db.cursor()

print("Item type (type 'l' to see the list):")
readList('item_type')
item_type = str(raw_input("Item type: "))

print("Location (type 'l' to see the list):")
readList('all_locations')
location = str(raw_input("Location: "))

if not location:
    cursor.execute("SELECT COUNT(*) FROM ITEMS WHERE item_type='%s' " %(item_type))

else:
    cursor.execute("SELECT COUNT(*) FROM ITEMS WHERE item_type='%s' AND location='%s' " %(item_type,location))


results = cursor.fetchone()
n = results[0]
#print n
if not location:
    print ("Total number of " + item_type + " is " + str(n))
else:
    print ("There are " + str(n) +" "+ item_type + " at " + location )

cursor.close()
db.close()

