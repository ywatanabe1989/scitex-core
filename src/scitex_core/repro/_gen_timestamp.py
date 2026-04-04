#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/repro/_gen_timestamp.py

"""
Timestamp generation utilities for file naming and versioning.
"""

from datetime import datetime


def gen_timestamp() -> str:
    """
    Generate a timestamp string for file naming.

    Returns a timestamp in the format YYYY-MMDD-HHMM, suitable for
    creating unique filenames or version identifiers.

    Returns
    -------
    str
        Timestamp string in format "YYYY-MMDD-HHMM"

    Examples
    --------
    >>> from scitex_core.repro import gen_timestamp
    >>> timestamp = gen_timestamp()
    >>> print(timestamp)
    '2025-0531-1230'

    >>> filename = f"experiment_{gen_timestamp()}.csv"
    >>> print(filename)
    'experiment_2025-0531-1230.csv'

    Notes
    -----
    - Format: YYYY-MMDD-HHMM (e.g., "2025-0531-1230")
    - Month and day are zero-padded to 2 digits
    - Hour and minute are zero-padded to 2 digits
    - Suitable for filesystem use (no special characters except hyphen)
    """
    return datetime.now().strftime("%Y-%m%d-%H%M")


# Alias for convenience
timestamp = gen_timestamp


__all__ = ["gen_timestamp", "timestamp"]

# EOF
