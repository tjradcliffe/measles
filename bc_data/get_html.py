from bs4 import BeautifulSoup

from playwright.sync_api import sync_playwright
from playwright._impl._errors import TimeoutError

class GetHTMLTimeout(Exception):
    """Timeout in the HTML processing"""
    pass


class GetHTML:

    knFirefox = 0
    knWebkit = 1
    knChromium = 2
    
    def __init__(self, nBrowser = knFirefox):
        self.pPlaywright = sync_playwright().start()
        if nBrowser == GetHTML.knFirefox:
            self.pBrowser = self.pPlaywright.firefox.launch()
        elif nBrowswer == GetHTML.knWebkit:
            self.pBrowser = self.pPlaywright.webkit.launch()
        elif nBrowswer == GetHTML.knChromium:
            self.pBrowser = self.pPlaywright.chromium.launch()
        self.pPage = self.pBrowser.new_page()
        
    def __del__(self):
        self.pPlaywright.stop()
        
    def getHTML(self, strURL):
        try:
            self.pPage.goto(strURL)
        except TimeoutError:
            raise GetHTMLTimeout("Timeout processing: "+strURL)
            
        return BeautifulSoup(self.pPage.content(), 'html.parser')

if __name__ == "__main__":
    pGetter = GetHTML()
    
    strURL = "http://www.bccdc.ca/health-info/diseases-conditions/measles"

    pSoup = pGetter.getHTML(strURL)
    with open("main_page.html", "w") as outFile:
        outFile.write(pSoup.prettify())
    