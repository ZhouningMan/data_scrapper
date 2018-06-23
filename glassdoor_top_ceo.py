import requests
import json
from bs4 import BeautifulSoup
import os
import lib.data_model as data_model

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
    nameCompoennts = name.split()
    if(len(nameCompoennts) > 2):
        name = "{} {}".format(nameCompoennts[0], nameCompoennts[-1])
    employer = ceoDiv.find("div", class_="cell middle panel-header-employer-name").string
    return data_model.Ceo(int(rank), name.strip(), employer.strip())


def dumpTopCeosToFile(topCeos):
    path  =  os.getcwd() + "/../data/TopCeos.json"
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(topCeos, fp, cls=data_model.DataJsonEncoder)

def main():
    processTopCeos()

if __name__ == '__main__':
    main()