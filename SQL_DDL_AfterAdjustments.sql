DELETE FROM CreatedBy;
DELETE FROM AppUser;
DELETE FROM Include;
DELETE FROM Song;
DELETE FROM Playlist;
DELETE FROM Tweet;

DROP TABLE CreatedBy;
DROP TABLE AppUser;

INSERT INTO Tweet
(
  tweet_id,
  tweet_url,
  user_handle,
  created_at,
  impression_count,
  like_count,
  reply_count,
  retweet_count,
  url_link_clicks,
  user_profile_clicks,
  positive_sentiment_percentage,
  neutral_sentiment_percentage,
  negative_sentiment_percentage
) VALUES
(
  't1',
  'http://tweet.com/',
  'someguy',
  '2021-11-29',
  1,
  1,
  1,
  1,
  1,
  1,
  0.33,
  0.33,
  0.33
);

INSERT INTO Playlist
(
  playlist_id,
  playlist_uri,
  tweet_id
) VALUES 
(
  'p1',
  'http://tweet.com/',
  't1'
);

INSERT INTO Song
(
  song_id,
  song_uri,
  acousticness,
  danceability,
  duration_ms,
  energy,
  instrumentalness,
  liveness,
  loudness,
  speechiness,
  tempo,
  valence
) VALUES 
(
  's1',
  'http://song.com/',
  0.2,
  0.2,
  123,
  0.2,
  0.2,
  0.2,
  0.2,
  0.2,
  0.2,
  0.2
);

INSERT INTO Include
(
  playlist_id,
  song_id
) VALUES
(
  'p1',
  's1'
);
