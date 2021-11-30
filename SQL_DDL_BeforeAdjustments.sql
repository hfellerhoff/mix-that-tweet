DROP TABLE IF EXISTS CreatedBy CASCADE;
DROP TABLE IF EXISTS AppUser CASCADE;
DROP TABLE IF EXISTS Include CASCADE;
DROP TABLE IF EXISTS Song CASCADE;
DROP TABLE IF EXISTS Playlist CASCADE;
DROP TABLE IF EXISTS Tweet CASCADE;

CREATE TABLE Tweet
(
  tweet_id VARCHAR(50) NOT NULL,
  tweet_url VARCHAR(50) NOT NULL,
  user_handle VARCHAR(50) NOT NULL,
  created_at DATE NOT NULL,
  impression_count INT(50) NOT NULL,
  like_count INT(50) NOT NULL,
  reply_count INT(50) NOT NULL,
  retweet_count INT(50) NOT NULL,
  url_link_clicks INT(50) NOT NULL,
  user_profile_clicks INT(50) NOT NULL,
  positive_sentiment_percentage FLOAT(50) NOT NULL,
  neutral_sentiment_percentage FLOAT(50) NOT NULL,
  negative_sentiment_percentage FLOAT(50) NOT NULL,
  PRIMARY KEY (tweet_id),
  UNIQUE (tweet_url)
);

CREATE TABLE Playlist
(
  playlist_id VARCHAR(50) NOT NULL,
  playlist_uri VARCHAR(50) NOT NULL,
  tweet_id VARCHAR(50) NOT NULL,
  PRIMARY KEY (playlist_id),
  FOREIGN KEY (tweet_id) REFERENCES Tweet(tweet_id),
  UNIQUE (playlist_uri)
);

CREATE TABLE Song
(
  song_id VARCHAR(50) NOT NULL,
  song_uri VARCHAR(50) NOT NULL,
  acousticness FLOAT(50) NOT NULL,
  danceability FLOAT(50) NOT NULL,
  duration_ms INT(50) NOT NULL,
  energy FLOAT(50) NOT NULL,
  instrumentalness FLOAT(50) NOT NULL,
  liveness FLOAT(50) NOT NULL,
  loudness FLOAT(50) NOT NULL,
  speechiness FLOAT(50) NOT NULL,
  tempo FLOAT(50) NOT NULL,
  valence FLOAT(50) NOT NULL,
  PRIMARY KEY (song_id),
  UNIQUE (song_uri)
);

CREATE TABLE Include
(
  playlist_id VARCHAR(50) NOT NULL,
  song_id VARCHAR(50) NOT NULL,
  PRIMARY KEY (playlist_id, song_id),
  FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
  FOREIGN KEY (song_id) REFERENCES Song(song_id)
);

CREATE TABLE AppUser
(
  AppUser_id VARCHAR(50) NOT NULL,
  AppUsername VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  PRIMARY KEY (AppUser_id),
  UNIQUE (AppUsername)
);

CREATE TABLE CreatedBy
(
  playlist_id VARCHAR(50) NOT NULL,
  AppUser_id VARCHAR(50) NOT NULL,
  PRIMARY KEY (playlist_id, AppUser_id),
  FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
  FOREIGN KEY (AppUser_id) REFERENCES AppUser(AppUser_id)
);
