import requests
import json
from io import BytesIO
from PIL import Image

url = "https://stablediffusionapi.com/api/v3/text2img"

prompt = "bmw e30"

payload = json.dumps({
    "key": "ox0GRrT64bbFQaKlcCoROtbLaIgUnLxQ46t4uBJMq2IW6rgUx3FqTOHjNe9V",
    "prompt": prompt,
    "negative_prompt": None,
    "width": "512",
    "height": "512",
    "samples": "1",
    "num_inference_steps": "20",
    "seed": None,
    "guidance_scale": 7.5,
    "safety_checker": "yes",
    "multi_lingual": "no",
    "panorama": "no",
    "self_attention": "no",
    "upscale": "no",
    "embeddings_model": None,
    "webhook": None,
    "track_id": None
})

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
result = response.json()

if "output" in result and len(result["output"]) > 0:
    # Get the URL of the generated image
    image_url = result["output"][0]

    # Download the image
    image_response = requests.get(image_url)

    # Check if the request was successful (status code 200)
    if image_response.status_code == 200:
        # Open the image using PIL (Python Imaging Library)
        image = Image.open(BytesIO(image_response.content))

        # Save the image to a local file
        image.save("generated_image.png")

        print("Image saved successfully.")
    else:
        print(
            f"Failed to download image. Status code: {image_response.status_code}")
else:
    print("No 'output' field in the API response.")
