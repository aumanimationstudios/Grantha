#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

sql = """DELETE FROM ITEMS WHERE item_id >= 4 """

try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

