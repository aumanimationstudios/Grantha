#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

loc = input("location: ")
iid = input("item_id: ")

sql = """UPDATE ITEMS SET location = loc WHERE item_id = iid """

try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

