import os

from PIL import Image, ImageDraw, ImageFont
from scripts.helpful_scripts import get_file_path

FILES_DIRECTORY: str = os.getenv('FILES_DIRECTORY')


def _get_index_start_price() -> int:
    """
    Retrieves the hardcoded start price for the index.

    The price is set as of a specific historical date.

    Returns:
        int: The hardcoded start price of the index.
    """
    HARDCODED_VALUE: int = 0.50  # Price in USD on date - 11.10.2023
    return HARDCODED_VALUE


def _generate_text_from_config(final_index_config: list) -> str:
    """
    Generates a text summary of the DeFi index configuration including price changes.

    Processes a list of tokens within the index, computing the total index price and its 
    percentage change from the start price.

    Args:
        final_index_config (list): A list of dictionaries with token pricing information.

    Returns:
        str: A string containing formatted information about the DeFi index.
    """
    index_price = 0
    for token in final_index_config:
        index_price += token['total_price']

    start_price = _get_index_start_price()

    print(f'Index price: {index_price}')

    # Calculate percentage change
    price_change_percentage = ((index_price - start_price) / start_price) * 100
    price_change_str = f"+{price_change_percentage:.2f}" if price_change_percentage >= 0 else f"-{price_change_percentage:.2f}"

    text = f"""
    DAO Envelop (NIFTSY)

    DeFi Index for Polygon №1
    Index Elements: UNI, 1INCH, KNC

    The price on the index now: {index_price:.3f} USD
    The start price of the index: {start_price:.2f} USD
    Change since start: {price_change_str}%

    UNI price: ${final_index_config[0]['price']:.2f} USD
    1INCH price: ${final_index_config[1]['price']:.2f} USD
    KNC price: ${final_index_config[2]['price']:.2f} USD
    """
    return text


def get_generated_index_image_name(image_name: str, final_index_config: dict) -> str:
    """
    Creates an image with overlay text detailing index configuration and saves it.

    Opens a specified image and overlays it with a semi-transparent rectangle and text
    containing information about the DeFi index. Saves the new image with a modified name.

    Args:
        image_name (str): The name of the base image file.
        final_index_config (dict): The index configuration data used to generate the text.

    Returns:
        str: The path to the saved image.
        str: The name of the new image.
    """

    text: str = _generate_text_from_config(final_index_config)
    image_path: str = get_file_path(image_name)
    img = Image.open(image_path).convert("RGBA")  # Convert image to RGBA mode

    # Create a new image with the same size as the original image
    overlay = Image.new('RGBA', img.size)

    # Initialize ImageDraw for the new image
    draw = ImageDraw.Draw(overlay)

    # Choose a font
    font = ImageFont.truetype("scripts/WorkSans-ExtraBold.ttf", 25)

    # Set the position of the text
    text_x = 0
    text_y = 100

    # Set the width and height of the block
    block_width = 550
    block_height = 380

    # Draw a semi-transparent rectangle on the new image
    draw.rectangle(
        [text_x, text_y, text_x + block_width, text_y + block_height],
        fill=(128, 128, 128, 120)  # Grey color with transparency
    )

    # Add text to the new image
    draw.text((text_x, text_y), text, font=font, fill="white")

    # Blend the new image with the original image
    img = Image.alpha_composite(img, overlay)

    # Save the image
    new_image_name: str = f'index-{image_name}'
    new_image_path: str = get_file_path(new_image_name)
    img.save(new_image_path)
    return new_image_path, new_image_name
