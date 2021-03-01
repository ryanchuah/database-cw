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
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Movies_table')
    results = [{movieId: title} for (movieId, title) in cursor]
    cursor.close()
    connection.close()

    return results

@app.route("/")
@cross_origin()
def index():
    return json.dumps({'movies': movies()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)