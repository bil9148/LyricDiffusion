import unittest
from unittest.mock import patch
from lyricExtractor import getLyrics


class TestGetLyrics(unittest.TestCase):

    @patch("lyricExtractor.Genius")
    def test_get_lyrics_successful(self, mock_genius):
        # Set up mock Genius instance
        genius_instance = mock_genius.return_value
        song_lyrics = "These are the lyrics\nIn multiple lines"
        genius_instance.search_song.return_value.lyrics = song_lyrics

        # Call the function with a known song and artist
        result = getLyrics("ExampleSong", "ExampleArtist")

        # Assertions
        self.assertEqual(result, song_lyrics.split("\n"))
        genius_instance.search_song.assert_called_once_with(
            "ExampleSong", "ExampleArtist")

    @patch("lyricExtractor.Genius")
    def test_get_lyrics_song_not_found(self, mock_genius):
        # Set up mock Genius instance
        genius_instance = mock_genius.return_value
        genius_instance.search_song.return_value = None

        # Call the function with a known song and artist
        result = getLyrics("NonExistentSong", "ExampleArtist")

        # Assertions
        self.assertIsNone(result)

    # Add more test cases as needed


if __name__ == "__main__":
    unittest.main()
