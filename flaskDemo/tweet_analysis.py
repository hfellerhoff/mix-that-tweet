import pandas as pd
import requests
import json
import yaml
import datetime

# pip install azure-ai-textanalytics
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

########## API Keys and Tokens ##########

# TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']
# AZURE_SUBSCRIPTION_KEY = os.environ['AZURE_SUBSCRIPTION_KEY']
# AZURE_ENDPOINT = os.environ['AZURE_ENDPOINT']

########## API Handling ##########

def process_yaml():
    with open('config.yaml') as file:
        return yaml.safe_load(file)

def process_tweet_link(link):
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

def twitter_auth_and_connect(yaml_data, url):
    headers = {
        # 'Authorization': 'Bearer {}'.format(TWITTER_BEARER_TOKEN), # ENV
        'Authorization': 'Bearer {}'.format(yaml_data['twitter']['bearer_token']), # YAML
        'User-Agent': 'v2TweetLookupPython'
    }
    response = requests.request('GET', url, headers=headers)
    return response.json()

def authenticate_azure_client(yaml_data):
    # ta_credential = AzureKeyCredential(AZURE_SUBSCRIPTION_KEY) # ENV
    ta_credential = AzureKeyCredential(yaml_data['azure']['subscription_key']) # YAML
    text_analytics_client = TextAnalyticsClient(
            # endpoint = AZURE_ENDPOINT, # ENV
            endpoint = yaml_data['azure']['endpoint'], # YAML
            credential = ta_credential)
    return text_analytics_client

def sentiment_analysis(client, text):
    doc = [text]
    response = client.analyze_sentiment(documents = doc)[0]
    overall_sentiment = response.sentiment
    positive_sentiment_score = response.confidence_scores.positive
    neutral_sentiment_score = response.confidence_scores.neutral
    negative_sentiment_score = response.confidence_scores.negative
    return overall_sentiment, positive_sentiment_score, neutral_sentiment_score, negative_sentiment_score

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
        if not character.isspace():
            spaces_count += 1
    return spaces_count / len(text)

########## Convenience Functions ##########

def get_ddl(ddl):
    return ddl

def get_mapping(map):
    return map

def pretty(doc):
    return json.dumps(doc, indent = 4)

########## Driver ##########

def main():
    yaml_data = process_yaml()

    testLink1 = "https://twitter.com/i/web/status/1465762217480097794?s=20"
    testLink2 = "https://twitter.com/FarhangNamdar/status/1230554753182003203?ref_src=twsrc%5Etfw"
    processed_tweet_id = process_tweet_link(testLink1)

    tweet_obj = twitter_auth_and_connect(yaml_data, create_twitter_url(processed_tweet_id))
    print('\nTweet lookup:\n', pretty(tweet_obj))

    text = tweet_obj['data'][0]['text']
    # Just commenting below out to save API requests
    azure_client = authenticate_azure_client(yaml_data)
    overall_sentiment, positive_sentiment_score, neutral_sentiment_score, negative_sentiment_score = sentiment_analysis(azure_client, text)

    print()

    print('Azure text sentiment analysis: {}'.format(overall_sentiment))
    print('Sentiment scores: \n\tPositive={} \n\tNeutral={} \n\tNegative={}'.format(
        positive_sentiment_score,
        neutral_sentiment_score,
        negative_sentiment_score,
    ))

    print()
    
    # Tweet data
    tweet_id = tweet_obj['data'][0]['id']
    tweet_url = create_twitter_url(processed_tweet_id)
    tweet_created_at = tweet_obj['data'][0]['created_at']
    retweet_count = tweet_obj['data'][0]['public_metrics']['retweet_count']
    reply_count = tweet_obj['data'][0]['public_metrics']['reply_count']
    like_count = tweet_obj['data'][0]['public_metrics']['like_count']
    quote_count = tweet_obj['data'][0]['public_metrics']['quote_count']

    # User data
    user_id = tweet_obj['includes']['users'][0]['id']
    name = tweet_obj['includes']['users'][0]['name']
    username = tweet_obj['includes']['users'][0]['username']
    user_created_at = tweet_obj['includes']['users'][0]['created_at']
    followers_count = tweet_obj['includes']['users'][0]['public_metrics']['followers_count']
    following_count = tweet_obj['includes']['users'][0]['public_metrics']['following_count']
    tweet_count = tweet_obj['includes']['users'][0]['public_metrics']['tweet_count']
    listed_count = tweet_obj['includes']['users'][0]['public_metrics']['listed_count']

    # Tweet SQL insertion DDL
    tweet_insert_ddl = 'INSERT INTO Tweet(tweet_id,tweet_url,tweet_created_at,text,retweet_count,reply_count,like_count,quote_count,positive_sentiment_percentage,neutral_sentiment_percentage,negative_sentiment_percentage) VALUES ("{}","{}","{}","{}",{},{},{},{},{},{},{});'.format(
        tweet_id,
        tweet_url,
        tweet_created_at,
        text,
        retweet_count,
        reply_count,
        like_count,
        quote_count,
        positive_sentiment_score,
        neutral_sentiment_score,
        negative_sentiment_score,
    )
    print('Tweet SQL insertion DDL:\n', get_ddl(tweet_insert_ddl))

    print()

    # User SQL insertion DDL
    user_insert_ddl = 'INSERT INTO User(user_id,name,username,user_created_at,followers_count,following_count,tweet_count,listed_count) VALUES ("{}","{}","{}","{}",{},{},{},{});'.format(
        user_id,
        name,
        username,
        user_created_at,
        followers_count,
        following_count,
        tweet_count,
        listed_count,
    )
    print('User SQL insertion DDL:\n', get_ddl(user_insert_ddl))

    print()

    # Tweet object to Spotify audio features
    time_period = (datetime.date.today() - datetime.date(int(tweet_created_at[0:4]), int(tweet_created_at[5:7]), int(tweet_created_at[8:10]))).days # In days
    danceability = retweet_count
    valence = positive_sentiment_score - negative_sentiment_score
    energy = reply_count
    tempo = positive_sentiment_score + negative_sentiment_score
    loudness = calculate_loudness(text)
    speechiness = calculate_speechiness(text)
    instrumentalness = like_count / reply_count
    liveness = calculate_liveness(text)
    acousticness = calculate_acousticness(text)

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
        'acousticness': acousticness
    }
    print('Tweet to Audio Features mapping:\n', get_mapping(tweet_to_audiofeatures_map))

    print()

    # Perhaps sort subset of matching songs by popularity and choose most popular songs for virability?

if __name__ == '__main__':
    main()