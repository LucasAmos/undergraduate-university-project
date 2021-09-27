from sendgridEmail import Email
from twilioSMS import SMS
from Shares.share_data import share_data
from manage import db
from Shares.models import User, Share, Userownedshare
from flask import render_template
from PortfolioData import PortfolioData
from sqlalchemy import desc


class PortfolioStatus():


    session = db.session()


    # for share in session.query(Share):
    #
    #     print share.tickermatch[0]

        # for sh in share:
        #
        #     print sh.user

    for share in session.query(Share):

        listy= list( share.tickermatch)

        #print listy

        for item in listy:

            print item.owner.email


