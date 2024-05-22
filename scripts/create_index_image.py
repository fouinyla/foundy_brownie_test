import os

from PIL import Image, ImageDraw, ImageFont

from .helpful_scripts import get_file_path


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
        index_price += token['total_price'] or 0

    start_price = _get_index_start_price()

    print(f'Index price: {index_price}')

    # Calculate percentage change
    price_change_percentage = ((index_price - start_price) / start_price) * 100
    price_change_str = (
        f"+{price_change_percentage:.2f}" if price_change_percentage >= 0 else f"-{price_change_percentage:.2f}"
    )

    print("index_price", index_price)
    print("start_price", start_price)
    print("price_change_str", price_change_str)
    print("final_index_config", final_index_config)

    # text = f"""
    # DAO Envelop (NIFTSY)

    # DeFi Index for Polygon №1
    # Index Elements: MATIC, NIFTSY

    # The price on the index now: {index_price:.3f} USD
    # The start price of the index: {start_price:.2f} USD
    # Change since start: {price_change_str}%
    # """

    text = f"${index_price:.2f}"
    return text


def get_text_metrics(font: ImageFont, text: str) -> dict[str, int]:
    _, descent = font.getmetrics()
    metrics = font.getmask(text=text).getbbox()
    
    return dict(width=metrics[2], height=metrics[3] + descent)


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
    font = ImageFont.truetype(get_file_path("fonts/space_grotesk.ttf"), 150)
    print("VARIATIONS", font.get_variation_names())

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
    text = "+88%"

    left_shape_x = (232, 911)
    left_shape_y = (2740, 2963)
    right_shape_x = (1248, 1927)
    right_shape_y = (2740, 2963)

    percent_text_x = left_shape_x[0] + ((left_shape_x[1] - left_shape_x[0]) / 2) - text_metrics["width"] / 2
    percent_text_y = left_shape_y[0] + ((left_shape_y[1] - left_shape_y[0]) / 2) - text_metrics["height"] / 2
    draw.text((percent_text_x, percent_text_y), text, fill=(14, 245, 157, 255), font=font)

    text = "+886$"
    text_metrics: dict[str, int] = get_text_metrics(font=font, text=text)

    percent_text_x = right_shape_x[0] + ((right_shape_x[1] - right_shape_x[0]) / 2) - text_metrics["width"] / 2
    percent_text_y = right_shape_y[0] + ((right_shape_y[1] - right_shape_y[0]) / 2) - text_metrics["height"] / 2
    draw.text((percent_text_x, percent_text_y), text, fill=(14, 245, 157, 255), font=font)

    # Blend the new image with the original image
    img = Image.alpha_composite(img, overlay)

    # Save the image
    new_image_name: str = f'index-{image_name}'
    new_image_path: str = get_file_path(new_image_name)
    img.save(new_image_path)
    return new_image_path, new_image_name
