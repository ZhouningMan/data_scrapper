import requests
import json
from bs4 import BeautifulSoup
import os

class Ceo:
    def __init__(self, rank, name, employer):
        self._rank = rank;
        self._name = name
        self._employer = employer

    @property
    def rank(self):
        return self._rank

    @property
    def name(self):
        return self._name;
    
    @property
    def employer(self):
        return self._employer

class CeoEncoder(json.JSONEncoder):
    def default(self, obj):
        if(isinstance(obj, Ceo)) :
            return {"rank": obj.rank, "name": obj.name, "employer": obj.employer}
        return json.JSONEncoder.default(self, obj)

def processTopCeos():
    ceoData = retrieveCeoHtmls()
    topCeos = []
    for yearlyData in ceoData:
        yearlyTopCeos = {}
        yearlyTopCeos["year"] = yearlyData["year"]
        yearlyTopCeos["ceos"] = parseTopCeoPage(yearlyData["html"])
        topCeos.append(yearlyTopCeos)
    dumpTopCeosToFile(topCeos)

def retrieveCeoHtmls():
    baseUrl = "https://www.glassdoor.com/"
    urls = {
        "2017":"Award/Top-CEOs-LST_KQ0,8.htm",
        "2016": "Award/Highest-Rated-CEOs-2016-LST_KQ0,23.htm",
        "2015": "Award/Highest-Rated-CEOs-2015-LST_KQ0,23.htm",
        "2014": "Award/Highest-Rated-CEOs-2014-LST_KQ0,23.htm",
        "2013" :"Award/50-Highest-Rated-CEOs-2013-LST_KQ0,26.htm"
    }
    
    headers = {'user-agent': 'my-app/0.0.1'}
    ceoData = []
    s = requests.Session()
    for key, val in urls.items():
        url = baseUrl + val
        page = s.get(url, headers=headers)
        yearlyData = {}
        yearlyData["year"] = int(key)
        yearlyData["html"] = page.text
        ceoData.append(yearlyData)
    return ceoData

def parseTopCeoPage(html):
    ceoSoup = BeautifulSoup(html, 'html.parser')
    yearlyCeos = []
    topCeoDiv = ceoSoup.find("div", class_="panel-heading tbl fill active")
    yearlyCeos.append(extractCeoFromCeoDiv(topCeoDiv))
    for ceoDiv in ceoSoup.find_all("div", class_="panel-heading tbl fill "):
        yearlyCeos.append(extractCeoFromCeoDiv(ceoDiv))
    return yearlyCeos

def extractCeoFromCeoDiv(ceoDiv):
    rank = ceoDiv.find("div", class_="cell middle rank").string
    name = ceoDiv.find("div", class_="cell middle ceo-name strong").string
    employer = ceoDiv.find("div", class_="cell middle panel-header-employer-name").string
    return Ceo(int(rank), name, employer)


def dumpTopCeosToFile(topCeos):
    path  =  os.getcwd() + "/../data/TopCeos.json"
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(topCeos, fp, cls=CeoEncoder)

def writeToFile(fileName, text, override = False):
    if(not override and os.path.exists(fileName)):
        return
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    processTopCeos()

if __name__ == '__main__':
    main()