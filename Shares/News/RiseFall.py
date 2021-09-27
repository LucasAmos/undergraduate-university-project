import urllib
from xml.etree import ElementTree
from Shares.models import Userownedshare
from sqlalchemy import desc
from Shares.share_data import share_data
import random


class RiseFall():

    @staticmethod
    def getTickers(user):

        tickers = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter_by(user=user)

        tickerset = set()
        for item in tickers:
            tickerset.add(item.ticker)

        tickerset = random.sample(tickerset, len(tickerset))

        return tickerset

    @staticmethod
    def getRiseFall(user):

        tickers = RiseFall.getTickers(user)

        results =[]
        for ticker in tickers:
            temp =share_data.JSONShareFall(ticker)['query']['results']['quote']
            results.append([temp['symbol'], temp['Name'], temp['Change']])


        return results
