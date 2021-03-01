-- CREATE DATABASE knights;
-- use knights;
--
-- CREATE TABLE favorite_colors (
--   movieID INT,
--   title VARCHAR(255)
-- );
--
-- LOAD DATA INFILE '/var/lib/mysql-files/test_movies_table.csv'
-- INTO TABLE favorite_colors
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- LINES TERMINATED BY '\n'
-- IGNORE 1 ROWS;
--
--
-- -- CREATE DATABASE moviesDB
-- -- use moviesDB
--
-- -- CREATE TABLE Movies_table (
-- --   movieId INT not null,
-- --   title VARCHAR(20) not null,
-- --   imdbId INT,
-- --   tmdbId INT,
-- --   PRIMARY KEY (movieId)
-- -- );
--
--
-- -- CREATE TABLE Movies_genre (
-- --   movieId INT not null,
-- --   genre VARCHAR(20) not null,
-- --   PRIMARY KEY (movieId, genre),
-- --   FOREIGN KEY (movieId)
-- -- );
--
--
-- -- CREATE TABLE Ratings (
-- --   movieId INT not null,
-- --   userId INT not null,
-- --   rating FLOAT not null,
-- --   PRIMARY KEY (movieId, userID),
-- --   FOREIGN KEY (movieId)
-- -- );
--
--
-- -- CREATE TABLE Tags (
-- --   tagId INT not null,
-- --   movieId INT not null,
-- --   userId INT not null,
-- --   tag VARCHAR(20) not null,
-- --   PRIMARY KEY (tagId),
-- --   FOREIGN KEY (movieId)
-- -- );
--
--
--
--

CREATE DATABASE movies_db;
use movies_db;

CREATE TABLE Movies_table (
  movieId INT not null,
  title VARCHAR(150) not null,
  imdbId INT default -1,
  tmdbId INT default -1,
  PRIMARY KEY (movieId)
);


CREATE TABLE Movies_genre (
  movieId INT not null,
  genre VARCHAR(20) not null,
  PRIMARY KEY (movieId, genre),
  FOREIGN KEY (movieId) REFERENCES Movies_table(movieId)
);


CREATE TABLE Ratings (
  movieId INT not null,
  userId INT not null,
  rating FLOAT not null,
  PRIMARY KEY (movieId, userID),
  FOREIGN KEY (movieId) REFERENCES Movies_table(movieId)
);


CREATE TABLE Tags (
  tagId INT not null,
  movieId INT not null,
  userId INT not null,
  tag VARCHAR(20) not null,
  PRIMARY KEY (tagId),
  FOREIGN KEY (movieId) REFERENCES Movies_table(movieId)
);



LOAD DATA INFILE '/var/lib/mysql-files/datasets/movies_table.csv'
INTO TABLE Movies_table
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


LOAD DATA INFILE '/var/lib/mysql-files/datasets/movies_genre.csv'
INTO TABLE Movies_genre
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


LOAD DATA INFILE '/var/lib/mysql-files/datasets/ratings.csv'
INTO TABLE Ratings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


LOAD DATA INFILE '/var/lib/mysql-files/datasets/tags.csv'
INTO TABLE Tags
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
