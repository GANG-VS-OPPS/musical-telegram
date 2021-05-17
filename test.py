from spotify_worker import Spotify_Worker
from scrapper import get_links
import unittest

TRACK_SAD_LINKS = {'spotify': 'https://open.spotify.com/track/3ee8Jmje8o58CHK66QrVC2',
                   'apple': 'https://music.apple.com/ua/album/sad/1359292515?i=1359293318&amp;app=itunes',
                   'youtube': 'https://music.youtube.com/watch?v=iAeYPfrXwk4',
                   'amazon': 'https://amazon.com/dp/B07BGG89PS'}
ARTISTS_POPULARITIES = {'XXXTENTACION': 93, 'Lil Pump': 75, 'Don Toliver': 86}
CORRECT_TRACK_NAMES = ['SAD!', 'Dumbass', "Don't Cry (feat. XXXTENTACION)"]


class TestBot(unittest.TestCase):
    '''
    Test functions that work with Spotify API.
    '''

    def setUp(self):
        '''
        Authenticate Spotify worker.
        '''
        self.worker = Spotify_Worker()

    def test_search_track(self):
        '''
        Test whether tracks search works properly.
        '''
        self.assertEqual(self.worker.search_track("Sad")['name'], "SAD!")
        self.assertEqual(self.worker.search_track("Дежавю")['name'], "Дежавю")
        self.assertEqual(self.worker.search_track("D rose")[
            'name'], "Gold Roses (feat. Drake)")

    def test_search_tracks_from_playlist(self):
        '''
        Test whether fetching playlists works properly.
        '''
        self.assertEqual(
            len(self.worker.search_tracks_from_playlist("40CNYqcq6ZT9MyqmW4az0D")), 2)
        self.assertEqual(
            len(self.worker.search_tracks_from_playlist("7LVBmPSeuTnRGLLvtkuusZ")), 2)

    def test_normalize_names(self):
        '''
        Test whether a list of incorrectly-inputed songs into a list correct ones.
        '''
        self.assertEqual(self.worker.normalize_names(
            ["SAd", "Dumbass", "don't cry"]), CORRECT_TRACK_NAMES)

    def test_get_artists_popularities(self):
        '''
        Test whether a dicationary of artists popularities is built correctly.
        '''
        self.assertEqual(self.worker.get_artists_popularities(
            ["XXXTENTACION", "Lil Pump", "Don Toliver"]), ARTISTS_POPULARITIES)

    def test_get_links(self):
        '''
        Test whether a dicationary of links to streaming services is built correctly.
        '''
        self.assertEqual(get_links(
            "https://open.spotify.com/track/3ee8Jmje8o58CHK66QrVC2?si=fa32f4538998460f"), TRACK_SAD_LINKS)


if __name__ == '__main__':
    unittest.main()
