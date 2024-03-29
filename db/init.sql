-- CREATE DATABASE movies_db;
use movies_db;

CREATE TABLE Movies (
  movieId INT not null,
  title VARCHAR(200) not null,
  imdbId INT default -1,
  tmdbId INT default -1,
  release_year INT default -1,
  poster_url VARCHAR(35),
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
  genres VARCHAR(20) not null,
  PRIMARY KEY (movieId, genres),
  FOREIGN KEY (movieId) REFERENCES Movies(movieId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Genres.csv'
INTO TABLE Genres
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


CREATE TABLE Users (
  userId INT not null,
  PRIMARY KEY (userId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Users.csv'
INTO TABLE Users
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


CREATE TABLE Ratings (
  userId INT not null,
  movieId INT not null,
  rating FLOAT not null,
  timestamp DATETIME not null,
  PRIMARY KEY (movieId, userID, timestamp),
  FOREIGN KEY (movieId) REFERENCES Movies(movieId),
  FOREIGN KEY (userId) REFERENCES Users(userId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Ratings.csv'
INTO TABLE Ratings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE Tags (
  userId INT not null,
  movieId INT not null,
  tag VARCHAR(100) not null,
  timestamp DATETIME not null,
  PRIMARY KEY (userId, movieId, tag),
  FOREIGN KEY (movieId) REFERENCES Movies(movieId),
  FOREIGN KEY (userId) REFERENCES Users(userId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Tags.csv'
INTO TABLE Tags
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


CREATE TABLE Actors (
  actorId VARCHAR(40) not null,
  actorName VARCHAR(255) not null,
  PRIMARY KEY (actorId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Actors.csv'
INTO TABLE Actors
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE Actor_Roles (
  actorId VARCHAR(40) not null,
  movieId INT not null,
  PRIMARY KEY (actorId, movieId),
  FOREIGN KEY (movieId) REFERENCES Movies(movieId),
  FOREIGN KEY (actorId) REFERENCES Actors(actorId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/Actor_Roles.csv'
INTO TABLE Actor_Roles
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


CREATE TABLE Personality_Attributes_table (
  hashed_userId VARCHAR(40) not null,
  openness FLOAT,
  agreeableness FLOAT,
  emotional_stability FLOAT,
  conscientiousness FLOAT,
  extraversion FLOAT,
  PRIMARY KEY (hashed_userId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/user_personalities.csv'
INTO TABLE Personality_Attributes_table
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

CREATE TABLE Personality_Ratings_table (
  hashed_userId VARCHAR(40) not null,
  movieId INT not null,
  predicted_rating FLOAT not null,
  PRIMARY KEY (hashed_userId, movieId),
  FOREIGN KEY (hashed_userId) REFERENCES Personality_Attributes_table(hashed_userId)
);

LOAD DATA INFILE '/var/lib/mysql-files/datasets/hashedUserId_movieid_ratings.csv'
INTO TABLE Personality_Ratings_table
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;









