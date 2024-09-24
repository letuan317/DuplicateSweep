from termcolor import colored
from pathlib import Path
import os
from collections import defaultdict


def read_gitignore(gitignore_path='.gitignore'):
    """
    Reads a .gitignore file and separates file and folder ignore patterns.
    Returns a dictionary with two keys: 'files' and 'folders'.
    """
    files = []
    folders = []

    if not os.path.exists(gitignore_path):
        return {'files': [], 'folders': []}

    with open(gitignore_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.endswith('/'):
            folders.append(line.rstrip('/'))
        else:
            files.append(line)

    return {'files': files, 'folders': folders}


def is_ignored(file_path, ignored_files, ignored_folders):
    """
    Checks if a given file or folder should be ignored based on .gitignore patterns.
    """
    file_name = file_path.name
    parent_folder = str(file_path.parent)

    if any(folder in parent_folder for folder in ignored_folders):
        return True

    if any(file_name.endswith(pattern.strip('*')) for pattern in ignored_files):
        return True

    return False


def get_all_files(directory, gitignore_data=None, verbose=True):
    """
    Recursively gets all files from the given directory, filtering ignored files and folders.
    """
    if verbose:
        print(colored("[#] Getting all files in the directory:",
              "blue"), colored(directory, "yellow"))

    all_files = []

    if gitignore_data is None:
        gitignore_data = read_gitignore()

    ignored_files = gitignore_data['files']
    ignored_folders = gitignore_data['folders']

    for root, folders, files in os.walk(directory):
        folders[:] = [folder for folder in folders if folder not in ignored_folders]

        for file in files:
            full_path = Path(root) / file

            if is_ignored(full_path, ignored_files, ignored_folders):
                continue

            all_files.append(str(full_path))

    if verbose:
        print(colored("[*] Found", "green"),
              colored(len(all_files), "yellow"), colored("files", "green"))

    return all_files


def get_files_with_size(directory, gitignore_data=None, verbose=True):
    """
    Gets all files with their sizes, filters ignored files and folders, and sorts the result by file size.
    """
    if verbose:
        print(colored("[#] Getting all files with size in the directory:", "blue"), colored(
            directory, "yellow"))

    files_with_size = []

    if gitignore_data is None:
        gitignore_data = read_gitignore()

    ignored_files = gitignore_data['files']
    ignored_folders = gitignore_data['folders']

    for root, folders, files in os.walk(directory):
        folders[:] = [folder for folder in folders if folder not in ignored_folders]

        for file in files:
            full_path = Path(root) / file

            if is_ignored(full_path, ignored_files, ignored_folders):
                continue

            try:
                file_size = full_path.stat().st_size
                files_with_size.append((str(full_path), file_size))
            except OSError as e:
                print(f"Error accessing file {full_path}: {e}")

    files_with_size.sort(key=lambda x: x[1])

    if verbose:
        print(colored("[*] Found", "green"),
              colored(len(files_with_size), "yellow"), colored("files", "green"))

    return files_with_size


def group_files_by_size(directory, gitignore_data=None, verbose=True):
    """
    Groups files by size from the given directory, filtering ignored files and folders.
    Returns a dictionary where keys are file sizes, and values are lists of file paths.
    """
    if verbose:
        print(colored("[#] Grouping files by size in the directory:", "blue"), colored(
            directory, "yellow"))

    files_by_size = defaultdict(list)
    count = 0

    if gitignore_data is None:
        gitignore_data = read_gitignore()

    ignored_files = gitignore_data['files']
    ignored_folders = gitignore_data['folders']

    root_path = Path(directory)

    for file_path in root_path.rglob('*'):
        if is_ignored(file_path, ignored_files, ignored_folders):
            continue

        if file_path.is_file():
            try:
                file_size = file_path.stat().st_size
                files_by_size[file_size].append(str(file_path))
                count += 1
            except OSError as e:
                print(f"Error accessing file {file_path}: {e}")

    if verbose:
        print(colored(f"[*] Found", "green"),
              colored(count, "yellow"), colored("files", "green"))

    return files_by_size
