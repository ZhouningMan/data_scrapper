import csv
import os
import datetime
import lib.libmysql as libmysql
import logging

class CompanyTechnical:
    def __init__(self, ticker, name = "", price=0, market_cap=0, revenue=0, pe=0, one_month=0, ytd=0, one_year=0, three_year=0, sentiment="", date=datetime.date.today()):
        self.ticker = ticker
        self.name = name
        self.price = price
        self.market_cap = market_cap
        self.revenue = revenue
        self.pe = pe
        self.one_month = one_month
        self.ytd = ytd
        self.one_year = one_year
        self.three_year = three_year
        self.sentiment = sentiment
        self.date = date
    
    @classmethod
    def createTechnical(cls, ticker):
        return cls(ticker)

    @staticmethod
    def toRows(technicals):
        return [t.toRow() for t in technicals]

    def toRow(self):
        return (self.ticker, self.price, self.market_cap, self.revenue, self.pe, 
        self.one_month, self.ytd, self.one_year, self.three_year, self.sentiment, self.date)

class IndexDbHolder:
    COMPANY_SQL = "INSERT INTO `{}` (`ticker`, `name`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name)"
    TECHNICAL_SQL = """
    INSERT INTO `company_technical` 
    (ticker, price, market_cap, revenue, pe, one_month, ytd, one_year, three_year, sentiment, date) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    def __init__(self, sql, rows):
        self.sql = sql
        self.rows = rows
    
    def getRows(self):
        return self.rows

    def getSql(self):
        return self.sql
    
    def __repr__(self):
        return "sql = {}\n rows = {}".format(self.sql, str(self.rows))

    @staticmethod
    def format_sql(format, table):
        return format.format(table)

class IndexLoader:
    INDICES_PATH_FORMAT = os.getcwd() + "/../data/indices/{}/{}/{}.csv"
    FUNDAMENTAL = "fundamental"
    PERFORMANCE = "performance"
    TECHNICAL = "technical"
    PRICE = "price"

    def __init__(self, index, date, table):
        self.index = index
        self.date = date
        self.table = table
        self.loadData()
    
    def fullFilePath(self, data_type):
        date_str = self.date.strftime("%Y_%m_%d")
        fileName = self.index + "_" + data_type
        return IndexLoader.INDICES_PATH_FORMAT.format(self.index, date_str, fileName)

    def getCompanies(self):
        sql = IndexDbHolder.format_sql(IndexDbHolder.COMPANY_SQL, self.table)
        rows = []
        for _, val in self.companyMap.items():
            rows.append((val.ticker, val.name))
        return IndexDbHolder(sql, rows)
    
    def getCompanyTechnicals(self):
        rows = []
        for _, val in self.companyMap.items():
            formattedDate = self.date.strftime("%Y-%m-%d")
            rows.append((val.ticker, val.price, val.market_cap, val.revenue, val.pe, val.one_month, val.ytd, val.one_year, val.three_year, val.sentiment, formattedDate))
        return IndexDbHolder(IndexDbHolder.TECHNICAL_SQL, rows)

    def loadData(self):
        companyMap = {}
        fundamental = self.fullFilePath(IndexLoader.FUNDAMENTAL)
        def fundamentalConsumer(row, company):
            name = row[0]
            company.name = name
            company.market_cap = self.convertAbbreviatedNumber(row[3])
            company.revenue = self.convertAbbreviatedNumber(row[4])
            company.pe = self.convertStrinToFloat(row[5])
        self.loadCsvFile(companyMap, fundamental, fundamentalConsumer)

        performance = self.fullFilePath(IndexLoader.PERFORMANCE)
        def performanceConsumer(row, company):
            company.one_month = self.convertPercentage(row[4])
            company.ytd = self.convertPercentage(row[5])
            company.one_year = self.convertPercentage(row[6])
            company.three_year = self.convertPercentage(row[7])
        self.loadCsvFile(companyMap, performance, performanceConsumer)

        price = self.fullFilePath(IndexLoader.PRICE)
        def priceConsumer(row, company):
            company.price = self.convertStrinToFloat(row[2])
        self.loadCsvFile(companyMap, price, priceConsumer)

        trend = self.fullFilePath(IndexLoader.TECHNICAL)
        def trendConsumer(row, company):
            company.sentiment = row[5]
        self.loadCsvFile(companyMap, trend, trendConsumer)

        self.companyMap = companyMap


    def convertAbbreviatedNumber(self, abbreviated):
        numberMap = {
            "T": 1000000,
            "B": 1000,
            "M": 1,
            "K": 0.001
        }
        rawNumber = abbreviated[:-1].replace(",", "")
        numberSymbol = abbreviated[-1:]
        return float(rawNumber) * numberMap[numberSymbol] if rawNumber else  0

    def convertStrinToFloat(self, string):
        commandRemoved = string.replace(",", "")
        return float(commandRemoved) if commandRemoved else 0

    def convertPercentage(self, percentage):
        try:
            percentRemoved = percentage.replace("%", "")
            return float(percentRemoved)
        except Exception:
            logging.error("index = {} percentage = {}".format(self.index, percentage))
            return 0
            
    def loadCsvFile(self, companyMap, file_path, row_consumer):
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                ticker =  row[1]
                if ticker not in companyMap:
                    companyMap[ticker] = CompanyTechnical.createTechnical(ticker)
                company = companyMap[ticker]
                row_consumer(row, company)
                companyMap
  

def insert_companies_into_db(connection, companies, table):
    bulkInsertSql = "INSERT INTO `{}` (`ticker`, `name`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name)".format(table)
    rows = [(comapny.ticker, comapny.name) for comapny in companies]
    libmysql.bulkInsert(connection, bulkInsertSql, rows)

def main():
    logging.basicConfig(level=logging.DEBUG)
    indicesAndTableMap = {
        "sp600": "s_and_p_600",
        "sp500": "s_and_p_500",
        "sp400": "s_and_p_400"
    }
    date = datetime.date(2018, 8, 4)
    for index, table in indicesAndTableMap.items():
        loader = IndexLoader(index, date, table)
        companies = loader.getCompanies()
        libmysql.bulkInsert(libmysql.DEFAULT_CONNECTION, companies.sql, companies.rows)
        technicals = loader.getCompanyTechnicals()
        libmysql.bulkInsert(libmysql.DEFAULT_CONNECTION, technicals.sql, technicals.rows)

if __name__ == "__main__":
    main()