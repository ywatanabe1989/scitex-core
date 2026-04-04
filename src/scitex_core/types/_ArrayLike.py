#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/types/_ArrayLike.py

"""
Array-like type definitions for scitex-core.

Provides type hints and validators for array-like objects commonly
used in scientific computing.
"""

from typing import List, Tuple, Union

import numpy as np


# Core array-like types (no heavy dependencies like pandas/xarray)
ArrayLike = Union[
    List,
    Tuple,
    np.ndarray,
]


def is_array_like(obj) -> bool:
    """
    Check if object is array-like.

    Checks for basic array-like types including lists, tuples, numpy arrays,
    and PyTorch tensors (if available).

    Parameters
    ----------
    obj : Any
        Object to check

    Returns
    -------
    bool
        True if object is array-like, False otherwise

    Examples
    --------
    >>> from scitex_core.types import is_array_like
    >>> import numpy as np
    >>>
    >>> is_array_like([1, 2, 3])
    True
    >>> is_array_like((1, 2, 3))
    True
    >>> is_array_like(np.array([1, 2, 3]))
    True
    >>> is_array_like(42)
    False

    Notes
    -----
    - Checks PyTorch tensors lazily to avoid import overhead
    - Does not include pandas/xarray to keep scitex-core lightweight
    - For pandas/xarray support, use the full scitex package
    """
    # First check against standard types
    is_standard_array = isinstance(obj, (list, tuple, np.ndarray))

    if is_standard_array:
        return True

    # Check torch tensor lazily to avoid circular imports
    try:
        import torch

        return torch.is_tensor(obj)
    except (ImportError, RuntimeError):
        return False


__all__ = ["ArrayLike", "is_array_like"]

# EOF
