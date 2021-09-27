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
        return appy

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def setUp(self):
        manage.inittestdb()
        rv = self.logout()
        print rv.data

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.post('/logout', follow_redirects=True)

    def test_login(self):

        rv = self.login('lucas2', 'test')
        assert 'Logged in successfully as lucas2' in rv.data

        rv = self.login('nouser', 'test')
        assert 'Incorrect username or password' in rv.data

        rv = self.login('lucas', 'wrongpassword')
        assert 'Incorrect username or password' in rv.data

        rv = self.logout()
        assert 'login' in rv.data
