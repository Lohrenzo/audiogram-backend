import os
from datetime import date
from rest_framework import serializers

from django.core.exceptions import ValidationError
from PIL import Image


def validate_dob(dob):
    """Check if the user is at least 18 years old."""
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    if age < 18:
        raise serializers.ValidationError("You must be at least 18 years old.")

    return dob


def validate_user_image_size(image):
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
