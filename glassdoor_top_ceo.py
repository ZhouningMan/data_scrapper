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
        yearlyTopCeos["size"] = yearlyData["size"]
        yearlyTopCeos["year"] = yearlyData["year"]
        yearlyTopCeos["ceos"] = parseTopCeoPage(yearlyData["html"])
        topCeos.append(yearlyTopCeos)
    dumpTopCeosToFile(topCeos)

def retrieveCeoHtmls():
    baseUrl = "https://www.glassdoor.com/"
    ceoLinks = [
        (2018, "Large", "Award/Top-CEOs-LST_KQ0,8.htm"),
        (2017, "Large", "Award/Highest-Rated-CEOs-2017-LST_KQ0,23.htm"),
        (2016, "Large", "Award/Highest-Rated-CEOs-2016-LST_KQ0,23.htm"),
        (2015, "Large", "Award/Highest-Rated-CEOs-2015-LST_KQ0,23.htm"),
        (2014, "Large", "Award/Highest-Rated-CEOs-2014-LST_KQ0,23.htm"),
        (2018, "Small_Medium", "Award/Top-CEOs-at-SMBs-LST_KQ0,16.htm"),
        (2017, "Small_Medium", "Award/Highest-Rated-CEOs-at-SMBs-2017-LST_KQ0,31.htm"),
        (2016, "Small_Medium", "Award/Highest-Rated-CEOs-at-SMBs-2016-LST_KQ0,31.htm"),
        (2015, "Small_Medium", "Award/Highest-Rated-CEOs-at-SMBs-2015-LST_KQ0,31.htm"),
        (2014, "Small_Medium", "Award/Highest-Rated-CEOs-at-SMBs-2014-LST_KQ0,31.htm")
    ]
    
    headers = {'user-agent': 'my-app/0.0.1'}
    ceoData = []
    s = requests.Session()
    for year, size, link in ceoLinks:
        url = baseUrl + link
        page = s.get(url, headers=headers)
        yearlyData = {}
        yearlyData["size"] = size
        yearlyData["year"] = year
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