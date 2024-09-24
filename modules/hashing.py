import hashlib
import filecmp
from termcolor import cprint


def hash_file(file_path):
    """Generate SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def compare_files_with_filecmp(file1, file2, verbose=True):
    """
    Compare two files using filecmp.

    Parameters:
    file1 (str): Path to the first file.
    file2 (str): Path to the second file.
    """
    try:
        are_equal = filecmp.cmp(file1, file2, shallow=False)
        if are_equal:
            if verbose:
                cprint("[!] The files are identical.", "yellow")
            return True
        else:
            if verbose:
                cprint("[@] The files are different.", "cyan")
    except Exception as e:
        print(f"Error: {e}")
    return False
