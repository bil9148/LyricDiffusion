import logging
from lyricExtractor import getLyrics
import lyrics2Images
import traceback
from logger import configure_logging


def generate(song_name, artist_name, model_id, num_inference_steps):
    """Runs the program"""
    try:
        # Validate the input
        assert song_name and len(song_name) > 0, "Song name cannot be empty"
        assert artist_name and len(
            artist_name) > 0, "Artist name cannot be empty"

        # Get the lyrics
        verses = getLyrics(song_name, artist_name)

        assert verses and len(verses) > 0, "No lyrics found"

        l2i = lyrics2Images.Lyrics2Images(
            num_inference_steps=num_inference_steps,
            use_auth_token=False,
            model_id=model_id,
            variant="fp16"
        )

        output_path = rf"C:\Users\andre\source\repos\AIG\images\{song_name} - {artist_name}"

        # Run the model
        l2i.run(verses=verses, output_path=output_path)

    except Exception as e:
        logging.error(
            f"Error in run(): {e}.\nStack trace: {traceback.format_exc()}")


if __name__ == "__main__":
    configure_logging()
    generate("Gangstas Paradise", "Coolio",
             "stabilityai/stable-diffusion-2-1", 50)
