-- CREATE DATABASE knights;
-- use knights;

-- CREATE TABLE favorite_colors (
--   name VARCHAR(20),
--   color VARCHAR(10)
-- );

-- INSERT INTO favorite_colors
--   (name, color)
-- VALUES
--   ('Zahra', 'blue'),
--   ('Chak', 'yellow');


CREATE DATABASE moviesDB
use moviesDB

CREATE TABLE Movies_table (
  movieId INT not null,
  title VARCHAR(20) not null,
  imdbId INT,
  tmdbId INT,
  PRIMARY KEY (movieId)
);


CREATE TABLE Movies_genre (
  movieId INT not null,
  genre VARCHAR(20) not null,
  PRIMARY KEY (movieId, genre),
  FOREIGN KEY (movieId)
);


CREATE TABLE Ratings (
  movieId INT not null,
  userId INT not null,
  rating FLOAT not null,
  PRIMARY KEY (movieId, userID),
  FOREIGN KEY (movieId)
);


CREATE TABLE Tags (
  tagId INT not null,
  movieId INT not null,
  userId INT not null,
  tag VARCHAR(20) not null,
  PRIMARY KEY (tagId),
  FOREIGN KEY (movieId)
);




