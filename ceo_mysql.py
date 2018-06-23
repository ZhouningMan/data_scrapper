import pymysql.cursors
import collections
import traceback
import json
import os
import lib.libmysql as libmysql

def createCeoTable(connection):
    #create the table if not exists
    createTableIfNotExist = """
        CREATE TABLE IF NOT EXISTS `ceo_rating`
            (`id` int(11) NOT NULL AUTO_INCREMENT,
            `rank` int(11) NOT NULL,
            `name` varchar(255) COLLATE utf8_bin NOT NULL,
            `employer` varchar(255) COLLATE utf8_bin NOT NULL,
            `year` int(11) NOT NULL,
            PRIMARY KEY (`id`)) 
            ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
            AUTO_INCREMENT=1
    """
    libmysql.execute(collections, createTableIfNotExist)

def removeCeoRatingData(connection):
    removeCeoRatingSql = """
        TRUNCATE `ceo_rating`
    """
    libmysql.execute(connection, removeCeoRatingSql)

def bulkInsertTopCeoData(connection, data):
    bulkInsertSql = """
        INSERT INTO `ceo_rating` (`rank`, `name`, `employer`, `year`) VALUES (%s, %s, %s, %s)
    """
    libmysql.bulkInsert(connection, bulkInsertSql, data)

def generateCeoRatings():
    path = os.getcwd() + "/../data/TopCeos.json"
    ceoRatingRows = []
    with open(path, "r", encoding="utf-8") as fp:
        ceoRatings = json.load(fp)
        for yearlyRating in ceoRatings:
            year = yearlyRating["year"]
            ceosPerYear = yearlyRating["ceos"]
            for ceo in ceosPerYear:
                ceoRatingRows.append(
                    (ceo["rank"], ceo["name"], ceo["employer"], year)
                )
    return ceoRatingRows


def main():
    credential = libmysql.createCredential("localhost", 3306, "admin", "admin321", "stock_picker")
    connection = libmysql.createConnection(credential)
    removeCeoRatingData(connection)
    data = generateCeoRatings()
    bulkInsertTopCeoData(connection, data)

if __name__ == '__main__':
    main()