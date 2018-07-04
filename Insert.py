#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

sql = """INSERT INTO ITEMS (serial_no, model, make, purchased_on,
         warranty_valid_till, item_type, location, user) VALUES 
         ('7CH3411077', 'A3P', 'HP', '2018-06-01', '2019-06-01', 'MOUSE', 'STOCK1', '')"""

try:
    cursor = db.cursor()
    cursor.execute(sql)
    # db.commit()
    cursor.close()
    print(db.insert_id())
except:
    #db.rollback()
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()


.print(

)