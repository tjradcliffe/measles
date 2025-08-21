from bs4 import BeautifulSoup
import re

reUpdate = re.compile(r'Measles\-update_20[0-9][0-90]\-[0-9][0-9]\-[0-9][0-9]\.pdf')
strSite = "http://www.bccdc.ca"
strURL = strSite+"/health-info/diseases-conditions/measles"

pSoup = BeautifulSoup(open("main_page.html").read(), 'html.parser')

lstA = pSoup.find_all("a")

for pA in lstA:
    if "href" in pA.attrs:
        strHref = pA.attrs['href']
        if reUpdate.search(strHref):
            print(strHref)
