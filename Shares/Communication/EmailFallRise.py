from Shares.share_data import share_data
from flask import render_template
from Shares import app, db, login_manager

class EmailFallRise():

    @staticmethod
    def emailnotification(dataarray, url='/'):
        with app.test_request_context(url):


            return render_template('email/emailfallrise.html', data=dataarray)
