from flask.ext.testing import TestCase
from flask import Flask
from Shares import db, app as appy
from Shares.models import User, Userownedshare, Share
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
        #print self.login('lucas', 'test').data

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def test_adduser(self):

        lucas = User(username="lucas", email="lucas@example.com", password="test")
        user2 = User(username="lucas", email="lucas@test.com")

        db.session.add(lucas)
        db.session.commit()

        assert lucas in db.session
        assert user2 not in db.session


    def test_deleteuser(self):

        mike = User(username="mike", email="mike@email.com", password="test")

        db.session.add(mike)
        db.session.commit()
        assert mike in db.session

        User.query.filter_by(username="mike").delete()
        assert mike not in db.session

    def test_addshare(self):

        share = Share(name="google", ticker="GOOG")

        db.session.add(share)
        db.session.commit()
        assert share in db.session


    def test_deleteshare(self):

        share = Share(name="apple", ticker="AAPL")

        db.session.add(share)
        db.session.commit()
        assert share in db.session

        Share.query.filter_by(ticker="AAPL").delete()
        assert share not in db.session

    def test_addUserownedshare(self):

        mike = User(username="mike", email="mike@email.com", password="test")
        db.session.add(mike)

        share = Share(name="google", ticker="GOOG")
        db.session.add(share)

        userownedshare = Userownedshare(ticker="GOOG", user="mike", quantity=5, portfolioid="testid")
        db.session.add(userownedshare)
        db.session.commit()

        assert userownedshare in db.session


    def test_deleteUserownedshare(self):

        mike = User(username="lucas", email="lucas@email.com", password="test")
        db.session.add(mike)

        share = Share(name="google", ticker="GOOG")
        db.session.add(share)

        userownedshare = Userownedshare(ticker="GOOG", user="lucas", quantity=5, portfolioid="testid")
        db.session.add(userownedshare)
        db.session.commit()

        assert userownedshare in db.session

        Userownedshare.query.filter_by(ticker="GOOG", user="lucas", portfolioid="testid").delete()
        assert userownedshare not in db.session
