import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#configure database
app.config['SECRET_KEY'] = '5\x91"\xee:/C\xfc\x03\x9c\x04C9\xdc\xae\x00]\xc8\xa4\x16~\xe5\xe16'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sharedb.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

#configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

#for displaying timestamps
moment = Moment(app)

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'public'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdMHxkTAAAAAPwhtJjpWwTA7h6kNWDKO9SzUw2U'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

import models
import views
