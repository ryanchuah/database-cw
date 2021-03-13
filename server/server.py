import mysql.connector
from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
from flask_caching import Cache

from query_results_templates import get_sorted_result, extract_genres, individual_movie_result, \
    get_all_movies_result, genres_movie_result, actors_movie_result, tags_movie_result, ratings_date_movie_result, \
    ratings_percentage_movie_result, tags_average_result, user_rating_average_result, predict_personality_result

# Flask config
app = Flask(__name__)

# cors settings needed to prevent CORS errors when testing on localhost
# this should be removed when we deploy to production servers
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#
# app = Flask(__name__)

cache = Cache(app, config={"CACHE_TYPE": "simple"})


config = {
    'user': 'user',
    'password': 'user',
    'host': 'db',
    'port': '3306',
    'database': 'movies_db'
}


# Use case 1: Browsing films in the database and
# Use Case 3: Reporting which are the most popular movies and which are the most polarising

# Viewing all the movies in the database and sorting them

# PARAMS:
# sortBy can only take ==> ['movieId', 'title', 'release_year', 'popularity', 'votes', 'avg_ratings', 'polarity_index']
# ascending ==> 1 or 0. 1 being descending order
# EXAMPLE: http://localhost:5000/movies?sortBy=release_year&limit=10&page=1&ascending=0
@cache.cached(timeout=3600)
@app.route('/movies')
@cross_origin()
def movies():
    limit, page, sortBy, ascending = validate_input()
    return _get_sorted_by_column(limit, page, sortBy, ascending)


# Searching for movies in the database
@cache.cached(timeout=3600)
@app.route("/search")
@cross_origin()
def search_movies():
    sortBy = request.args.get('sortBy')

    Movies_columns = ['movieId', 'title', 'imdbId', 'tmdbId']
    search_criteria = request.args.get('search_criteria')
    movies = []

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

    if not sortBy == None:
        holders = None
        command = "SELECT * FROM Movies WHERE title like \'%{search_criteria}%\' ORDER BY {sortBy} LIMIT {limit}"
        movies = query(command, holders, get_all_movies_result)
    else:
        holders = None
        command = "SELECT * FROM Movies WHERE title like \'%{search_criteria}%\' LIMIT {limit}"
        movies = query(command, holders, get_all_movies_result)

    return {"movies": movies}


# Use case 2: Searching for a film to obtain a report on viewer reaction to it
# Use case 4: Segmenting the audience for a released movie
@cache.cached(timeout=3600)
@app.route('/movies/<movie_id>')
@cross_origin()
def single_movie(movie_id):
    holders = movie_id,

    details_command = '''SELECT Movies.title, Movies.release_year, Movies.poster_url, Avg(Ratings.rating) as avg_rating
                 FROM Ratings, Movies
                 WHERE Movies.movieId = %s AND Ratings.movieId = Movies.movieId
                 GROUP BY Movies.title, Movies.release_year, Movies.poster_url
                 '''

    genre_command = '''SELECT genres FROM Genres WHERE Genres.movieId = %s'''

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
    genres = query(genre_command, holders, genres_movie_result)
    tags_dict = query(tags_command, holders, tags_movie_result)

    movie_details = {'details': query(details_command, holders, individual_movie_result),
                     'genres': genres,
                     'actors': query(actors_command, holders, actors_movie_result),
                     'tags': tags_dict,
                     'ratings_date': query(ratings_date_command, holders, ratings_date_movie_result),
                     'ratings_percentage': query(ratings_percentage_command, holders, ratings_percentage_movie_result),
                     'similar_genres_by_genre': _get_similar_rated_genres(genres),
                     'similar_genres_by_tag': _get_similar_tagged_genres(tags_dict)
                     }

    # print(movie_details)
    # return "individual movie page data will be returned here for movieid: "+movie_id
    return movie_details


# Use case 5: Predicting the likely viewer ratings for a soon-to-be-released film based on the tags and or ratings for
# the film provided by a preview panel of viewers drawn from the population of viewers in the database.
@cache.cached(timeout=3600)
@app.route("/predict_rating")
@cross_origin()
def predict_ratings():
    # get tags from front end
    responses = tuple(request.args.getlist('responses'))
    userId = request.args.get('userId')
    tags = tuple(request.args.getlist('tags'))
    rating = request.args.get('rating')

    responses = [[userId, tags, rating]]
    
    tag_sum = 0
    rating_sum = 0
    total_sum = 0
    count = 0
    average_rating = 0

    for response in responses:
        userId = response[0]
        tags = response[1]
        rating = response[2]
        try:
            rating = float(rating)
        except:
            rating = 0.0
        condition = create_condition(tags, col='Tags.tag')
        # get predicted rating from tags
        tags_average_command = f'''SELECT avg(Ratings.rating) as average_rating
                            FROM Ratings, Tags
                            WHERE Ratings.movieId = Tags.movieId AND {condition}'''
        tag_score = query(tags_average_command, tags, tags_average_result)[0]['average_rating'][0]
        if tag_score:
            tag_sum += tag_score

        # find other movies with same rating from user x and and average their rating - average those
        holders = userId, float(rating),

        user_rating_average_command = '''SELECT Avg(average_rating_individuals) as average_rating
            FROM (SELECT Avg(Ratings.rating) as average_rating_individuals
                    FROM Ratings
                    WHERE Ratings.movieId IN
                        (SELECT Ratings.movieId as movie
                            FROM Ratings WHERE (userId = %s AND abs(rating - %s) < 0.1)
                        )
                ) AS B'''

        user_rating_score = query(user_rating_average_command, holders, user_rating_average_result)[0]['average_rating'][0]
        if user_rating_score:
            rating_sum += user_rating_score

        count += 1
        total_sum += float(rating)

    if tag_sum != 0 and rating_sum != 0:
        average_rating = ((tag_sum/count) + (rating_sum/count) + (total_sum/count)) / 3
    elif tag_sum != 0:
        average_rating = ((tag_sum/count) + (total_sum/count)) / 2
    elif rating_sum != 0:
        average_rating = ((rating_sum/count) + (total_sum/count)) / 2
    else:
        try:
            average_rating = total_sum/count
        except:
            average_rating = 0

    return {'predicted_rating': average_rating}

# Use Case 6: Predicting the personality traits of viewers who will give a high rating to a soon-to-be-released film
# whose tags are known.
@cache.cached(timeout=3600)
@app.route("/predict_personality")
@cross_origin()
def predict_personality():
    tags = tuple(request.args.getlist('tags'))
    condition = create_condition(tags, col='Tags.tag')
    command = f'''SELECT avg(openness) as avg_openness, avg(agreeableness) as avg_agreeableness, avg(emotional_stability) as avg_emotional_stability, avg(conscientiousness) as conscientiousness, avg(extraversion) as extraversion
                    FROM Personality_Attributes_table
                    INNER JOIN Personality_Ratings_table ON Personality_Attributes_table.hashed_userId = Personality_Ratings_table.hashed_userId
                    INNER JOIN (SELECT movieId FROM Tags WHERE {condition}) as temp ON temp.movieId = Personality_Ratings_table.movieId
                    WHERE Personality_Ratings_table.predicted_rating > 4.5'''
    return {"personality": query(command, tags, predict_personality_result)}


# # Error routes
# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return "Page not found", 404


# @app.errorhandler(403)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return "403", 403


# @app.errorhandler(410)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return "410", 410


# @app.errorhandler(500)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return "Internal server error", 500


# Function to run queries
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


# Helper function for validating input for displaying list of movies
def validate_input():
    sortBy = request.args.get('sortBy')
    ascending = int(request.args.get('ascending'))
    limit = int(request.args.get('limit'))
    page = int(request.args.get('page'))
    Movies_columns = ['movieId', 'title', 'release_year',
                      'popularity', 'votes', 'avg_ratings', 'polarity_index']
    if sortBy not in Movies_columns:
        raise ValueError(
            f"the request query column={sortBy} is not recognized. Either developer error, or SQL injection attempt")
    return limit, page, sortBy, ascending


# Helper function for ORing a list of values in a query
def create_condition(columns, col):
    if not len(columns):
        return "FALSE"
    result = '('
    for i in range(len(columns)):
        result += f'{col} = %s'
        if i != len(columns) - 1:
            result += ' or '
    return result + ')'


# Helper functions for task 4

# PARAM: a movieId
# Returns a list of genres [a, b...] each associated with a proportion
# of users that like this movie and that genre
# Can display 'd% of users that like (animation and adventure) also like genre a'
#             'c% of users that like (action and thiller) also like genere b' etc..
def _get_similar_rated_genres(genres):
    condition = create_condition(genres, col="Genres.genres")
    nUsers = _get_nUsers(condition, genres)
    return _similar_genres(nUsers, condition, genres)


# PARAM: a movieId
# Returns a list of genres [a, b...] each associated with a proportion
# of users that have used this movie's tags and like that genre.
# Also returns this movie's tags
# Can display 'd% of users that used tags x,y,z and like this movie also like genre a'
#            'c% of users that used tags x,y,z and like this movie also like genre b' etc..
def _get_similar_tagged_genres(tags_dict):
    tags = [element['tag'] for element in tags_dict]
    condition = create_condition(tags, col='Tags.tag')
    nUsers = _get_users_with_tags(condition, tags)
    return _tagged_genres(nUsers, condition, tags)


def _similar_genres(nUsers, condition, genres):
    having_condition = create_condition(genres, col='genres')
    command = f'''SELECT genres, count(genres)/{nUsers} as proportion
                    FROM (SELECT Genres.genres as genres 
                    FROM Ratings
                    INNER JOIN Movies ON Movies.movieId = Ratings.movieId
                    INNER JOIN Genres ON Genres.movieId = Ratings.movieId
                    INNER JOIN (SELECT  DISTINCT Ratings.userId as userId
                                FROM Ratings
                                INNER JOIN Movies ON Ratings.movieId = Movies.movieId
                                INNER JOIN Genres ON Movies.movieId = Genres.movieId
                                WHERE Ratings.rating > 3 
                                and {condition}) as userSpace ON userSpace.userId = Ratings.userId
                    WHERE Ratings.rating > 3
                    GROUP BY Ratings.userId, Genres.genres)as genreSets
                    GROUP BY genres
                    HAVING NOT {having_condition}
                    ORDER BY proportion DESC'''
    return query(command, genres + genres, extract_genres)


# returns the start_th to the end_th most/least 'sortby' movies inclusive depending on ascending
# requirements => start and end are both ints, start <= end, start >= 1 and end >= 1
## optimise this
def _get_sorted_by_column(limit, page, sortBy='popularity', ascending=1):
    start = limit * page - (limit - 1)
    end = limit * page
    holders = end - start + 1, start - 1
    ordering = 'DESC' if ascending else 'ASC'
    command = f'''SELECT Movies.movieId as movieId, Movies.title as title, Movies.release_year as release_year, Sum(Ratings.rating) as popularity, 
                 Count(Ratings.rating) as votes, Avg(Ratings.rating) as avg_ratings, VARIANCE(Ratings.rating) as polarity_index 
                 FROM Ratings, Movies 
                 WHERE Ratings.movieId = Movies.movieId 
                 GROUP BY Ratings.movieId 
                 ORDER BY {sortBy} {ordering} 
                 LIMIT %s OFFSET %s'''
    return {'movies': query(command, holders, get_sorted_result)}

# optimise this
def _get_nUsers(condition, genres):
    command = f'''SELECT  COUNT(DISTINCT Ratings.userId) as interested_user 
                  FROM Genres, Ratings, Movies 
                  WHERE Ratings.rating > 3 and Ratings.movieId = Movies.movieId 
                  and Movies.movieId = Genres.movieId and {condition}'''
    return query(command, genres, lambda cursor: cursor.fetchone()[0])


# optimise this
def _tagged_genres(nUsers, condition, tags):
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


def _get_users_with_tags(condition, tags):
    command = f''' SELECT count(Distinct Tags.userId)
                  FROM Tags
                  WHERE {condition}'''
    return query(command, tags, lambda cursor: cursor.fetchone()[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
