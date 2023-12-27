from lyricsgenius import Genius

apiKey = "REDACTED_GENIUS_API_KEY"
genius = Genius(apiKey)

songName = "Dior"
artistName = "Pop Smoke"

song = genius.search_song(songName, artistName)

print(song.lyrics)
