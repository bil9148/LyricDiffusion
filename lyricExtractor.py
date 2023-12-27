from lyricsgenius import Genius


def getLyrics(songName: str, artistName: str):
    """Returns the lyrics of a song given the song name and artist name"""

    try:
        geniusApiKey = "0r7QN8utjRy_k7Ims4oLjaxHzBo9XPbtKi9W8IE6vTdgIhpTus0IZ8TOYHMFJMUQ"
        genius = Genius(geniusApiKey)

        song = genius.search_song(songName, artistName)

        # Ask user if the found song is the correct one
        if song is None:
            raise Exception("Song not found")

        songCorrect = input(
            f"Is this the correct song? (y/n)\n{song.artist}-{song.title}\n")

        if songCorrect.lower() != "y":
            raise Exception("Song not found")

        # Split the lyrics into verses
        verses = song.lyrics.split("\n")

        if len(verses) == 0:
            raise Exception("No lyrics found")

        return verses

    except Exception as e:
        print(e)
        return


def testGetLyrics():
    """Tests the getLyrics function"""

    verses = getLyrics("Dior", "Pop Smoke")

    assert len(verses) == 78, "The number of verses is not correct, expected 78 verses, got " + \
        str(len(verses)) + " verses instead."


testGetLyrics()
