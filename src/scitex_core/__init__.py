#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/__init__.py

"""
scitex-core: Core infrastructure for the SciTeX ecosystem.

Provides foundational utilities used across all SciTeX packages:
- logging: Enhanced logging with colored output and file support
- errors: Common error classes with rich context
- sh: Safe shell command execution
- str: String utilities including ANSI color formatting
- path: File path and directory utilities
- repro: Reproducibility utilities (ID generation, random state management)
- types: Shared type definitions and validators
"""

try:
    from importlib.metadata import version as _v, PackageNotFoundError
    try:
        __version__ = _v("scitex-core")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"
# Re-export main modules for convenient imports
from . import errors
from . import logging
from . import path
from . import repro
from . import sh
from . import str
from . import types
from . import dict
from . import parallel
from . import dt

__all__ = [
    "errors",
    "logging",
    "path",
    "repro",
    "sh",
    "str",
    "types",
    "dict",
    "parallel",
    "dt",
    "__version__",
]

# EOF
