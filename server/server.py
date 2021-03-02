from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# cors settings needed to prevent CORS errors when testing on localhost
# this should be removed when we deploy to production servers
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'  

from typing import List, Dict
from flask import render_template
import mysql.connector
from mysql.connector import errorcode
import json

app = Flask(__name__)


config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'movies_db'
    }


def _get_all_movies() -> List[Dict]:
    # Creating a connection cursor
    results = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Movies')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def _get_movies_by_requirements(search_criteria, limit) -> List[Dict]:
    # Creating a connection cursor
    results = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Movies '
                   'WHERE title CONTAINS \'' + search_criteria +
                   '\' ORDER BY movieId ' +
                   ' LIMIT ' + limit)
    results = [{movieId: title} for (movieId, title) in cursor]
    cursor.close()
    connection.close()
    return results


def _get_movie_name(movieId):
    # Creating a connection cursor
    results = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Movies '
                   'WHERE movieId = ' + movieId)
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    return results


def _get_movie_genres(movieId):
    # Creating a connection cursor
    results = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Movies '
                   'WHERE movieId = ' + movieId)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def _get_average_movie_rating(movieId):
    # Creating a connection cursor
    results = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT AVG(IF movieId = ' + movieId +  ') FROM Ratings ')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results






@app.route("/")
@cross_origin()
def index():
    movies = _get_all_movies()
    return json.dumps({'movies': _get_all_movies()})


@app.route("/search/<search_criteria>/<limit>")
def searchMovies(search_criteria, limit):
    return json.dumps({'movies': server._get_movies_by_requirements(search_criteria, limit)})


@app.route('/movies/<movie_id>')
def movie_details(movie_id):
    name = server._get_movie_name(movie_id)
    genres = server._get_movie_genres(movie_id)
    rating = _get_average_movie_rating(movie_id)
    return name, genres, rating


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)