import os

from PIL import Image, ImageDraw, ImageFont
from azure.storage.blob import BlobClient

from .helpful_scripts import get_file_path
from core.settings import azureSettings


def _get_index_start_price() -> int:
    """
    Retrieves the hardcoded start price for the index.

    The price is set as of a specific historical date.

    Returns:
        int: The hardcoded start price of the index.
    """
    HARDCODED_VALUE: int = 25
    return HARDCODED_VALUE


def _generate_text_from_config(final_index_config: list) -> dict:
    """
    Generates a text summary of the DeFi index configuration including price changes.

    Processes a list of tokens within the index, computing the total index price and its
    percentage change from the start price.

    Args:
        final_index_config (list): A list of dictionaries with token pricing information.

    Returns:
        str: A string containing formatted information about the DeFi index.
    """
    index_price = sum(token['total_price'] for token in final_index_config)

    start_price = _get_index_start_price()

    print(f'Index price: {index_price}')

    # Calculate percentage change
    percentage = ((index_price - start_price) / start_price) * 100
    profit = index_price - start_price

    return dict(
        current_price=f"${index_price:.2f}",
        profit=f"${profit:.2f}",
        percentage=f"{percentage:.2f}%",
    )


def get_text_metrics(font: ImageFont, text: str) -> dict[str, int]:
    _, descent = font.getmetrics()
    metrics = font.getmask(text=text).getbbox()
    
    return dict(width=metrics[2], height=metrics[3] + descent)


def load_to_blob(image_file: str) -> None:
    blob_client = BlobClient.from_connection_string(
        conn_str=azureSettings.CONNECTION_STRING,
        container_name=azureSettings.CONTAINER_NAME,
        blob_name=azureSettings.BLOB_NAME,
    )

    with open("static/FC10.png", "rb") as f:
        blob_client.upload_blob(f, overwrite=True)


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

    info: dict = _generate_text_from_config(final_index_config)
    image_path: str = get_file_path(image_name)
    img = Image.open(image_path).convert("RGBA")  # Convert image to RGBA mode

    # Create a new image with the same size as the original image
    overlay = Image.new('RGBA', img.size)

    # Initialize ImageDraw for the new image
    draw = ImageDraw.Draw(overlay)

    # Choose a font
    font = ImageFont.truetype(get_file_path("fonts/space_grotesk.ttf"), 150)

    text = info["current_price"]
    text_metrics: dict[str, int] = get_text_metrics(font=font, text=text)

    font.set_variation_by_name(font.get_variation_names()[3])

    # Set the position of the text
    text_x = img.width / 2 - text_metrics["width"] / 2
    text_y = 3 * img.height / 4 - text_metrics["height"] / 2

    # Add text to the new image
    draw.text((text_x, text_y), text, fill="black", font=font)

    font = ImageFont.truetype(get_file_path("fonts/space_grotesk.ttf"), 100)
    font.set_variation_by_name(font.get_variation_names()[2])

    text = "+88$"
    text_metrics: dict[str, int] = get_text_metrics(font=font, text=text)
    text = info["percentage"]

    left_shape_x = (232, 911)
    left_shape_y = (2740, 2963)
    right_shape_x = (1248, 1927)
    right_shape_y = (2740, 2963)

    percent_text_x = left_shape_x[0] + ((left_shape_x[1] - left_shape_x[0]) / 2) - text_metrics["width"] / 2
    percent_text_y = left_shape_y[0] + ((left_shape_y[1] - left_shape_y[0]) / 2) - text_metrics["height"] / 2
    draw.text((percent_text_x, percent_text_y), text, fill=(14, 245, 157, 255), font=font)

    text = info["profit"]
    text_metrics: dict[str, int] = get_text_metrics(font=font, text=text)

    percent_text_x = right_shape_x[0] + ((right_shape_x[1] - right_shape_x[0]) / 2) - text_metrics["width"] / 2
    percent_text_y = right_shape_y[0] + ((right_shape_y[1] - right_shape_y[0]) / 2) - text_metrics["height"] / 2
    draw.text((percent_text_x, percent_text_y), text, fill=(14, 245, 157, 255), font=font)

    # Blend the new image with the original image
    img = Image.alpha_composite(img, overlay)

    # Save the image
    new_image_name: str = f'FC10.png'
    new_image_path: str = get_file_path(new_image_name)
    
    img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    img.save(new_image_path, optimize=True)

    load_to_blob(image_file=new_image_path)

    return new_image_path, new_image_name
