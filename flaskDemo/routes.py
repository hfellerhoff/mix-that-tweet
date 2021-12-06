import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import TweetForm
from flaskDemo.models import Include, Playlist, Song, Tweet
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home")
def home():
    form = TweetForm()
    return render_template('home.html', form=form)

   


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Route for showing the playlist of songs created from entering the tweet url
@app.route("/playlist/<playlist_id>")
def playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    # still working on this, but have the html page for it created at least
    return redirect('playlist.html', playlist=playlist)
