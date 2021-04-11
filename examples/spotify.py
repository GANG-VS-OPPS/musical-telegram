'''Module with key functions for working with Spotify API.

Модуль був доповнений додатковими функціями під час другого етапу виконання завдання.
'''
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

# authenticate
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="YOUR_CLIENT_ID",
                                                           client_secret="YOUR_CLIENT_SECRET"))


def search_track(name: str):
    '''
    Search tracks by name. Print the best match.
    '''
    results = sp.search(q=f'track: {name}', limit=1)

    # if no tracks were found, return None
    if results['tracks']['items'] == []:
        return None

    # extract the first result
    results = results['tracks']['items'][0]
    audio_features = sp.audio_features(results['id'])[0]

    # add needed features to the track
    audio_features['artists'] = [artist['name']
                                 for artist in results['artists']]
    audio_features['name'] = results['name']
    audio_features['year'] = int(results['album']['release_date'][:4])
    audio_features['explicit'] = int(results['explicit'])

    # delete unused features
    del audio_features['analysis_url'], audio_features[
        'track_href'], audio_features['type'], audio_features['uri']

    return audio_features


def search_playlists(username: str):
    '''
    Search for playlists of a certain user. Print a list of them.
    '''
    playlists = sp.user_playlists(username)

    while playlists:
        for idx, playlist in enumerate(playlists['items']):
            print(
                f"{idx + 1 + playlists['offset']} {playlist['uri']} {playlist['name']}")

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


def search_tracks_from_playlist(playlist_id: str):
    '''
    Print all tracks from a certain playlist by its ID.
    '''
    offset = 0

    while True:
        response = sp.playlist_items(playlist_id,
                                     offset=offset,
                                     fields='items.track.id,total',
                                     additional_types=['track'])

        if len(response['items']) == 0:
            break

        pprint(response['items'])
        offset = offset + len(response['items'])
        print(offset, "/", response['total'])


def get_artists_popularities(artists):
    '''
    Traverse through a given list of artists and search
    for their popularity using Spotify API. Return
    a dictionary of key-value pairs where keys are
    artists and values are their popularity rate.
    '''
    popularities = {}

    for artist in artists:
        if artist not in popularities:
            search_results = sp.search(artist, 1, 0, 'artist')[
                'artists']['items']

            if search_results:
                popularities[artist] = search_results[0]['popularity']

    return popularities
