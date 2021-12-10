from tweet_analysis import analyzeTweet
link = "https://twitter.com/FarhangNamdar/status/1230554753182003203?ref_src=twsrc%5Etfw"
tweet_insert_ddl, tweeter_insert_ddl, tweet_to_audiofeatures_map = analyzeTweet(link)
print('\nTweet SQL insertion DDL:\n', tweeter_insert_ddl)
print('\nTweeter SQL insertion DDL:\n', tweeter_insert_ddl)
print('\nTweet to Audio Features mapping:\n', tweet_to_audiofeatures_map)