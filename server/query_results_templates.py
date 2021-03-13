def get_sorted_result(cursor):
    return [{"movieId": movieId, "title": title, "release_year": release_year, "popularity": popularity,
             "votes": votes, "avg_ratings": round(avg_ratings, 2), "polarity_index": polarity_index}
            for movieId, title, release_year, popularity, votes, avg_ratings, polarity_index in cursor]


def extract_genres(cursor):
    return [{"genre": genres, "proportion": float(proportion)} for genres, proportion in cursor]


def individual_movie_result(cursor):
    return [{"title": title, "release_year": release_year, "poster_url": poster_url, "avg_rating": avg_rating}
            for title, release_year, poster_url, avg_rating in cursor]


def get_all_movies_result(cursor):
    return [{"movieId": movieId, "movieTitle": movieTitle, "imdbId": imdbId, "tmdbId": tmdbId}
            for movieId, movieTitle, imdbId, tmdbId in cursor]


def genres_movie_result(cursor):
    return [genre[0] for genre in cursor]


def actors_movie_result(cursor):
    return [{"actor": actorName}
            for actorName in cursor]


def tags_movie_result(cursor):
    return [{"tag": tag, "occurence": occurence} for tag, occurence in cursor]


def ratings_date_movie_result(cursor):
    return [{"rating": rating, "timestamp": timestamp}
            for rating, timestamp in cursor]


def ratings_percentage_movie_result(cursor):
    return [{"rating": rating, "occurence": occurence}
            for rating, occurence in cursor]


def predict_personality_result(cursor):
    return [
        {"openness": avg_openness, "agreeableness": avg_agreeableness, "emotional_stability": avg_emotional_stability,
         "conscientiousness": avg_conscientiousness, "extraversion": avg_extraversion}
        for avg_openness, avg_agreeableness, avg_emotional_stability, avg_conscientiousness, avg_extraversion in cursor]


def tags_average_result(cursor):
    return [{"average_rating": average_rating}
        for average_rating in cursor]


def user_rating_average_result(cursor):
    return [{"average_rating": average_rating}
            for average_rating in cursor]
