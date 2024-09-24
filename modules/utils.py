from termcolor import colored, cprint
import os
from datetime import datetime


def convert_size(size_bytes):
    """
    Convert a file size in bytes to a human-readable format (KB, MB, GB, etc.).

    :param size_bytes: The size in bytes
    :return: A human-readable string representing the size
    """
    if size_bytes == 0:
        return "0B"

    size_units = ["B", "KB", "MB", "GB", "TB", "PB"]
    index = 0

    # Loop to divide the size by 1024 to get the appropriate size unit
    while size_bytes >= 1024 and index < len(size_units) - 1:
        size_bytes /= 1024.0
        index += 1

    # Format to 2 decimal places for readability
    return colored(f"{size_bytes:.2f}", "yellow") + colored(size_units[index], "cyan")


def get_human_readable_time(timestamp):
    """
    Converts a timestamp to a human-readable format.

    :param timestamp: The timestamp to convert
    :return: Human-readable string in the format YYYY-MM-DD HH:MM:SS
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def sort_files_by_creation_time(file_list):
    """
    Sorts a list of files by their creation time.

    :param file_list: List of file paths to be sorted
    :return: List of file paths sorted by creation time
    """
    # Sort the files based on their creation time
    sorted_files = sorted(file_list, key=os.path.getctime)

    return sorted_files
