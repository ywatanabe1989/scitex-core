#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/repro/__init__.py

"""
Reproducibility utilities for scientific computing.

This module provides tools for ensuring reproducible scientific experiments:
- Unique ID generation (gen_id)
- Timestamp generation (gen_timestamp)
- Array hashing for verification (hash_array)
- Random state management across libraries (RandomStateManager)
"""

# ID and timestamp generation
from ._gen_id import gen_id, gen_ID
from ._gen_timestamp import gen_timestamp, timestamp

# Array hashing
from ._hash_array import hash_array

# Random state management
from ._RandomStateManager import RandomStateManager, get, reset

__all__ = [
    # ID generation
    "gen_id",
    "gen_ID",  # Backward compatibility
    # Timestamp generation
    "gen_timestamp",
    "timestamp",  # Alias
    # Array hashing
    "hash_array",
    # Random state management
    "RandomStateManager",
    "get",  # Get global instance
    "reset",  # Reset global instance
]

# EOF
