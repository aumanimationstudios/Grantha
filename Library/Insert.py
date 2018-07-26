#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
from colours import *

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
db.autocommit(1)

#usage message
print CGREEN + "Insert Details of the Item" + CEND

#user input
sl = str(raw_input("Serial_No: "))
mdl = str(raw_input("Model: "))
mk = str(raw_input("Make: "))
po = str(raw_input("Purchase_Date[YYYY-MM-DD]: "))
wt = str(raw_input("Warranty_Till[YYYY-MM-DD]: "))
it = str(raw_input("Item_type[CABLE, GRAPHICS_CARD-GT730-4GB, HARD_DISK-1TB_BLUE, HEADPHONE, KEYBOARD,"
                   " MONITOR, MOUSE, PEN_DISPLAY, PEN_TABLET, RAM-8GB-DDR3, SMPS]: "))
loc = str(raw_input("Location[aum_r(01-03)_stock01, aum_r01_workspace_(01-09), aum_r02_workspace_M01, "
                    "aum_r02_workspace_(pA1-pA10),aum_r02_workspace_(pB1-pB8), aum_r02_workspace_(pC1-pC9), "
                    "blue(0001-0035)]: "))
usr = str(raw_input("User: "))

#sql query to insert an item to the ITEMS table with user input data
sql = """INSERT INTO ITEMS (serial_no, model, make, purchased_on,
         warranty_valid_till, item_type, location, user) VALUES 
         ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" %(sl, mdl, mk, po, wt, it, loc, usr)

try:
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    print("Item added to the list")
    #print("Item added, Item_id: "+ str(db.insert_id()))
except:
    print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

