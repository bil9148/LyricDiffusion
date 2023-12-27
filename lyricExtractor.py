from lyricsgenius import Genius

apiKey = "0r7QN8utjRy_k7Ims4oLjaxHzBo9XPbtKi9W8IE6vTdgIhpTus0IZ8TOYHMFJMUQ"
genius = Genius(apiKey)

songName = "Dior"
artistName = "Pop Smoke"

song = genius.search_song(songName, artistName)

print(song.lyrics)
