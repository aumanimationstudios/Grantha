# #!/usr/bin/python2.7
# # *-* coding: utf-8 *-*
#
# import MySQLdb
# import sys
# import os
#
# #filePath = os.path.abspath(__file__)
# #progPath = os.sep.join(filePath.split(os.sep)[:-2])
# #libraryPath = os.path.join(progPath,"Library","External_Modules")
# #sys.path.append(libraryPath)
#
# #from tabulate import tabulate
#
# '''db = MySQLdb.connect("localhost","test","test123","INVENTORY")
# cursor = db.cursor()
#
# cursor.execute("SELECT SUM(price) FROM ITEMS")
# total_all = cursor.fetchone()[0]
# #a = total1[0]
# print ("Total = " + str(total_all))
# #print tabulate(total1, headers=['total all'])
#
# item_type = str(raw_input("Item type: "))
# cursor.execute("SELECT SUM(price) FROM ITEMS WHERE item_type='%s' " %(item_type))
# total = cursor.fetchone()[0]
# print ("Total = " + str(total))
# #print tabulate(total2, headers=['total amount of the item'])
#
# cursor.close()
# db.close()'''
#
# import datetime
# import time
# import MySQLdb
# import arrow
#
# db = MySQLdb.connect("localhost", "test", "test123", "INVENTORY")
# db.autocommit(1)
# cursor = db.cursor()
#
# sln = '123'
# loc = 'REPAIR'
# cursor.execute("SELECT date_time FROM UPDATE_LOG WHERE serial_no='%s' AND new_location ='%s' " %(sln,loc))
# results = cursor.fetchone()
# logTime = str(results[0])
#
# a = arrow.get(logTime).shift(hours=-5,minutes=-30)
#
# print a.humanize()
#
#
# #print logTime
# #print("logtime :"+ str(logTime))
#
# #b = arrow.now()
# # c = a.to('Asia/Kolkata')
# #d = arrow.utcnow().shift(hours=5,minutes=30)
# #print a
# #print d
# # print c
# # time.strftime('%Y-%m-%d %H:%M:%S')
#
# #date_1 = arrow.get('2015-12-23 18:40:48','YYYY-MM-DD HH:mm:ss')
# #date_2 = arrow.get('2017-11-15 13:18:20','YYYY-MM-DD HH:mm:ss')
# #print(date_1)
# #print(date_2)
#
# #diff = d - a
# #print diff
#
# '''format = '%Y-%m-%d %H:%M:%S'
# #logtime = datetime.datetime.strptime(result, format)
# now = datetime.datetime.now()
# #print logtime
# now1 = now.strftime(format)
# print now1
# def convertTimestampToSQLDateTime(value):
#     return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(value))
# def convertSQLDateTimeToTimestamp(value):
#     return time.mktime(time.strptime(value, '%Y-%m-%d %H:%M:%S'))
# a = convertSQLDateTimeToTimestamp(logTime)
# b = convertSQLDateTimeToTimestamp(now1)
# print a
# print b
#
# print b-a
# '''
#
# '''print("Item type (type 'l' to see the list):")
# readList('item_type')
# item_type = str(raw_input("Item type: "))
#
# print("Location (type 'l' to see the list):")
# readList('all_locations')
# location = str(raw_input("Location: "))
#
# if not location:
#     cursor.execute("SELECT COUNT(*) FROM ITEMS WHERE item_type='%s' " %(item_type))
#
# else:
#     cursor.execute("SELECT COUNT(*) FROM ITEMS WHERE item_type='%s' AND location='%s' " %(item_type,location))
#
#
# results = cursor.fetchone()
# n = results[0]
# #print n
# if not location:
#     print ("Total number of " + item_type + " is " + str(n))
# else:
#     print ("There are " + str(n) +" "+ item_type + " at " + location )
#
# cursor.close()
# db.close()'''


import sys
import os
from bs4 import BeautifulSoup
import urllib2
import re

user = sys.argv[1]

htmlPage = urllib2.urlopen("https://gist.github.com/{0}".format(user))
soup = BeautifulSoup(htmlPage, 'html.parser')

# for link in soup.findAll('a', attrs={'href': re.compile("(?=.*2.8)(?=.*linux-glibc217-x86_64.tar.bz2)")}):

for link in soup.findAll('a', attrs={'href': re.compile("(?=.*gist)(?=.*{0})".format(user))}):
    fileName = link.get('href')
    print(fileName)
