#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import readchar
import MySQLdb
import os
import sys

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

from tabulate import tabulate
from colours import *

while True:
    key = readchar.readkey()
    if(key == 'l'):
        db = MySQLdb.connect("localhost","test","test123","INVENTORY")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM ITEM_TYPE")
        results = cursor.fetchall()
        print tabulate(results)

        cursor.close()
        db.close()
        break
    elif readchar.key.ENTER:
        break
    else:
        print("Press a valid key")

