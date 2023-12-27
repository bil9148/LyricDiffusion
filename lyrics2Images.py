import os
from tqdm import tqdm
from utils import auth_hugging_face

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


class Lyrics2Images:
    def __init__(self,
                 model_id: str = "CompVis/stable-diffusion-v1-4",
                 revision: str = "fp16",
                 torch_dtype: torch.dtype = torch.float16,
                 prompt: str = "digital art",
                 num_inference_steps: int = 50,
                 use_auth_token: bool = False,


                 ):
        self.model_id = model_id
        self.revision = revision
        self.torch_dtype = torch_dtype
        self.prompt = prompt
        self.num_inference_steps = num_inference_steps
        self.use_auth_token = use_auth_token

        if self.use_auth_token:
            auth_hugging_face()

    def load_model_pipeline(self) -> StableDiffusionPipeline:
        return StableDiffusionPipeline.from_pretrained(self.model_id,
                                                       revision=self.revision,
                                                       torch_dtype=self.torch_dtype,
                                                       use_auth_token=self.use_auth_token).to("cuda")

    def runL2I(self, verses: list[str], output_path: str):
        """Runs the model on the given verses and saves the images to the output path"""

        # Load the model pipeline
        pipe = self.load_model_pipeline()

        # Create the output folder if it doesn't exist
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        # Run the model on each verse
        with autocast("cuda"):
            for idx, verse in enumerate(verses):
                result = pipe(
                    verse, num_inference_steps=self.num_inference_steps)

                assert "images" in result, "Key 'images' not present in the result dictionary."

                # Get the first image from the 'images' key
                image = result['images'][0]
                image.save(f"{output_path}/{idx}.png")


def testLyrics2Images():
    l2i = Lyrics2Images()
    verses = ["Nissan R33 GTR",
              "BMW e30"]

    l2i.runL2I(verses=verses,
               output_path=r"C:\Users\andre\source\repos\AIG\images")

    assert os.path.exists(
        r"C:\Users\andre\source\repos\AIG\images\0.png"), "Image 0 does not exist"
    assert os.path.exists(
        r"C:\Users\andre\source\repos\AIG\images\1.png"), "Image 1 does not exist"


testLyrics2Images()
