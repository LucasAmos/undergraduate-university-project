import urllib
from xml.etree import ElementTree
from Shares.models import Userownedshare
from sqlalchemy import desc


class News():

    @staticmethod
    def getTickers(user):

        tickers = Userownedshare.query.order_by(desc(Userownedshare.ticker)).filter_by(user=user)

        tickerstring =""
        for row in tickers:
            name = row.ticker + ".L"

            tickerstring+=name
            tickerstring+=","

        return tickerstring

    @staticmethod
    def getNews(user):


        try:

            ticker = News.getTickers(user)

            base_url = 'http://finance.yahoo.com/rss/headline?s='
            query = ticker

            url = base_url + query
           # print url
            response = urllib.urlopen(url)
            data = response.read()

            dom = ElementTree.fromstring(data)

            items = dom.findall('channel/item')

            dict ={}

            for item in items:
                title = item.find('title').text
                item = item.find('link').text
                dict[title] = item

            return dict

        except:

            print "fail"











