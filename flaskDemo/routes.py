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
        tracks = get_recommendations(
            tweet_to_audiofeatures_map, genre=form.genre.data)
        
        playlist_id='p_' + tweet_dict["tweet_id"]


        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        # create playlist
        if not playlist:
            playlist = Playlist(
                playlist_id=playlist_id,
                playlist_uri=tweet_dict["tweet_url"],
                tweet_id=tweet_dict["tweet_id"],
            )
            db.session.add(playlist)
            db.session.commit()
        
        playlist_includes_songs = Include.query.filter_by(playlist_id=playlist_id).all()
        old_song_ids = []
        
        # Clear the playlist and delete pre-existing songs
        for included_song in playlist_includes_songs:
            Include.query.filter_by(playlist_id=playlist_id).delete()
            old_song_ids.append(included_song.song_id)
        Include.query.filter_by(playlist_id=playlist_id).delete()
        db.session.commit()
        
        # Delete songs not being referenced in other playlists
        for song_id in old_song_ids:
            song_in_another_playlist = Include.query.filter_by(song_id=song_id).first()
            if not song_in_another_playlist:
                Song.query.filter_by(song_id=song_id).delete()
        db.session.commit()
        
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
        
        for song_id in song_ids:
            playlist_includes_song = Include(
                playlist_id=playlist_id,
                song_id=song_id
            )
            db.session.add(playlist_includes_song)
        db.session.commit()
        
        return redirect(url_for('playlist', playlist_id=playlist_id, genre=form.genre.data))
    return render_template('home.html', form=form, title='Mix That Tweet')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


# Route for showing the playlist of songs created from entering the tweet url
@app.route("/playlist/<playlist_id>", methods=['GET', 'POST'])
def playlist(playlist_id):
    form = TweetRemixForm()
    
    genre = request.args.get('genre')
    song_count = Include.query.filter_by(playlist_id=playlist_id).count()
    
    # our beloved join query
    join_data = Include.query.join(Song, Include.song_id == Song.song_id) \
        .add_columns(Song.song_id, Song.song_uri) \
        .join(Playlist, Playlist.playlist_id == Include.playlist_id) \
        .add_columns(Playlist.tweet_id) \
        .join(Tweet, Playlist.tweet_id == Tweet.tweet_id) \
        .add_columns(Tweet.tweet_url, Tweet.tweet_text, Tweet.author_id) \
        .join(Tweeter, Tweet.author_id == Tweeter.tweeter_id) \
        .add_columns(Tweeter.tweeter_username) \
        .filter(Include.playlist_id == playlist_id)
                    
    songs = []
    for entry in join_data:
        song = dict()
        song['song_id'] = entry[1]
        song['song_uri'] = entry[2]
        song['tweet_url'] = entry[4]
        song['tweet_text'] = entry[5]
        song['tweet_author'] = entry[7]
                
        songs.append(song)

    if form.validate_on_submit():
        tweet_dict, tweeter_dict, tweet_to_audiofeatures_map = analyzeTweet(songs[0]['tweet_url'])

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
        tracks = get_recommendations(
            tweet_to_audiofeatures_map, genre=form.genre.data)
        
        playlist_id='p_' + tweet_dict["tweet_id"]


        playlist = Playlist.query.filter_by(playlist_id=playlist_id).first()
        # create playlist
        if not playlist:
            playlist = Playlist(
                playlist_id=playlist_id,
                playlist_uri=tweet_dict["tweet_url"],
                tweet_id=tweet_dict["tweet_id"],
            )
            db.session.add(playlist)
            db.session.commit()
        
        playlist_includes_songs = Include.query.filter_by(playlist_id=playlist_id).all()
        old_song_ids = []
        
        # Clear the playlist and delete pre-existing songs
        for included_song in playlist_includes_songs:
            Include.query.filter_by(playlist_id=playlist_id).delete()
            old_song_ids.append(included_song.song_id)
        Include.query.filter_by(playlist_id=playlist_id).delete()
        db.session.commit()
        
        # Delete songs not being referenced in other playlists
        for song_id in old_song_ids:
            song_in_another_playlist = Include.query.filter_by(song_id=song_id).first()
            if not song_in_another_playlist:
                Song.query.filter_by(song_id=song_id).delete()
        db.session.commit()
        
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
        
        for song_id in song_ids:
            playlist_includes_song = Include(
                playlist_id=playlist_id,
                song_id=song_id
            )
            db.session.add(playlist_includes_song)
        db.session.commit()
        
        return redirect(url_for('playlist', playlist_id=playlist_id, genre=form.genre.data))

    return render_template('sad_playlist.html', form=form, songs=songs, song_count=song_count, genre=genre)

# @app.route("/playlist/<playlist_id>")
# def playlist(playlist_id):
#     playlist = Playlist.query.get_or_404(playlist_id)
#     # still working on this, but have the html page for it created at least
#     return redirect('playlist.html', playlist=playlist)
