from get_html import *

from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from math import sqrt
from pypdf import PdfReader
from random import random
from time import sleep

import os
import re

reUpdate = re.compile(r'Measles\-update_20[0-9][0-90]\-[0-9][0-9]\-[0-9][0-9]\.pdf')
strSite = "http://www.bccdc.ca"
strURL = strSite+"/health-info/diseases-conditions/measles"

pGetter = GetHTML()

strMainPage = "main_page.html"
pStat = os.stat(strMainPage)
#print(pStat.st_mtime)
pFileDate = datetime.fromtimestamp(pStat.st_mtime).date()
#print(pFileDate)

if pFileDate != date.today():
    print("Getting main file...")
    pSoup = pGetter.getHTML(strURL)
    with open(strMainPage, "w") as outFile:
        outFile.write(pSoup.prettify())
else:
    pSoup = BeautifulSoup(open(strMainPage).read(), 'html.parser')

lstA = pSoup.find_all("a")
mapResults = {}
for pA in lstA:
    if "href" in pA.attrs:
        strHref = pA.attrs['href']
        if reUpdate.search(strHref):
            strText = ""
            strLocalFile = os.path.split(strHref)[-1]
            strDate = strLocalFile.split("_")[-1].replace(".pdf", "").strip()
            pDate = date.fromisoformat(strDate)
            if not os.path.exists(strLocalFile):
                strURL = strSite+strHref
                print("Downloading to: ", strLocalFile)
                strText = getPDF(strURL, strLocalFile)
                sleep(1+random())
            else:
                pReader = PdfReader(strLocalFile)
                for pPage in pReader.pages:
                    strText += pPage.extract_text() + "\n"
            
            lstText = strText.split("\n")
            for strTag in ["Total", "British Columbia"]:
                for strLine in lstText:
                    if strLine.strip().startswith(strTag):
                        lstData = strLine.split()[3:]
                        if len(lstData) == 0: break
                        if "%" in lstData[0]:
                            lstData = strLine.split()[4:]
                            lstData.pop()
#                        print(lstData)
                        mapResults[pDate] = " ".join(lstData)+" "+str(sqrt(int(lstData[-1])))
                        break

with open("bc_measles.dat") as inFile:
    for strLine in inFile:
        strLine = strLine.strip()
        if strLine.startswith("#"): continue
        pLast = date.fromisoformat(strLine.split()[0])

lstKeys = list(mapResults.keys())
lstKeys.sort()
with open("bc_measles.dat", "a") as outFile:
#    outFile.write("#Date Confirmed Suspected Total TotalError\n")
    for pDate in lstKeys:
        if pDate > pLast:
            outFile.write(str(pDate)+" "+mapResults[pDate]+"\n")

pEndDate = date.today()+timedelta(days=7)
with open("play_bc.gno", "w") as outFile:
    outFile.write("delay: 0.1\n")
    outFile.write("set yrange [0:]\n")
    outFile.write("set format x date\n")
    outFile.write("set xrange [2025-07-01:"+str(pEndDate)+"]\n")
    outFile.write('set xlabel "Date"\n')
    outFile.write('set ylabel "Known Cases"\n')
    outFile.write("f(x) = A*exp((x-datetime(2025, 7, 7)).days/B)\n")
    outFile.write("A = 103.13\n")
    outFile.write("B = 55.95\n")
    outFile.write('plot "bc_measles.dat" using 1:4:5 with errorbars title "BC Measles Cases", f(x) title "Exponential Fit, Doubling Time = 38.8 days"\n')
