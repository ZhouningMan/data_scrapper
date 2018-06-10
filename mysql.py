import pymysql.cursors
import collections
import traceback
import json
import os

DatabaseCredential = collections.namedtuple("DatabaseCredential", ["host", "port", "user", "password", "database"])
STOCK_PICKER_DB_CREDENTIAL = DatabaseCredential("localhost", 3306, "admin", "admin321", "stock_picker")


def bulkInsertTopCeoData(connection):
    #create the table if not exists
    with connection.cursor() as cursor:
        createTableIfNotExist = """
            CREATE TABLE IF NOT EXISTS `ceo_rating`
                (`rank` int(11) NOT NULL,
                `name` varchar(255) COLLATE utf8_bin NOT NULL,
                `employer` varchar(255) COLLATE utf8_bin NOT NULL,
                `year` int(11) NOT NULL,
                PRIMARY KEY (`rank`, `name`, `employer`, `year`)) 
                ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                AUTO_INCREMENT=1
        """
        cursor.execute(createTableIfNotExist)
        connection.commit()

    with connection.cursor() as cursor:
        bulkInsertSql = """
          INSERT INTO `ceo_rating` (`rank`, `name`, `employer`, `year`) VALUES (%s, %s, %s, %s)
        """
        ceoRatingRows = generateCeoRatings()
        affected = cursor.executemany(bulkInsertSql, ceoRatingRows)
        print("Inserted {} rows" + affected)
        connection.commit()

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


def bulkUpdateData():
    connection = pymysql.connect(host=STOCK_PICKER_DB_CREDENTIAL.host,
                                 port=STOCK_PICKER_DB_CREDENTIAL.port,
                                 user=STOCK_PICKER_DB_CREDENTIAL.user,
                                 password=STOCK_PICKER_DB_CREDENTIAL.password,
                                 db=STOCK_PICKER_DB_CREDENTIAL.database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        bulkInsertTopCeoData(connection)
    except Exception as ex:
        print("Exception: " + str(ex))
        traceback.print_exc()
    finally:
        connection.close()

def main():
    bulkUpdateData()

if __name__ == '__main__':
    main()