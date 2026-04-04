#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/path/_this_path.py

"""
Utilities for getting the path of the currently executing script.

Useful for scripts that need to reference files relative to their own location.
"""

import inspect
from typing import Optional


def this_path(ipython_fake_path: str = "/tmp/ipython_fake.py") -> str:
    """
    Get the absolute path of the calling script.

    Parameters
    ----------
    ipython_fake_path : str, optional
        Fallback path to use when running in IPython/Jupyter.
        Default is "/tmp/ipython_fake.py"

    Returns
    -------
    str
        Absolute path to the calling script

    Examples
    --------
    >>> from scitex_core.path import this_path
    >>> # In a script at /home/user/scripts/my_script.py:
    >>> script_path = this_path()
    >>> print(script_path)  # '/home/user/scripts/my_script.py'

    >>> # Use it to find files relative to the script
    >>> import os
    >>> script_dir = os.path.dirname(this_path())
    >>> config_path = os.path.join(script_dir, "config.yaml")

    Notes
    -----
    - Uses inspect.stack() to get the caller's filename
    - Handles IPython/Jupyter environments by returning fake path
    - Returns the caller's file path, not this module's path
    """
    # Get caller's frame (one level up the stack)
    frame = inspect.stack()[1]
    caller_file = frame.filename

    # Check if running in IPython/Jupyter
    if "ipython" in caller_file.lower() or "<" in caller_file:
        return ipython_fake_path

    return caller_file


# Alias for backward compatibility
get_this_path = this_path


__all__ = ["this_path", "get_this_path"]

# EOF
