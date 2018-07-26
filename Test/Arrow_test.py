#!/usr/bin/python2.7
# *-* coding: utf-8 *-*

import datetime
import arrow

utc = arrow.utcnow()
print(utc)

local = utc.to('Asia/Kolkata')
print(local)

print(local.timestamp)

print(local.format())

print(local.format('DD-MM-YYYY HH:mm:ss'))

print(local.humanize())

print(arrow.get(datetime.date(2018, 7, 1)))

