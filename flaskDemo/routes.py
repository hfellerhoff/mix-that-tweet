# import os
# import secrets
# from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskDemo import app, db, bcrypt
from flaskDemo import tweet_analysis
from flaskDemo.forms import TweetForm, TweetRemixForm
from flaskDemo.models import Include, Playlist, Song, Tweet, Tweeter
# from datetime import datetime
from flaskDemo.tweet_analysis import analyzeTweet
from flaskDemo.spotify import get_recommendations


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = TweetForm()
    if form.validate_on_submit():
        tweet_dict, tweeter_dict, tweet_to_audiofeatures_map = analyzeTweet(
            form.tweet_url.data)
        
        if not tweet_dict:
            flash('Tweet is private. Try another Tweet!', 'error')
            return render_template('home.html', form=form, title='Mix That Tweet')

        tweet_url = Tweet.query.filter_by(
            tweet_id=tweet_dict["tweet_id"]).first()

        if not tweet_url:
            tweeter_id = Tweeter.query.filter_by(
                tweeter_id=tweeter_dict['tweeter_id']).first()
            # Create new
            if not tweeter_id:
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

            # Update tweeter
            else:
                tweeter = db.session.query(Tweeter).get(
                    tweeter_dict['tweeter_id'])
                tweeter.followers_count = tweeter_dict["followers_count"],
                tweeter.following_count = tweeter_dict["following_count"]
                tweeter.tweet_count = tweeter_dict["tweet_count"]
                tweeter.listed_count = tweeter_dict["listed_count"]
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

            flash(
                'Your Tweet has been added! You are now able to see your playlist', 'success')
        else:
            tweeter = db.session.query(Tweeter).get(tweeter_dict['tweeter_id'])
            tweeter.followers_count = tweeter_dict["followers_count"],
            tweeter.following_count = tweeter_dict["following_count"]
            tweeter.tweet_count = tweeter_dict["tweet_count"]
            tweeter.listed_count = tweeter_dict["listed_count"]
            db.session.commit()

            tweet = db.session.query(Tweet).get(tweet_dict['tweet_id'])
            tweet.retweet_count = tweet_dict["retweet_count"],
            tweet.reply_count = tweet_dict["reply_count"],
            tweet.like_count = tweet_dict["like_count"],
            tweet.quote_count = tweet_dict["quote_count"],
            tweet.positive_sentiment_score = tweet_dict["positive_sentiment_score"],
            tweet.neutral_sentiment_score = tweet_dict["neutral_sentiment_score"],
            tweet.negative_sentiment_score = tweet_dict["negative_sentiment_score"]
            db.session.commit()

            flash(
                'Your Tweet has been updated! Your playlist will now reflect these changes.', 'success')

        # getting recommendations
        tracks = get_recommendations(tweet_to_audiofeatures_map, genre=form.genre.data)

        # track.id
        # track.uri
        # track.name
        # track.duration_ms

        # adding songs
        songs = list()
        song_ids = list()
        for track in tracks:
            song = Song.query.filter_by(song_id=track['id']).first()
            if not song:
                song = Song(
                    song_id=track['id'],
                    song_uri=track['uri'],
                    # song_name=track.name
                )
                db.session.add(song)
            songs.append(song)
            song_ids.append(track['id'])
        db.session.commit()

        # create playlist
        # playlist = Playlist(
        #     playlist_id='p_' + tweet_dict["tweet_id"],
        #     playlist_uri=track.uri,
        #     tweet_id=track.duration_ms,
        # )
        # db.session.add(playlist)
        # db.session.commit()
        # add songs/playlist to playlist_includes_song
        song_id_string = ','.join(song_ids)
        return redirect(url_for('playlist', genre=form.genre.data, song_ids=song_id_string, tweet_url=tweet_dict["tweet_url"], tweet_text=tweet_dict["tweet_text"], tweet_author=tweeter_dict["tweeter_name"]))
    return render_template('home.html', form=form, title='Mix That Tweet')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Route for showing the playlist of songs created from entering the tweet url
@app.route("/playlist", methods=['GET', 'POST'])
def playlist():
    form = TweetRemixForm()
    songs = request.args.get('song_ids').split(',')
    tweet_text = request.args.get('tweet_text')
    tweet_author = request.args.get('tweet_author')
    tweet_url = request.args.get('tweet_url')
    
    if form.validate_on_submit():
        tweet_dict, tweeter_dict, tweet_to_audiofeatures_map = analyzeTweet(
            tweet_url)
        
        if not tweet_dict:
            flash('That Tweet is likely private. Try another Tweet!', 'error')
            return redirect(url_for('home'))

        tweet_url = Tweet.query.filter_by(
            tweet_id=tweet_dict["tweet_id"]).first()

        if not tweet_url:
            tweeter_id = Tweeter.query.filter_by(
                tweeter_id=tweeter_dict['tweeter_id']).first()
            # Create new
            if not tweeter_id:
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

            # Update tweeter
            else:
                tweeter = db.session.query(Tweeter).get(
                    tweeter_dict['tweeter_id'])
                tweeter.followers_count = tweeter_dict["followers_count"],
                tweeter.following_count = tweeter_dict["following_count"]
                tweeter.tweet_count = tweeter_dict["tweet_count"]
                tweeter.listed_count = tweeter_dict["listed_count"]
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

            flash(
                'Your Tweet has been added! You are now able to see your playlist', 'success')
        else:
            tweeter = db.session.query(Tweeter).get(tweeter_dict['tweeter_id'])
            tweeter.followers_count = tweeter_dict["followers_count"],
            tweeter.following_count = tweeter_dict["following_count"]
            tweeter.tweet_count = tweeter_dict["tweet_count"]
            tweeter.listed_count = tweeter_dict["listed_count"]
            db.session.commit()

            tweet = db.session.query(Tweet).get(tweet_dict['tweet_id'])
            tweet.retweet_count = tweet_dict["retweet_count"],
            tweet.reply_count = tweet_dict["reply_count"],
            tweet.like_count = tweet_dict["like_count"],
            tweet.quote_count = tweet_dict["quote_count"],
            tweet.positive_sentiment_score = tweet_dict["positive_sentiment_score"],
            tweet.neutral_sentiment_score = tweet_dict["neutral_sentiment_score"],
            tweet.negative_sentiment_score = tweet_dict["negative_sentiment_score"]
            db.session.commit()

            flash(
                'Your Tweet has been updated! Your playlist will now reflect these changes.', 'success')

        # getting recommendations
        tracks = get_recommendations(tweet_to_audiofeatures_map, genre=form.genre.data)

        # track.id
        # track.uri
        # track.name
        # track.duration_ms

        # adding songs
        songs = list()
        song_ids = list()
        for track in tracks:
            song = Song.query.filter_by(song_id=track['id']).first()
            if not song:
                song = Song(
                    song_id=track['id'],
                    song_uri=track['uri'],
                    # song_name=track.name
                )
                db.session.add(song)
            songs.append(song)
            song_ids.append(track['id'])
        db.session.commit()

        # create playlist
        # playlist = Playlist(
        #     playlist_id='p_' + tweet_dict["tweet_id"],
        #     playlist_uri=track.uri,
        #     tweet_id=track.duration_ms,
        # )
        # db.session.add(playlist)
        # db.session.commit()
        # add songs/playlist to playlist_includes_song
        song_id_string = ','.join(song_ids)
        return redirect(url_for('playlist', genre=form.genre.data, song_ids=song_id_string, tweet_url=tweet_dict["tweet_url"], tweet_text=tweet_dict["tweet_text"], tweet_author=tweeter_dict["tweeter_name"]))
    
    return render_template('sad_playlist.html', form=form, songs=songs, tweet_text=tweet_text, tweet_author=tweet_author)

# @app.route("/playlist/<playlist_id>")
# def playlist(playlist_id):
#     playlist = Playlist.query.get_or_404(playlist_id)
#     # still working on this, but have the html page for it created at least
#     return redirect('playlist.html', playlist=playlist)
