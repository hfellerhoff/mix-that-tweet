from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
from dotenv import load_dotenv
import random
load_dotenv()

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))


def clamp(value, min_value=0, max_value=1):
    return max(min_value, min(max_value, value))


def get_recommendations(attributes):
    # target_acousticness = clamp(attributes['acousticness'], 0, 1),
    # print('target_acousticness:', target_acousticness)
    print('target_danceability:', attributes['danceability'])
    target_danceability = clamp(attributes['danceability'], 0.1, 0.9),
    print('target_danceability:', target_danceability)
    # target_energy = clamp(attributes['energy'], 0, 1),
    # print('target_energy:', target_energy)
    print('target_instrumentalness:', attributes['instrumentalness'])
    target_instrumentalness = clamp(attributes['instrumentalness'], 0, 1),
    print('target_instrumentalness:', target_instrumentalness)
    # target_liveness = clamp(attributes['liveness'], 0, 1),
    # print('target_liveness:', target_liveness)
    # target_loudness = clamp(attributes['loudness'], 0, 1),
    # print('target_loudness:', target_loudness)
    # target_speechiness = clamp(attributes['speechiness'], 0, 1),
    # print('target_speechiness:', target_speechiness)
    # target_tempo = clamp(attributes['tempo'], 0, 1),
    # print('target_tempo:', target_tempo)
    print('target_valence:', attributes['valence'])
    target_valence = clamp(attributes['valence'], 0, 1),
    print('target_valence:', target_valence)
    # target_popularity = clamp(attributes['popularity'], 1, 100),
    # print('target_popularity:', target_popularity)

    try:
        results = spotify.recommendations(
            seed_genres=['pop'],
            country='US',
            #  use time period somehow
            target_valence=target_valence,
            target_danceability=target_danceability,
            target_instrumentalness=target_instrumentalness,
            target_acousticness=random.random(),
            target_energy=random.random(),
            target_liveness=random.random(),
            target_loudness=random.random(),
            target_speechiness=random.random(),
            target_tempo=random.random(),
            # target_energy=target_energy,
            # target_acousticness=target_acousticness,
            # target_liveness=target_liveness,
            # target_loudness=target_loudness,
            # target_speechiness=target_speechiness,
            # target_tempo=target_tempo,
            # target_popularity=target_popularity,
            limit=10
        )
        return results['tracks']
    except:
        print('something went wrong fetching recommendations :(')


# get_playlist(target_acousticness=0.5,
#              target_danceability=0.5,
#              target_energy=0.5,
#              target_instrumentalness=0.5,
#              target_liveness=0.5,
#              target_loudness=0.5,
#              target_speechiness=0.5,
#              target_tempo=0.5,
#              target_valence=0.5,
#              target_popularity=50,  # This is 0-100, I don't know why
#              )
