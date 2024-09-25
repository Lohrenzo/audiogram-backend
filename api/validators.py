import os

from django.core.exceptions import ValidationError
from PIL import Image

# from io import BytesIO


def validate_cover_image_size(image):
    """
    Validate the size of the cover image.
    """
    max_width = 4032
    max_height = 4032
    max_size = 5 * 1024 * 1024  # 5 MB

    if image.size > max_size:
        raise ValidationError("Image size cannot exceed 5MB.")

    # Open the uploaded image using PIL
    img = Image.open(image)
    width, height = img.size

    if width > max_width or height > max_height:
        raise ValidationError(
            "Image dimensions cannot exceed 4032 X 4032 pixels.",
        )

    return image


def validate_image_file_extension(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not extension.lower() in valid_extensions:
        raise ValidationError("Unsupported file format!!")
