from ..lyricExtractor import getLyrics
import unittest
from unittest.mock import patch


class TestGetLyrics(unittest.TestCase):

    @patch("lyricExtractor.Genius")
    def test_get_lyrics_successful(self, mock_genius):
        # Set up mock Genius instance
        song_lyrics = ['[Verse 1]', "Hello, it's me", "I was wondering if, after all these years, you'd like to meet", 'To go over everything', "They say that time's supposed to heal ya", "But I ain't done much healin'", 'Hello, can you hear me?', "I'm in California dreaming about who we used to be", 'When we were younger and free', "I've forgotten how it felt before the world fell at our feet", '', '[Pre-Chorus]', "There's such a difference between us", 'And a million miles', '[Chorus]', 'Hello from the other side', "I must've called a thousand times", "To tell you I'm sorry for everything that I've done", 'But when I call, you never seem to be home', 'Hello from the outside', "At least, I can say that I've tried", "To tell you I'm sorry for breaking your heart", "But it don't matter, it clearly doesn't tear you apart anymore", '', '[Verse 2]', 'Hello, how are you?', "It's so typical of me to talk about myself, I'm sorry", "I hope that you're well", 'Did you ever make it out of that town', 'Where nothing ever happened?', '', '[Pre-Chorus]', "It's no secret that the both of us", 'Are running out of time', '[Chorus]',
                       'So hello from the other side (Other side)', "I must've called a thousand times (Thousand times)", "To tell you I'm sorry for everything that I've done", 'But when I call, you never seem to be home', 'Hello from the outside (Outside)', "At least, I can say that I've tried (I've tried)", "To tell you I'm sorry for breaking your heart", "But it don't matter, it clearly doesn't tear you apart anymore", '', '[Bridge]', '(Highs, highs, highs, highs, lows, lows, lows, lows)', 'Ooh, anymore', '(Highs, highs, highs, highs, lows, lows, lows, lows)', 'Ooh, anymore', '(Highs, highs, highs, highs, lows, lows, lows, lows)', 'Ooh, anymore', '(Highs, highs, highs, highs, lows, lows, lows, lows)', 'Anymore', '[Chorus]', 'Hello from the other side (Other side)', "I must've called a thousand times (Thousand times)", "To tell you I'm sorry for everything that I've done", 'But when I call, you never seem to be home', 'Hello from the outside (Outside)', "At least, I can say that I've tried (I've tried)", "To tell you I'm sorry for breaking your heart", "But it don't matter, it clearly doesn't tear you apart anymore", '', '[Music Video]']

        # Call the function with a known song and artist
        result = getLyrics("Hello", "Adele")

        # Assertions
        self.assertEqual(result, song_lyrics)

    @patch("lyricExtractor.Genius")
    def test_get_lyrics_song_not_found(self, mock_genius):
        # Call the function with a known song and artist
        result = getLyrics("NonExistentSong", "ExampleArtist")

        # Assertions
        self.assertListEqual(result, [])


if __name__ == "__main__":
    unittest.main()
