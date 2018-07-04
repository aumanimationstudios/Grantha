#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
cursor = db.cursor()

sql = "SELECT * FROM ITEMS"
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print row[0:9]
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

cursor.close()
db.close()

