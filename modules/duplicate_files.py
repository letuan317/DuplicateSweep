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
        print(colored("\n[!] Duplicate files found:", "red"),
              colored(len(duplicate_files_list), "yellow"))

    return duplicate_files_list


def delete_duplicate_files_in_directory(directory, verbose=True, force=False, dry_run=False):
    """
    Deletes duplicate files in a given directory.

    :param directory: The directory to search for duplicates.
    :param verbose: Whether to print detailed information.
    :param force: If True, automatically delete duplicates without confirmation.
    :param dry_run: If True, display duplicates without deleting them.
    :return: A list of deleted files (if any).
    """
    duplicate_files_list = duplicate_files_in_directory(directory, verbose)
    deleted_files = []

    if duplicate_files_list:
        for idx, files in enumerate(duplicate_files_list):
            if verbose:
                print(f"\n{idx + 1}/{len(duplicate_files_list)}",
                      colored(files[0], "cyan"))
                for _file in files[1:]:
                    print(colored(_file, "red"))

            for _file in files[1:]:
                if os.path.exists(_file):
                    if not dry_run:
                        try:
                            os.remove(_file)
                            deleted_files.append(_file)
                            if verbose:
                                print(
                                    colored(f"[-] Deleted", "red"), colored(_file, "light_red"))
                        except OSError as e:
                            print(
                                colored(f"[!] Error deleting {_file}: {e}", "red"))
                    else:
                        if verbose:
                            print(
                                colored(f"[Dry run] {_file} would be deleted", "yellow"))

    if not deleted_files and not dry_run:
        if verbose:
            print(colored("[!] No duplicate files were deleted.", "yellow"))

    return deleted_files
