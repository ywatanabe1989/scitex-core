#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/path/__init__.py

"""
File path and directory utilities for scitex-core.

This module provides comprehensive path manipulation, file/directory search,
symbolic link management, and path normalization utilities.
"""

# Find utilities
from ._find import find_dir, find_file, find_git_root

# Path utilities
from ._this_path import get_this_path, this_path

# Path cleaning
from ._clean import clean

# Symlink utilities
from ._symlink import (
    create_relative_symlink,
    fix_broken_symlinks,
    is_symlink,
    list_symlinks,
    readlink,
    resolve_symlinks,
    symlink,
    unlink_symlink,
)

__all__ = [
    # Find utilities
    "find_dir",
    "find_file",
    "find_git_root",
    # Path utilities
    "this_path",
    "get_this_path",
    # Path cleaning
    "clean",
    # Symlink utilities
    "symlink",
    "is_symlink",
    "readlink",
    "resolve_symlinks",
    "create_relative_symlink",
    "unlink_symlink",
    "list_symlinks",
    "fix_broken_symlinks",
]

# EOF
