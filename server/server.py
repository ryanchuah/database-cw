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
        connection.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
