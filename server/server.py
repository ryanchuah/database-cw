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

@app.route("/search")
def search_movies():
    sortBy = request.args.get('sortBy')

    Movies_columns = ['movieId', 'title', 'imdbId', 'tmdbId']
    search_criteria = request.args.get('search_criteria')

    if sortBy not in Movies_columns:
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
        if not sortBy == None:
            query = ("SELECT * FROM Movies WHERE title like \'%{search_criteria}%\' ORDER BY {sortBy} LIMIT {limit}")
            cursor.execute(query)
        else:
            query = ("SELECT * FROM Movies WHERE title like \'%{search_criteria}%\' LIMIT {limit}")
            cursor.execute(query)
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


@app.route('/movies')
def movie_details():
    movie_id = request.args.get('movie_id')
    try:
        movie_id = int(request.args.get('movie_id'))
    except ValueError as e:
        abort(400, e)

    result = []
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = "SELECT title, release_year, poster_url FROM Movies WHERE Movies.movieId = %s"
        cursor.execute(query, (movie_id,))
        result = [{"title": title, "release_year": release_year, "poster_url": poster_url}
                  for title, release_year, poster_url in cursor]

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            abort(500, "Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            abort(500, "Database does not exist")
        else:
            abort(500, err)
    finally:
        cursor.close()
        connection.close()
    print(result)

    return result

# returns the start_th to the end_th most popular movies inclusive
# requirements => start and end are both ints, start <= end, start >= 1 and end >= 1
#EXAMPLE: http://0.0.0.0:5000/popular?start=1&end=10
@app.route("/popular")
def get_most_popular():
    start, end = check_popular_input()
    holders = end - start + 1 , start - 1
    command = '''SELECT Movies.movieId, Movies.title, Movies.release_year, Sum(Ratings.rating) as total_ratings, 
                 Count(Ratings.rating) as votes, Avg(Ratings.rating) as avg_ratings 
                 FROM Ratings, Movies 
                 WHERE Ratings.movieId = Movies.movieId 
                 GROUP BY Ratings.movieId 
                 ORDER BY total_ratings DESC 
                 LIMIT %s OFFSET %s'''
    return json.dumps({'most_popular' : query(command, holders, popularity_result)})

# returns the start_th to the end_th most polar movies inclusive
# requirements => start and end are both ints, start <= end, start >= 1 and end >= 1
#EXAMPLE: http://0.0.0.0:5000/polarity?start=1&end=10
@app.route("/polarity")
def get_most_polarising():
    start, end = check_popular_input()
    holders = end - start + 1 , start - 1
    command = '''SELECT Movies.movieId, Movies.title, Movies.release_year, 
                 VARIANCE(Ratings.rating) as polarity_index 
                 FROM Ratings, Movies 
                 WHERE Ratings.movieId = Movies.movieId 
                 GROUP BY Ratings.movieId 
                 ORDER BY polarity_index DESC 
                 LIMIT %s OFFSET %s'''
    return json.dumps({'most_polarising' : query(command, holders, polarity_result)})

#PARAM: a list of genres [x, y, z...]
#Returns a list of genres [a, b...] each associated with the propotion of users that like [x,y,z]
#Can display 'd% of users that like x,y,z also like a'
#            'd% of users that like x,y,z also like b' etc..
#EXAMPLE: http://localhost:5000/similar_genres?genre=Animation&genre=Adventure
@app.route("/similar_genres")
def get_similar_genres():
    genres = tuple(request.args.getlist('genre', type=str))
    condition = create_condition(genres)
    nUsers = get_interested_users(condition, genres)
    return json.dumps({'similar_genres' : similar_genres(nUsers, condition, genres)})


def query(command, holders, get_result):
    result = None
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute(command, (holders))
        result = get_result(cursor)
    except mysql.connector.Error as err:
            abort(500, err)
    finally:
        cursor.close()
        connection.close()
    return result


def extract_genres(cursor):
    return [{"genres": genres, "proportion": float(proportion)} for genres, proportion in cursor]

def popularity_result(cursor):
    return [{"movieId": movieId, "title": title, "release_year": release_year, "votes": votes, "avg_ratings": avg_ratings}
            for movieId, title, release_year, total_ratings, votes, avg_ratings in cursor]


def polarity_result(cursor):
    return [{"movieId": movieId, "title" : title, "release_year" : release_year, "polarity_index":polarity_index} 
             for movieId, title, release_year, polarity_index in cursor]

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


def similar_genres(nUsers, condition, genres):
    having_condition = create_condition(genres, col='genres')
    command = f'''SELECT genres, count(genres) / {nUsers} as proportion
                FROM (SELECT  Genres.genres as genres
                    FROM Ratings, Movies, Genres,
                        (SELECT  DISTINCT Ratings.userId as uniqueUsers
                        FROM Genres, Ratings, Movies
                        WHERE Ratings.rating > 3 
                        and Ratings.movieId = Movies.movieId
                        and Movies.movieId = Genres.movieId
                        and {condition}
                        ) as userSpace
                    WHERE Ratings.rating > 3 
                    and userSpace.uniqueUsers = Ratings.userId
                    and Ratings.movieId = Movies.movieId
                    and Movies.movieId = Genres.movieId
                    GROUP BY Ratings.userId, Genres.genres
                    ) as genreSets
                GROUP BY genres
                HAVING NOT {having_condition}
                ORDER BY proportion DESC'''
    return query(command, genres + genres, extract_genres)
    

def get_interested_users(condition, genres):
    command = f'''SELECT  COUNT(DISTINCT Ratings.userId) as interested_user 
                  FROM Genres, Ratings, Movies 
                  WHERE Ratings.rating > 3 and Ratings.movieId = Movies.movieId 
                  and Movies.movieId = Genres.movieId and {condition}'''
    return query(command, genres, lambda cursor : cursor.fetchone()[0])

def create_condition(genres, col='Genres.genres'):
    result = '('
    for i in range(len(genres)):
        result += f'{col} = %s'
        if i != len(genres) - 1: result += ' or '
    return result + ')'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)