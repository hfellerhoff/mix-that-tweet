import pandas as pd
import requests
import json
import ast
import yaml
import datetime

def create_twitter_url():
    # Need Elevated Twitter API authentication for below 'tweet_fields'
    # tweet_fields = 'tweet.fields=created_at,public_metrics,non_public_metrics,possibly_sensitive'
    tweet_fields = 'tweet.fields=id,created_at,public_metrics,possibly_sensitive'
    expansions = 'expansions=author_id'
    url = "https://api.twitter.com/2/tweets/20?{}&{}".format(tweet_fields, expansions)
    return url

def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)

def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]

def twitter_auth_and_connect(bearer_token, url):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()

def pretty(doc):
    return json.dumps(doc, indent = 4)

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

def get_ddl(ddl):
    return ddl

def get_mapping(map):
    return map

def main():     
    # Test Tweet
    # testURL = 'https://twitter.com/holy_schnitt/status/1465762217480097794?s=20'
    # uniformURL = 'https://twitter.com/i/web/status/1465762217480097794'
    
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, create_twitter_url())
    print(pretty(res_json))

    print()
    
    # Tweet object
    tweet_id = 'tweet1' # Either DB-generated index or from 
    tweet_url = create_twitter_url()
    text = res_json['data']['text']
    user_handle = res_json['includes']['users'][0]['name']
    created_at = res_json['data']['created_at']
    retweet_count = res_json['data']['public_metrics']['retweet_count']
    reply_count = res_json['data']['public_metrics']['reply_count']
    like_count = res_json['data']['public_metrics']['like_count']
    # quote_count = res_json['data']['public_metrics']['quote_count']
    impression_count = 353 # Need from 'non_public_metrics' w/ Elevated Twitter API authentication
    url_link_clicks = 353 # Need from 'non_public_metrics' w/ Elevated Twitter API authentication
    user_profile_clicks = 353 # Need from 'non_public_metrics' w/ Elevated Twitter API authentication
    positive_sentiment_percentage = 0.33 # Need from Azure API
    neutral_sentiment_percentage = 0.33 # Need from Azure API
    negative_sentiment_percentage = 0.33 # Need from Azure API

    # Tweet SQL insertion DDL
    insert_ddl = 'INSERT INTO Tweet(tweet_id,tweet_url,user_handle,created_at,impression_count,like_count,reply_count,retweet_count,url_link_clicks,user_profile_clicks,positive_sentiment_percentage,neutral_sentiment_percentage,negative_sentiment_percentage) VALUES (\'{}\',\'{}\',\'{}\',\'{}\',{},{},{},{},{},{});'.format(tweet_id,tweet_url,user_handle,created_at,impression_count,like_count,reply_count,retweet_count,url_link_clicks,user_profile_clicks,positive_sentiment_percentage,neutral_sentiment_percentage,negative_sentiment_percentage)
    print('Tweet SQL insertion DDL:\n', get_ddl(insert_ddl))

    print()

    # Tweet object to Spotify audio features
    time_period = (datetime.date.today() - datetime.date(int(created_at[0:4]), int(created_at[5:7]), int(created_at[9:10]))).days # In days
    danceability = retweet_count
    valence = positive_sentiment_percentage - negative_sentiment_percentage
    energy = reply_count
    tempo = positive_sentiment_percentage + negative_sentiment_percentage
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

if __name__ == "__main__":
    main()