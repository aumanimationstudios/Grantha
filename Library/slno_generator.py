#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import sys
import string
import random
import MySQLdb

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for n in range(size))

db = MySQLdb.connect("localhost","test","test123","INVENTORY")
db.autocommit(1)
while(True):
    try:
        id = id_generator()
        cursor=db.cursor()
        cursor.execute("""INSERT INTO SERIAL_NO (serial_no) VALUES ("%s") """ %(id))
        print id
        cursor.close()
        break
    except:
        print "Error: unable to fetch data : "+ str(sys.exc_info())

db.close()

