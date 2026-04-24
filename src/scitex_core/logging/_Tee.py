#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2025-10-13 07:12:49 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex_repo/src/scitex/logging/_Tee.py
# ----------------------------------------
from __future__ import annotations

import os

__FILE__ = "./src/scitex/logging/_Tee.py"
__DIR__ = os.path.dirname(__FILE__)
# ----------------------------------------

THIS_FILE = "/home/ywatanabe/proj/scitex_repo/src/scitex/gen/_tee.py"

"""
Functionality:
    * Redirects and logs standard output and error streams
    * Filters progress bar outputs from stderr logging
    * Maintains original stdout/stderr functionality while logging
Input:
    * System stdout/stderr streams
    * Output file paths for logging
Output:
    * Wrapped stdout/stderr objects with logging capability
    * Log files containing stdout and stderr outputs
Prerequisites:
    * Python 3.6+
    * scitex package for path handling and colored printing
"""

"""Imports"""
import os as _os
import re
import sys
from typing import Any, TextIO


# Inlined simple utilities to avoid external dependencies
def clean_path(path_string: str) -> str:
    """Clean and normalize a file system path."""
    import os

    return os.path.normpath(str(path_string))


def printc(message: str, c: str = "blue", **kwargs):
    """Simple colored print (fallback if colorama not available)."""
    try:
        from colorama import Fore, Style

        colors = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
        }
        color_code = colors.get(c, "")
        print(f"{color_code}{message}{Style.RESET_ALL}")
    except ImportError:
        print(message)


"""Functions & Classes"""


def _get_logger():
    """Get logger lazily to avoid circular import during module initialization."""
    from scitex import logging

    return logging.getLogger(__name__)


class Tee:
    def __init__(self, stream: TextIO, log_path_or_stream, verbose=True) -> None:
        self.verbose = verbose
        self._stream = stream
        # Accept either a filesystem path (str/PathLike) or an open stream.
        if hasattr(log_path_or_stream, "write"):
            self._log_path = getattr(log_path_or_stream, "name", None)
            self._log_file = log_path_or_stream
            self._owns_log_file = False
        else:
            log_path = _os.fspath(log_path_or_stream)
            self._log_path = log_path
            try:
                self._log_file = open(log_path, "w", buffering=1)
                self._owns_log_file = True
                if verbose:
                    logger = _get_logger()
                    stream_name = "stderr" if stream is sys.stderr else "stdout"
                    logger.debug(f"Tee [{stream_name}]: {log_path}")
            except Exception as e:
                printc(f"Failed to open log file {log_path}: {e}", c="red")
                self._log_file = None
                self._owns_log_file = False
        self._is_stderr = stream is sys.stderr

    def write(self, data: Any) -> None:
        self._stream.write(data)
        if self._log_file is not None:
            if self._is_stderr:
                if isinstance(data, str) and not re.match(
                    r"^[\s]*[0-9]+%.*\[A*$", data
                ):
                    self._log_file.write(data)
                    self._log_file.flush()  # Ensure immediate write
            else:
                self._log_file.write(data)
                self._log_file.flush()  # Ensure immediate write

    def flush(self) -> None:
        self._stream.flush()
        if self._log_file is not None:
            self._log_file.flush()

    def isatty(self) -> bool:
        return self._stream.isatty()

    def fileno(self) -> int:
        return self._stream.fileno()

    @property
    def buffer(self):
        return self._stream.buffer

    def close(self):
        """Explicitly close the log file (only if we opened it)."""
        if hasattr(self, "_log_file") and self._log_file is not None:
            try:
                self._log_file.flush()
                if getattr(self, "_owns_log_file", True):
                    self._log_file.close()
                if self.verbose:
                    # Use lazy logger to avoid circular import
                    logger = _get_logger()
                    logger.debug(f"Tee: Closed log file: {self._log_path}")
                self._log_file = None  # Prevent double-close
            except Exception:
                pass

    def __del__(self):
        # Only attempt cleanup if Python is not shutting down
        # This prevents "Exception ignored" errors during interpreter shutdown
        if hasattr(self, "_log_file") and self._log_file is not None:
            try:
                # Check if the file object is still valid
                if hasattr(self._log_file, "closed") and not self._log_file.closed:
                    self.close()
            except Exception:
                # Silently ignore exceptions during cleanup
                pass


class _TeeContext:
    """Context manager that redirects ``sys.stdout`` to a ``Tee``.

    Used by the path-based form of :func:`tee`.
    """

    def __init__(self, path: str, verbose: bool = False) -> None:
        self._path = _os.fspath(path)
        self._verbose = verbose
        self._original_stdout = None
        self._tee = None
        self._file = None

    def __enter__(self):
        self._original_stdout = sys.stdout
        self._file = open(self._path, "w", buffering=1)
        self._tee = Tee(self._original_stdout, self._file, verbose=self._verbose)
        sys.stdout = self._tee
        return self._tee

    def __exit__(self, exc_type, exc, tb):
        try:
            if self._tee is not None:
                try:
                    self._tee.flush()
                except Exception:
                    pass
        finally:
            sys.stdout = self._original_stdout
            if self._file is not None:
                try:
                    self._file.flush()
                    self._file.close()
                except Exception:
                    pass
        return False


def tee(sys_or_path=None, sdir=None, verbose=True):
    """Tee stdout/stderr to files.

    Two calling styles are supported:

    1. ``tee(sys_module, sdir=None)`` — the legacy call that returns
       ``(stdout_tee, stderr_tee)`` wrapping ``sys.stdout`` / ``sys.stderr``.
    2. ``tee(path)`` — context-manager form that redirects ``sys.stdout``
       to a :class:`Tee` writing to both the original stdout and ``path``.

    Example
    -------
    >>> with tee("/tmp/out.log"):
    ...     print("hello")  # printed + logged to /tmp/out.log
    """
    # Path / PathLike / str → context-manager form
    if isinstance(sys_or_path, (str, bytes)) or hasattr(sys_or_path, "__fspath__"):
        return _TeeContext(sys_or_path, verbose=verbose)

    sys = sys_or_path
    import inspect

    ####################
    ## Determine sdir
    ## DO NOT MODIFY THIS
    ####################
    if sdir is None:
        THIS_FILE = inspect.stack()[1].filename
        if "ipython" in THIS_FILE:
            THIS_FILE = f"/tmp/{_os.getenv('USER')}.py"
        sdir = clean_path(_os.path.splitext(THIS_FILE)[0] + "_out")

    sdir = _os.path.join(sdir, "logs/")
    _os.makedirs(sdir, exist_ok=True)

    spath_stdout = sdir + "stdout.log"
    spath_stderr = sdir + "stderr.log"
    sys_stdout = Tee(sys.stdout, spath_stdout)
    sys_stderr = Tee(sys.stderr, spath_stderr)

    if verbose:
        message = f"Standard output/error are being logged at:\n\t{spath_stdout}\n\t{spath_stderr}"
        logger = _get_logger()
        logger.info(message)
        # printc(message)

    return sys_stdout, sys_stderr


if __name__ == "__main__":
    # Argument Parser
    import matplotlib.pyplot as plt
    import scitex

    main = tee

    # import argparse
    # parser = argparse.ArgumentParser(description='')
    # parser.add_argument('--var', '-v', type=int, default=1, help='')
    # parser.add_argument('--flag', '-f', action='store_true', default=False, help='')
    # args = parser.parse_args()
    # Main
    CONFIG, sys.stdout, sys.stderr, plt, CC = scitex.session.start(
        sys, plt, verbose=False
    )
    main(sys, CONFIG["SDIR"])
    scitex.session.close(CONFIG, verbose=False, notify=False)

# EOF
