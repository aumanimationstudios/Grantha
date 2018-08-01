#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import os

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

from tabulate import tabulate

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
cursor = db.cursor()

cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
col = sum(cursor.fetchall(), ())
#print col

sql = "SELECT " + ','.join(col) + " FROM ITEMS ORDER BY item_type"

#sql = "SELECT %s,%s,%s,%s,%s,%s,%s,%s FROM ITEMS ORDER BY item_type" %(a,b,c,d,e,f,g,h)
#sql = "SELECT * FROM ITEMS ORDER BY item_type"
#sql = "SELECT serial_no, model, make, purchased_on, warranty_valid_till, item_type, location, user FROM ITEMS"

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    #cursor.execute("SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
    #WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')")
    #head = sum(cursor.fetchall(), ())
    print tabulate(results, headers=col)
    #for row in results:
        #item_id = row[0]
        #serial_no = row[1]
        #model = row[2]
        #make = row[3]
        #purchased_on = row[4]
        #warranty_valid_till = row[5]
        #item_type = row[6]
        #location = row[7]
        #user = row[8]
        #print ("item_id=%s, serial_no=%s, model=%s, make=%s, purchased_on=%s, warranty_valid_till=%s, item_type=%s, " \
              #"location=%s, user=%s" %(item_id,serial_no,model,make,purchased_on,warranty_valid_till,item_type,
                                      #location,user))
except:
    print ("Error: unable to fetch data : "+ str(sys.exc_info()))

cursor.close()
db.close()

