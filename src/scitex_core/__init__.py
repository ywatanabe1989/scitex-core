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

from __future__ import annotations

import warnings

try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _v

    try:
        __version__ = _v("scitex-core")
    except PackageNotFoundError:
        __version__ = "0.0.0+local"
    del _v, PackageNotFoundError
except ImportError:  # pragma: no cover — only on ancient Pythons
    __version__ = "0.0.0+local"

warnings.warn(
    "scitex-core is deprecated and will be removed. Every submodule has "
    "moved to its own standalone peer: scitex_logging, scitex_dict, "
    "scitex_str, scitex_path, scitex_repro, scitex_parallel, "
    "scitex_types, scitex_sh, scitex_datetime (formerly scitex_core.dt). "
    "scitex_core.errors will be relocated; pin scitex-core for now if you "
    "rely on it. Migrate to the standalones (or use the `scitex` umbrella "
    "which routes scitex.<short> directly to the peer).",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export main modules for convenient imports
from . import dict, dt, errors, logging, parallel, path, repro, sh, str, types

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
