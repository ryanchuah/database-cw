CREATE DATABASE knights;
use knights;

CREATE TABLE favorite_colors (
  name VARCHAR(20),
  color VARCHAR(10)
);

INSERT INTO favorite_colors
  (name, color)
VALUES
  ('Zahra', 'blue'),
  ('Chak', 'yellow');