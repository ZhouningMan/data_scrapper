import pymysql.cursors
import collections
import traceback
import json
import os
import re
import lib.libmysql as libmysql

def createCeoCompTableIfNotExist(connection):
    createTableIfNotExist = """
        CREATE TABLE IF NOT EXISTS `ceo_compensation`
            (`id` int(11) NOT NULL AUTO_INCREMENT,
            `ceo` varchar(80) COLLATE utf8_bin NOT NULL,
            `compensation` BIGINT(12) NOT NULL,
            `compchange` decimal(6,2) NOT NULL,
            `company` varchar(80) COLLATE utf8_bin NOT NULL,
            `industry` varchar(20) COLLATE utf8_bin NOT NULL,
            `ticker` varchar(10) COLLATE utf8_bin NOT NULL,
            `year` int(5) NOT NULL,
            PRIMARY KEY (`id`)) 
            ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
            AUTO_INCREMENT=1
    """
    libmysql.execute(connection, createTableIfNotExist)

def insertCeoData(connection, data):
    bulkInsertSql = """
    INSERT INTO `ceo_compensation` 
    (`ceo`, `compensation`, `compchange`, `company`, `industry`, `ticker`, `year`) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    libmysql.bulkInsert(connection, bulkInsertSql, data)

def loadCeoCompensationData():
    path = os.getcwd() + "/../data/ceo_compensation.json"
    ceoCompensationRows = []
    with open(path, "r", encoding="utf-8") as fp:
        ceoCompensations = json.load(fp)
        for compensation in ceoCompensations:
            compensationVal = convertCompensationToInt(compensation["compensation"])
            compChangeVal = convertCompChangeToFloat(compensation["compchange"])
            row =  (compensation["ceo"], 
            compensationVal, 
            compChangeVal, 
            compensation["company"],
            compensation["industry"],
            compensation["ticker"],
            compensation["year"])
            ceoCompensationRows.append(row)
    return ceoCompensationRows

def convertCompensationToInt(comp):
    matched = re.match(r'\$(.*) Million|\$(.*)$', comp)
    compVal = 0
    if matched.group(1):
        compVal = int(float(matched.group(1)) * 1000000)
    else:
        compVal = int(matched.group(2).replace(",", ""))
    return compVal

def convertCompChangeToFloat(compChange):
    changeVal = compChange.replace("%", "")
    return float(changeVal)

def main():
    credential = libmysql.createCredential("localhost", 3306, "admin", "admin321", "stock_picker")
    connection = libmysql.createConnection(credential)
    data = loadCeoCompensationData()
    insertCeoData(connection, data)

if __name__ == '__main__':
    main()