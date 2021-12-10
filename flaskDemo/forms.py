from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Include, Playlist, Song, Tweet
from wtforms.fields.html5 import DateField

class TweetForm(FlaskForm):
    tweet_url=StringField('Tweet URL', validators=[DataRequired()])
    submit=SubmitField('Submit')

