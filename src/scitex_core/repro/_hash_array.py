#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/repro/_hash_array.py

"""
Deterministic array hashing for reproducibility verification.

Provides utilities to compute deterministic hashes of numerical arrays,
useful for verifying data integrity and ensuring reproducibility.
"""

import hashlib

import numpy as np


def hash_array(array_data: np.ndarray) -> str:
    """
    Generate hash for array data.

    Creates a deterministic hash for numpy arrays, useful for
    verifying data integrity and reproducibility.

    Parameters
    ----------
    array_data : np.ndarray
        Array to hash

    Returns
    -------
    str
        16-character hash string

    Examples
    --------
    >>> import numpy as np
    >>> from scitex_core.repro import hash_array
    >>> data = np.array([1, 2, 3, 4, 5])
    >>> hash1 = hash_array(data)
    >>> hash2 = hash_array(data)
    >>> hash1 == hash2
    True

    >>> # Different data produces different hash
    >>> data2 = np.array([1, 2, 3, 4, 6])
    >>> hash3 = hash_array(data2)
    >>> hash1 != hash3
    True

    Notes
    -----
    - Uses SHA-256 hashing algorithm
    - Returns first 16 characters of hex digest
    - Same array will always produce same hash
    - Useful for detecting changes in data
    """
    # Include shape and dtype in the hash so that arrays with the same
    # flat content but different shapes/dtypes produce different hashes.
    shape_bytes = str(array_data.shape).encode("utf-8")
    dtype_bytes = str(array_data.dtype).encode("utf-8")
    data_bytes = array_data.tobytes()
    hasher = hashlib.sha256()
    hasher.update(shape_bytes)
    hasher.update(b"|")
    hasher.update(dtype_bytes)
    hasher.update(b"|")
    hasher.update(data_bytes)
    return hasher.hexdigest()[:16]


__all__ = ["hash_array"]

# EOF
