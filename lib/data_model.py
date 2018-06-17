import json

class Ceo:
    def __init__(self, rank, name, employer):
        self._rank = rank;
        self._name = name
        self._employer = employer

    @property
    def rank(self):
        return self._rank

    @property
    def name(self):
        return self._name;
    
    @property
    def employer(self):
        return self._employer


class Company:
    def __init__(self, name, industry, ticker, ceo, year):
        self._name = name
        self._industry = industry
        self._ticker = ticker;
        self._ceo = ceo
        self._year = year

    @property
    def name(self):
        return self._name

    @property
    def industry(self):
        return self._industry

    @property
    def ticker(self):
        return self._ticker

    @property
    def ceo(self):
        return self._ceo

    @property
    def year(self):
        return self._year


class Timestamp:
    def __init__(self, year, month, date):
        self._year = year
        self._month = month
        self._date = date
    
    @property
    def year(self):
        return self._year
    
    @property
    def month(self):
        return self._month

    @property
    def date(self):
        return self._date


class CeoPay:
    def __init__(self, company, industry, ticker, ceo, ceoComp, compChange, year):
        self._company = company
        self._industry = industry
        self._ticker = ticker;
        self._ceo = ceo
        self._ceoComp = ceoComp
        self._compChange = compChange
        self._year = year

    @property
    def company(self):
        return self._company

    @property
    def industry(self):
        return self._industry

    @property
    def ticker(self):
        return self._ticker

    @property
    def ceo(self):
        return self._ceo

    @property
    def ceoComp(self):
        return self._ceoComp

    @property
    def compChange(self):
        return self._compChange

    @property
    def year(self):
        return self._year

class DataJsonEncoder(json.JSONEncoder):
    def default(self, obj):
            if(isinstance(obj, CeoPay)):
                return {
                "ceo": obj.ceo,
                "compensation": obj.ceoComp,
                "compchange": obj.compChange,
                "company": obj.company, 
                "industry": obj.industry,
                "ticker": obj.ticker,
                "year": obj.year
                }
            elif(isinstance(obj, Ceo)) :
                return {"rank": obj.rank, "name": obj.name, "employer": obj.employer}
            return json.JSONEncoder.default(self, obj)    