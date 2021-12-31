import os
from PIL import Image
import click


@click.command()
@click.argument("path-to-image")
@click.argument("color-format")
def convert(path_to_image: str, color_format: str):
    image = Image.open(path_to_image)
    file_name, _ = os.path.splitext(path_to_image)
    output_path = os.path.join(
        os.path.dirname(path_to_image), f"{file_name}_{color_format}.jpg"
    )

    if image.format == "PNG":
        image = image.convert(color_format)
        image.save(output_path, "JPEG")
        return

    if image.format == color_format:
        raise ValueError("No need to convert")
    image = image.convert(color_format)
    image.save(output_path)


if __name__ == "__main__":
    convert()
