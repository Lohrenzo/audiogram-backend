import os
from datetime import date
from rest_framework import serializers

from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_dob(dob):
    """Check if the user is at least 18 years old."""
    today = date.today()
    age = today.year - dob.year - (
        (today.month, today.day) < (dob.month, dob.day)
    )

    if age < 18:
        raise serializers.ValidationError("You must be at least 18 years old.")

    return dob


def validate_user_image_size(image):
    """
    Validate and resize the user image if it exceeds the required dimensions.
    """
    max_width = 4032
    max_height = 4032
    max_size = 5 * 1024 * 1024  # 5 MB

    # Check if the image size exceeds the 5MB limit
    if image.size > max_size:
        raise ValidationError("Image size cannot exceed 5MB.")

    # Open the uploaded image using PIL
    img = Image.open(image)
    width, height = img.size

    # Check if image dimensions exceed the allowed size
    if width > max_width or height > max_height:
        # Calculate the resize ratio while maintaining the aspect ratio
        resize_ratio = min(max_width / width, max_height / height)
        new_width = int(width * resize_ratio)
        new_height = int(height * resize_ratio)

        # Resize the image
        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        # Save the resized image to an in-memory file
        output = BytesIO()
        img_format = (
            image.format if image.format else "JPEG"
        )  # Use original format or fallback to JPEG
        img.save(output, format=img_format)
        output.seek(0)

        # Replace the original image with the resized image
        image = InMemoryUploadedFile(
            output,  # The resized image as a file
            image.field_name,  # Field name in the form
            image.name,  # Original image file name
            image.content_type,  # Original content type (e.g., image/jpeg)
            output.getbuffer().nbytes,  # Size of the resized image
            image.charset,  # Character set of the original file
        )

    return image


def validate_image_file_extension(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not extension.lower() in valid_extensions:
        raise ValidationError("Unsupported file format!!")
