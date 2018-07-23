#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
from tabulate import tabulate

db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
cursor = db.cursor()

sql = """ SELECT serial_no, model, make, purchased_on, warranty_valid_till, item_type, location, user FROM ITEMS """

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

