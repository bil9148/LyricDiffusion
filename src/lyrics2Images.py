import os
from tqdm import tqdm
from utils import auth_hugging_face
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from diffusers import AutoPipelineForText2Image
import logging
import lyrics2Images
import traceback
from lyricExtractor import getLyrics
from output import OUTPUT_PATH
from PySide6 import QtWidgets


class Lyrics2Images:
    def __init__(self,
                 model_id: str = "CompVis/stable-diffusion-v1-4",
                 variant: str = "fp16",
                 torch_dtype: torch.dtype = torch.float16,
                 prompt: str = "digital art",
                 num_inference_steps: int = 50,
                 use_auth_token: bool = False,
                 ):
        self.model_id = model_id
        self.variant = variant
        self.torch_dtype = torch_dtype
        self.prompt = prompt
        self.num_inference_steps = num_inference_steps
        self.use_auth_token = use_auth_token

        if self.use_auth_token:
            auth_hugging_face()

    def load_model_pipeline(self) -> AutoPipelineForText2Image:
        return StableDiffusionPipeline.from_pretrained(self.model_id,
                                                       variant=self.variant,
                                                       torch_dtype=self.torch_dtype,
                                                       use_auth_token=self.use_auth_token).to("cuda")

    def load_auto_pipeline(self) -> AutoPipelineForText2Image:
        return AutoPipelineForText2Image.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype, variant=self.variant, use_auth_token=self.use_auth_token).to("cuda")

    def process_verse(self, verse: str, output_path: str, index: int, pipe: AutoPipelineForText2Image):
        try:
            # Skip empty verses
            if len(verse) == 0 or (verse.startswith("[") and verse.endswith("]")):
                logging.info(f"Skipping verse: {verse}")
                return

            result = pipe(
                prompt=verse, num_inference_steps=self.num_inference_steps)

            assert "images" in result, "Key 'images' not present in the result dictionary."

            # Get the first image from the 'images' key
            image = result['images'][0]
            image.save(os.path.join(output_path, f"{index}.png"))
        except Exception as e:
            logging.error(
                f"Error in process_verse(): Verse: {verse}\n Exception: {e}.\nStack trace: {traceback.format_exc()}")

    def generate(self, verses: list[str], output_path: str, loading_bar, textbox_info):
        """Runs the model on the given verses and saves the images to the output path"""
        # Load the model pipeline
        pipe = self.load_auto_pipeline()

        # Create the output directory
        os.makedirs(output_path, exist_ok=True)

        if loading_bar is not None:
            # Set max value for the loading bar
            loading_bar.setMaximum(len(verses))
            loading_bar.setValue(0)

        # Run the model on each verse
        with autocast("cuda"):
            for i, verse in enumerate(tqdm(verses)):
                if textbox_info is not None:
                    # Update the textbox
                    textbox_info.setText(verse)

                if loading_bar is not None:
                    # Update the loading bar
                    loading_bar.setValue(i)

                # Force UI update
                QtWidgets.QApplication.processEvents()

                self.process_verse(verse, output_path, i, pipe)

        # Update the UI
        if loading_bar is not None:
            loading_bar.setValue(loading_bar.maximum())

        if textbox_info is not None:
            textbox_info.setText("Done")


def run(song_name, artist_name, model_id, num_inference_steps, loading_bar, textbox_info):
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

        output_path = os.path.join(
            OUTPUT_PATH, "images", f"{song_name} - {artist_name}")

        logging.info(
            f"Starting generation for {song_name} - {artist_name}.\nModel: {model_id}.\nOutput path: {output_path}\nTorch dtype: {l2i.torch_dtype}\nVariant: {l2i.variant}\nNum inference steps: {l2i.num_inference_steps}")

        # Run the model
        l2i.generate(verses=verses, output_path=output_path,
                     loading_bar=loading_bar, textbox_info=textbox_info)

    except Exception as e:
        logging.error(
            f"Error in run(): {e}.\nStack trace: {traceback.format_exc()}")
