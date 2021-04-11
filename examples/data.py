'''Module with functions to work with Spotify datasets.'''
import pandas as pd
import json
from artists import get_artists, has_known_artist, get_mean_popularity


def get_datasets():
    '''
    Import a small dataset with 160K songs and a big dataset with 1.2M songs
    and clean up the data. Return a tuple of datasets.
    '''
    # Import the 1.2M dataset
    df_big = pd.read_csv("data/data_big.csv")

    # Drop columns that are not useful for the model
    df_big.drop(columns=['album', 'album_id', 'artist_ids', 'disc_number', 'duration_ms',
                         'release_date', 'time_signature', 'track_number', 'year'], inplace=True)

    # Convert 'explicit' column to numerical type
    df_big["explicit"] = df_big["explicit"].apply(
        lambda is_explicit: int(is_explicit))

    # Reorder columns alphabetically
    df_big = df_big.reindex(sorted(df_big.columns), axis=1)

    # Import the 160K dataset
    df_small = pd.read_csv("data/data_small.csv")

    # Drop columns that are not useful for the model
    df_small.drop(columns=['release_date', "year",
                           "duration_ms", "popularity"], inplace=True)

    # Fix the 'artists' column in both datasets
    df_small["artists"] = df_small["artists"].apply(
        lambda raw_artist_data: tuple(eval(raw_artist_data)))
    df_big["artists"] = df_big["artists"].apply(
        lambda raw_artist_data: tuple(eval(raw_artist_data)))

    # Create a set of artists from 160K dataset
    artists_160k = get_artists(df_small)

    # Filter tracks from 1.2M dataset based on whether a track contains an artist from the 160K dataset
    df_big_from_160k = df_big[df_big["artists"].apply(
        lambda artist_data: has_known_artist(artist_data, artists_160k))]

    # Merge two datasets and drop duplicate tracks
    df = pd.merge(df_big_from_160k, df_small, how='outer')
    df = df.drop_duplicates(subset='id', keep="first")

    # Construct a dictionary with popularity of every artist
    with open('data/artists_small.json', 'r') as artists_popularity_data:
        popularity = json.load(artists_popularity_data)
    with open('data/artists_big.json', 'r') as artists_new_popularity_data:
        popularity.update(json.load(artists_new_popularity_data))

    # Add the 'popularity' column with a mean popularity value of every artist
    df["popularity"] = df["artists"].apply(
        lambda artists: get_mean_popularity(artists, popularity))

    # Drop tracks with missing popularity data
    df = df.dropna(how="any")

    return df_small, df_big


if __name__ == '__main__':
    df_small, df_big = get_datasets()

    print('160K Spotify dataset')
    print(df_small)

    print('1.2M Spotify dataset')
    print(df_big)
