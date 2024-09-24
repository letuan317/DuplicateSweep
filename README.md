# DuplicateSweep

Scan duplicate files

```
DuplicateFinder/
│
├── src/                # Source code directory
│   ├── __init__.py     # Marks the directory as a Python package
│   ├── cli.py          # Command-line interface implementation
│   ├── finder.py       # Core logic for finding duplicate files
│   ├── hashing.py      # Functions related to file hashing
│   ├── metadata.py     # Functions for metadata comparison (size, timestamps)
│   ├── utils.py        # Utility functions (logging, error handling, etc.)
│   ├── file_comparer.py# Byte-by-byte comparison logic
│   └── config.py       # Configuration handling (settings, paths, etc.)
│
├── tests/              # Unit and integration tests
│   ├── test_finder.py  # Tests for duplicate finding logic
│   ├── test_hashing.py # Tests for hashing logic
│   ├── test_metadata.py# Tests for metadata comparison
│   └── test_utils.py   # Tests for utility functions
│
├── data/               # Optional folder for any test data
│   └── sample_files/   # Sample files for testing purposes
│
├── logs/               # Log files (if applicable)
│
├── scripts/            # Optional folder for any utility scripts
│   └── clean_logs.sh   # Script to clean old logs (example)
│
├── docs/               # Documentation for the project
│   └── usage.md        # Instructions on how to use the tool
│
├── requirements.txt    # Python dependencies for the project
├── README.md           # Project overview and setup instructions
├── setup.py            # Script for packaging and installation (if applicable)
└── LICENSE             # License file for the project
```

# Methods

- Get all files
- Get files with sizes
-
