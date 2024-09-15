import re
import time


def format_title(title):
    """
    Replace spaces with underscores and limit the title to 20 characters.
    """
    return re.sub(r"\s+", "_", title.lower())[:20]


def get_timestamp():
    """
    Get the current timestamp in seconds.
    """
    return str(int(time.time()))


def album_cover_upload_path(instance, filename):
    """
    Generate the file path for the album cover image.
    The filename will be based on the formatted title of the album
    and the current timestamp.
    """
    formatted_title = format_title(instance.title)
    timestamp = get_timestamp()  # Get the current timestamp
    extension = filename.split(".")[-1]  # Get the file extension
    return f"album_covers/{formatted_title}_{timestamp}.{extension.lower()}"


def audio_cover_upload_path(instance, filename):
    """
    Generate the file path for the audio cover image.
    The filename will be based on the formatted title of the audio
    and the current timestamp.
    """
    formatted_title = format_title(instance.title)
    timestamp = get_timestamp()  # Get the current timestamp
    extension = filename.split(".")[-1]  # Get the file extension
    return f"audio_covers/{formatted_title}_{timestamp}.{extension.lower()}"


def audio_file_upload_path(instance, filename):
    """
    Generate the file path for the audio file.
    The filename will be based on the formatted title of the audio
    and the current timestamp.
    """
    formatted_title = format_title(instance.title)
    timestamp = get_timestamp()  # Get the current timestamp
    extension = filename.split(".")[-1]  # Get the file extension
    return f"audios/{formatted_title}_{timestamp}.{extension.lower()}"
