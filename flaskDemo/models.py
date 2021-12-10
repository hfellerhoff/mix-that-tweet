from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)


@login_manager.user_loader
# used for Mix That Tweet
class Include(db.Model):
    __table__ = db.Model.metadata.tables['Playlist_Includes_Song']


class Playlist(db.Model):
    __table__ = db.Model.metadata.tables['Playlist']


class Song(db.Model):
    __table__ = db.Model.metadata.tables['Song']


class Tweet(db.Model):
    __table__ = db.Model.metadata.tables['Tweet']


class Tweeter(db.Model):
    __table__ = db.Model.metadata.tables['Tweeter']
