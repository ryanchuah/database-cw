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


@app.route('/movies/<movie_id>')
@cross_origin()
def single_movie(movie_id):
    #TODO: Add in poster and language and actors when tavles created
    holders = movie_id,
    details_command = '''SELECT Movies.title, Movies.release_year, Avg(Ratings.rating) as avg_ratings
                 FROM Ratings, Movies
                 WHERE Movies.movieId = %s AND Ratings.movieId = Movies.movieId
                 '''

    genre_command = '''SELECT genres FROM Genres
                 WHERE Genres.movieId = %s'''

    actors_command = '''SELECT actorName
                        FROM Actors, Actor_Roles
                        WHERE Actors.actorId = Actor_Roles.actorId AND Actor_Roles.movieId = %s'''


    tags_command = '''SELECT tag, COUNT(tag) AS occurence
                      FROM Tags
                      WHERE Tags.movieId = %s
                      GROUP BY tag
                      ORDER BY occurence DESC 
                      LIMIT 3
                      '''

    ratings_date_command = '''SELECT Ratings.rating, Ratings.timestamp
                      FROM Ratings, Movies
                      WHERE Ratings.movieId = %s = Movies.movieId AND (extract(YEAR from timestamp) < Movies.release_year + 2) 
                      ORDER BY timestamp ASC
                      '''

    ratings_percentage_command = '''SELECT rating, COUNT(rating) AS occurence
                      FROM Ratings
                      WHERE Ratings.movieId = %s
                      GROUP BY rating
                      ORDER BY rating ASC
                 '''


    movie_details = {'details': query(details_command, holders, individual_movie_result),
                     'genres': query(genre_command, holders, genres_movie_result),
                     'actors': query(actors_command, holders, actors_movie_result),
                     'tags': query(tags_command, holders, tags_movie_result),
                     'ratings_date': query(ratings_date_command, holders, ratings_date_movie_result),
                     'ratings_percentage': query(ratings_percentage_command, holders, ratings_percentage_movie_result)}

    # print(movie_details)
    # return "individual movie page data will be returned here for movieid: "+movie_id
    return movie_details

@app.route('/movies')
@cross_origin()
def movies():

    sortBy = request.args.get('sortBy')
    limit = request.args.get('limit')
    page = request.args.get('page')
    limit = int(limit)
    page = int(page)
    print(sortBy)
    if sortBy == 'popularity':
        return get_most_popular(limit, page)
    elif sortBy == 'polarity':
        return get_most_polarising(limit, page)
    elif sortBy == 'column':
        column = request.args.get('column')
        return get_sorted_by_column(limit, page, column)
    else:
        print("sortBy= ", sortBy + " not recognized")

# returns the start_th to the end_th most popular movies inclusive
# requirements => start and end are both ints, start <= end, start >= 1 and end >= 1
# EXAMPLE: http://0.0.0.0:5000/popular?start=1&end=10
# @app.route("/popular")


def get_most_popular(limit, page):
    start = limit * page - (limit-1)
    end = limit * page
    holders = end - start + 1, start - 1
    command = '''SELECT Movies.movieId, Movies.title, Movies.release_year, Sum(Ratings.rating) as total_ratings, 
                 Count(Ratings.rating) as votes, Avg(Ratings.rating) as avg_ratings 
                 FROM Ratings, Movies 
                 WHERE Ratings.movieId = Movies.movieId 
                 GROUP BY Ratings.movieId 
                 ORDER BY total_ratings DESC 
                 LIMIT %s OFFSET %s'''
    return {'movies': query(command, holders, popularity_result)}

# returns the start_th to the end_th most polar movies inclusive
# requirements => start and end are both ints, start <= end, start >= 1 and end >= 1
# EXAMPLE: http://0.0.0.0:5000/polarity?start=1&end=10


def get_most_polarising(limit, page):
    start = limit * page - (limit-1)
    end = limit * page
    holders = end - start + 1, start - 1
    command = '''SELECT Movies.movieId, Movies.title, Movies.release_year, 
                 VARIANCE(Ratings.rating) as polarity_index 
                 FROM Ratings, Movies 
                 WHERE Ratings.movieId = Movies.movieId 
                 GROUP BY Ratings.movieId 
                 ORDER BY polarity_index DESC 
                 LIMIT %s OFFSET %s'''
    return {'movies': query(command, holders, polarity_result)}


def get_sorted_by_column(limit, page, column):
    Movies_columns = ['movieId', 'title', 'imdbId', 'tmdbId']

    if column not in Movies_columns:
        column = None
        raise ValueError(
            f"the request query column={column} is not recognized. Either developer error, or SQL injection attempt")

    start = limit * page - (limit-1)
    end = limit * page

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = '''SELECT Movies.movieId, Movies.title, Movies.release_year, Sum(Ratings.rating) as total_ratings, 
                 Count(Ratings.rating) as votes, Avg(Ratings.rating) as avg_ratings 
                 FROM Ratings, Movies 
                 WHERE Ratings.movieId = Movies.movieId 
                 GROUP BY Ratings.movieId 
                 ORDER BY ''' + column + ' ASC LIMIT %s OFFSET %s'
        cursor.execute(query, (end - start + 1, start - 1))

        movies = [{"movieId": movieId, "title": title, "release_year": release_year, "votes": votes, "avg_ratings": round(avg_ratings, 2)}
                  for movieId, title, release_year, total_ratings, votes, avg_ratings in cursor]

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
            query = (
                "SELECT * FROM Movies WHERE title like \'%{search_criteria}%\' ORDER BY {sortBy} LIMIT {limit}")
            cursor.execute(query)
        else:
            query = (
                "SELECT * FROM Movies WHERE title like \'%{search_criteria}%\' LIMIT {limit}")
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


# PARAM: a movieId
# Returns a list of genres [a, b...] each associated with a proportion
# of users that like this movie and that genre
# Can display 'd% of users that like Toy story also like genre a'
#             'c% of users that like avengers also like genere b' etc..
#EXAMPLE: http://localhost:5000/similar_genres?movieId=3
@app.route("/similar_genres")
def get_similar_genres():
    movieId = int(request.args.get('movieId', type=int))
    if not movieId: abort(400, 'Please use \'movieId\' as param')
    genre_command = '''SELECT genres FROM Genres WHERE Genres.movieId = %s'''
    holders = movieId,
    genres = query(genre_command, holders, genres_movie_result)
    if not genres: return {'similar_genres' : 'no genres'}
    condition = create_condition(genres)
    nUsers = get_nUsers(condition, genres)
    return {'similar_genres': similar_genres(nUsers, condition, genres)}


# PARAM: a movieId
# Returns a list of genres [a, b...] each associated with a proportion
# of users that have used this movie's tags and like that genre.
# Also returns this movie's tags
#Can display 'd% of users that used tags x,y,z also like genre a'
#            'c% of users that used tags x,y,z also like genre b' etc..
#Example: http://localhost:5000/similar_tags?movieId=1
@app.route("/similar_tags")
def get_tagged_genres():
    movieId = int(request.args.get('movieId', type=int))
    if not movieId: abort(400, 'Please use \'movieId\' as param')
    tags_command = '''SELECT tag, COUNT(tag) AS occurence
                      FROM Tags
                      WHERE Tags.movieId = %s
                      GROUP BY tag
                      ORDER BY occurence DESC
                      '''
    holders = movieId,
    tags_dict = query(tags_command, holders, tags_movie_result)
    tags = [element['tag'] for element in tags_dict]
    condition = create_condition(tags, col='Tags.tag')
    nUsers = get_users_with_tags(condition, tags)
    return {'similar_genres': tagged_genres(nUsers, condition, tags), "tags": tags_dict}


@app.route("/predict_rating")
def predict_ratings():
    # get tags from front end
    responses = request.args.getlist('responses')

    tag_sum = 0
    tag_count = 0
    rating_sum = 0
    rating_count = 0

    for response in responses:
        userId = response[0]
        tags = response[1]
        rating = response[2]

        #get predicted rating from tags
        for tag in tags:
            holders = tag,
            tags_average_command = '''SELECT avg(Rating) as average_rating
                                FROM Rating, Tags
                                WHERE Rating.movieId = Tag.MovieId AND Tags.tag = %s'''
            tag_sum += int(query(tags_average_command, holders, tags_average_result()))
            tag_count += 1

        #find other movies with same rating from user x and and average their rating - average those
        holders = userId, rating,
        user_rating_average_command = '''SELECT avg(Rating) as average_rating
                            FROM Rating
                            WHERE Rating.userId = %s and Rating.rating = %s'''
        rating_sum += int(query(user_rating_average_command, holders, user_rating_average_result()))
        rating_count += 1


    average_rating = (tag_sum + rating_sum) / (tag_count + rating_count)

    return {'average rating': average_rating}



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
    return [{"movieId": movieId, "title": title, "release_year": release_year, "votes": votes, "avg_ratings": round(avg_ratings, 2)}
            for movieId, title, release_year, total_ratings, votes, avg_ratings in cursor]


def polarity_result(cursor):
    return [{"movieId": movieId, "title": title, "release_year": release_year, "polarity_index": polarity_index}
            for movieId, title, release_year, polarity_index in cursor]


def individual_movie_result(cursor):
    return [{"title": title, "release_year": release_year, "avg_rating": avg_rating}
            for title, release_year, avg_rating in cursor]

def genres_movie_result(cursor):
    return [genre[0] for genre in cursor]


def actors_movie_result(cursor):
    return [{"actor": actorName}
            for actorName in cursor]


def tags_movie_result(cursor):
    return [{"tag": tag, "occurence" : occurence} for tag, occurence in cursor]


def ratings_date_movie_result(cursor):
    return [{"rating": rating, "timestamp": timestamp}
            for rating, timestamp in cursor]

def ratings_percentage_movie_result(cursor):
    return [{"rating": rating, "occurence": occurence}
            for rating, occurence in cursor]

def tags_average_result(cursor):
    return [{"average_rating": average_rating}
            for average_rating, occurence in cursor]

def user_rating_average_result(cursor):
    return [{"average_rating": average_rating}
            for average_rating, occurence in cursor]


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


def get_nUsers(condition, genres):
    command = f'''SELECT  COUNT(DISTINCT Ratings.userId) as interested_user 
                  FROM Genres, Ratings, Movies 
                  WHERE Ratings.rating > 3 and Ratings.movieId = Movies.movieId 
                  and Movies.movieId = Genres.movieId and {condition}'''
    return query(command, genres, lambda cursor: cursor.fetchone()[0])


def tagged_genres(nUsers, condition, tags):
    command = f''' SELECT genres, count(genres) / {nUsers} as proportion
                    FROM (
                        SELECT Tags.userId as userId, Genres.genres as genres
                        FROM Tags, Ratings, Users, Genres
                        WHERE {condition}
                        and Users.userId = Tags.userId
                        and Ratings.userId = Tags.userId
                        and Ratings.movieId = Tags.movieId
                        and Genres.movieId = Ratings.movieId
                        and Ratings.rating > 3
                        GROUP BY Genres.genres, Tags.userId) as temp
                    GROUP BY genres
                    ORDER BY proportion DESC'''
    return query(command, tags, extract_genres)

def get_users_with_tags(condition, tags):
    command = f''' SELECT count(Distinct Tags.userId)
                  FROM Tags
                  WHERE {condition}'''
    return query(command, tags, lambda cursor: cursor.fetchone()[0])          

def create_condition(genres, col='Genres.genres'):
    if not len(genres):return "FALSE"
    result = '('
    for i in range(len(genres)):
        result += f'{col} = %s'
        if i != len(genres) - 1:
            result += ' or '
    return result + ')'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
