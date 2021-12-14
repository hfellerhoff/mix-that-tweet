import pandas as pd
import requests
import json
import datetime
import os
import re

# pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()

# pip install azure-ai-textanalytics
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

########## API Keys and Tokens ##########

TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
AZURE_SUBSCRIPTION_KEY = os.environ['AZURE_SUBSCRIPTION_KEY']
AZURE_ENDPOINT = os.environ['AZURE_ENDPOINT']

########## API Handling ##########

def process_tweet_link(link):
    print(link)
    link = link.split('/')
    for index, component in enumerate(link):
        if component == 'status':
            id = link[index + 1]
            if id.count('?') != 0:
                return id[:id.index('?')]
            else:
                return id

def create_twitter_url(tweet_id):
    id = 'ids=' + str(tweet_id)
    tweet_fields = 'tweet.fields=id,created_at,public_metrics,possibly_sensitive'
    expansions = 'expansions=author_id'
    user_fields = 'user.fields=created_at,public_metrics'
    url = 'https://api.twitter.com/2/tweets?{}&{}&{}&{}'.format(
        id, 
        tweet_fields, 
        expansions, 
        user_fields
    )
    return url

def twitter_auth_and_connect(url):
    headers = {
        'Authorization': 'Bearer {}'.format(TWITTER_BEARER_TOKEN),
        'User-Agent': 'v2TweetLookupPython'
    }
    response = requests.request('GET', url, headers=headers)
    return response.json()

def authenticate_azure_client():
    ta_credential = AzureKeyCredential(AZURE_SUBSCRIPTION_KEY)
    text_analytics_client = TextAnalyticsClient(
            endpoint = AZURE_ENDPOINT,
            credential = ta_credential)
    return text_analytics_client

def sentiment_analysis(client, text):
    doc = [text]
    response = client.analyze_sentiment(documents = doc)[0]
    positive_sentiment_score = response.confidence_scores.positive
    neutral_sentiment_score = response.confidence_scores.neutral
    negative_sentiment_score = response.confidence_scores.negative
    return positive_sentiment_score, neutral_sentiment_score, negative_sentiment_score

########## Metric Conversions ##########

def calculate_loudness(text):
    caps_count = 0
    for character in text:
        if character.isupper():
            caps_count += 1
    return caps_count / len(text)

def calculate_speechiness(text):
    chars_count = 0
    for character in text:
        if character.isalnum():
            chars_count += 1
    return chars_count / 140

def calculate_liveness(text):
    symbols_count = 0
    for character in text:
        if not character.isalnum():
            symbols_count += 1
    return symbols_count / len(text)

def calculate_acousticness(text):
    spaces_count = 0
    for character in text:
        if character.isspace():
            spaces_count += 1
    return spaces_count / len(text)

########## Convenience Functions ##########

def get_ddl(ddl):
    return ddl

def get_mapping(map):
    return map

def pretty(doc):
    return json.dumps(doc, indent = 4)

########## Flask Handling ##########

def analyzeTweet(link):
    processed_tweet_id = process_tweet_link(link)
    tweet_obj = twitter_auth_and_connect(create_twitter_url(processed_tweet_id))
    
    print(tweet_obj)
    
    if 'errors' in tweet_obj:
        tweet = None
        tweeter = None
        tweet_to_audiofeatures_map = None
        return tweet, tweeter, tweet_to_audiofeatures_map
    else:
        text = tweet_obj['data'][0]['text']
        azure_client = authenticate_azure_client()
        positive_sentiment_score, neutral_sentiment_score, negative_sentiment_score = sentiment_analysis(azure_client, text)

        # Tweet data
        tweet_id = tweet_obj['data'][0]['id']
        tweet_url = create_twitter_url(processed_tweet_id)
        tweet_created_at = tweet_obj['data'][0]['created_at']
        retweet_count = tweet_obj['data'][0]['public_metrics']['retweet_count']
        reply_count = tweet_obj['data'][0]['public_metrics']['reply_count']
        like_count = tweet_obj['data'][0]['public_metrics']['like_count']
        quote_count = tweet_obj['data'][0]['public_metrics']['quote_count']

        # Tweeter data
        tweeter_id = tweet_obj['includes']['users'][0]['id']
        tweeter_name = tweet_obj['includes']['users'][0]['name']
        tweeter_username = tweet_obj['includes']['users'][0]['username']
        tweeter_created_at = tweet_obj['includes']['users'][0]['created_at']
        followers_count = tweet_obj['includes']['users'][0]['public_metrics']['followers_count']
        following_count = tweet_obj['includes']['users'][0]['public_metrics']['following_count']
        tweet_count = tweet_obj['includes']['users'][0]['public_metrics']['tweet_count']
        listed_count = tweet_obj['includes']['users'][0]['public_metrics']['listed_count']
        
        # Handling of emojis in Tweeter username
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags = re.UNICODE
        )
        
        tweeter_name = emoji_pattern.sub(r'', tweeter_name)

        tweet = {
            'tweet_id': tweet_obj['data'][0]['id'],
            'tweet_url': link,
            'author_id': tweet_obj['includes']['users'][0]['id'],
            'tweet_created_at': tweet_obj['data'][0]['created_at'][0:10],
            'tweet_text': text,
            'retweet_count': tweet_obj['data'][0]['public_metrics']['retweet_count'],
            'reply_count': tweet_obj['data'][0]['public_metrics']['reply_count'],
            'like_count': tweet_obj['data'][0]['public_metrics']['like_count'],
            'quote_count': tweet_obj['data'][0]['public_metrics']['quote_count'],
            'positive_sentiment_score': positive_sentiment_score,
            'neutral_sentiment_score': neutral_sentiment_score,
            'negative_sentiment_score': negative_sentiment_score
        }

        tweeter = {
            'tweeter_id': tweet_obj['includes']['users'][0]['id'],
            'tweeter_name': tweeter_name,
            'tweeter_username': tweet_obj['includes']['users'][0]['username'],
            'tweeter_created_at': tweet_obj['includes']['users'][0]['created_at'][0:10],
            'followers_count': tweet_obj['includes']['users'][0]['public_metrics']['followers_count'],
            'following_count': tweet_obj['includes']['users'][0]['public_metrics']['following_count'],
            'tweet_count': tweet_obj['includes']['users'][0]['public_metrics']['tweet_count'],
            'listed_count': tweet_obj['includes']['users'][0]['public_metrics']['listed_count']
        }

        # Tweet object to Spotify audio features
        danceability = retweet_count / (followers_count / 200) # Highest retweet count to date
        valence = positive_sentiment_score
        
        instrumental_modifier = neutral_sentiment_score if neutral_sentiment_score is 0 else 0.01
        instrumentalness = reply_count / (like_count * instrumental_modifier)
        
        time_period = (datetime.date.today() - datetime.date(int(tweet_created_at[0:4]), int(tweet_created_at[5:7]), int(tweet_created_at[8:10]))).days # In days
        energy = (reply_count + like_count) / followers_count 
        tempo = positive_sentiment_score + negative_sentiment_score
        loudness = calculate_loudness(text)
        speechiness = calculate_speechiness(text)
        liveness = calculate_liveness(text)
        acousticness = calculate_acousticness(text)
        popularity = followers_count / 1000000


        # Tweet object to Spotify audio features mapping
        tweet_to_audiofeatures_map = {
            'time_period': time_period,
            'danceability': danceability,
            'valence': valence,
            'energy': energy,
            'tempo': tempo,
            'loudness': loudness,
            'speechiness': speechiness,
            'instrumentalness': instrumentalness,
            'liveness': liveness,
            'acousticness': acousticness,
            'popularity': popularity
        }

        return tweet, tweeter, tweet_to_audiofeatures_map