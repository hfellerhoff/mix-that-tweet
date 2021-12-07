import pandas as pd
import requests
import json
import ast
import yaml
import datetime

########## API Handling ##########

def create_twitter_url():
    id = 'ids=1465762217480097794'
    #tweet_fields = 'tweet.fields=created_at,public_metrics,non_public_metrics,possibly_sensitive'
    tweet_fields = 'tweet.fields=id,created_at,public_metrics,possibly_sensitive'
    expansions = 'expansions=author_id'
    user_fields = 'user.fields=created_at,public_metrics'
    #url = "https://api.twitter.com/2/tweets/20?{}&{}".format(tweet_fields, expansions)
    url = "https://api.twitter.com/2/tweets?{}&{}&{}&{}".format(id, tweet_fields, expansions, user_fields)
    return url

def process_yaml():
    with open("config.yaml") as file:
        return yaml.safe_load(file)

def create_bearer_token(data):
    return data["search_tweets_api"]["bearer_token"]

def twitter_auth_and_connect(bearer_token, url):
    headers = {
        "Authorization": "Bearer {}".format(bearer_token),
        'User-Agent': 'v2TweetLookupPython'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def lang_data_shape(res_json):
    data_only = res_json["data"]
    doc_start = '"documents": {}'.format(data_only)
    str_json = "{" + doc_start + "}"
    dump_doc = json.dumps(str_json)
    doc = json.loads(dump_doc)
    return ast.literal_eval(doc)

def connect_to_azure(data):
    azure_url = "https://week.cognitiveservices.azure.com/"
    language_api_url = "{}text/analytics/v2.1/languages".format(azure_url)
    sentiment_url = "{}text/analytics/v2.1/sentiment".format(azure_url)
    subscription_key = data["azure"]["subscription_key"]
    return language_api_url, sentiment_url, subscription_key

def azure_header(subscription_key):
    return {"Ocp-Apim-Subscription-Key": subscription_key}

def generate_languages(headers, language_api_url, documents):
    response = requests.post(language_api_url, headers=headers, json=documents)
    return response.json()


def combine_lang_data(documents, with_languages):
    langs = pd.DataFrame(with_languages["documents"])
    lang_iso = [x.get("iso6391Name")
                for d in langs.detectedLanguages if d for x in d]
    data_only = documents["documents"]
    tweet_data = pd.DataFrame(data_only)
    tweet_data.insert(2, "language", lang_iso, True)
    json_lines = tweet_data.to_json(orient="records")
    return json_lines


def add_document_format(json_lines):
    docu_format = '"' + "documents" + '"'
    json_docu_format = "{}:{}".format(docu_format, json_lines)
    docu_align = "{" + json_docu_format + "}"
    jd_align = json.dumps(docu_align)
    jl_align = json.loads(jd_align)
    return ast.literal_eval(jl_align)


def sentiment_scores(headers, sentiment_url, document_format):
    response = requests.post(
        sentiment_url, headers=headers, json=document_format)
    return response.json()


def mean_score(sentiments):
    sentiment_df = pd.DataFrame(sentiments["documents"])
    return sentiment_df["score"].mean()


def week_logic(week_score):
    if week_score > 0.75 or week_score == 0.75:
        print("You had a positve week")
    elif week_score > 0.45 or week_score == 0.45:
        print("You had a neautral week")
    else:
        print("You had a negative week, I hope it gets better")

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
    data = process_yaml()
    bearer_token = create_bearer_token(data)
    res_json = twitter_auth_and_connect(bearer_token, create_twitter_url())
    print(pretty(res_json))

    # documents = lang_data_shape(res_json)
    # language_api_url, sentiment_url, subscription_key = connect_to_azure(data)
    # headers = azure_header(subscription_key)
    # with_languages = generate_languages(headers, language_api_url, documents)
    # json_lines = combine_lang_data(documents, with_languages)
    # document_format = add_document_format(json_lines)
    # sentiments = sentiment_scores(headers, sentiment_url, document_format)
    # week_score = mean_score(sentiments)
    # print(week_score)
    # week_logic(week_score)

    print()
    
    # Tweet object
    tweet_id = 'tweet1' # Either DB-generated index or from 
    tweet_url = create_twitter_url()
    text = res_json['data'][0]['text']
    user_handle = res_json['includes']['users'][0]['name']
    created_at = res_json['data'][0]['created_at']
    retweet_count = res_json['data'][0]['public_metrics']['retweet_count']
    reply_count = res_json['data'][0]['public_metrics']['reply_count']
    like_count = res_json['data'][0]['public_metrics']['like_count']
    # quote_count = res_json['data'][0]['public_metrics']['quote_count']
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
    time_period = (datetime.date.today() - datetime.date(int(created_at[0:4]), int(created_at[5:7]), int(created_at[8:10]))).days # In days
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

    # Perhaps sort subset of matching songs by popularity and choose most popular songs for virability?

if __name__ == "__main__":
    main()