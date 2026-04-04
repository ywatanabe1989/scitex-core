#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/types/__init__.py

"""
Type definitions and type checking utilities for scitex-core.

This module provides:
- ArrayLike: Type hint for array-like objects (lists, tuples, numpy arrays)
- ColorLike: Type hint for color specifications (strings, RGB/RGBA tuples)
- Type checking utilities for validating list element types
"""

from ._ArrayLike import ArrayLike, is_array_like
from ._ColorLike import ColorLike
from ._is_listed_X import is_list_of_type, is_listed_X

__all__ = [
    # Type definitions
    "ArrayLike",
    "ColorLike",
    # Type validators
    "is_array_like",
    "is_list_of_type",
    "is_listed_X",
]

# EOF
