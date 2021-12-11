import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import TweetForm
from flaskDemo.models import Include, Playlist, Song, Tweet, Tweeter
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flaskDemo.tweet_analysis import analyzeTweet


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = TweetForm()
    if form.validate_on_submit():
        tweet_dict, tweeter_dict, tweet_to_audiofeatures_map = analyzeTweet(form.tweet_url.data)
        tweeter = Tweeter(
            tweeter_id=tweeter_dict["tweeter_id"],
            tweeter_name=tweeter_dict["tweeter_name"],
            tweeter_username=tweeter_dict["tweeter_username"],
            tweeter_created_at=tweeter_dict["tweeter_created_at"],
            followers_count=tweeter_dict["followers_count"],
            following_count=tweeter_dict["following_count"],
            tweet_count=tweeter_dict["tweet_count"],
            listed_count=tweeter_dict["listed_count"]
        )
        db.session.add(tweeter)
        db.session.commit()
        flash('Your tweet has been added! You are now able to see your playlist', 'success')
        return redirect(url_for('playlist/<playlist_id>'))
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
