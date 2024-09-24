
from modules import duplicate_files

import sys

if __name__ == "__main__":
    directory = sys.argv[1]
    duplicate_files.duplicate_files_in_directory(directory)
