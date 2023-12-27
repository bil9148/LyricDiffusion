from lyricExtractor import getLyrics
import lyrics2Images


def run():
    """Runs the program"""

    songName = "Dior"
    artistName = "Pop Smoke"

    # Get the lyrics
    verses = getLyrics(songName, artistName)

    l2i = lyrics2Images.Lyrics2Images()

    outputPath = rf"C:\Users\andre\source\repos\AIG\images\{songName} - {artistName}"

    # Run the model
    l2i.runL2I(l2i, verses=verses, output_path=outputPath)


run()
