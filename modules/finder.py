from termcolor import colored
from pathlib import Path
from termcolor import cprint, colored
import os
from collections import defaultdict


def get_all_files(directory, verbose=True):
    if verbose:
        print(colored("[#] Getting all files in the directory:",
                      "blue"), colored(directory, "yellow"))

    """
    Recursively gets all files from the given directory and its subfolders.

    :param directory: The root directory to start the search
    :return: A list of full file paths
    """
    all_files = []

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            # Construct full file path
            full_path = os.path.join(root, file)
            all_files.append(full_path)

    if verbose:
        print(colored("[*] Found", "green"),
              colored(len(all_files), "yellow"), colored("files", "green"))

    return all_files


def get_files_with_size(directory, verbose=True):
    if verbose:
        print(colored("[#] Getting all files with size in the directory:",
                      "blue"), colored(directory, "yellow"))
    """
    Recursively gets all files from the given directory and its subfolders, along with their sizes.
    Files are sorted by size.

    :param directory: The root directory to start the search
    :return: A list of tuples (file_path, file_size) sorted by file size
    """
    files_with_size = []

    # Walk through the directory and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            # Construct full file path
            full_path = os.path.join(root, file)

            # Get the file size
            file_size = os.path.getsize(full_path)

            # Append the file path and size as a tuple
            files_with_size.append((full_path, file_size))

    # Sort files by size (second element in the tuple)
    files_with_size.sort(key=lambda x: x[1])

    if verbose:
        print(colored("[*] Found", "green"),
              colored(len(files_with_size), "yellow"), colored("files", "green"))

    return files_with_size


def group_files_by_size(directory: str, verbose: bool = True) -> dict[int, list[str]]:
    """
    Recursively gets all files from the given directory and its subfolders, groups them by file size.

    :param directory: The root directory to start the search
    :param verbose: Whether to print progress information
    :return: A dictionary where keys are file sizes, and values are lists of file paths with that size
    """
    if verbose:
        print(colored(f"[#] Group files by size in the directory:", "blue"), colored(
            directory, "yellow"))

    files_by_size = defaultdict(list)
    count = 0

    # Using pathlib for clearer and safer path management
    root_path = Path(directory)

    for file_path in root_path.rglob('*'):  # rglob gets all files recursively
        if file_path.is_file():  # Ensure it's a file
            count += 1
            try:
                file_size = file_path.stat().st_size  # Efficient way to get file size
                # Append file path as a string
                files_by_size[file_size].append(str(file_path))
            except OSError as e:
                print(f"Error accessing file {file_path}: {e}")

    if verbose:
        print(colored(f"[*] Found {count} files", "green"))

    return files_by_size
