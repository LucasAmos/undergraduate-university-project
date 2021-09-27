from Shares.share_data import share_data
from flask import render_template
from Shares import app, db, login_manager

class PortfolioData():

    @staticmethod
    def sharedata(user, url='/'):
        with app.test_request_context(url):

            allshares = share_data.getalljsonshares(user)
            sharesinportfolio = []

            for share in allshares:
                share['profit'] =(float(share['price']) * share['quantity']) - (share['averagepurchaseprice'] * share['quantity'])
                sharesinportfolio.append(share)

            profits ={}
            for share in sharesinportfolio:

                if share['portfolioid'] in profits:

                    profits[share['portfolioid']] = profits[share['portfolioid']] + share['profit']

                else:
                    profits[share['portfolioid']] = share['profit']

            return render_template('email/sharedataemail2.html', data=sharesinportfolio,
                                   portfoliovalues=share_data.getportfoliovalues(user), portfolioprofits=profits)
