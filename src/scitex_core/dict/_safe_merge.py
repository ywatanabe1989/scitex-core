#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: "ywatanabe (2024-11-03 00:47:50)"
# File: ./scitex_repo/src/scitex/dict/_safe_merge.py

"""
Functionality:
    - Safely merges multiple dictionaries without overlapping keys
Input:
    - Multiple dictionaries to be merged
Output:
    - A single merged dictionary
Prerequisites:
    - None (stdlib only)
"""

from typing import Any as _Any
from typing import Dict


def safe_merge(*dicts: Dict[_Any, _Any]) -> Dict[_Any, _Any]:
    """Merges dictionaries while checking for key conflicts.

    Example
    -------
    >>> dict1 = {'a': 1, 'b': 2}
    >>> dict2 = {'c': 3, 'd': 4}
    >>> safe_merge(dict1, dict2)
    {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    Parameters
    ----------
    *dicts : Dict[_Any, _Any]
        Variable number of dictionaries to merge

    Returns
    -------
    Dict[_Any, _Any]
        Merged dictionary

    Raises
    ------
    ValueError
        If overlapping keys are found between dictionaries
    """
    try:
        merged_dict: Dict[_Any, _Any] = {}
        for current_dict in dicts:
            # Check for overlapping keys using set intersection
            overlap = set(merged_dict.keys()) & set(current_dict.keys())
            if overlap:
                raise ValueError(
                    f"Overlapping keys found between dictionaries: {overlap}"
                )
            merged_dict.update(current_dict)
        return merged_dict
    except Exception as error:
        raise ValueError(f"Dictionary merge failed: {str(error)}")


# EOF
