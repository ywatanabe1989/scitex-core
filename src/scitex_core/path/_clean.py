#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/path/_clean.py

"""
Path string cleaning and normalization utilities.
"""

import os
from typing import Union
from pathlib import Path


def clean(path_string: Union[str, Path]) -> str:
    """
    Clean and normalize a file system path string.

    Performs the following operations:
    - Converts Path objects to strings
    - Replaces spaces with underscores
    - Normalizes ../ and ./ references
    - Removes duplicate slashes
    - Preserves trailing slash for directories

    Parameters
    ----------
    path_string : str or Path
        File path to clean

    Returns
    -------
    str
        Normalized path string

    Examples
    --------
    >>> from scitex_core.path import clean
    >>> clean('/home/user/./folder/../file.txt')
    '/home/user/file.txt'

    >>> clean('path/./to//file.txt')
    'path/to/file.txt'

    >>> clean('path with spaces')
    'path_with_spaces'

    >>> clean('directory/')
    'directory/'

    Notes
    -----
    - Empty strings return empty string
    - Trailing slashes are preserved to indicate directories
    - Spaces are replaced with underscores for filesystem safety
    """
    # Convert Path objects to strings
    if hasattr(path_string, '__fspath__'):
        path_string = str(path_string)

    if not path_string:
        return ""

    # Remember if path ends with slash (directory indicator)
    is_directory = path_string.endswith("/")

    # Replace spaces with underscores
    path_string = path_string.replace(" ", "_")

    # Normalize path (handles ../ and ./)
    cleaned_path = os.path.normpath(path_string)

    # Remove duplicate slashes
    while "//" in cleaned_path:
        cleaned_path = cleaned_path.replace("//", "/")

    # Restore trailing slash if it was a directory
    if is_directory and not cleaned_path.endswith("/"):
        cleaned_path += "/"

    return cleaned_path


__all__ = ["clean"]

# EOF
