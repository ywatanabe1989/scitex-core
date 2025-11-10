#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scitex-core: Core infrastructure for the SciTeX ecosystem

Provides shared utilities for logging, error handling, and shell operations.
"""

__version__ = "1.0.0"

# Import main modules
from . import logging
from . import errors
from . import sh

# Export commonly used items
from .errors import (
    SciTeXError,
    SciTeXWarning,
    ConfigurationError,
    ValidationError,
    FileNotFoundError as SciTeXFileNotFoundError,
)

__all__ = [
    "logging",
    "errors",
    "sh",
    "SciTeXError",
    "SciTeXWarning",
    "ConfigurationError",
    "ValidationError",
    "__version__",
]
