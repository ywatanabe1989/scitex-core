#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/types/_ColorLike.py

"""
Color type definitions for scitex-core.

Provides type hints for color specifications commonly used in
scientific visualization.
"""

from typing import List, Tuple, Union


# Define ColorLike type for matplotlib/plotting
ColorLike = Union[
    str,  # Color name or hex code (e.g., "red", "#FF0000")
    Tuple[float, float, float],  # RGB tuple (0-1 range)
    Tuple[float, float, float, float],  # RGBA tuple (0-1 range)
    List[float],  # RGB or RGBA as list
]


__all__ = ["ColorLike"]

# EOF
