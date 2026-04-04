#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/types/_is_listed_X.py

"""
Type checking utilities for lists of specific types.
"""

from typing import Any, Type, Union

import numpy as np


def is_listed_X(obj: Any, types: Union[Type, tuple, list]) -> bool:
    """
    Check if obj is a list where all elements are of one of the specified types.

    Parameters
    ----------
    obj : Any
        Object to check
    types : type or list/tuple of types
        Type or types to check against

    Returns
    -------
    bool
        True if obj is a list and all elements are of one of the specified types

    Examples
    --------
    >>> from scitex_core.types import is_listed_X
    >>>
    >>> obj = [3, 2, 1, 5]
    >>> is_listed_X(obj, int)  # Returns True
    >>> is_listed_X(obj, (int, float))  # Returns True
    >>> is_listed_X(obj, str)  # Returns False
    >>>
    >>> mixed = [1, "a", 3]
    >>> is_listed_X(mixed, int)  # Returns False
    >>>
    >>> floats = [1.0, 2.0, 3.0]
    >>> is_listed_X(floats, float)  # Returns True

    Notes
    -----
    - Returns False if obj is not a list
    - Returns False if any element doesn't match the specified types
    - Empty lists return True
    """
    try:
        # Check if it's a list
        if not isinstance(obj, list):
            return False

        # Ensure types is a list or tuple
        if not isinstance(types, (list, tuple)):
            types = [types]

        # Check if all elements match one of the types
        conditions = []
        for typ in types:
            conditions.append(np.array([isinstance(o, typ) for o in obj]).all())

        return np.any(conditions)

    except Exception:
        return False


def is_list_of_type(obj: Any, types: Union[Type, tuple, list]) -> bool:
    """
    Check if obj is a list where all elements are of one of the specified types.

    This is an alias for is_listed_X with a more conventional name.

    Parameters
    ----------
    obj : Any
        Object to check
    types : type or list/tuple of types
        Type or types to check against

    Returns
    -------
    bool
        True if obj is a list and all elements are of one of the specified types

    Examples
    --------
    >>> from scitex_core.types import is_list_of_type
    >>>
    >>> numbers = [1, 2, 3, 4]
    >>> is_list_of_type(numbers, int)
    True
    >>>
    >>> mixed = [1, 2.0, "3"]
    >>> is_list_of_type(mixed, (int, float, str))
    False

    See Also
    --------
    is_listed_X : Original function name
    """
    return is_listed_X(obj, types)


__all__ = ["is_listed_X", "is_list_of_type"]

# EOF
