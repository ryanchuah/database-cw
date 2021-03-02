from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# cors settings needed to prevent CORS errors when testing on localhost
# this should be removed when we deploy to production servers
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'  

from typing import List, Dict
from flask import Flask
import mysql.connector
from mysql.connector import errorcode
import json

app = Flask(__name__)


def movies() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'movies_db'
    }
    results = None
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Movies")
        results = []
        for movieId, movieTitle, year, imdbId, tmdbId in cursor:
            results.append((movieId, movieTitle, year, imdbId, tmdbId))
        cursor.close()
        return results
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        connection.close()

    # connection = mysql.connector.connect(**config)
    # cursor = connection.cursor()
    # cursor.execute('SELECT * FROM Movies')
    # results = [{movieId: title} for (movieId, title, _, _) in cursor]
    # cursor.close()
    # connection.close()

    return results

@app.route("/")
@cross_origin()
def index():
    return json.dumps({'movies': movies()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)