import os
from PIL import Image
import click


@click.command(name="reduce-image-size")
@click.argument("path-to-images")
@click.argument("new_width", default=1900.0)
def reduce_image_size_command(path_to_images: str, new_width: int):
    for root, dirs, files in os.walk(path_to_images):
        for file in files:
            file_path = os.path.join(root, file)
            image = Image.open(file_path)
            file_name, ext = os.path.splitext(file_path)
            output_path = os.path.join(os.path.dirname(file_path), f"{file_name}m.{ext}")
            width, height = image.size
            image = image.resize((int(new_width), int(new_width * height / width)), Image.ANTIALIAS)
            image.save(output_path, optimize=True, quality=95)


if __name__ == "__main__":
    reduce_image_size_command()
