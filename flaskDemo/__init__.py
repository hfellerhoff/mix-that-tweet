from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sys import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# line 10 is for running in the VM for what Sophie named the db in her phpMyAdmin

# pick connection string based on operating system
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://student:student@127.0.0.1:8889/mix_that_tweet' if platform == "darwin" else 'mysql://student:student@localhost/mix_that_tweet'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskDemo import routes
from flaskDemo import models

models.db.create_all()
