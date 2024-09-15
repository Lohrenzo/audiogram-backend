import os

from datetime import datetime
from django.utils.text import slugify


def rename_image(instance, filename):
    """
    Rename the image file based on the user's first name or username
    """
    base_filename, file_extension = os.path.splitext(filename)
    new_filename = slugify(
        instance.username or instance.first_name
    )  # Use slugified username or first name if username is unavailable
    new_filename = (
        f"{new_filename}_{datetime.now().strftime('%Y%m%d%H%M%S')}{file_extension}"
    )
    return f"img/account/{new_filename}"  # Path to save image
