from lyricsgenius import Genius
import settings as settings
import gui

GENIUSAPIKEY = "0r7QN8utjRy_k7Ims4oLjaxHzBo9XPbtKi9W8IE6vTdgIhpTus0IZ8TOYHMFJMUQ"


def getLyrics(songName: str, artistName: str, askIfCorrect: bool = False):
    """Returns the lyrics of a song given the song name and artist name"""

    try:
        song = getSong(songName, artistName, askIfCorrect=askIfCorrect)

        if song is None:
            raise Exception("Song not found")

        # Split the lyrics into verses
        verses = song.lyrics.split("\n")

        if len(verses) == 0:
            raise Exception("No lyrics found")

        return verses

    except Exception as e:
        gui.BasicUI.HandleError(e)

    return []


def getSong(songName: str, artistName: str, askIfCorrect: bool = False):
    """Returns the song object given the song name and artist name"""

    try:
        genius = Genius(GENIUSAPIKEY)

        song = genius.search_song(songName, artistName)

        if askIfCorrect:
            # Ask the user if the song is correct
            correct = gui.BasicUI.AskYesNo(
                f"Is this the correct song? \n{song.title} - {song.artist}")

            if not correct:
                return None

        return song

    except Exception as e:
        gui.BasicUI.HandleError(e)

    return None
