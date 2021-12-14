DELETE FROM CreatedBy;
DELETE FROM AppUser;
DELETE FROM Playlist_Includes_Song;
DELETE FROM Song;
DELETE FROM Playlist;
DELETE FROM Tweet;

DROP TABLE CreatedBy;
DROP TABLE AppUser;

DROP TABLE IF EXISTS Tweeter;

CREATE TABLE Tweeter
(
  tweeter_id VARCHAR(50) NOT NULL,
  tweeter_name VARCHAR(50) NOT NULL,
  tweeter_username VARCHAR(50) NOT NULL,
  tweeter_created_at DATE NOT NULL,
  followers_count INT(25) NOT NULL,
  following_count INT(25) NOT NULL,
  tweet_count INT(25) NOT NULL,
  listed_count INT(25) NOT NULL,
  PRIMARY KEY (tweeter_id),
  UNIQUE (tweeter_username)
);

INSERT INTO Tweeter
(
  tweeter_id,
  tweeter_name,
  tweeter_username,
  tweeter_created_at,
  followers_count,
  following_count,
  tweet_count,
  listed_count
) VALUES
(
  'tweeter1',
  'T. Weeter',
  'reteewt',
  '2021-12-10',
  1,
  1,
  1,
  1
);

ALTER TABLE Tweet ADD FOREIGN KEY (author_id) REFERENCES Tweeter(tweeter_id);

INSERT INTO Tweet
(
  tweet_id,
  tweet_url,
  author_id,
  tweet_created_at,
  tweet_text,
  retweet_count,
  reply_count,
  like_count,
  quote_count,
  positive_sentiment_score,
  neutral_sentiment_score,
  negative_sentiment_score
) VALUES
(
  'tweet1',
  'http://twitter.com/',
  'tweeter1',
  '2021-11-29',
  "It's ya boy uhhhhhh skinny _____.",
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
  'playlist1',
  'http://playlist.com/',
  'tweet1'
);

ALTER TABLE Song 
  DROP COLUMN acousticness, 
  DROP COLUMN danceability,
  DROP COLUMN energy,
  DROP COLUMN instrumentalness,
  DROP COLUMN liveness,
  DROP COLUMN loudness,
  DROP COLUMN speechiness,
  DROP COLUMN tempo,
  DROP COLUMN valence;
  DROP COLUMN duration_ms;

INSERT INTO Song
(
  song_id,
  song_uri,
  duration_ms
) VALUES 
(
  'song1',
  'http://song.com/',
  123
);

INSERT INTO Playlist_Includes_Song
(
  playlist_id,
  song_id
) VALUES
(
  'playlist1',
  'song1'
);
