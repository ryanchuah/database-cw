import json
from mysql.connector import errorcode
import mysql.connector
from flask import Flask
from typing import List, Dict
from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# cors settings needed to prevent CORS errors when testing on localhost
# this should be removed when we deploy to production servers
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

<<<<<<< HEAD
from typing import List, Dict
from flask import Flask, abort
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

def movies() -> List[Dict]:
    results = []
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Movies")
        for movieId, movieTitle, year, imdbId, tmdbId in cursor:
            results.append((movieId, movieTitle, year, imdbId, tmdbId))
=======

app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'movies_db'
}


@app.route("/")
@cross_origin()
def index():
    sortBy = request.args.get('sortBy')
    Movies_columns = ['movieId', 'title', 'imdbId', 'tmdbId']

    if sortBy and sortBy not in Movies_columns:
        sortBy = None
        raise ValueError(
            f"the request query sortby={sortBy} is not recognized. Either developer error, or SQL injection attempt")

    limit = request.args.get('limit')
    if limit:
        try:
            limit = int(limit)
        except ValueError:
            raise ValueError(
                f"the request query limit={limit} is not recognized. Either developer error, or SQL injection attempt")
    else:
        limit = 10
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        if sortBy:
            query = (f"SELECT * FROM Movies ORDER BY {sortBy} LIMIT %s")
            cursor.execute(query, (limit,))
        else:
            query = ("SELECT * FROM Movies LIMIT %s")
            cursor.execute(query, (limit,))

        movies = []
        for movieId, movieTitle, imdbId, tmdbId in cursor:
            movies.append({'movieId': movieId, 'movieTitle': movieTitle,
                           'imdbId': imdbId, 'tmdbId': tmdbId})
>>>>>>> f2098243085cb16b5a885e6aaad99bf1a63bd42a
        cursor.close()
        return {"movies": movies}
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cursor.close()
        connection.close()
    return results

def popular(start, end)-> List[Dict]:
    result = []
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        nRows = end - start + 1
        # command = "SELECT movies.title, movies.release_year, "
        # "Sum(rating) as total_ratings, Count(rating) as votes, Avg(rating) as avg_ratings" 
        # "FROM ratings, movies"
        # "WHERE ratings.movieId = movies.movieId" 
        # "GROUP BY ratings.movieId"
        # "ORDER BY total_ratings DESC"
        # "LIMIT" + str(nRows) + "OFFSET" + str(start - 1) + ";"
        command = "SELECT Movies.title, Movies.release_year, Sum(Ratings.rating) as total_ratings, Count(Ratings.rating) as votes, Avg(Ratings.rating) as avg_ratings FROM Ratings, Movies WHERE Ratings.movieId = Movies.movieId GROUP BY Ratings.movieId ORDER BY total_ratings DESC LIMIT " + str(nRows) + " OFFSET " + str(start - 1)
        cursor.execute(command)
        result = [{"title" : title, "release_year" : release_year, "votes": votes, "avg_ratings":avg_ratings} 
                   for title, release_year, total_ratings, votes, avg_ratings in cursor]
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            abort(500, "Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            abort(500  ,"Database does not exist")
        else:
            abort(500, err)
    finally:
        cursor.close()
        connection.close()

<<<<<<< HEAD
    return result



@app.route("/")
@cross_origin()
def index():
    return json.dumps({'movies': movies()})
=======
>>>>>>> f2098243085cb16b5a885e6aaad99bf1a63bd42a

# returns the start_th to the end_th most popular movies inclusive
# requirements => start and end are both ints, start <= end, start >= 1 and end >= 1
@app.route("/popular/<int:start>/<int:end>")
def getMostPopular(start, end):
    if start < 1 or end < 1 or start > end: abort(400)
    return json.dumps({'most_popular' : popular(start, end)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
