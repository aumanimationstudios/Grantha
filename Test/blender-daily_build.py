#!/usr/bin/python2
# *-* coding: utf-8 *-*
__author__ = "Sanath Shetty K"
__license__ = "GPL"
__email__ = "sanathshetty111@gmail.com"

## UTILITY TO UPDATE BLENDER-DAILY BUILDS ##

import sys
import os
from bs4 import BeautifulSoup
import urllib2
import re

htmlPage = urllib2.urlopen("https://builder.blender.org/download/")
soup = BeautifulSoup(htmlPage, 'html.parser')
downloadLink = None
fileName = None
untaredFolder = None
optDir = "/opt/blender-daily_build/"
# optDir = "/opt/blender-daily_build/"

for link in soup.findAll('a', attrs={'href': re.compile("(?=.*2.82)(?=.*linux-glibc217-x86_64.tar.bz2)")}):
    fileName = link.get('href').replace("/download/","")
    untaredFolder = fileName.replace(".tar.bz2","")
    downloadLink = ("https://builder.blender.org"+link.get('href'))
    print (downloadLink)
    print(fileName)

if(downloadLink):
    if(os.path.exists(os.path.join(optDir,untaredFolder))):
        os.system("sudo ln -sf " + optDir + untaredFolder + "/blender /usr/local/bin/blender")
        print("already up to date")
        sys.exit(0)
    else:
        os.system("sudo aria2c -c -s 10 -x 10 -d "+optDir+" "+ downloadLink)
        os.system("cd "+optDir+" ;sudo tar -xvf "+ fileName +" ; cd -")
        # os.system("sudo rm -frv /usr/local/bin/blender")
        os.system("sudo ln -sf "+optDir+untaredFolder+"/blender /usr/local/bin/blender")
else:
    print("Wrong Syntax.")
