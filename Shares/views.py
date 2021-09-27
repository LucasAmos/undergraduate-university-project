#! /usr/bin/env python
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from Shares import app, db, login_manager
from forms import *
from models import User, Userownedshare, Share
from share_data import *
from News.News import News
from News.RiseFall import RiseFall
import datetime

@login_manager.user_loader
def load_user(userid):

    if userid is None or userid == 'None':
        userid =0
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():

    if current_user.is_authenticated:

        try:

            return render_template('index.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                                   news=News.getNews(current_user.username), sharesexist=share_data.getnonemptyportfolios(current_user.username))

        except:
            return render_template("connectiondown.html", portfolioids=share_data.getportfolioidsfromtable(current_user.username))

    else: return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data.lower(),
                    password=form.password.data,
                    phonenumber=form.phonenumber.data,
                    emailfrequency=0,
                    smsenabled=False)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('index'))

        flash('Incorrect username or password.')
    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/addportfolio', methods=['GET', 'POST'] )
@login_required
def addportfolio():

    form = AddPortfolioForm()

    if form.validate_on_submit():
        name = form.name.data.lower()

        portfolio = Portfolios(portfolioname=name.lower(), username=current_user.username)
        db.session.add(portfolio)
        db.session.commit()

        flash("Added portfolio '{}'".format(name))
        return redirect(url_for('index'))

    return render_template('addportfolio.html', form=form, portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                           news=News.getNews(current_user.username))


@app.route('/deleteportfolio', methods=['GET', 'POST'])
@login_required
def deleteportfolio():

    d_form = DeletePortfolioForm()
    d_form.name.choices = [(h, h) for h in share_data.getportfolioidsfromtable(current_user.username)]


    if d_form.validate_on_submit():
        name2 = d_form.name.data

        portfolio = share_data.getPortfolioIDbyusernameandPortfolioName(current_user.username, name2)
        db.session.delete(portfolio)
        db.session.commit()

        flash("deleted portfolio '{}'".format(name2))
        return redirect(url_for('index'))

    return render_template('deleteportfolio.html', d_form=d_form, portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                           news=News.getNews(current_user.username))


@app.route('/delete/<share_id>', methods=['GET', 'POST'])
@login_required
def delete_share(share_id):
    tempshare = Userownedshare.query.get_or_404(share_id)
    if current_user.username != tempshare.user:
        abort(403)

    if request.method == "POST":

        transaction = Transactions()
        transaction.user = current_user.username
        transaction.portfolioid = tempshare.portfolioid
        transaction.buySell = 3
        transaction.ticker = tempshare.ticker
        now = datetime.datetime.now()
        transaction.time = now.replace(microsecond=0)

        db.session.add(transaction)
        db.session.delete(tempshare)
        db.session.commit()
        flash("You have successfully deleted the share: '{}'". format(tempshare.name.name))
        return redirect(url_for('list_portfolio', portfolio_id=tempshare.portfolioid))
    # else:
    #     flash("Please confirm deleting the share.")

    return render_template('confirm_deletes_share.html', portfolioids=Userownedshare.listportfolios(current_user.username),
                           share=tempshare, nolinks=True, news=News.getNews(current_user.username), portfolio_id=tempshare.portfolioid)


@app.route('/portfolio/<string:portfolio_id>', methods=['GET', 'POST'])
@login_required
def list_portfolio(portfolio_id):


    try:

        allshares = share_data.getalljsonsharesInPortfolio(current_user.username, portfolio_id)
        sharesinportfolio = []
        profit = 0


        for share in allshares:

            if share['portfolioid'] == portfolio_id:
                share['profit'] =(float(share['price']) * share['quantity']) - (share['averagepurchaseprice'] * share['quantity'])
                sharesinportfolio.append(share)
                profit += share['profit']


        sharevalue = 0.0
        dividends = 0.0
        portfoliovalue = 0.0

        for share in allshares:

            shareprice = float (share['price'])
            quantity = share['quantity']
            shareholding = shareprice * quantity
            dividends = dividends + share['dividends']
            sharevalue += shareholding
            portfoliovalue = sharevalue + dividends

        dictvalues = {'portfoliovalue': round(portfoliovalue, 2), 'sharevalue': sharevalue, 'dividends': dividends}

        return render_template('portfolio.html', id=portfolio_id, portfolioids = share_data.getportfolioidsfromtable(current_user.username),
                               portfolioshares=sharesinportfolio, portfoliovalue=dictvalues,
                               portfolioprofit=profit, news=News.getNews(current_user.username))

    except:
        return render_template("connectiondown.html", portfolioids=share_data.getportfolioidsfromtable(current_user.username))


@app.route('/add', methods=['GET', 'POST'], )
@login_required
def add():
    form = AddShareForm()
    form.portfolioid.choices = [(h, h) for h in share_data.getportfolioidsfromtable(current_user.username)]
    form.ticker.choices = [('AAL','ANGLO AMERICAN'),('AHT','ASHTEAD GROUP PLC'),
                           ('BKG','BERKELY GROUP HOLDING'), ('CARD','CARD FACTORY'),('CLLN','CARILLION PLC'),
                           ('DCC','DCC PLC'),
                           ('DTY','DIGNITY PLC'),('FAN','VOLUTION GROUP'), ('GLEN','GLENCORE PLC'), ('HSBA','HSBC'),
                           ('IHG','INTERCONTINENTAL HOTELS GROUP PLC'), ('LLOY','LLOYDS BANKING GROUP'),
                           ('MKS', 'MARKS & SPENCER'), ('OML','OLD MUTUAL PLC'), ('RBS', 'ROYAL BANK OF SCOTLAND'),
                           ('RUS','RAVEN RUSSIA'),('PFG','PROVIDENT FINANCIAL PLC'), ('STAN','STANDARD CHARTERED PLC'),
                           ('WTB','WHITBREAD PLC')]

    if form.validate_on_submit():

        transaction = Transactions()
        transaction.user = current_user.username
        transaction.portfolioid = form.portfolioid.data
        transaction.buySell = 0
        transaction.ticker = form.ticker.data.upper()
        transaction.quantity = form.quantity.data
        transaction.dividends = form.dividends.data
        transaction.price = share_data.JSONSharePrice(form.ticker.data)['query']['results']['quote']['LastTradePriceOnly']
        now = datetime.datetime.now()
        transaction.time = now.replace(microsecond=0)
        db.session.add(transaction)

        ticker = form.ticker.data.upper()
        quantity = form.quantity.data
        dividends = form.dividends.data
        purchaseprice = form.purchaseprice.data
        portfolioid = form.portfolioid.data


        if not Share.exists(ticker):

            sharedata = share_data.JSONSharePrice(ticker)
            sharename = sharedata['query']['results']['quote']['Name']

            newshare = Share(ticker=ticker, name=sharename)
            db.session.add(newshare)

        share = Userownedshare(user=current_user.username, quantity=quantity, ticker=ticker, dividends=dividends,
                               averagepurchaseprice=purchaseprice, portfolioid=portfolioid, smsalert=False,
                               emailalert=False, triggerlevel=0)

        db.session.add(share)
        db.session.commit()
        flash("Added share '{}'".format(ticker))
        return redirect(url_for('index'))
    return render_template('add.html', form=form, portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                           news=News.getNews(current_user.username))


@app.route('/addadditionalshares/<string:share_id>', methods=['GET', 'POST'], )
@login_required
def addadditionalshares(share_id):
    share = Userownedshare.query.get_or_404(share_id)

    if current_user.username != share.user:
        abort(403)

    form = AddAdditionalShares()

    share.averagepurchaseprice

    if form.validate_on_submit():

        transaction = Transactions()
        transaction.user = current_user.username
        transaction.portfolioid = share.portfolioid
        transaction.buySell = 1
        transaction.ticker = share.ticker


        if form.sharequantity.data and form.shareprice.data:

            totalshares = float(share.quantity) + form.sharequantity.data
            newaveragepurchaseprice = (((float(share.averagepurchaseprice) * share.quantity) + (form.sharequantity.data * form.shareprice.data)) / totalshares)
            share.averagepurchaseprice = newaveragepurchaseprice
            share.quantity += form.sharequantity.data

            transaction.quantity = form.sharequantity.data
            transaction.price = form.shareprice.data


        if form.dividends.data:
            share.dividends += float(form.dividends.data)
            transaction.dividends = form.dividends.data

        now = datetime.datetime.now()
        transaction.time = now.replace(microsecond=0)
        db.session.add(transaction)
        db.session.commit()


        flash("You have successfully edited the share: '{}'". format(share.name.name))
        return redirect(url_for('list_portfolio', portfolio_id=share.portfolioid))

    return render_template('addadditionalshares.html', form=form,
                           portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                           name=share.name.name, news=News.getNews(current_user.username))


@app.route('/sell/<share_id>', methods=['GET', 'POST'])
@login_required
def sell_share(share_id):
    share = Userownedshare.query.get_or_404(share_id)
    if current_user.username != share.user:
        abort(403)
    #form = RemoveShareForm(obj=tempeditshare)
    form = RemoveShareForm()
    form.ticker.data = share.ticker

    # form.portfolioid.choices = [(h, h) for h in share_data.getportfolioidsfromtable(current_user.username)]
    form.originalportfolioid.data = Userownedshare.query.get_or_404(share_id).portfolioid
    form.shareID.data=share_id

    if form.validate_on_submit():

        transaction = Transactions()
        transaction.user = current_user.username
        transaction.portfolioid = share.portfolioid
        transaction.buySell = 2
        transaction.ticker = share.ticker
        transaction.quantity = form.quantity.data
        transaction.price = form.price.data

        originalpurchaseprice = float(share.averagepurchaseprice)
        originalquantity = float(share.quantity)
        salequantity = float(form.quantity.data)
        saleprice = float(form.price.data)



        if (originalquantity - salequantity) == 0:

            newpurchaseprice = 0

        else:
            newpurchaseprice = str(((originalpurchaseprice * originalquantity) - (saleprice * salequantity)) /
                                   (originalquantity-salequantity)
                                   )

        share.averagepurchaseprice = newpurchaseprice
        share.quantity = (originalquantity - salequantity)

        now = datetime.datetime.now()
        transaction.time = now.replace(microsecond=0)
        db.session.add(transaction)
        db.session.commit()

        flash("You have successfully edited the share: '{}'". format(share.name.name))
        return redirect(url_for('list_portfolio', portfolio_id=share.portfolioid))

    return render_template('sellshare_form.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username), form=form, news=News.getNews(current_user.username), name=share.name.name)
    #return render_template('sellshare_form.html', form=form)


@app.route('/notifications', methods=['GET', 'POST'], )
@login_required
def notifications():

    if current_user.is_authenticated:
        user = User.query.get_or_404(current_user.id)
        form = NotificationSettingsForm(request.form, emailfrequency=user.emailfrequency, smsenabled=int(user.smsenabled))


        if form.validate_on_submit():
            user.emailfrequency = form.emailfrequency.data
            user.smsenabled = form.smsenabled.data

            db.session.commit()
            flash("You have successfully updated your notification preferences")
            return redirect(url_for('settings'))

        #   share = Userownedshare.query.get_or_404(share_id)
        # if current_user.username != share.user:
        #     abort(403)
        # #form = RemoveShareForm(obj=tempeditshare)
        # form = RemoveShareForm()
        # form.ticker.data = share.ticker



        return render_template('notifications.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                               form=form, news=News.getNews(current_user.username))


@app.route('/setnotification/<share_id>', methods=['GET', 'POST'])
@login_required
def setNotification(share_id):
        share = Userownedshare.query.get_or_404(share_id)

        if current_user.username != share.user:
            abort(403)


        if share.triggerlevel == 0:
            trigger = 0
            positivenegative = 0

        elif share.triggerlevel < 0:
            trigger=abs(share.triggerlevel) /100
            positivenegative=0

        else:
            trigger=share.triggerlevel /100
            positivenegative=1

        form = ShareNotificationForm(request.form, smsenabled=int(share.smsalert), emailenabled=int(share.emailalert),
                                     triggerlevel=trigger, positivenegative=positivenegative)

        if form.validate_on_submit():

            share.emailalert=form.emailenabled.data
            share.smsalert=form.smsenabled.data

            if (int(form.positivenegative.data) == 0):
                triggervalue = 0.00
                triggervalue = triggervalue - float(form.triggerlevel.data)

                share.triggerlevel=triggervalue *100

            elif int(form.positivenegative.data) == 0:
                trigger=form.triggerlevel.data

                share.triggerlevel=trigger *100


            else:
                share.triggerlevel=form.triggerlevel.data *100

            print form.positivenegative.data
            db.session.commit()

            flash("You amended the notifcations settings for '{}'".format(share.name.name))
            return redirect(url_for('list_portfolio', portfolio_id=share.portfolioid))

        return render_template('setnotification.html', news=News.getNews(current_user.username), tempshare=share,
                               form=form, portfolioids=share_data.getportfolioidsfromtable(current_user.username))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    return render_template('settings.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                           user=current_user)


@app.route('/accountsettings', methods=['GET', 'POST'])
@login_required
def accountsettings():

    form=EditSettingsForm()
    user = current_user


    if form.validate_on_submit():

        if form.email.data:
            user.email = form.email.data.lower()

        if form.phonenumber.data:
            user.phonenumber = form.phonenumber.data

        if form.password.data:
            user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('settings'))

    return render_template('accountsettings.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                           user=current_user, form=form)


@app.route('/transactions/<user>', methods=['GET', 'POST'])
@login_required
def transactions(user):

    if current_user.username != user:
        abort(403)

    transactiondata = share_data.getTransactions(current_user.username)
    return render_template('transactions.html', portfolioids=share_data.getportfolioidsfromtable(current_user.username),
                           user=current_user, transactiondata = transactiondata)



@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

from StringIO import StringIO
io = StringIO()

@app.route('/sharedata')
def sharedata():

    if current_user.is_authenticated:

        allshares = share_data.getalljsonshares(current_user.username)
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


        portfolioids=share_data.getportfolioidsfromtable(current_user.username)

        portfoliovalues = {}
        for id in portfolioids:



            sharevalue = 0.0
            dividends = 0.0
            portfoliovalue = 0.0

            for share in allshares:

                if share['portfolioid'] == id:


                    shareprice = float (share['price'])
                    quantity = share['quantity']
                    shareholding = shareprice * quantity
                    dividends = dividends + share['dividends']
                    sharevalue += shareholding
                    portfoliovalue = sharevalue + dividends

                    dictvalues = {'portfoliovalue': round(portfoliovalue, 2), 'sharevalue': sharevalue, 'dividends': dividends}
                    portfoliovalues[id] = dictvalues



        return render_template('sharedata.html', data=sharesinportfolio,
                               portfoliovalues=portfoliovalues, portfolioprofits=profits,
                               ids=share_data.getportfolioidsfromtable(current_user.username))


@app.route('/sharedatanolivedata')
def sharedatanolivedata():

    if current_user.is_authenticated:


        return render_template('sharedatanolivedata.html', data=share_data.getSharesNoLiveData(current_user.username),
                               ids=share_data.getnonemptyportfolios(current_user.username))


@app.route('/newsdata')
def newsdata():

    if current_user.is_authenticated:


        return render_template('news/news.html', news=News.getNews(current_user.username))

@app.route('/risefall')
def risefall():

    if current_user.is_authenticated:


        return render_template('news/risefall.html', data=RiseFall.getRiseFall(current_user.username))


@app.route('/allnews')
def allnews():

    if current_user.is_authenticated:

        return render_template('news/allnews.html', news=News.getNews(current_user.username),
                               portfolioids=share_data.getportfolioidsfromtable(current_user.username))

@app.route('/allrisefall')
def allrisefall():

    if current_user.is_authenticated:


        return render_template('news/allrisefall.html', data=RiseFall.getRiseFall(current_user.username),
                               portfolioids=share_data.getportfolioidsfromtable(current_user.username))


@app.route('/sidebarshare', methods=['GET', 'POST'] )
def sidebarshare():

    form = SidebarShareForm()
    form.ticker.choices = [('AAL','ANGLO AMERICAN'),('AHT','ASHTEAD GROUP PLC'),
                           ('BKG','BERKELY GROUP HOLDING'), ('CARD','CARD FACTORY'),('CLLN','CARILLION PLC'),
                           ('DCC','DCC PLC'),
                           ('DTY','DIGNITY PLC'),('FAN','VOLUTION GROUP'), ('GLEN','GLENCORE PLC'), ('HSBA','HSBC'),
                           ('IHG','INTERCONTINENTAL HOTELS GROUP PLC'), ('LLOY','LLOYDS BANKING GROUP'),
                           ('MKS', 'MARKS & SPENCER'), ('OML','OLD MUTUAL PLC'), ('RBS', 'ROYAL BANK OF SCOTLAND'),
                           ('RUS','RAVEN RUSSIA'),('PFG','PROVIDENT FINANCIAL PLC'), ('STAN','STANDARD CHARTERED PLC'),
                           ('WTB','WHITBREAD PLC')]

    if current_user.is_authenticated:

        if form.validate_on_submit():

            return redirect(url_for('sidebar/addshare.html'))




        return render_template('sidebar/addshare.html', form=form)