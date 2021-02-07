CREATE DATABASE knights;
use knights;

CREATE TABLE favorite_colors (
  movieID INT,
  title VARCHAR(255)
);

-- INSERT INTO favorite_colors
--   (name, color)
-- VALUES
--   ('Zahra', 'blue'),
--   ('Chak', 'yellow');

LOAD DATA INFILE '/var/lib/mysql-files/test_movies_table.csv' 
INTO TABLE favorite_colors 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
