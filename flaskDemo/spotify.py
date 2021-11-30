from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv
load_dotenv()

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))


def get_playlist(target_acousticness=None,
                 target_danceability=None,
                 target_energy=None,
                 target_instrumentalness=None,
                 target_liveness=None,
                 target_loudness=None,
                 target_speechiness=None,
                 target_tempo=None,
                 target_valence=None,
                 target_popularity=None):
    try:
        results = spotify.recommendations(
            seed_genres=['classical'],
            # seed_tracks=['0c6xIDDpzE81m2q797ordA'],
            # seed_artists=['2WX2uTcsvV5OnS0inACecP'],
            country='US',
            target_acousticness=target_acousticness,
            target_danceability=target_danceability,
            target_energy=target_energy,
            target_instrumentalness=target_instrumentalness,
            target_liveness=target_liveness,
            target_loudness=target_loudness,
            target_speechiness=target_speechiness,
            target_tempo=target_tempo,
            target_valence=target_valence,
            target_popularity=target_popularity,
            # min_acousticness=0.45,
            # max_acousticness=0.55,
            # min_danceability=0.45,
            # max_danceability=0.55,
            # min_energy=0.45,
            # max_energy=0.55,
            # min_instrumentalness=0.45,
            # max_instrumentalness=0.45,
            # min_liveness=0.55,
            # max_liveness=0.55,
            # min_loudness=0.55,
            # max_loudness=0.55,
            # min_popularity=0.55,
            # max_popularity=0.55,
            # min_speechiness=0.55,
            # max_speechiness=0.55,
            # min_tempo=0.55,
            # max_tempo=0.55,
        )
        for track in results['tracks']:
            print(track['name'])
    except:
        print('something went wrong fetching recommendations :(')


get_playlist(target_acousticness=0.5,
             target_danceability=0.5,
             target_energy=0.5,
             target_instrumentalness=0.5,
             target_liveness=0.5,
             target_loudness=0.5,
             target_speechiness=0.5,
             target_tempo=0.5,
             target_valence=0.5,
             target_popularity=50,  # This is 0-100, I don't know why
             )
