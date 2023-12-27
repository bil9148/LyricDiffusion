from lyricExtractor import getLyrics
import lyrics2Images


def run():
    """Runs the program"""

    songName = "Dior"
    artistName = "Pop Smoke"

    # Get the lyrics
    verses = getLyrics(songName, artistName)

    assert len(verses) > 0, "No lyrics found"

    l2i = lyrics2Images.Lyrics2Images()

    outputPath = rf"C:\Users\andre\source\repos\AIG\images\{songName} - {artistName}"

    # Run the model
    l2i.runL2I(verses=verses, output_path=outputPath)


run()
