#!/usr/bin/env python3
"""Minimal DotDict implementation for str module."""


class DotDict(dict):
    """
    A dictionary that allows attribute-like access.
    Simplified version for scitex-core.
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
