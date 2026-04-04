#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./src/scitex_core/repro/_gen_id.py

"""
Unique identifier generation with timestamps and random components.

Provides utilities for creating reproducible yet unique identifiers
for experiments, runs, and sessions.
"""

import random
import string
from datetime import datetime


def gen_id(time_format: str = "%YY-%mM-%dD-%Hh%Mm%Ss", N: int = 8) -> str:
    """
    Generate a unique identifier with timestamp and random characters.

    Creates a unique ID by combining a formatted timestamp with random
    alphanumeric characters. Useful for creating unique experiment IDs,
    run identifiers, or temporary file names.

    Parameters
    ----------
    time_format : str, optional
        Format string for timestamp portion. Default is "%YY-%mM-%dD-%Hh%Mm%Ss"
        which produces "2025Y-05M-31D-12h30m45s" format.
    N : int, optional
        Number of random characters to append. Default is 8.

    Returns
    -------
    str
        Unique identifier in format "{timestamp}_{random_chars}"

    Examples
    --------
    >>> from scitex_core.repro import gen_id
    >>> id1 = gen_id()
    >>> print(id1)
    '2025Y-05M-31D-12h30m45s_a3Bc9xY2'

    >>> id2 = gen_id(time_format="%Y%m%d", N=4)
    >>> print(id2)
    '20250531_xY9a'

    >>> # For experiment tracking
    >>> exp_id = gen_id()
    >>> save_path = f"results/experiment_{exp_id}.pkl"

    Notes
    -----
    - Random component uses alphanumeric characters (a-z, A-Z, 0-9)
    - Same timestamp will produce different IDs due to random component
    - IDs are suitable for filesystem use (no special characters)
    """
    now_str = datetime.now().strftime(time_format)
    rand_str = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(N)
    )
    return f"{now_str}_{rand_str}"


# Backward compatibility alias
gen_ID = gen_id


__all__ = ["gen_id", "gen_ID"]

# EOF
