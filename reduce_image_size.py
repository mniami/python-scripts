import os
from PIL import Image, ImageOps
import click
import shutil
from typing import Optional

IMAGES_EXTS = ["jpg", "png"]


@click.command(name="reduce-image-size")
@click.argument("path-to-images")
@click.argument("new_width", default=1920)
@click.option("--quality", default=95)
@click.option("--grayscale", is_flag=True)
@click.option("--move-original")
def reduce_image_size_command(
    path_to_images: str,
    new_width: int,
    quality: int,
    grayscale: bool,
    move_original: Optional[str],
):
    for root, _, files in os.walk(path_to_images):
        for file in files:
            file_path = os.path.join(root, file)
            file_name, ext = os.path.splitext(file)
            ext = ext[1:]

            if ext not in IMAGES_EXTS:
                continue

            image = Image.open(file_path)
            output_path = os.path.join(
                os.path.dirname(file_path), f"{file_name}m.{ext}"
            )
            width, height = image.size
            if width > height:
                image = image.resize(
                    (new_width, new_width * height // width), Image.DEFAULT_STRATEGY
                )
            else:
                image = image.resize(
                    (new_width * width // height, new_width), Image.DEFAULT_STRATEGY
                )
            image.save(output_path, optimize=True, quality=quality)

            if grayscale:
                gray_image = ImageOps.grayscale(image)
                gray_image.save(output_path)

            if move_original:
                original_dir_path = os.path.join(root, move_original)
                if not os.path.exists(original_dir_path):
                    os.makedirs(original_dir_path)
                shutil.move(file_path, os.path.join(root, move_original, file))


if __name__ == "__main__":
    reduce_image_size_command()
