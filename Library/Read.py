#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import os

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

from colours import *
from tabulate import tabulate

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
cursor = db.cursor()

#usage message
print (CGREEN + "Read the list for a specific item, location or item type")
print ("Leave the field blank if not applicable" + CEND)

#user input
sln = str(raw_input("Serial_no: "))
loc = str(raw_input("Location[aum_r(01-03)_stock01, aum_r01_workspace_(01-09), aum_r02_workspace_M01, "
                    "aum_r02_workspace_(pA1-pA10),aum_r02_workspace_(pB1-pB8), aum_r02_workspace_(pC1-pC9), "
                    "blue(0001-0035)]: "))
it = str(raw_input("Item_type[CABLE, GRAPHICS_CARD-GT730-4GB, HARD_DISK-1TB_BLUE, HEADPHONE, KEYBOARD,"
                   " MONITOR, MOUSE, PEN_DISPLAY, PEN_TABLET, RAM-8GB-DDR3, SMPS]: "))
usr = str(raw_input("User: "))

#sql query to select rows which satisfies the conditions from user input
sql = """SELECT serial_no, model, make, purchased_on, warranty_valid_till, item_type, location, user FROM ITEMS
         WHERE serial_no= "%s" OR location= "%s" OR item_type= "%s" OR user= "%s" """ %(sln,loc,it,usr)

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    print tabulate(results, headers=['serial_no', 'model', 'make', 'purchased_on', 'warranty_valid_till',
                                     'item_type', 'location', 'user'])
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

