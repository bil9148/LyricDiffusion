import os
from tqdm import tqdm
from utils import auth_hugging_face

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


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

    def load_model_pipeline(self) -> StableDiffusionPipeline:
        return StableDiffusionPipeline.from_pretrained(self.model_id,
                                                       variant=self.variant,
                                                       torch_dtype=self.torch_dtype,
                                                       use_auth_token=self.use_auth_token).to("cuda")

    def runL2I(self, verses: list[str], output_path: str):
        """Runs the model on the given verses and saves the images to the output path"""
        try:
            if verses is None:
                raise Exception("Verses cannot be None")

            # Load the model pipeline
            pipe = self.load_model_pipeline()

            # Create the output folder if it doesn't exist
            if not os.path.exists(output_path):
                os.mkdir(output_path)

            print(verses)

            # Run the model on each verse
            with autocast("cuda"):
                for i in tqdm(range(len(verses))):
                    try:

                        verse = verses[i]

                        print(f"Verse: {verse}")

                        result = pipe(
                            verse, num_inference_steps=self.num_inference_steps)

                        assert "images" in result, "Key 'images' not present in the result dictionary."

                        # Get the first image from the 'images' key
                        image = result['images'][0]
                        image.save(f"{output_path}/{i}.png")
                    except Exception as e:
                        print(f"Error for verse: {verse}\n{e}\n")
                        continue

        except Exception as e:
            print(f"Error in runL2I(): {e}")
            return
