#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
cursor = db.cursor()

iid = str(raw_input("Item_id: "))

sql = """ SELECT * FROM UPDATE_LOG WHERE item_id ="%s" """ %(iid)

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        date_time = row[0]
        item_id = row[1]
        old_location = row[2]
        new_location = row[3]
        print "Date_Time=%s, Item_id=%s, Old_location=%s, New_location=%s" \
              %(date_time, item_id, old_location, new_location)
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

cursor.close()
db.close()

