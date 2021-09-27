#test
#! /usr/bin/env python

from Shares import app, db

from Shares.models import User, Userownedshare, Share, Portfolios, Transactions
from flask.ext.script import Manager, prompt_bool
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand



manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
        db.create_all()
        # reindert=User(username="reindert", email="reindert@example.com", password="test")
        # db.session.add(reindert)

        lucas=User(username="lucas", email="", password="test", emailfrequency=2, smsenabled=True, phonenumber="")
        db.session.add(lucas)

        portfolio = Portfolios(username="lucas", portfolioname="test")
        db.session.add(portfolio)




        google = Userownedshare(user="lucas", ticker="MKS", quantity=1, portfolioid="test", triggerlevel=0, smsalert=False, emailalert=False)
        db.session.add(google)

        share = Share(ticker="MKS", name="Marks & Spencer")
        db.session.add(share)

        db.session.commit()


        print('Database initialised')


@manager.command
def inittestdb():
        db.create_all()
        testuser=User(username="test", email="test@test.com", password="test")
        db.session.add(testuser)
        lucas=User(username="lucas2", email="lucas2@example.com", password="test", phonenumber= "07506292708", emailfrequency=0, smsenabled=0)
        db.session.add(lucas)
        portfolio=Portfolios(portfolioname="Portfolio1", username="test")
        db.session.add(portfolio)

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data?"):
        db.drop_all()
        print('Dropped the database')

if __name__ == '__main__':
    manager.run()
