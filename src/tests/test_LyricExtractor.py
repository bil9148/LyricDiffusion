from ..lyricExtractor import getLyrics
import unittest
from unittest.mock import patch


class TestGetLyrics(unittest.TestCase):

    @patch("lyricExtractor.Genius")
    def test_get_lyrics_successful(self, mock_genius):
        # Call the function with a known song and artist
        result = getLyrics("Coolio", "Gangsta's Paradise",askIfCorrect=False)

        # Assertions
        self.assertTrue(len(result) > 0)

    @patch("lyricExtractor.Genius")
    def test_get_lyrics_song_not_found(self, mock_genius):
        # Call the function with a known song and artist
        result = getLyrics("NonExistentSong", "ExampleArtist",askIfCorrect=False)

        # Assertions
        self.assertListEqual(result, [])


if __name__ == "__main__":
    unittest.main()
