import pandas as pd
import pickle
from collections import defaultdict
import csv
import sys
import itertools

# def remove_dups():
#     df = pd.read_csv('datasets/Movies.csv')
#     df = df.drop_duplicates('tmdbId')
#     # df.loc[:, ~df.columns.str.contains('^Unnamed')].to_csv(
#     #     'Movies.csv', index=False)
#     df.to_csv('Movies.csv')
# remove_dups()
# sys.exit()


def tmdbId_to_movieId(tmdbId, movies_df):
    try:
        return int(movies_df.loc[tmdbId].movieId)
    except TypeError as e:
        print("ERR")
        print(tmdbId)
        print(movies_df.loc[tmdbId])


def handle_posterurls():
    with open('results-posterUrls', 'rb') as fi:
        data = defaultdict(list)
        poster_urls = pickle.load(fi)
        movies_df = pd.read_csv('datasets/Movies.csv')
        movies_df['movieId'] = pd.to_numeric(movies_df['movieId'])

        initial_len_of_movies = len(movies_df)
        initial_columns = movies_df.columns

        movies_df = movies_df.set_index('tmdbId', drop=False)
        for item in poster_urls:
            movieId = tmdbId_to_movieId(item['tmdbId'], movies_df)
            data['movieId'].append(int(movieId))
            data['posterUrl'].append(item['posterUrl'])

        movies_df = movies_df.set_index('movieId', drop=True)
        data_df = pd.DataFrame(data)
        data_df['movieId'] = pd.to_numeric(data_df['movieId'])

        data_df = data_df.set_index('movieId', drop=True)

        res = movies_df.merge(data_df, how='left',
                              left_index=True, right_index=True)

        # drop dups
        res = res[~res.index.duplicated(keep='first')]

        assert initial_len_of_movies == len(res)

        res.reset_index().to_csv('Movies.csv', index=False)


def handle_actors():
    with open('results-actors', 'rb') as fi:
        movies_df = pd.read_csv(
            'datasets/Movies.csv')[['movieId', 'tmdbId']].set_index('tmdbId', drop=True)

        data = pickle.load(fi)
        roles_td = []
        actors_td = []
        count = 0
        for movie in data:
            tmdbId = movie['tmdbId']
            movieId = tmdbId_to_movieId(tmdbId, movies_df)
            for actor in movie['actors']:
                id_a = actor.get('profilePath', None)
                if id_a:
                    id_a = id_a[1:-4]
                else:
                    id_a = "0" + actor['name']
                    # print(
                    #     f"Missing actor= {actor['name']} from movieId= {movieId} tmdbId= {tmdbId}")
                actors_td.append((id_a, actor['name']))
                roles_td.append((id_a, movieId))

        # remove dups
        actors_td.sort()
        actors_td = list(actors_td for actors_td,
                         _ in itertools.groupby(actors_td))

        roles_td.sort()
        roles_td = list(roles_td for roles_td,
                        _ in itertools.groupby(roles_td))

        actors_df = pd.DataFrame(actors_td)
        actors_df.columns = ['actorId', 'actorName']
        actors_df.to_csv('Actors.csv', index=False)

        roles_df = pd.DataFrame(roles_td)
        roles_df.columns = ['actorId', 'movieId']
        roles_df.to_csv('Actor_Roles.csv', index=False)


# handle_actors()
