from . import finder, utils, hashing

from termcolor import cprint, colored
import os
from alive_progress import alive_bar


def duplicate_files_in_directory(directory):
    files_by_size = finder.group_files_by_size(directory)

    duplicate_files_list = []

    with alive_bar(len(files_by_size)) as bar:
        for file_size, files in files_by_size.items():
            if len(files) > 1:  # Only show sizes with more than one file

                files = utils.sort_files_by_creation_time(file_list=files)

                keep_file = files[0]
                remain_files = files[1:]
                temp_list = [keep_file]

                for file in remain_files:
                    if hashing.compare_files_with_filecmp(keep_file, file, verbose=False):
                        temp_list.append(file)

                if len(temp_list) > 2:
                    duplicate_files_list.append(temp_list)

                    file_size = os.path.getsize(temp_list[0])
                    print(f"\nFiles with size {file_size} bytes:",
                          utils.convert_size(file_size))

                    for _file in temp_list:
                        print(colored(f" - {_file}", "red"))
            bar()

    if len(duplicate_files_list) == 0:
        cprint("\n[!] No duplicate files found.", "yellow")
        return False
    cprint("\n[!] Duplicate files:", "red")
    for duplicate_files in duplicate_files_list:
        for file in duplicate_files:
            print(colored(f" - {file}", "red"))
        print()
