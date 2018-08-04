#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import sys
import os
import readchar

filePath = os.path.abspath(__file__)
progPath = os.sep.join(filePath.split(os.sep)[:-2])
libraryPath = os.path.join(progPath,"Library","External_Modules")
sys.path.append(libraryPath)

from tabulate import tabulate

def readList(option):
    db = MySQLdb.connect("localhost","test","test123","INVENTORY")
    cursor = db.cursor()

    if (option == 'all_locations'):
        while True:
            key = readchar.readkey()
            if(key == 'l'):
                cursor.execute("SELECT location FROM LOCATION")
                results = cursor.fetchall()
                print tabulate(results)
                break
            elif readchar.key.ENTER:
                break
            else:
                print("Press a valid key")
    elif (option == 'item_type'):
         while True:
            key = readchar.readkey()
            if(key == 'l'):
                cursor.execute("SELECT * FROM ITEM_TYPE")
                results = cursor.fetchall()
                print tabulate(results)
                break
            elif readchar.key.ENTER:
                break
            else:
                print("Press a valid key")
    elif(option == 'user'):
        while True:
            key = readchar.readkey()
            if(key == 'l'):
                cursor.execute("SELECT * FROM USER")
                results = cursor.fetchall()
                print tabulate(results)
                break
            elif readchar.key.ENTER:
                break
            else:
                print("Press a valid key")

