from sqlalchemy import desc
from flask import render_template, redirect, url_for
import urllib
import json
from models import Userownedshare, Portfolios, Transactions


class share_data():

    @staticmethod
    def JSONShareFall(ticker):

        try:

            base_url = 'https://query.yahooapis.com/v1/public/yql?'
            query = {
                'q': 'select LastTradePriceOnly, Change, symbol, Name from yahoo.finance.quote where symbol in ("{}","")'.format(ticker + ".L"),
                'format': 'json',
                'env': 'store://datatables.org/alltableswithkeys'
            }

            url = base_url + urllib.urlencode(query)
            response = urllib.urlopen(url)
            data = response.read()
            quote = json.loads(data)

            return quote

        except:
            return render_template("connectiondown.html")

    @staticmethod
    def JSONSharePrice(ticker):

        try:

            base_url = 'https://query.yahooapis.com/v1/public/yql?'
            query = {
                'q': 'select LastTradePriceOnly, symbol, Name from yahoo.finance.quote where symbol in ("{}{}","")'.format(ticker,".L"),
                'format': 'json',
                'env': 'store://datatables.org/alltableswithkeys'
            }

            url = base_url + urllib.urlencode(query)
            response = urllib.urlopen(url)
            data = response.read()
            quote = json.loads(data)

            return quote

        except:
            return render_template("connectiondown.html")

    @staticmethod
    def getSharesNoLiveData(user):

        tempshares = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter(Userownedshare.user == user)

        sharearray = []

        for row in tempshares:

            sharedata = {
                'symbol': row.name.ticker,
                'quantity': row.quantity,
                'price': "--",
                'averagepurchaseprice': row.averagepurchaseprice,
                'name': row.name.name,
                'dividends': row.dividends,
                'id': row.id,

                'portfolioid': row.portfolioid
            }
            sharearray.append(sharedata)

        return sharearray


    @staticmethod
    def getalljsonshares(user):

        tempshares = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter(Userownedshare.user == user)

        sharearray = []

        for row in tempshares:

            ticker = row.ticker
            quote = share_data.JSONSharePrice(ticker)
            sharedata = {
                ### change this line to fix symbol display in portfolio page
                'symbol': quote['query']['results']['quote']['symbol'],
                'quantity': row.quantity,
                'price': float(quote['query']['results']['quote']['LastTradePriceOnly']) /100,
                'averagepurchaseprice': row.averagepurchaseprice,
                'name': row.name.name,
                'dividends': row.dividends,
                'id': row.id,

                'portfolioid': row.portfolioid
            }
            sharearray.append(sharedata)

        return sharearray


    @staticmethod
    def getalljsonsharesInPortfolio(user, portfolio):

        tempshares = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter(Userownedshare.user == user, Userownedshare.portfolioid == portfolio)

        sharearray = []

        for row in tempshares:

            ticker = row.ticker
            quote = share_data.JSONSharePrice(ticker)
            sharedata = {
                ### change this line to fix symbol display in portfolio page
                'symbol': quote['query']['results']['quote']['symbol'][:-2],
                'quantity': row.quantity,
                'price': float(quote['query']['results']['quote']['LastTradePriceOnly']) /100,
                'averagepurchaseprice': row.averagepurchaseprice,
                'name': row.name.name,
                'dividends': row.dividends,
                'id': row.id,

                'portfolioid': row.portfolioid
            }
            sharearray.append(sharedata)

        return sharearray


    @staticmethod
    def getportfoliovalue(user):
        tempshares = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter(Userownedshare.user == user)

        sharearray = []

        sharevalue = 0.0
        dividends = 0.0
        portfoliovalue = 0.0

        for row in tempshares:

            ticker = row.ticker
            quote = share_data.JSONSharePrice(ticker)

            shareprice = float (quote['query']['results']['quote']['LastTradePriceOnly'])
            quantity = row.quantity
            shareholding = shareprice * quantity
            dividends = dividends + row.dividends
            sharevalue += shareholding
            portfoliovalue = sharevalue + dividends

        sharearray.append(sharevalue)
        sharearray.append(dividends)
        sharearray.append(portfoliovalue)
        dictvalues = {'portfoliovalue': portfoliovalue, 'sharevalue': sharevalue, 'dividends': dividends}

        return dictvalues

    #not used anywhere, move code from models.py to here
    # @staticmethod
    # def getportfolioids(user):
    #
    #     portfolioids= Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter_by(user=user).filter(Userownedshare.portfolioid != None)
    #
    #     tempset = set()
    #     for row in portfolioids:
    #         id = row.portfolioid
    #         tempset.add(id)
    #
    #         templist = list(tempset)
    #         return templist

    @staticmethod
    def getportfolioidsfromtable(user):

        portfolioids = Portfolios.query.order_by(desc(Portfolios.portfolioname)).filter_by(username=user)

        tempset = set()
        templist = list(tempset)
        for row in portfolioids:
            name = row.portfolioname
            tempset.add(name)

            templist = list(tempset)
        return templist

    @staticmethod
    def getsubportfoliovalue(user, portfolio):
        tempshares = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter_by(user=user).filter(Userownedshare.portfolioid == portfolio)

        sharevalue = 0.0
        dividends = 0.0
        portfoliovalue = 0.0

        for row in tempshares:

            ticker = row.ticker
            quote = share_data.JSONSharePrice(ticker)

            shareprice = float (quote['query']['results']['quote']['LastTradePriceOnly'])
            quantity = row.quantity
            shareholding = shareprice * quantity
            dividends = dividends + row.dividends
            sharevalue += shareholding

        sharevalue = sharevalue/100
        portfoliovalue = sharevalue + dividends
        dictvalues = {'portfoliovalue': round(portfoliovalue, 2), 'sharevalue': sharevalue, 'dividends': dividends}

        return dictvalues


    @staticmethod
    def getportfoliovalues(user):

        portfolioids = Userownedshare.listportfolios(user)
        portfoliovalues ={}

        for id in portfolioids:
            portfoliovalues[id] = share_data.getsubportfoliovalue(user, id)

        return portfoliovalues


    @staticmethod
    def getnonemptyportfolios(user):

        tempset = set()
        templist = list(tempset)

        portfoliovalues =[]
        portfolionames = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter_by(user=user).filter(Userownedshare.portfolioid != "")

        for row in portfolionames:
            id = row.portfolioid
            tempset.add(id)
            templist = list(tempset)

        return templist


    @staticmethod
    def getPortfolioIDbyusernameandPortfolioName(username, portfolioname):

        ID = Portfolios.query.filter_by(portfolioname=portfolioname).filter_by(username=username).first()

        return ID

    @staticmethod
    def isValidShare(ticker):

        quote = share_data.JSONSharePrice(ticker)

        if quote['query']['results']['quote']['LastTradePriceOnly']:
            return True

        else:
            return False

    @staticmethod
    def getTransactions(username):

        transactions = Transactions.query.filter(Transactions.user == username).order_by(desc(Transactions.time))

        transactionarray = []
        for row in transactions:


            transaction = {
                'portfolioid': row.portfolioid,
                'date': row.time,
                'name': row.name.name,
                'buysell': row.buySell,
                'quantity': row.quantity,
                'dividends': row.dividends,
                'price': row.price,
                'ticker': row.ticker
            }

            transactionarray.append(transaction)

        return transactionarray







