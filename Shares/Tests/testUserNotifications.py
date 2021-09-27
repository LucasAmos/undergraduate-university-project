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

        appy.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return appy

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True



    def setUp(self):
        manage.inittestdb()

        self.login('lucas2', 'test')

        # rv = self.accountsettings("lucas")
        # print rv.data


    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def changeAccountsettings(self, email, phonenumber):
        return self.client.post('/accountsettings', data=dict(
            email=email,
            phonenumber=phonenumber

        ), follow_redirects=True)


    def testChangeAccountDetails(self):

        rv = self.accountsettings("dummy")
        assert "lucas2@example.com" in rv.data
        assert "07506292708" in rv.data

        rv = self.changeAccountsettings("abc@gmail.com", "07506292704")
        assert "abc@gmail.com" in rv.data
        assert "07506292704" in rv.data


    def testAccountSettings(self):

        rv = self.accountsettings("dummy")
        assert "lucas2@example.com" in rv.data
        assert "07506292708" in rv.data

        rv = self.changeAccountsettings("abc@gmail.com", "07506292704")
        assert "abc@gmail.com" in rv.data
        assert "07506292704" in rv.data

    def accountsettings(self, dummy):
        return self.client.post('/accountsettings', data=dict(
        ), follow_redirects=True)

    def changeNotificationSettings(self, frequency):
        return self.client.post('/notifications', data=dict(
            emailfrequency = frequency
        ), follow_redirects=True)


    def testNotificationSettings(self):
        rv = self.accountsettings("dummy")
        assert "Portfolio emails disabled" in rv.data

        rv = self.changeNotificationSettings(1)
        assert "Daily" in rv.data

        rv = self.changeNotificationSettings(2)
        assert "Weekly" in rv.data

    def changeSMSEnabled(self, smsenabled):
        return self.client.post('/notifications', data=dict(
            smsenabled=smsenabled
        ), follow_redirects=True)


    def testSMSSettings(self):
        rv = self.accountsettings("dummy")
        assert "Share rise/fall notifications disabled" in rv.data

        rv = self.changeSMSEnabled(1)
        assert "Share rise/fall notifications enabled" in rv.data


