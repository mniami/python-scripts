from typing import Generator
import os
import imghdr
from PIL import Image
import imagehash

IMAGE_FILE_EXTS = ["jpg", "png", "gif", "jpeg"]


def _is_image_file(file_path: str) -> bool:
    return imghdr.what(file_path) in IMAGE_FILE_EXTS


def find_image_files(path: str) -> Generator[str, None, None]:
    for root_dir, _, files in os.walk(path, topdown=True):
        for file_name in files:
            file_path = os.path.join(root_dir, file_name)

            if _is_image_file(file_path):
                yield file_path


def get_image_hash(file_path: str) -> str:
    with Image.open(file_path) as image:
        hash = str(imagehash.phash(image))
        return hash
