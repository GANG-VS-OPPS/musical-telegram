'''Module with functions for working with Spotify API.'''
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from scipy.spatial.distance import cdist
import numpy as np
import pandas as pd
from config import *


class Spotify_Worker:
    '''
    Class with functions to work with Spotify.
    '''

    def __init__(self):
        '''
        Authenticate Spotify user for later usage.
        '''
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="24e9586f0ee949599af59c1ddbb92e3c",
                                                                        client_secret="9f68b7d9b48c40beb4c708ba8aaa3ec0"))

    def search_track(self, name: str):
        '''
        Search tracks by name. Print the best match.
        '''
        results = self.sp.search(q=f'track: {name}', limit=1)

        # If no tracks were found, return None
        if results['tracks']['items'] == []:
            return None

        # Extract the first result
        results = results['tracks']['items'][0]
        audio_features = self.sp.audio_features(results['id'])[0]
        audio_features["popularity"] = results["popularity"]

        # Add needed features to the track
        audio_features['artists'] = [artist['name']
                                     for artist in results['artists']]
        audio_features['name'] = results['name']
        audio_features['explicit'] = int(results['explicit'])

        # Delete unused features
        del audio_features['analysis_url'], audio_features[
            'track_href'], audio_features['type'], audio_features['uri'], audio_features['duration_ms']

        return audio_features

    def search_tracks_from_playlist(self, playlist_id: str):
        '''
        Print all tracks from a certain playlist by its ID.
        '''
        offset = 0
        tracks = []

        while True:
            response = self.sp.playlist_items(playlist_id,
                                              offset=offset,
                                              fields='items.track.name,total',
                                              additional_types=['track'])

            if len(response['items']) == 0:
                break

            tracks += [item['track']['name'] for item in response['items']]

            offset = offset + len(response['items'])

        return tracks

    def get_url(self, name: str):
        '''
        Get the Spotify url for the track.
        '''
        results = self.sp.search(q=f'track: {name}', type='track', limit=1)
        return results['tracks']['items'][0]["external_urls"]["spotify"]

    def get_mean_vector(self, song_list):
        song_vectors = []

        for song in song_list:
            song_data1 = self.search_track(song)
            song_data = pd.DataFrame(
                [song_data1.values()], columns=song_data1.keys())

            if song_data is None:
                continue

            song_vector = song_data[NUMERIC_COLS].values
            song_vectors.append(song_vector)

        song_matrix = np.array(list(song_vectors))

        return np.mean(song_matrix, axis=0)

    def normalize_names(self, songs):
        '''
        Search for tracks and return their actual names in the Spotify database.
        '''
        songs_names = []

        for song in songs:
            res = self.sp.search(q=song, type='track', limit=1)

            for _, track in enumerate(res['tracks']['items']):
                songs_names.append(track['name'])

        return songs_names

    def get_artists_popularities(self, artists):
        '''
        Traverse through a given list of artists and search
        for their popularity using Spotify API. Return
        a dictionary of key-value pairs where keys are
        artists and values are their popularity rate.
        '''
        popularities = {}

        for artist in artists:
            if artist not in popularities:
                search_results = self.sp.search(artist, 1, 0, 'artist')[
                    'artists']['items']

                if search_results:
                    popularities[artist] = search_results[0]['popularity']

        return popularities

    def recommend_songs(self, songs, spotify_data, song_cluster_pipeline, n_songs=10):
        '''
        Recommend songs based on the given list of songs and the dataset.
        '''
        data_cols = ['name',  'artists', 'id']
        songs = self.normalize_names(songs)

        # Build distances to songs with the ML model
        song_center = self.get_mean_vector(songs)
        scaler = song_cluster_pipeline.steps[0][1]
        scaled_data = scaler.transform(spotify_data[NUMERIC_COLS])
        scaled_song_center = scaler.transform(song_center.reshape(1, -1))
        distances = cdist(scaled_song_center, scaled_data, 'cosine')

        # Get indices of closest 'n_songs' songs
        index = list(np.argsort(distances)[:, :n_songs][0])
        recommended_songs = spotify_data.iloc[index]

        # Remove songs that are already present in user's tracklist
        recommended_songs = recommended_songs[(~recommended_songs['name'].isin(
            songs)) & (recommended_songs['name'].str.len() <= 64)]

        # Remove duplicates
        recommended_songs = recommended_songs.drop_duplicates(subset=['name'])

        return recommended_songs[data_cols].to_dict(orient='records')
