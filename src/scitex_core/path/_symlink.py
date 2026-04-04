#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/path/_symlink.py

"""
Symlink creation and management utilities.

Provides comprehensive symbolic link operations including creation,
validation, resolution, and management of broken links.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Union


def symlink(
    src: Union[str, Path],
    dst: Union[str, Path],
    overwrite: bool = False,
    target_is_directory: Optional[bool] = None,
    relative: bool = False,
) -> Path:
    """
    Create a symbolic link pointing to src named dst.

    Parameters
    ----------
    src : str or Path
        Source path (target of the symlink)
    dst : str or Path
        Destination path (the symlink to create)
    overwrite : bool, optional
        If True, remove existing dst before creating symlink
    target_is_directory : bool, optional
        On Windows, specify if target is directory (auto-detected if None)
    relative : bool, optional
        If True, create relative symlink instead of absolute

    Returns
    -------
    Path
        Path object of the created symlink

    Raises
    ------
    FileExistsError
        If dst exists and overwrite=False
    OSError
        If symlink creation fails

    Examples
    --------
    >>> from scitex_core.path import symlink
    >>> # Create absolute symlink
    >>> symlink("/path/to/source", "/path/to/link")

    >>> # Create relative symlink
    >>> symlink("../source", "link", relative=True)

    >>> # Overwrite existing symlink
    >>> symlink("/path/to/new_source", "/path/to/link", overwrite=True)

    Notes
    -----
    - Allows creating symlinks to non-existent targets (valid in Unix/Linux)
    - Automatically creates parent directories if needed
    - On Windows, may require administrator privileges
    """
    src_path = Path(src)
    dst_path = Path(dst)

    # Handle existing destination
    if dst_path.exists() or dst_path.is_symlink():
        if not overwrite:
            raise FileExistsError(f"Destination already exists: {dst_path}")
        else:
            # Remove existing file/symlink
            if dst_path.is_symlink():
                dst_path.unlink()
            elif dst_path.is_file():
                dst_path.unlink()
            elif dst_path.is_dir():
                import shutil
                shutil.rmtree(dst_path)

    # Create parent directory if needed
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine if target is directory (for Windows)
    if target_is_directory is None and src_path.exists():
        target_is_directory = src_path.is_dir()

    # Create symlink
    if relative:
        # Calculate relative path from dst to src
        if src_path.is_absolute():
            try:
                rel_path = os.path.relpath(src_path, dst_path.parent)
                src_for_link = Path(rel_path)
            except ValueError:
                # Can't create relative path (e.g., different drives on Windows)
                src_for_link = src_path.absolute()
        else:
            # Both paths are relative
            src_abs = src_path.resolve()
            dst_parent_abs = dst_path.parent.resolve()
            try:
                rel_path = os.path.relpath(src_abs, dst_parent_abs)
                src_for_link = Path(rel_path)
            except ValueError:
                src_for_link = src_path
    else:
        src_for_link = src_path.absolute()

    dst_path.symlink_to(src_for_link, target_is_directory=target_is_directory)

    return dst_path


def is_symlink(path: Union[str, Path]) -> bool:
    """
    Check if a path is a symbolic link.

    Parameters
    ----------
    path : str or Path
        Path to check

    Returns
    -------
    bool
        True if path is a symlink, False otherwise

    Examples
    --------
    >>> from scitex_core.path import is_symlink
    >>> is_symlink("/path/to/link")
    False
    """
    return Path(path).is_symlink()


def readlink(path: Union[str, Path]) -> Path:
    """
    Return the path to which the symbolic link points.

    Parameters
    ----------
    path : str or Path
        Symlink path to read

    Returns
    -------
    Path
        Path object pointing to the symlink target

    Raises
    ------
    OSError
        If path is not a symlink

    Examples
    --------
    >>> from scitex_core.path import readlink
    >>> target = readlink("/path/to/link")
    >>> print(target)
    """
    path = Path(path)
    if not path.is_symlink():
        raise OSError(f"Path is not a symbolic link: {path}")

    return Path(os.readlink(path))


def resolve_symlinks(path: Union[str, Path]) -> Path:
    """
    Resolve all symbolic links in a path.

    Parameters
    ----------
    path : str or Path
        Path potentially containing symlinks

    Returns
    -------
    Path
        Fully resolved absolute path

    Examples
    --------
    >>> from scitex_core.path import resolve_symlinks
    >>> resolved = resolve_symlinks("/path/with/symlinks")
    >>> print(resolved)
    """
    return Path(path).resolve()


def create_relative_symlink(
    src: Union[str, Path], dst: Union[str, Path], overwrite: bool = False
) -> Path:
    """
    Create a relative symbolic link.

    This is a convenience wrapper around symlink() with relative=True.

    Parameters
    ----------
    src : str or Path
        Source path (target of the symlink)
    dst : str or Path
        Destination path (the symlink to create)
    overwrite : bool, optional
        If True, remove existing dst before creating symlink

    Returns
    -------
    Path
        Path object of the created symlink

    Examples
    --------
    >>> from scitex_core.path import create_relative_symlink
    >>> # Create relative symlink from current dir to parent dir file
    >>> create_relative_symlink("../data/file.txt", "link_to_file")
    """
    return symlink(src, dst, overwrite=overwrite, relative=True)


def unlink_symlink(path: Union[str, Path], missing_ok: bool = True) -> None:
    """
    Remove a symbolic link.

    Parameters
    ----------
    path : str or Path
        Symlink to remove
    missing_ok : bool, optional
        If True, don't raise error if symlink doesn't exist

    Raises
    ------
    FileNotFoundError
        If symlink doesn't exist and missing_ok=False
    OSError
        If path is not a symlink

    Examples
    --------
    >>> from scitex_core.path import unlink_symlink
    >>> unlink_symlink("/path/to/link")
    """
    path = Path(path)

    if not path.exists() and not path.is_symlink():
        if missing_ok:
            return
        raise FileNotFoundError(f"Symlink does not exist: {path}")

    if not path.is_symlink():
        raise OSError(f"Path is not a symbolic link: {path}")

    path.unlink()


def list_symlinks(
    directory: Union[str, Path], recursive: bool = False
) -> List[Path]:
    """
    List all symbolic links in a directory.

    Parameters
    ----------
    directory : str or Path
        Directory to search
    recursive : bool, optional
        If True, search recursively

    Returns
    -------
    list of Path
        List of Path objects for all symlinks found

    Examples
    --------
    >>> from scitex_core.path import list_symlinks, readlink
    >>> symlinks = list_symlinks("/path/to/dir")
    >>> for link in symlinks:
    ...     print(f"{link} -> {readlink(link)}")
    """
    directory = Path(directory)
    symlinks = []

    if recursive:
        for path in directory.rglob("*"):
            if path.is_symlink():
                symlinks.append(path)
    else:
        for path in directory.iterdir():
            if path.is_symlink():
                symlinks.append(path)

    return symlinks


def fix_broken_symlinks(
    directory: Union[str, Path],
    recursive: bool = False,
    remove: bool = False,
    new_target: Optional[Union[str, Path]] = None,
) -> Dict[str, List[Path]]:
    """
    Find and optionally fix broken symbolic links.

    Parameters
    ----------
    directory : str or Path
        Directory to search
    recursive : bool, optional
        If True, search recursively
    remove : bool, optional
        If True, remove broken symlinks
    new_target : str or Path, optional
        If provided, repoint broken symlinks to this target

    Returns
    -------
    dict
        Dictionary with 'found', 'fixed', and 'removed' lists of paths

    Examples
    --------
    >>> from scitex_core.path import fix_broken_symlinks
    >>> # Find broken symlinks
    >>> result = fix_broken_symlinks("/path/to/dir")
    >>> print(f"Found {len(result['found'])} broken symlinks")

    >>> # Remove broken symlinks
    >>> result = fix_broken_symlinks("/path/to/dir", remove=True)
    """
    directory = Path(directory)
    result: Dict[str, List[Path]] = {"found": [], "fixed": [], "removed": []}

    symlinks = list_symlinks(directory, recursive=recursive)

    for link in symlinks:
        try:
            # Check if target exists
            target = Path(os.readlink(link))
            if not link.parent.joinpath(target).exists() and not target.is_absolute():
                # Relative link with non-existent target
                result["found"].append(link)
            elif target.is_absolute() and not target.exists():
                # Absolute link with non-existent target
                result["found"].append(link)
        except (OSError, ValueError):
            result["found"].append(link)

    # Fix or remove broken symlinks
    for link in result["found"]:
        if remove:
            link.unlink()
            result["removed"].append(link)
        elif new_target:
            link.unlink()
            symlink(new_target, link)
            result["fixed"].append(link)

    return result


__all__ = [
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
