from flask.ext.testing import TestCase
from flask import Flask
from Shares import db, app as appy
from Shares.models import User, Userownedshare, Share
from testDatabase import test
import mock

import manage

class test(TestCase):

    def create_app(self):
        appy.config['TESTING'] = True
        appy.config['WTF_CSRF_ENABLED'] = False
        return appy

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True



    def setUp(self):
        manage.inittestdb()

        self.login('lucas2', 'test')
        self.addPortfolio("testportfolio")
        self.addPortfolio("testportfolio2222")

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def addPortfolio(self, portfolioname):
        return self.client.post('/addportfolio', data=dict(
            name=portfolioname
        ), follow_redirects=True)

    def deletePortfolio(self, portfolioname):
        return self.client.post('/deleteportfolio', data=dict(
            name2=portfolioname
        ), follow_redirects=True)

    def testDeletePortfolio(self):
        self.login('lucas2', 'test')

        rv = self.addPortfolio("testportfolio")
        assert "testportfolio" in rv.data
        #
        # rv=self.deletePortfolio("testportfolio")
        # assert "testportfolio" not in rv.data
