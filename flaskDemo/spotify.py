import random
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os

# pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()

########## API Keys and Tokens ##########
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

########## API Handling ##########

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

########## Convenience Functions ##########

def clamp(value, min_value=0, max_value=1):
    return max(min_value, min(max_value, value))

########## Flask Handling ##########

def get_recommendations(attributes, genre = 'Pop'):
    target_danceability = clamp(attributes['danceability'], 0.1, 0.9),
    target_instrumentalness = clamp(attributes['instrumentalness'], 0, 1),
    target_valence = clamp(attributes['valence'], 0, 1),

    try:
        results = spotify.recommendations(
            seed_genres=[genre],
            country='US',
            target_valence=target_valence,
            target_danceability=target_danceability,
            target_instrumentalness=target_instrumentalness,
            target_acousticness=random.random(),
            target_energy=random.random(),
            target_liveness=random.random(),
            target_loudness=random.random(),
            target_speechiness=random.random(),
            target_tempo=random.random(),
            limit=10
        )
        
        return results['tracks']
    except:
        print('ERROR: Something went wrong fetching recommendations :(')