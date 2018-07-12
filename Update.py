#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import arrow

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

utc = arrow.utcnow()
local = utc.to('Asia/Kolkata')

iid = str(raw_input("item_id: "))

cursor = db.cursor()
cursor.execute(""" SELECT location FROM ITEMS WHERE item_id="%s" """ %(iid))
results = cursor.fetchall()
for row in results:
    location = row[0]
    print("Item is at "+ '%s' ) %(location)

loc = str(raw_input("New location[REPAIR, STOCK(1-3), WORKSPACE(1-35)]: "))

sql = """ UPDATE ITEMS SET location = '%s' WHERE item_id = '%s' """ %(loc, iid)

try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    print("Item location changed to "+ loc)
    print(local.format('DD-MM-YYYY HH:mm:ss'))
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

cursor = db.cursor()
for row in results:
    location = row[0]
    cursor.execute(""" INSERT INTO UPDATE_LOG (date_time, item_id, old_location, new_location) VALUES
              ('%s', '%s', '%s', '%s') """ %(local, iid, location, loc) )

db.close()

