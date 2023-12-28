from lyricExtractor import getLyrics
import lyrics2Images
import traceback

# DGSpitzer/Cyberpunk-Anime-Diffusion - works
# stabilityai/sdxl-turbo - argument of type 'NoneType' is not iterable
# SG161222/Realistic_Vision_V6.0_B1_noVAE - doesn't work
# SG161222/Realistic_Vision_V2.0 - doesn't work
# Lykon/DreamShaper - generates black images
# stabilityai/stable-diffusion-2-1 - works
# CompVis/stable-diffusion-v1-4 - works


def run():
    """Runs the program"""
    try:
        songName = "Gangstas Paradise"
        artistName = "Coolio"

        # Validate the input
        assert songName is not None and len(
            songName) > 0, "Song name cannot be empty"
        assert artistName is not None and len(
            artistName) > 0, "Artist name cannot be empty"

        # Get the lyrics
        verses = getLyrics(songName, artistName)

        assert verses is not None and len(verses) > 0, "No lyrics found"

        l2i = lyrics2Images.Lyrics2Images(
            num_inference_steps=50, use_auth_token=False, model_id="stabilityai/stable-diffusion-2-1", variant="fp16")

        outputPath = rf"C:\Users\andre\source\repos\AIG\images\{songName} - {artistName}"

        # Run the model
        l2i.run(verses=verses, output_path=outputPath)

    except Exception as e:
        print(f"Error in run(): {e}.\nStack trace: {traceback.format_exc()}")
        return


run()
