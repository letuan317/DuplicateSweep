import argparse
from termcolor import cprint
from modules import duplicate_files


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Find and delete duplicate files in a directory."
    )

    # Positional argument for the directory path
    parser.add_argument(
        "-s", "--source",
        help="The directory to scan for duplicate files."
    )
    parser.add_argument(
        "-t", "--target",
        help="The target directory to scan for duplicate files."
    )

    # Optional argument to delete duplicate files
    parser.add_argument(
        "-d", "--delete",
        action="store_true",
        help="Delete duplicate files found in the directory."
    )

    # Force deletion without asking for confirmation
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force deletion of duplicate files without confirmation.",
        default=False
    )

    # Verbose output
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information during execution.",
        default=True
    )

    # Parse the arguments
    args = parser.parse_args()

    # Display which directory we're scanning
    if args.verbose:
        cprint(f"[*] Scanning directory: {args.source}", "blue")

    if args.target:
        duplicate_files = duplicate_files.duplicate_files_from_source_directory_with_target_directory(
            source_directory=args.source,
            target_directory=args.target,
            verbose=args.verbose
        )

    elif args.source:
        duplicate_files = duplicate_files.duplicate_files_in_directory(
            directory=args.source,
            verbose=args.verbose
        )

    if duplicate_files and args.delete:
        duplicate_files.delete_duplicate_files(
            duplicate_files_list=duplicate_files,
            verbose=args.verbose,
            force=args.force
        )
