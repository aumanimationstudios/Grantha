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

    getSN = "SELECT * FROM SERIAL_NO"

    getIT = "SELECT * FROM ITEM_TYPE"

    getLOC = "SELECT location FROM LOCATION"

    getUSR = "SELECT * FROM USER"

    getDESC = "SELECT * FROM DESCRIPTION"

    getMK = "SELECT * FROM MAKE"

    getMDL = "SELECT * FROM MODEL"

    def __init__(self):
        self.database = MySQLdb.connect("localhost","test","test123","INVENTORY")
        self.database.autocommit(1)
        self.cursor = self.database.cursor(MySQLdb.cursors.DictCursor)

        # self.col = "SELECT (COLUMN_NAME) FROM INFORMATION_SCHEMA.COLUMNS \
        #               WHERE TABLE_NAME = 'ITEMS' AND COLUMN_NAME NOT IN ('item_id')"
        #
        # self.cmd = "SELECT * FROM ITEMS ORDER BY item_type "

    def getColumns(self):
        try:
            self.cursor.execute(DataBase.col)
            column = self.cursor.fetchall()
            return column
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

    def getRows(self,query):
        try:
            self.cursor.execute(query)
            slSearch = self.cursor.fetchall()
            return slSearch
        except:
            print ("Error: Unable to fetch data : " + str(sys.exc_info()))

    def getValues(self,query,init=False):
        try:
            if(init == False):
                result = self.cursor.fetchone()
                return result
            else:
                self.cursor.execute(query)
        except:
            print ("Error: Unable to fetch data : "+ str(sys.exc_info()))


    def listOfSerialNo(self):
        try:
            self.cursor.execute(DataBase.getSN)
            sn = self.cursor.fetchall()
            return sn
        except:
            print("Error: unable to fetch data : "+ str(sys.exc_info()))

    def listOfItemType(self):
        try:
            self.cursor.execute(DataBase.getIT)
            it = self.cursor.fetchall()
            return it
        except:
            print ("Error: unable to fetch data : "+ str(sys.exc_info()))

    def listOfLocation(self):
        try:
            self.cursor.execute(DataBase.getLOC)
            loc = self.cursor.fetchall()
            return loc
        except:
            print ("Error: unable to fetch data : "+ str(sys.exc_info()))

    def listOfUser(self):
        try:
            self.cursor.execute(DataBase.getUSR)
            usr = self.cursor.fetchall()
            return usr
        except:
            print ("Error: unable to fetch data : "+ str(sys.exc_info()))

    def listOfDescription(self):
        try:
            self.cursor.execute(DataBase.getDESC)
            desc = self.cursor.fetchall()
            return desc
        except:
            print ("Error: unable to fetch data : "+ str(sys.exc_info()))

    def listOfMake(self):
        try:
            self.cursor.execute(DataBase.getMK)
            mk = self.cursor.fetchall()
            return mk
        except:
            print ("Error: unable to fetch data : "+ str(sys.exc_info()))

    def listOfModel(self):
        try:
            self.cursor.execute(DataBase.getMDL)
            mdl = self.cursor.fetchall()
            return mdl
        except:
            print ("Error: unable to fetch data : "+ str(sys.exc_info()))

    def insertItem(self,query):
        try:
            self.cursor.execute(query)
            okMsg = "Item Added Successfully"
            return okMsg
            # print "Item Added"
        except:
            print ("Error: Unable to fetch data : " + str(sys.exc_info()))
            errMsg = str(sys.exc_info())
            return errMsg

    def insertDescription(self, query):
        try:
            self.cursor.execute(query)
        except:
            print ("Error: Unable to fetch data : " + str(sys.exc_info()))

    def insertMake(self, query):
        try:
            self.cursor.execute(query)
        except:
            print ("Error: Unable to fetch data : " + str(sys.exc_info()))

    def insertModel(self, query):
        try:
            self.cursor.execute(query)
        except:
            print ("Error: Unable to fetch data : " + str(sys.exc_info()))

    def insertSerialNo(self, query):
        try:
            self.cursor.execute(query)
        except:
            print ("Error: Unable to fetch data : " + str(sys.exc_info()))



if __name__ == '__main__':
    # database = MySQLdb.connect("localhost","test","test123","INVENTORY")
    # cursor = database.cursor(MySQLdb.cursors.DictCursor)
    # dbu = DataBase(database,cursor)
    dbu = DataBase()

    # cursor.close()
    # database.close()

