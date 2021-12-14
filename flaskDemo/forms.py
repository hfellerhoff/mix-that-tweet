from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, URL
from flaskDemo import db
from flaskDemo.models import Genre
from wtforms.fields.html5 import DateField

genres_db = Genre.query.all()
genre_choices = [(row.seed_genre, row.genre_name) for row in genres_db]
genre_choices.reverse()


class TweetForm(FlaskForm):
    tweet_url = StringField('Tweet URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')
    genre = SelectField("Genre", choices=genre_choices)

    def validate_tweet_url(self, tweet_url):
        if tweet_url.data.find('https://twitter.com/') != 0:
            raise ValidationError(
                'Please provide a link to a Tweet from Twitter.'
            )


class TweetRemixForm(FlaskForm):
    genre = SelectField("Genre", choices=genre_choices)
    submit = SubmitField('Remix!')
