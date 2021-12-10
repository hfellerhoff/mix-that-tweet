DROP TABLE IF EXISTS CreatedBy;
DROP TABLE IF EXISTS AppUser;
DROP TABLE IF EXISTS Include;
DROP TABLE IF EXISTS Song;
DROP TABLE IF EXISTS Playlist;
DROP TABLE IF EXISTS Tweet;

CREATE TABLE Tweet
(
  tweet_id VARCHAR(50) NOT NULL,
  tweet_url VARCHAR(50) NOT NULL,
  author_id VARCHAR(50) NOT NULL,
  tweet_created_at DATE NOT NULL,
  tweet_text VARCHAR(280) NOT NULL,
  retweet_count INT(25) NOT NULL,
  reply_count INT(25) NOT NULL,
  like_count INT(25) NOT NULL,
  quote_count INT(25) NOT NULL,
  positive_sentiment_score FLOAT(25) NOT NULL,
  neutral_sentiment_score FLOAT(25) NOT NULL,
  negative_sentiment_score FLOAT(25) NOT NULL,
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
  acousticness FLOAT(25) NOT NULL,
  danceability FLOAT(25) NOT NULL,
  duration_ms INT(25) NOT NULL,
  energy FLOAT(25) NOT NULL,
  instrumentalness FLOAT(25) NOT NULL,
  liveness FLOAT(25) NOT NULL,
  loudness FLOAT(25) NOT NULL,
  speechiness FLOAT(25) NOT NULL,
  tempo FLOAT(25) NOT NULL,
  valence FLOAT(25) NOT NULL,
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
