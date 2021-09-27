from flask_wtf import Form
from wtforms.fields import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField, \
    HiddenField, FloatField, RadioField
from flask.ext.wtf.html5 import DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, url, ValidationError, number_range, \
    optional
from wtforms_components import read_only
from share_data import *
from wtforms.widgets import TextInput

from flask_login import current_user
from models import *

class MyTextInput(TextInput):
    def __init__(self, error_border=u'errorborder'):
        super(MyTextInput, self).__init__()
        self.error_class = error_border

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            kwargs['class'] = u'%s %s' % (self.error_class, c)
        return super(MyTextInput, self).__call__(field, **kwargs)


class ExistingShareInPortfolioValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"That share is already in that portfolio"
        self.message = message

    def __call__(self, form, field):

        ticker = form.data['ticker']
        portfolioid = form.data['portfolioid']
        originalportfolioid = form.data['originalportfolioid']

        if Userownedshare.query.filter_by(ticker=ticker.upper()).filter_by(user=current_user.username).filter_by(portfolioid=portfolioid).first() and originalportfolioid != portfolioid:
            raise ValidationError(self.message)


class ExistingPortfolioValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"A portfolio with that name already exists"
        self.message = message

    def __call__(self, form, field):

        name = form.data['name'].lower()

        if Portfolios.query.filter_by(portfolioname=name).filter_by(username=current_user.username).first():
            raise ValidationError(self.message)

        if name == "":
            raise ValidationError("You must enter a portfolio name")


class EmptyPortfolioValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"You cannot delete portfolios that contain shares"
        self.message = message

    def __call__(self, form, field):

        name = form.data['name']

        if Userownedshare.query.filter_by(user=current_user.username).filter_by(portfolioid=name).first():
            raise ValidationError(self.message)


class SharePricevalidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"Enter the share quantity purchased"
        self.message = message

    def __call__(self, form, field):

        if field.data and not form.data['sharequantity']:
            raise ValidationError(self.message)


class ShareQuantityValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"Enter the price paid for these shares"
        self.message = message

    def __call__(self, form, field):

        if field.data and not form.data['shareprice']:
            raise ValidationError(self.message)


class ShareTickerValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"No company exists for that symbol"
        self.message = message

    def __call__(self, form, field):

        symbol = form.data['ticker']

        if not share_data.isValidShare(symbol):
            raise ValidationError(self.message)


class SellShareValidator(object):
    def __init__(self, message=None):
        if not message:
            message = u"That is more shares than you own"
        self.message = message

    def __call__(self, form, field):

        shareID = form.data['shareID']
        share = Userownedshare.query.get_or_404(shareID)

        if share.quantity - form.data['quantity'] < 0:
            raise ValidationError(self.message)


class AddShareForm(Form):
    ticker = SelectField('Select a share to add &nbsp ')

    quantity = IntegerField('Quantity of shares purchased', validators=[number_range(min=1, max=10000)],
                            widget=MyTextInput())
    dividends = FloatField('Dividends for these shares &nbsp', validators=[optional(),
                            number_range(min=0.00)], widget=MyTextInput())
    originalportfolioid = HiddenField("hidden field")
    purchaseprice = DecimalField(u'Purchase price for each share &nbsp',
                                 validators=[number_range(min=0.0, max=120)], render_kw={"placeholder": "0.00"}, widget=MyTextInput())
    portfolioid = SelectField(u'Choose a portfolio', validators=[ExistingShareInPortfolioValidator()])

    def validate(self):

        if not Form.validate(self):
            return False

        return True


class SidebarShareForm(Form):
    ticker = SelectField('')


    def validate(self):

        if not Form.validate(self):
            return False

        return True


class RemoveShareForm(Form):
    ticker = StringField('The share ticker:', validators=[DataRequired(), Regexp(r'^[a-zA-Z]*$',
                                                                                 message="The share ticker must only be letters")])
    quantity = IntegerField('How many of this share did you sell:', validators=[DataRequired(), SellShareValidator(),number_range(min=1, max=10000)])
    price = DecimalField('What price did you sell them for', validators=[DataRequired(), number_range(min=0.00)])
    shareID = HiddenField("hidden field")
    originalportfolioid = HiddenField("hidden field")
    # portfolioid = SelectField('Choose a portfolio to add the share to:', validators=[ExistingShareInPortfolioValidator()])

    def validate(self):

        if not Form.validate(self):
            return False

        return True

    def __init__(self, *args, **kwargs):
        super(RemoveShareForm, self).__init__(*args, **kwargs)
        read_only(self.ticker)


class LoginForm(Form):
    username = StringField('Your Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')
    # recaptcha = RecaptchaField()


class SignupForm(Form):
    username = StringField('Username',
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp('^[A-Za-z0-9_]{3,}$',
                                      message='Usernames consist of numbers, letters and underscores')])

    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password &nbsp', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 80), Email()])
    phonenumber = StringField('Mobile phone number &nbsp',
                           validators=[
                               DataRequired(),
                               Regexp('^(\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$',
                                      message='Not a valid UK mobile phone number')])




    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There is already a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')

    def validate_phonenumber(self, phonenumber_field):
        if User.query.filter_by(phonenumber=phonenumber_field.data).first():
            raise ValidationError('A user with that phone number is already registered')


class AddPortfolioForm(Form):
    name = StringField('New portfolio name: &nbsp ', validators=[ExistingPortfolioValidator(),
                        Regexp(r'^[a-zA-Z0-9_\s]*$', message="The portfolio name must contain only letters and numbers")])

    def validate(self):

        if not Form.validate(self):
            return False

        return True


class AddAdditionalShares(Form):
    name = StringField('Share name')
    sharequantity = IntegerField('Have you bought any additional shares:', validators=[optional(),ShareQuantityValidator(), number_range(min=1, max=10000)])
    shareprice = FloatField('How much did you pay for these shares:', validators=[optional(),SharePricevalidator(), number_range(min=0.01, max=10000)])
    dividends = DecimalField('Have you received any new dividends: &nbsp', validators=[optional(), number_range(min=0.00)])

    def validate(self):

        if not Form.validate(self):
            return False

        return True


class DeletePortfolioForm(Form):
    name = SelectField('Select a portfolio to delete: &nbsp ', validators=[EmptyPortfolioValidator()])

    def validate(self):

        if not Form.validate(self):
            return False

        return True


class NotificationSettingsForm(Form):
    emailfrequency = RadioField(u'How often do you wish to receive emails about your portfolio value?', choices=[('0', 'Never'), ('1', 'Daily'), ('2', 'Weekly')]  )
    smsenabled = RadioField(u'Set the status of your share price alerts', choices=[('0', 'Disabled'), ('1', 'Enabled')], default='0')

    def validate(self):

        if not Form.validate(self):
            return False

        return True


class ShareNotificationForm(Form):
    emailenabled = RadioField(u'Receive email notifications?', choices=[('0', 'No'), ('1', 'Yes')])
    smsenabled = RadioField(u'Receive SMS notifications?', choices=[('0', 'No'), ('1', 'Yes')])
    triggerlevel = DecimalField(u'Set price change at which <br> to send notification')
    positivenegative = RadioField(u' ',choices=[('0', 'Fall by'), ('1', 'Rise by')], validators=[DataRequired()])


    def validate(self):

        if not Form.validate(self):
            return False

        return True


class EditSettingsForm(Form):


    password = PasswordField('Password',
                             validators=[
                                 EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password &nbsp')
    email = StringField('Email',
                        validators=[optional(), Email()])
    phonenumber = StringField('Mobile phone number &nbsp',
                           validators=[optional(),
                               Regexp('^(\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$',
                                      message='Not a valid UK mobile phone number')])




