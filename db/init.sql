CREATE DATABASE movies_db;
use movies_db;

CREATE TABLE Movies (
  movieId INT not null,
  title VARCHAR(200) not null,
  imdbId INT default -1,
  tmdbId INT default -1,
  PRIMARY KEY (movieId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Movies.csv'
INTO TABLE Movies
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE Genres (
  movieId INT not null,
  genre VARCHAR(20) not null,
  PRIMARY KEY (movieId, genre),
  FOREIGN KEY (movieId) REFERENCES Movies(movieId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Genres.csv'
INTO TABLE Genres
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE Ratings (
  userId INT not null,
  movieId INT not null,
  rating FLOAT not null,
  PRIMARY KEY (movieId, userID),
  FOREIGN KEY (movieId) REFERENCES Movies(movieId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Ratings.csv'
INTO TABLE Ratings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE Tags (
  tagId INT not null,
  userId INT not null,
  movieId INT not null,
  tag VARCHAR(100) not null,
  PRIMARY KEY (tagId),
  FOREIGN KEY (movieId) REFERENCES Movies(movieId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Tags.csv'
INTO TABLE Tags
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
