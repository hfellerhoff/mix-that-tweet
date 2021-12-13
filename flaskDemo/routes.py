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

        checkExisting = Tweet.query.get_or_404(tweet_dict["tweet_id"])
        if not checkExisting:
        # if form.tweet_exists == False:
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

            tweet = Tweet(
                tweet_id=tweet_dict["tweet_id"],
                tweet_url=tweet_dict["tweet_url"],
                author_id=tweet_dict["author_id"],
                tweet_created_at=tweet_dict["tweet_created_at"],
                tweet_text=tweet_dict["tweet_text"],
                retweet_count=tweet_dict["retweet_count"],
                reply_count=tweet_dict["reply_count"],
                like_count=tweet_dict["like_count"],
                quote_count=tweet_dict["quote_count"],
                positive_sentiment_score=tweet_dict["positive_sentiment_score"],
                neutral_sentiment_score=tweet_dict["neutral_sentiment_score"],
                negative_sentiment_score=tweet_dict["negative_sentiment_score"]
            )
            db.session.add(tweet)
            db.session.commit()

            flash('Your Tweet has been added! You are now able to see your playlist', 'success')
        else:
            tweeter = db.session.query(Tweeter).get(tweeter_dict['tweeter_id'])
            tweeter.followers_count = tweeter_dict["followers_count"],
            tweeter.following_count = tweeter_dict["following_count"]
            tweeter.tweet_count = tweeter_dict["tweet_count"]
            tweeter.listed_count = tweeter_dict["listed_count"]
            db.session.commit()

            tweet = db.session.query(Tweet).get(tweet_dict['tweet_id'])
            tweet.retweet_count=tweet_dict["retweet_count"],
            tweet.reply_count=tweet_dict["reply_count"],
            tweet.like_count=tweet_dict["like_count"],
            tweet.quote_count=tweet_dict["quote_count"],
            tweet.positive_sentiment_score=tweet_dict["positive_sentiment_score"],
            tweet.neutral_sentiment_score=tweet_dict["neutral_sentiment_score"],
            tweet.negative_sentiment_score=tweet_dict["negative_sentiment_score"]
            db.session.commit()

            flash('Your Tweet has been updated! Your playlist will now reflect these changes.', 'success')

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
