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
- types: Shared type definitions
"""

__version__ = "0.1.1"

# Re-export main modules for convenient imports
from . import errors
from . import logging
from . import sh
from . import str

__all__ = ["errors", "logging", "sh", "str", "__version__"]

# EOF
