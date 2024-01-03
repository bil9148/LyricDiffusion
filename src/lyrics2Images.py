import os
from tqdm import tqdm
from utils import auth_hugging_face
import torch
from torch import autocast
# from diffusers import StableDiffusionPipeline
from diffusers import AutoPipelineForText2Image
import lyrics2Images
from lyricExtractor import getLyrics
import settings as settings
from PySide6 import QtWidgets
import gui


class Lyrics2Images:
    def __init__(self,
                 model_id: str = "CompVis/stable-diffusion-v1-4",
                 torch_dtype: torch.dtype = torch.float16,
                 prompt: str = "digital art",
                 num_inference_steps: int = 5,
                 use_auth_token: bool = False,
                 ):
        self.model_id = model_id
        self.torch_dtype = torch_dtype
        self.prompt = prompt
        self.num_inference_steps = num_inference_steps
        self.use_auth_token = use_auth_token

        if self.use_auth_token:
            auth_hugging_face()

    def load_model_pipeline(self) -> AutoPipelineForText2Image:
        pass
        # return StableDiffusionPipeline.from_pretrained(self.model_id,
        #                                                torch_dtype=self.torch_dtype,
        #                                                use_auth_token=self.use_auth_token).to("cuda")

    def load_auto_pipeline(self) -> AutoPipelineForText2Image:
        return AutoPipelineForText2Image.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype).to("cuda")  # , variant=self.variant

    def should_skip_verse(self, verse: str) -> bool:
        return len(verse) == 0 or "[" in verse or "]" in verse or "(" in verse or ")" in verse or "{" in verse or "}" in verse

    def process_verse(self, verse: str, output_path: str, index: int, pipe: AutoPipelineForText2Image, skip_empty_verses):
        try:
            # Skip empty verses
            if skip_empty_verses and self.should_skip_verse(verse):
                settings.logging.info(f"Skipping verse: {verse}")
                return

            result = pipe(
                prompt=verse, num_inference_steps=self.num_inference_steps)

            assert "images" in result, "Key 'images' not present in the result dictionary."

            # Get the first image from the 'images' key
            image = result['images'][0]
            image.save(os.path.join(output_path, f"{index}.png"))
        except Exception as e:
            gui.BasicUI.HandleError(e)

    def generate(self, verses: list[str], output_path: str, uiWidget):
        """Runs the model on the given verses and saves the images to the output path"""
        # Load the model pipeline
        pipe = self.load_auto_pipeline()

        # Create the output directory
        os.makedirs(output_path, exist_ok=True)

        if uiWidget is not None:
            uiWidget.loading_bar.setMaximum(len(verses))
            uiWidget.loading_bar.setValue(0)

        skip_empty_verses = settings.SkipEmptyVerses.getSkipEmptyVerses()

        # Run the model on each verse
        with autocast("cuda"):
            for i, verse in enumerate(tqdm(verses)):

                if uiWidget is not None:
                    uiWidget.textbox_info.setText(verse)
                    uiWidget.loading_bar.setValue(i)

                # Force UI update
                QtWidgets.QApplication.processEvents()

                self.process_verse(verse, output_path, i,
                                   pipe, skip_empty_verses)

        # Update the UI
        if uiWidget is not None:
            uiWidget.loading_bar.setValue(uiWidget.loading_bar.maximum())
            uiWidget.textbox_info.setText("Done")


def run(song_name, artist_name, model_id, num_inference_steps, uiWidget):
    """Runs the program"""
    try:
        # Get the lyrics
        verses = getLyrics(song_name, artist_name, askIfCorrect=True)

        if verses is None or len(verses) == 0:
            return

        l2i = lyrics2Images.Lyrics2Images(
            num_inference_steps=num_inference_steps,
            torch_dtype=torch.float16,
            use_auth_token=False,
            model_id=model_id,
        )

        output_path = os.path.join(
            settings.OutputPath.getOutputPath(), "images", f"{song_name} - {artist_name}")

        settings.logging.info(
            f"Starting generation for {song_name} by {artist_name}.\nModel: {model_id}.\nOutput path: {output_path}\nTorch dtype: {l2i.torch_dtype}\nNum inference steps: {l2i.num_inference_steps}")

        # Run the model
        l2i.generate(verses=verses, output_path=output_path, uiWidget=uiWidget)

    except Exception as e:
        gui.BasicUI.HandleError(e)
