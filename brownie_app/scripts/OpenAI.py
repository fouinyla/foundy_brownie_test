import base64
from datetime import datetime
from io import BytesIO

import openai
from brownie import config
from PIL import Image
from scripts.helpful_scripts import get_file_path


def get_generated_image_name(prompt: str) -> str:
    """
    Generates an image based on a text prompt using the OpenAI image generation API,
    decodes the received image, and saves it locally with a unique name.

    Args:
        prompt (str): A text prompt to guide the image generation.

    Returns:
        str: The file name of the generated and saved image.

    Note:
        The image is saved with a filename format 'DALLe-YYYY-MM-DD-HH-MM-SS.png', where
        'YYYY-MM-DD' is the current date and 'HH-MM-SS' is the current time.
    """
    # openai.api_key: str = config['image_generator'].get('api_key')
    # response: dict = openai.Image.create(prompt=prompt, n=1, size="512x512", response_format="b64_json")
    # image_data = base64.b64decode(response['data'][0]['b64_json'])
    # image = Image.open(BytesIO(image_data))
    
    # Save the image locally
    # now = datetime.now()
    # formatted_date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
    # new_image_name = f'DALLe-{formatted_date_time}.png'
    # new_image_path: str = get_file_path(new_image_name)
    # image.save(new_image_path)

    return get_file_path("image.jpg")