#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/types/_is_listed_X.py

"""
Type checking utilities for lists of specific types.
"""

from typing import Any, Type, Union


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

        # Ensure types is a tuple (isinstance accepts tuple of types)
        if isinstance(types, list):
            type_tuple = tuple(types)
        elif isinstance(types, tuple):
            type_tuple = types
        else:
            type_tuple = (types,)

        # Each element must be an instance of at least one of the allowed types.
        return all(isinstance(o, type_tuple) for o in obj)

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
