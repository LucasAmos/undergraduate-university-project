#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        manage.inittestdb()
        return appy

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

    def test_addPortfolio(self):

        self.login('lucas2', 'test')

        rv = self.addPortfolio("portfolio1")
        assert "Added portfolio &#39;portfolio1&#39;" in rv.data

        rv = self.addPortfolio("portfolio1")
        assert "A portfolio with that name already exists" in rv.data

        rv = self.addPortfolio("Portfolio1")
        assert "A portfolio with that name already exists" in rv.data

        rv = self.addPortfolio("Test``¬¬|||")
        assert "The portfolio name must contain only letters and numbers" in rv.data


