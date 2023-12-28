from lyricsgenius import Genius
import logging


def getLyrics(songName: str, artistName: str):
    """Returns the lyrics of a song given the song name and artist name"""

    try:
        geniusApiKey = "0r7QN8utjRy_k7Ims4oLjaxHzBo9XPbtKi9W8IE6vTdgIhpTus0IZ8TOYHMFJMUQ"
        genius = Genius(geniusApiKey)

        song = genius.search_song(songName, artistName)

        if song is None:
            raise Exception("Song not found")

        # Split the lyrics into verses
        verses = song.lyrics.split("\n")

        if len(verses) == 0:
            raise Exception("No lyrics found")

        return verses

    except Exception as e:
        logging.error(
            f"Error getting lyrics: {e}.\nStacktrace:{e.__traceback__}")
        return []
