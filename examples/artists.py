'''Module with functions to work with artists data.

Під час підбору потрібного датасету ми зіткнулися з проблемою:
більший датасет не мав інформації щодо популярності композицій.
Через це ми вирішили побудувати свій власний критерій популярності,
що базується на популярності артистів, що працювали над певною композицією.
За допомогою цих функцій, ми зібрали інформацію про популярність виконавців
з меншого датасету - таких всього 32 тисячі. Потім, ми відкинули всі пісні з
більшого датасету, у яких список виконавців не мав хоча б одного з
малого датасету. В результаті маємо датасет на більше ніж 600
тисяч пісень замість початково запланованих 160 тисяч.
'''
from typing import List, Set
import pandas as pd


def get_artists(data: pd.DataFrame) -> set:
    '''
    Return a set of artists from the dataset.
    '''
    artists_set = set()

    for artist_data in data['artists']:
        # Add a single artist
        if len(artist_data) == 1:
            artists_set.add(artist_data[0])
        # Add a group of artists
        else:
            for artist in artist_data:
                artists_set.add(artist)

    return artists_set


def has_known_artist(artist_data: List[str], artists: Set[str]):
    '''
    Return True if at least one artist is
    present in the given set, False otherwise.
    '''
    # Check if at least one artist from the group is known
    for artist in artist_data:
        if artist in artists:
            return True

    return False


def get_mean_popularity(artists, popularity):
    '''
    Return mean popularity value for among given artists.
    Return None if there is missing data for at least one artist.
    '''
    try:
        return sum(popularity[artist] for artist in artists) / len(artists)
    except:
        return None
