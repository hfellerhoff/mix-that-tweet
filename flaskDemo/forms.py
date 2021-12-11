from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp, URL
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import Include, Playlist, Song, Tweet
from wtforms.fields.html5 import DateField

class TweetForm(FlaskForm):
    tweet_url=StringField('Tweet URL', validators=[DataRequired(), URL()])
    submit=SubmitField('Submit')

    # TODO: validation for tweet
    # def validate_tweet(self, tweet_url):
        # tweet_url = Tweet.query.filter_by(tweet_url=tweet_url.data).first()

        # if tweet_url:

