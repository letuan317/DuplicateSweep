from . import finder, utils

from termcolor import cprint, colored
from alive_progress import alive_bar
import filecmp
import os


def duplicate_files_in_directory(directory, verbose=True):
    """
    Identifies duplicate files in a given directory by comparing file sizes and content.

    :param directory: The directory to search for duplicates.
    :param verbose: Whether to print detailed information.
    :return: A list of lists, where each inner list contains duplicate files.
    """
    files_by_size = finder.group_files_by_size(directory)
    duplicate_files_list = []

    if verbose:
        print(colored(
            f"[#] Scanning {len(files_by_size)} file groups for duplicates.", "blue"))

    with alive_bar(len(files_by_size)) as bar:
        for file_size, files in files_by_size.items():
            if len(files) > 1:  # Only consider files with matching sizes
                # Sort files by creation time (oldest first)
                files = utils.sort_files_by_creation_time(file_list=files)

                keep_file = files[0]
                remain_files = files[1:]
                temp_list = [keep_file]

                for file in remain_files:
                    try:
                        # Compare files using hashing or filecmp
                        if filecmp.cmp(keep_file, file, shallow=False):
                            temp_list.append(file)
                    except Exception as e:
                        cprint(
                            f"Error comparing files {keep_file} and {file}: {e}", "red")

                if len(temp_list) >= 2:  # Consider it a duplicate set if there are at least 2 files
                    duplicate_files_list.append(temp_list)

                    if verbose:
                        file_size = os.path.getsize(temp_list[0])
                        print(
                            f"\nFiles with size {file_size} bytes: {utils.convert_size(file_size)}")
                        for _file in temp_list:
                            print(colored(f" - {_file}", "red"))
            bar()

    if len(duplicate_files_list) == 0:
        if verbose:
            cprint("\n[!] No duplicate files found.", "yellow")
        return False

    if verbose:
        cprint("\n[!] Duplicate files found:", "red")
        for duplicate_files in duplicate_files_list:
            for file in duplicate_files:
                print(colored(f" - {file}", "red"))
            print()

    return duplicate_files_list
