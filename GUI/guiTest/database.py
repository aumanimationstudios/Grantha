#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import MySQLdb
import MySQLdb.cursors
import sys

class DataBase:
    col = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
           WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')"

    all = "SELECT * FROM ITEMS ORDER BY item_type"

    comp = "SELECT serial_no,item_type,location,user FROM ITEMS"

    def __init__(self):
        self.database = MySQLdb.connect("localhost","test","test123","INVENTORY")
        self.cursor = self.database.cursor(MySQLdb.cursors.DictCursor)

        # self.col = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
        #               WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')"
        #
        # self.cmd = "SELECT * FROM ITEMS ORDER BY item_type "

    def getColumns(self):
        try:
            self.cursor.execute(DataBase.col)
            column = self.cursor.fetchall()
            # columnNames =  [x['COLUMN_NAME'] for x in column]
            return column
            # print columnNames
        except:
            print ("Error: unable to fetch data : "+ str(sys.exc_info()))

    def getAllRows(self):
        try:
            self.cursor.execute(DataBase.all)
            rows = self.cursor.fetchall()
            return rows

        except:
            print ("Error: unable to fetch data : "+ str(sys.exc_info()))

    def getAllValues(self,init=False):
        try:
            if(init == False):
                result = self.cursor.fetchone()
                return result
            else:
                self.cursor.execute(DataBase.all)

        except:
            print ("Error: Unable to fetch data : "+ str(sys.exc_info()))

    def Completer(self):
        try:
            self.cursor.execute(DataBase.comp)
            slList = self.cursor.fetchall()
            return slList

        except:
            print ("Error: Unable to fetch data : " + str(sys.exc_info()))


if __name__ == '__main__':
    # database = MySQLdb.connect("localhost","test","test123","INVENTORY")
    # cursor = database.cursor(MySQLdb.cursors.DictCursor)
    # dbu = DataBase(database,cursor)
    dbu = DataBase()

    # cursor.close()
    # database.close()

