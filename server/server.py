import json
from mysql.connector import errorcode
import mysql.connector
from flask import Flask
from typing import List, Dict
from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# cors settings needed to prevent CORS errors when testing on localhost
# this should be removed when we deploy to production servers
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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
        for movie in cursor:
            movies.append({'movieId': movie[0], 'movieTitle': movie[1],
                           'imdbId': movie[2], 'tmdbId': movie[3]})
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

def query(start, end, command, get_result) -> List[Dict]:
    result = []
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(command)
        result = get_result(cursor)
    except mysql.connector.Error as err:
            abort(500, err)
    finally:
        cursor.close()
        connection.close()
    return result

def get_popularity_result(cursor):
    return [{"title": title, "release_year": release_year, "votes": votes, "avg_ratings": avg_ratings}
            for title, release_year, total_ratings, votes, avg_ratings in cursor]

def get_polarity_result(cursor):
    return [{"title" : title, "release_year" : release_year, "polarity_index":polarity_index} 
             for title, release_year, polarity_index in cursor]

def check_popular_input():
    start = None
    end = None
    try:
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        if start < 1 or end < 1 or start > end: abort(400)
    except ValueError as e:
        abort(400, e)
        
    return start, end

# returns the start_th to the end_th most popular movies inclusive
# requirements => start and end are both ints, start <= end, start >= 1 and end >= 1
@app.route("/popular")
def get_most_popular():
    start, end = check_popular_input()
    nRows = end - start + 1
    command = "SELECT Movies.title, Movies.release_year, Sum(Ratings.rating) as total_ratings, Count(Ratings.rating) as votes, Avg(Ratings.rating) as avg_ratings FROM Ratings, Movies WHERE Ratings.movieId = Movies.movieId GROUP BY Ratings.movieId ORDER BY total_ratings DESC LIMIT " + str( nRows) + " OFFSET " + str(start - 1)
    return json.dumps({'most_popular' : query(start, end, command, get_popularity_result)})

# returns the start_th to the end_th most polar movies inclusive
# requirements => start and end are both ints, start <= end, start >= 1 and end >= 1
@app.route("/polarity")
def get_most_polarising():
    start, end = check_popular_input()
    nRows = end - start + 1
    command = "SELECT Movies.title, Movies.release_year, VARIANCE(Ratings.rating) as polarity_index FROM Ratings, Movies WHERE Ratings.movieId = Movies.movieId GROUP BY Ratings.movieId ORDER BY polarity_index DESC LIMIT " + str(nRows) + " OFFSET " + str(start - 1)
    return json.dumps({'most_polarising' : query(start, end, command, get_polarity_result)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)