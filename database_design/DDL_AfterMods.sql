DELETE FROM CreatedBy;
DELETE FROM AppUser;
DELETE FROM Playlist_Includes_Song;
DELETE FROM Song;
DELETE FROM Playlist;
DELETE FROM Tweet;

DROP TABLE IF EXISTS CreatedBy;
DROP TABLE IF EXISTS AppUser;

DROP TABLE IF EXISTS Tweeter;
DROP TABLE IF EXISTS Genre;

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
  DROP COLUMN duration_ms,
  DROP COLUMN energy,
  DROP COLUMN instrumentalness,
  DROP COLUMN liveness,
  DROP COLUMN loudness,
  DROP COLUMN speechiness,
  DROP COLUMN tempo,
  DROP COLUMN valence;

INSERT INTO Song
(
  song_id,
  song_uri
) VALUES 
(
  'song1',
  'http://song.com/'
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


CREATE TABLE Genre
(
  seed_genre VARCHAR(50),
  genre_name VARCHAR(50),
  PRIMARY KEY (seed_genre),
  UNIQUE (genre_name)
);

INSERT INTO Genre (seed_genre, genre_name) VALUES ('pop', 'Pop');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('country', 'Country');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('r-n-b', 'RnB');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('disney', 'Disney');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('turkish', 'Turkish');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('holidays', 'Holidays');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('anime', 'Anime');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('british', 'British');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('chicago-house', 'Chicago House');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('classical', 'Classical');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('emo', 'Emo');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('german', 'German');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('edm', 'EDM');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('gospel', 'Gospel');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('hip-hop', 'Hip-Hop');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('honky-tonk', 'Honky Tonk');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('indie-pop', 'Indie Pop');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('jazz', 'Jazz');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('k-pop', 'K-Pop');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('rock-n-roll', "Rock 'n Roll");
INSERT INTO Genre (seed_genre, genre_name) VALUES ('trance', 'Trance');
INSERT INTO Genre (seed_genre, genre_name) VALUES ('opera', 'Opera');