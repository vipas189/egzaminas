from PIL import Image
from config import Config
import os


def allowed_file(file):
    # Check file extension
    if (
        "." not in file.filename
        or file.filename.rsplit(".", 1)[1].lower() not in Config.ALLOWED_EXTENSIONS
    ):
        return False

    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > Config.MAX_FILE_SIZE_MB * 1024 * 1024:
        return False

    try:
        img = Image.open(file)
        img.verify()
    except Exception:
        return False

    return True
