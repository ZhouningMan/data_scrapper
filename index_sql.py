import csv
import os
import lib.libmysql as libmysql

class Company:
    INDEX_FILE = os.getcwd() + "/../raw_data/investing_com/s&p_600/2018_7_20/S&P 600_performance.csv"
    def __init__(self, name, ticker):
        self.name =name
        self.ticker = ticker

    def __repr__(self):
        return "[name = {}, ticker = {}]".format(self.name, self.ticker)

    @staticmethod
    def construct_companies_from_file(file):
        companies = []
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                companies.append(Company(row[0], row[1]))
        return companies


def insert_companies_into_db(connection, companies, table):
    bulkInsertSql = "INSERT INTO `{}` (`ticker`, `name`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name)".format(table)
    rows = [(comapny.ticker, comapny.name) for comapny in companies]
    libmysql.bulkInsert(connection, bulkInsertSql, rows)

def main():
    companies = Company.construct_companies_from_file(Company.INDEX_FILE)
    insert_companies_into_db(libmysql.DEFAULT_CONNECTION, companies, "s_and_p_600")

if __name__ == "__main__":
    main()