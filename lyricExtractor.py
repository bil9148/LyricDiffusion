from lyricsgenius import Genius


def getLyrics(songName: str, artistName: str):
    """Returns the lyrics of a song given the song name and artist name"""

    geniusApiKey = "REDACTED_GENIUS_API_KEY"
    genius = Genius(geniusApiKey)

    song = genius.search_song(songName, artistName)

    # Split the lyrics into verses
    verses = song.lyrics.split("\n")

    return verses


getLyrics("Dior", "Pop Smoke")
