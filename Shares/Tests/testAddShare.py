from flask.ext.testing import TestCase
from flask import Flask
from Shares import db, app as appy
from Shares.models import User, Userownedshare, Share
from testDatabase import test

import manage


class test(TestCase):

    def create_app(self):
        appy.config['TESTING'] = True
        appy.config['WTF_CSRF_ENABLED'] = False
        appy.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return appy

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def setUp(self):
        manage.inittestdb()
        self.login('lucas2', 'test')
        self.addPortfolio("testportfolio")

        #rv = self.addShare("RBS", 1, 1, 100, "testportfolio")
        #print rv.data




    def tearDown(self):

        db.session.remove()
        db.drop_all()
        manage.initdb()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def addPortfolio(self, portfolioname):
        return self.client.post('/addportfolio', data=dict(
            name=portfolioname
        ), follow_redirects=True)

    def addShare(self, ticker, quantity, dividends, purchaseprice, portfolioid):

        #self.addPortfolio(portfolioid)
        return self.client.post('/add', data=dict(
            ticker=ticker,
            quantity=quantity,
            dividends=dividends,
            purchaseprice=purchaseprice,
            portfolioid=portfolioid
        ), follow_redirects=True)


    def testAddShare(self):
        #self.login('lucas2', 'test')

        # Test initial add
        self.addPortfolio("testportfolio")
        rv = self.addShare("MKS", 5000, 0, 100, "testportfolio")
        assert "Added share &#39;MKS&#39;" in rv.data

        # Test existing share cannot be added
        rv = self.addShare("MKS", 10, 0, 100, "testportfolio")
        assert "That share is already in that portfolio" in rv.data

        # Test same share can be added to a different portfolio
        self.addPortfolio("secondtestportfolio")
        rv = self.addShare("MKS", 10, 0, 100, "secondtestportfolio")
        assert "Added share &#39;MKS&#39;" in rv.data




    def testQuantityBoundaries(self):

        # Test boundaries for share quantity
        self.addPortfolio("secondtestportfolio")
        rv = self.addShare("LLOY", 0, 0, 100, "secondtestportfolio")
        assert "Number must be between 1 and 10000" in rv.data

        rv = self.addShare("LLOY", -1, 0, 100, "secondtestportfolio")
        assert "Number must be between 1 and 10000" in rv.data

        rv = self.addShare("LLOY", 10001, 0, 100, "secondtestportfolio")
        assert "Number must be between 1 and 10000" in rv.data

        self.addPortfolio("testportfolio")
        rv = self.addShare("RBS", 1, 0, 100, "testportfolio")
        assert "Added share &#39;RBS&#39;" in rv.data

        self.addPortfolio("testportfolio")
        rv = self.addShare("MKS", 5000, 0, 100, "testportfolio")
        assert "Added share &#39;MKS&#39;" in rv.data

        self.addPortfolio("testportfolio")
        rv = self.addShare("HSBA", 9999, 0, 100, "testportfolio")
        assert "Added share &#39;HSBA&#39;" in rv.data

    def testDividendBoundaries(self):

        # Test boundaries for dividends
        self.addPortfolio("secondtestportfolio")

        rv = self.addShare("LLOY", 1, 0, 100, "testportfolio")
        assert "Added share &#39;LLOY&#39;" in rv.data
        #assert "100" in rv.data

        rv = self.addShare("LLOY", 1, -1, 100, "testportfolio")
        assert "Number must be at least 0.0" in rv.data

    def testPriceBoundaries(self):

        # Test boundaries for share price
        self.addPortfolio("secondtestportfolio")

        rv = self.addShare("RBS", 1, 0, -0.01, "testportfolio")
        assert "Number must be between 0.0 and 120" in rv.data

        rv = self.addShare("RBS", 1, 0, 0.00, "testportfolio")
        assert "Added share &#39;RBS&#39;" in rv.data

        rv = self.addShare("LLOY", 1, 0, 0.01, "testportfolio")
        assert "Added share &#39;LLOY&#39;" in rv.data


        rv = self.addShare("HSBA", 1, 0, 100, "testportfolio")
        assert "Added share &#39;HSBA&#39;" in rv.data




