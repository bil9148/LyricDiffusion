from lyricsgenius import Genius


def getLyrics(songName: str, artistName: str):
    """Returns the lyrics of a song given the song name and artist name"""

    geniusApiKey = "0r7QN8utjRy_k7Ims4oLjaxHzBo9XPbtKi9W8IE6vTdgIhpTus0IZ8TOYHMFJMUQ"
    genius = Genius(geniusApiKey)

    song = genius.search_song(songName, artistName)

    # Split the lyrics into verses
    verses = song.lyrics.split("\n")

    return verses


def testGetLyrics():
    """Tests the getLyrics function"""

    verses = getLyrics("Dior", "Pop Smoke")

    assert len(verses) == 78, "The number of verses is not correct, expected 78 verses, got " + \
        str(len(verses)) + " verses instead."


testGetLyrics()
