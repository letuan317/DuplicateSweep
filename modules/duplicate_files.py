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
        return []

    if verbose:
        print(colored("\n[!] Duplicate files found:", "red"),
              colored(len(duplicate_files_list), "yellow"))

    return duplicate_files_list


def duplicate_files_from_source_directory_with_target_directory(source_directory, target_directory, verbose=True):
    """
    Identifies duplicate files from source directory with target directory, if duplicate, delete source file

    :param source_directory: The directory to search for duplicates.
    :param target_directory: The directory to move the duplicate files to.
    :param verbose: Whether to print detailed information.
    :return: A list of moved files (if any).
    """
    source_files = finder.get_all_files(source_directory)
    target_files_by_size = finder.group_files_by_size(target_directory)

    duplicate_files_list = []

    with alive_bar(len(source_files)) as bar:
        for source_file in source_files:
            print(colored(f"[>] Checking", "blue"),
                  colored(source_file, "cyan"))

            source_file_size = os.path.getsize(source_file)

            if target_files_by_size.get(source_file_size):
                _target_files = target_files_by_size[source_file_size]

                for _target_file in _target_files:
                    try:
                        if filecmp.cmp(source_file, _target_file, shallow=False):
                            duplicate_files_list.append(
                                [_target_file, source_file])
                            print(colored("[+] Duplicate file found:", "red"),
                                  colored(_target_file, "cyan"), "\n")
                            break
                    except Exception as e:
                        cprint(
                            f"Error comparing files {source_file} and {_target_file}: {e}", "red")
            bar()

    if len(duplicate_files_list) == 0:
        cprint("\n[!] No duplicate files found.", "yellow")
    else:
        print(colored("\n[!] Duplicate files found:", "red"),
              colored(len(duplicate_files_list), "yellow"))

    return duplicate_files_list


def delete_duplicate_files(duplicate_files_list, verbose=True, force=False):
    """
    Deletes duplicate files in a given duplicate_files_list. Will keep first file in the list. and all other files will be deleted.

    :param directory: The directory to search for duplicates.
    :param verbose: Whether to print detailed information.
    :param force: If True, automatically delete duplicates without confirmation.
    :return: A list of deleted files (if any).
    """

    for idx, files in enumerate(duplicate_files_list):
        print(f"\n{idx + 1}/{len(duplicate_files_list)}",
              colored(files[0], "cyan"))

        delete_files = files[1:]
        for _file in delete_files:
            print(colored(_file, "red"))

        if not force:
            confirm = input(
                colored(
                    "[?] Are you sure you want to delete these files? (y/N) ", "blue")
            )

            if confirm.lower() != "y":
                continue

        for _file in delete_files:
            if os.path.exists(_file):
                try:
                    os.remove(_file)
                    if verbose:
                        print(
                            colored(f"[-] Deleted", "red"), colored(_file, "light_red"))
                except OSError as e:
                    print(
                        colored(f"[!] Error deleting {_file}: {e}", "red"))
