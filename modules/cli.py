import argparse
from termcolor import cprint
from modules.duplicate_files import duplicate_files_in_directory, delete_duplicate_files_in_directory


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
        help="Force deletion of duplicate files without confirmation."
    )

    # Dry run mode: show duplicates without deleting them
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which duplicate files would be deleted without actually deleting them."
    )

    # Verbose output
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information during execution."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Display which directory we're scanning
    if args.verbose:
        cprint(f"[*] Scanning directory: {args.source}", "blue")

    # If --delete is specified, delete duplicate files
    if args.delete:
        delete_duplicate_files_in_directory(
            directory=args.source,
            verbose=args.verbose,
            force=args.force,
            dry_run=args.dry_run
        )
    else:
        # Otherwise, just find duplicate files and show them
        duplicate_files_in_directory(
            directory=args.source,
            verbose=args.verbose
        )
