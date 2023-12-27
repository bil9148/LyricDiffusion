from lyricExtractor import getLyrics
import lyrics2Images


def run():
    try:
        """Runs the program"""

        # songName = input("Enter the song name: ")
        # artistName = input("Enter the artist name: ")

        songName = "Hello"
        artistName = "Adele"

        assert len(songName) > 0, "Song name cannot be empty"
        assert len(artistName) > 0, "Artist name cannot be empty"

        # Get the lyrics
        verses = getLyrics(songName, artistName)

        assert len(verses) > 0, "No lyrics found"

        # DGSpitzer/Cyberpunk-Anime-Diffusion
        # stabilityai/sdxl-turbo -
        # SG161222/Realistic_Vision_V6.0_B1_noVAE -
        # SG161222/Realistic_Vision_V2.0 -
        # Lykon/DreamShaper -
        # stabilityai/stable-diffusion-2-1 -

        l2i = lyrics2Images.Lyrics2Images(
            num_inference_steps=50, use_auth_token=False, prompt=f"vibrant and joyful visuals inspired by the sunny lyrics of {songName} by {artistName}", model_id="DGSpitzer/Cyberpunk-Anime-Diffusion", variant="fp16")

        outputPath = rf"C:\Users\andre\source\repos\AIG\images\{songName} - {artistName}"

        # Run the model
        l2i.runL2I(verses=verses, output_path=outputPath)

    except Exception as e:
        print(e)
        return


run()
