"""Provides common utility functions."""
from django.conf import settings
import os


def media_file_path(prefix=None):
    """return the path for the media file."""
    if prefix:
        return os.path.join(settings.MAKAHIKI_MEDIA_PREFIX, prefix)
    else:
        return settings.MAKAHIKI_MEDIA_PREFIX


def format_usage(usage, rate):
    """format the resource usage to show integer if greater than the rate, otherwise
    show one decimal place."""
    usage = float(usage) / rate

    if usage < 1:
        usage = round(usage, 1)
    else:
        usage = int(round(usage, 0))
    return usage
