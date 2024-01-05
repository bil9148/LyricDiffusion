from ..geniusAPI import getLyrics, getSong
import unittest
from unittest.mock import patch


class TestGetLyrics(unittest.TestCase):

    @patch("geniusAPI.Genius")
    def test_get_lyrics_successful(self, mock_genius):
        # Call the function with a known song and artist
        result = getLyrics("Coolio", "Gangsta's Paradise", askIfCorrect=False)

        # Assertions
        self.assertTrue(len(result) > 0)

    @patch("geniusAPI.Genius")
    def test_get_lyrics_song_not_found(self, mock_genius):
        # Call the function with a known song and artist
        result = getLyrics("NonExistentSong",
                           "ExampleArtist", askIfCorrect=False)

        # Assertions
        self.assertListEqual(result, [])

    def test_getSong_successful(self):
        # Call the function with a known song and artist
        result = getSong("Coolio", "Gangsta's Paradise")

        # Assertions
        self.assertIsNotNone(result)

    def test_getSong_song_not_found(self):
        # Call the function with a known song and artist
        result = getSong("NonExistentSong", "ExampleArtist")

        # Assertions
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
