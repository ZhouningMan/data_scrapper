import requests
from bs4 import BeautifulSoup
import os

def retriveBestCEOs():
    baseUrl = "https://www.glassdoor.com/"
    urls = {
        "2017":"Award/Top-CEOs-LST_KQ0,8.htm",
        "2016": "Award/Highest-Rated-CEOs-2016-LST_KQ0,23.htm",
        "2015": "Award/Highest-Rated-CEOs-2015-LST_KQ0,23.htm",
        "2014": "Award/Highest-Rated-CEOs-2014-LST_KQ0,23.htm",
        "2013" :"Award/50-Highest-Rated-CEOs-2013-LST_KQ0,26.htm"
    }
    baseFolder = os.getcwd() + "/../data/"
    headers = {'user-agent': 'my-app/0.0.1'}
    s = requests.Session()
    for key, val in urls.items():
        url = baseUrl + val
        page = s.get(url, headers=headers)
        ceos = BeautifulSoup(page.text, 'html.parser')
        print(url + " --> " + str(page.status_code))
        writeToFile(baseFolder + key + "_ceos", ceos.prettify())

def writeToFile(fileName, text, override = False):
    if(not override and os.path.exists(fileName)):
        return
    with open(fileName, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    retriveBestCEOs()

if __name__ == '__main__':
    main()