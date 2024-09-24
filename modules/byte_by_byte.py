def compare_files_byte_by_byte(file1, file2):
    """
    Compare two files byte by byte.
    Return True if the files are identical, False if they differ.
    Print where they differ if they are not identical.
    """
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            byte_position = 0
            while True:
                b1 = f1.read(1)
                b2 = f2.read(1)

                # End of both files
                if not b1 and not b2:
                    return True  # Files are identical

                # One file ended before the other
                if b1 != b2:
                    return False  # Files are different

                byte_position += 1
    except Exception as e:
        print(f"Error: {e}")
        return False  # Return False if there's an error
