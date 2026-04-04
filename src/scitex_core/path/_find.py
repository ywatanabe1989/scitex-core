#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/path/_find.py

"""
File and directory search utilities for scitex-core.

Provides Unix find-like functionality for locating files and directories,
with optional git repository detection.
"""

import fnmatch
import os
from typing import List, Optional, Union


def find_git_root(start_path: str = ".") -> Optional[str]:
    """
    Find the root directory of a git repository.

    Parameters
    ----------
    start_path : str, optional
        Starting directory for search. Default is current directory.

    Returns
    -------
    str or None
        Path to git repository root, or None if not in a git repository

    Examples
    --------
    >>> from scitex_core.path import find_git_root
    >>> root = find_git_root()
    >>> print(root)  # e.g., '/home/user/my-project'

    Notes
    -----
    This function searches for a .git directory by walking up the directory tree.
    It does not require the gitpython package.
    """
    current = os.path.abspath(start_path)

    while True:
        git_dir = os.path.join(current, ".git")
        if os.path.isdir(git_dir):
            return current

        parent = os.path.dirname(current)
        if parent == current:  # Reached root directory
            return None
        current = parent


def find_dir(root_dir: str, pattern: Union[str, List[str]] = "*") -> List[str]:
    """
    Find directories matching a pattern.

    Parameters
    ----------
    root_dir : str
        Root directory to start search
    pattern : str or list of str, optional
        Pattern(s) to match directory names. Default is "*" (all).

    Returns
    -------
    list of str
        List of matching directory paths

    Examples
    --------
    >>> from scitex_core.path import find_dir
    >>> dirs = find_dir("/home/user", "test_*")
    >>> dirs = find_dir("/home/user", ["src", "lib"])
    """
    return _find(root_dir, type="d", pattern=pattern)


def find_file(root_dir: str, pattern: Union[str, List[str]] = "*") -> List[str]:
    """
    Find files matching a pattern.

    Parameters
    ----------
    root_dir : str
        Root directory to start search
    pattern : str or list of str, optional
        Pattern(s) to match file names. Default is "*" (all).

    Returns
    -------
    list of str
        List of matching file paths

    Examples
    --------
    >>> from scitex_core.path import find_file
    >>> files = find_file("/home/user", "*.py")
    >>> files = find_file("/home/user", ["*.txt", "*.md"])
    """
    return _find(root_dir, type="f", pattern=pattern)


def _find(
    rootdir: str,
    type: str = "f",
    pattern: Union[str, List[str]] = "*",
    exclude: Optional[List[str]] = None,
) -> List[str]:
    """
    Core find implementation mimicking Unix find command.

    Parameters
    ----------
    rootdir : str
        Root directory to search
    type : str, optional
        Type to search for: 'f' (files), 'd' (directories), or None (both)
    pattern : str or list of str, optional
        Pattern(s) to match names against
    exclude : list of str, optional
        Path patterns to exclude from results

    Returns
    -------
    list of str
        List of matching paths

    Notes
    -----
    Default exclusions: /lib/, /env/, /build/, __pycache__
    """
    if isinstance(pattern, str):
        pattern = [pattern]

    if exclude is None:
        exclude = ["/lib/", "/env/", "/build/", "__pycache__"]

    matches = []

    for pat in pattern:
        for root, dirs, files in os.walk(rootdir):
            # Choose list based on type
            if type == "f":  # Files only
                names = files
            elif type == "d":  # Directories only
                names = dirs
            else:  # All entries
                names = files + dirs

            for name in names:
                # Construct full path
                path = os.path.join(root, name)

                # Pattern matching
                if pat and not fnmatch.fnmatch(name, pat):
                    continue

                # Type checking
                if type == "f" and not os.path.isfile(path):
                    continue
                if type == "d" and not os.path.isdir(path):
                    continue

                # Exclusions
                if any(ex in path for ex in exclude):
                    continue

                matches.append(path)

    return matches


__all__ = ["find_git_root", "find_dir", "find_file"]

# EOF
