from lyricExtractor import getLyrics
import lyrics2Images


def run():
    try:
        """Runs the program"""

        songName = input("Enter the song name: ")
        artistName = input("Enter the artist name: ")

        assert len(songName) > 0, "Song name cannot be empty"
        assert len(artistName) > 0, "Artist name cannot be empty"

        # Get the lyrics
        verses = getLyrics(songName, artistName)

        assert len(verses) > 0, "No lyrics found"

        l2i = lyrics2Images.Lyrics2Images(
            num_inference_steps=100, use_auth_token=False, prompt="lyrics", model_id="CompVis/stable-diffusion-v1-4", revision="fp16")

        outputPath = rf"C:\Users\andre\source\repos\AIG\images\{songName} - {artistName}"

        # Run the model
        l2i.runL2I(verses=verses, output_path=outputPath)

    except Exception as e:
        print(e)
        return


run()
