#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

sl = str(raw_input("Serial_No: "))
mdl = str(raw_input("Model: "))
mk = str(raw_input("Make: "))
po = str(raw_input("Purchase_Date[YYYY-MM-DD]: "))
wt = str(raw_input("Warranty_Till[YYYY-MM-DD]: "))
it = str(raw_input("Item_type: "))
loc = str(raw_input("Location: "))
usr = str(raw_input("User: "))

sql = """INSERT INTO ITEMS (serial_no, model, make, purchased_on,
         warranty_valid_till, item_type, location, user) VALUES 
         ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" %(sl, mdl, mk, po, wt, it, loc, usr)

try:
    cursor = db.cursor()
    cursor.execute(sql)
    # db.commit()
    cursor.close()
    #print(db.insert_id())
    print("Item added "+ str(db.insert_id()))
except:
    #db.rollback()
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

