import lib.libutil as libutil
import lib.data_model as data_model
import os
from bs4 import BeautifulSoup

def processCeoCompData(html):
    compSoup = BeautifulSoup(html, 'html.parser')
    ceosComp = []
    ceoCompRows = []
    ceoCompRows.extend(compSoup.find_all("tr", class_="exec odd"))
    ceoCompRows.extend(compSoup.find_all("tr", class_="exec even"))
    for row in ceoCompRows:
        ceosComp.append(extractCeoPayFromCeoHtmlRow(row))
    return ceosComp

def extractCeoPayFromCeoHtmlRow(ceoRow):
    company = ceoRow.find("td", class_="company").find(text=True, recursive=False)
    ticker = ceoRow["co"]
    industry = ceoRow["industry"]
    ceo = ceoRow.find("td", class_="name").string
    ceoNameComponents= ceo.split()
    if(len(ceoNameComponents) > 2):
        ceo = "{} {}".format(ceoNameComponents[0], ceoNameComponents[-1])
    pay = ceoRow.find("td", class_="num pay sorting_1").find(text=True, recursive=False)
    payChangeData = ceoRow.find("td", class_="pos num tsr")
    payChangeValue = payChangeData.string  if payChangeData else "+0%"
    year = ceoRow.find("td", class_="num fiscalYear").string
    ceoPay = data_model.CeoPay(company.strip(), 
    industry.strip(), 
    ticker.strip(), 
    ceo.strip(),
    pay.strip(), 
    payChangeValue.strip(), 
    year.strip())
    return ceoPay
    
def sourceFile():
    return os.getcwd() + "/../raw_data/CEO_Pay_for_the_SP_500_WSJ.html"

def targetFile():
    return os.getcwd() + "/../data/ceo_compensation.json"

def main():
    rawData = sourceFile()
    html = libutil.readTextFile(rawData)
    ceosComp = processCeoCompData(html)
    destination = targetFile()
    libutil.dumpToJsonFile(ceosComp, data_model.DataJsonEncoder, destination)

if __name__ == "__main__":
    main()