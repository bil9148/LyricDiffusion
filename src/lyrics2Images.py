import os
from tqdm import tqdm
from utils import auth_hugging_face
import traceback
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from diffusers import AutoPipelineForText2Image
import logging


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
            if len(verse) == 0 or (verse.startswith("[") and verse.endswith("]")):
                logging.info(f"Skipping verse: {verse}")
                return

            # TODO - instead of logging this, show in the UI
            logging.info(f"Verse: {verse}")

            result = pipe(
                prompt=verse, num_inference_steps=self.num_inference_steps)

            assert "images" in result, "Key 'images' not present in the result dictionary."

            # Get the first image from the 'images' key
            image = result['images'][0]
            image.save(f"{output_path}/{index}.png")
        except Exception as e:
            logging.error(
                f"Error in process_verse(): {e}.\nStack trace: {traceback.format_exc()}")

    def run(self, verses: list[str], output_path: str):
        """Runs the model on the given verses and saves the images to the output path"""
        # Load the model pipeline
        pipe = self.load_auto_pipeline()

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        # Run the model on each verse
        with autocast("cuda"):
            for i, verse in enumerate(tqdm(verses)):
                self.process_verse(verse, output_path, i, pipe)