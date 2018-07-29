import os
from lib import libmysql
import csv

class Company:
    FILES = {
        "AMEX": os.getcwd() + "/../data/public_companies/07-29-2018/AMEX.csv",
        "NASDAQ": os.getcwd() + "/../data/public_companies/07-29-2018/NASDAQ.csv",
        "NYSE": os.getcwd() + "/../data/public_companies/07-29-2018/NYSE.csv"
    }
    def __init__(self, ticker, name, ipo_year, sector, industry, exchange):
        self.ticker = ticker
        self.name = name
        self.ipo_year = ipo_year
        self.sector = sector
        self.industry = industry
        self.exchange = exchange

    def __repr__(self):
        return "[ticker = {}, name = {}, ipo_year = {}, sector = {}, industry = {}, exchange = {}]".format(
            self.ticker, self.name, self.ipo_year, self.sector, self.industry, self.exchange
        )

    @staticmethod
    def construct_companies_from_file(exchange, file):
        companies = []
        with open(file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                companies.append(Company(row[0], row[1], row[4], row[5], row[6], exchange))
        return companies


def insert_companies_into_db(connection, companies):
    bulkInsertSql = """
    INSERT INTO `public_company` (`ticker`, `name`, `ipo_year`, `sector`, `industry`, `exchange`) 
    VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
    name = VALUES(name), ipo_year = VALUES(ipo_year), sector = VALUES(sector), 
    industry = VALUES(industry),  exchange = VALUES(exchange)
    """
    rows = [(company.ticker, company.name, company.ipo_year, company.sector, company.industry, company.exchange) for company in companies]
    libmysql.bulkInsert(connection, bulkInsertSql, rows)

def main():
    companies = []
    for exchange, file in Company.FILES.items():
        companies.extend(Company.construct_companies_from_file(exchange, file))

    insert_companies_into_db(libmysql.DEFAULT_CONNECTION, companies)

if __name__ == "__main__":
    main()


