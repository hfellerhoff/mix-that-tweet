from datetime import datetime
from flaskDemo import db  # , login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm
from sys import platform


db.Model.metadata.reflect(db.engine)


# This is to fix this issue:
# https://stackoverflow.com/questions/8771743/mysql-windows-and-the-lowercase-table-name
# If this is not applicable, set this value manually
areTablesLowercase = platform == 'win32'

tables = {
    'playlist_includes_song': 'Playlist_Includes_Song',
    'playlist': 'Playlist',
    'song': 'Song',
    'tweet': 'Tweet',
    'tweeter': 'Tweeter',
    'genre': 'Genre',
}

if areTablesLowercase:
    for row in tables:
        tables[row] = tables[row].lower()

# @login_manager.user_loader
# used for Mix That Tweet


class Include(db.Model):
    __table__ = db.Model.metadata.tables[tables['playlist_includes_song']]


class Playlist(db.Model):
    __table__ = db.Model.metadata.tables[tables['playlist']]


class Song(db.Model):
    __table__ = db.Model.metadata.tables[tables['song']]


class Tweet(db.Model):
    __table__ = db.Model.metadata.tables[tables['tweet']]


class Tweeter(db.Model):
    __table__ = db.Model.metadata.tables[tables['tweeter']]

# Full list of genres available:
# https://gist.github.com/drumnation/91a789da6f17f2ee20db8f55382b6653


class Genre(db.Model):
    __table__ = db.Model.metadata.tables[tables['genre']]
