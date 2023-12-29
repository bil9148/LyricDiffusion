from ..lyricExtractor import getLyrics
import unittest
from unittest.mock import patch


class TestGetLyrics(unittest.TestCase):

    @patch("lyricExtractor.Genius")
    def test_get_lyrics_successful(self, mock_genius):
        # Set up mock Genius instance
        song_lyrics = ['244 ContributorsTranslationsEspañolMagyarGangsta’s Paradise Lyrics[Recording Info]', '', '[Verse 1: Coolio]', 'As I walk through the valley of the shadow of death', "I take a look at my life and realize there's nothin' left", "'Cause I've been blastin' and laughin' so long that", 'Even my momma thinks that my mind is gone', "But I ain't never crossed a man that didn't deserve it", "Me be treated like a punk, you know that's unheard of", "You better watch how ya talkin' and where you walkin'", 'Or you and your homies might be lined in chalk', 'I really hate to trip, but I gotta loc', 'As they croak, I see myself in the pistol smoke, fool', "I'm the kinda G the little homies wanna be like", "On my knees in the night, sayin' prayers in the streetlight", '', '[Chorus: LV]', "We've been spendin' most their lives livin' in the gangsta's paradise", "We've been spendin' most their lives livin' in the gangsta's paradise", "We keep spendin' most our lives livin' in the gangsta's paradise", "We keep spendin' most our lives livin' in the gangsta's paradise", '', '[Verse 2: Coolio]', "Look at the situation they got me facin'", "I can't live a normal life, I was raised by the state", 'So I gotta be down with the hood team', "Too much television watchin' got me chasin' dreams", "I'm a educated fool with money on my mind", 'Got my ten in my hand and a gleam in my eye', "I'm a loc'd out gangsta, set trippin' banger", "And my homies is down, so don't arouse my anger, fool", "Death ain't nothin' but a heartbeat away", "I'm livin' life do-or-die, what can I say?", "I'm 23 now, but will I live to see 24?", "The way things is goin', I don't know", 'You might also like[Refrain: LV]', 'Tell me why are we so blind to see', 'That the ones we hurt are you and me?', '', '[Chorus: LV]', "We've been spendin' most their lives livin' in the gangsta's paradise", "We've been spendin' most their lives livin' in the gangsta's paradise", "We keep spendin' most our lives livin' in the gangsta's paradise", "We keep spendin' most our lives livin' in the gangsta's paradise", '', '[Verse 3: Coolio]', 'Power and the money, money and the power', 'Minute after minute, hour after hour', "Everybody's runnin', but half of them ain't lookin'", "It's goin' on in the kitchen, but I don't know what's cookin'", "They say I gotta learn, but nobody's here to teach me", "If they can't understand it, how can they reach me?", "I guess they can't, I guess they won't, I guess they front", "That's why I know my life is out of luck, fool", '', '[Chorus: LV]', "We've been spendin' most their lives livin' in the gangsta's paradise", "We've been spendin' most their lives livin' in the gangsta's paradise", "We keep spendin' most our lives livin' in the gangsta's paradise", "We keep spendin' most our lives livin' in the gangsta's paradise", '[Refrain: LV]', 'Tell me, why are we so blind to see', 'That the ones we hurt are you and me?', 'Tell me, why are we so blind to see', 'That the ones we hurt are you and me?182Embed']

        # Call the function with a known song and artist
        result = getLyrics("Coolio", "Gangsta's Paradise")

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
