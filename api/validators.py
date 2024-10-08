import os
import mimetypes

from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_cover_image_size(image):
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

        # Resize the image using the new LANCZOS resampling method
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image to an in-memory file
        output = BytesIO()

        # Use original format or fallback to JPEG
        img_format = img.format if img.format else "JPEG"

        img.save(output, format=img_format)
        output.seek(0)

        # Replace the original image with the resized image
        # image = InMemoryUploadedFile(
        #     output,  # The resized image as a file
        #     image.field_name,  # Field name in the form
        #     image.name,  # Original image file name
        #     image.content_type,  # Original content type (e.g., image/jpeg)
        #     output.getbuffer().nbytes,  # Size of the resized image
        #     image.charset,  # Character set of the original file
        # )

        # Get the MIME type based on the file extension using mimetypes module
        mime_type, _ = mimetypes.guess_type(image.name)
        if not mime_type:
            mime_type = "image/jpeg"  # Default to JPEG if MIME type is unknown

        # Create a new InMemoryUploadedFile
        image_name = image.name
        image_file = InMemoryUploadedFile(
            output,  # The resized image as a file
            None,  # Field name, can be None when handling this manually
            image_name,  # Original image file name
            mime_type,  # The detected MIME type (e.g., image/jpeg)
            output.getbuffer().nbytes,  # Size of the resized image
            None,  # Charset can be None for image files
        )

        # Return the resized image
        return image_file

    # Return the original image if it passes all validations
    return image


def validate_image_file_extension(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    if not extension.lower() in valid_extensions:
        raise ValidationError("Unsupported file format!!")
