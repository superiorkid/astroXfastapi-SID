import os
import shutil

from fastapi import UploadFile


def check_content_type(content_type: str) -> bool:
    valid_image_types = ["image/jpeg", "image/png", "image/jpg", "image/webp", "image/avif"]
    if content_type not in valid_image_types:
        return False

    return True


def check_file_size(file_size: int) -> bool:
    if file_size > 2 * 1024 * 1024:
        return False

    return True


async def save_image(cover: UploadFile, destination: str) -> str:
    upload_dir = os.path.join(os.getcwd(), destination)

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    dest = os.path.join(upload_dir, cover.filename)

    with open(dest, "wb") as buffer:
        shutil.copyfileobj(cover.file, buffer)

    return dest

