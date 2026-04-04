#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/types/test_ArrayLike.py

"""Tests for scitex_core.types ArrayLike."""

import numpy as np
import pytest

from scitex_core.types import ArrayLike, is_array_like


class TestIsArrayLike:
    """Test is_array_like function."""

    def test_is_array_like_list(self):
        """Test with list."""
        data = [1, 2, 3]
        assert is_array_like(data) is True

    def test_is_array_like_tuple(self):
        """Test with tuple."""
        data = (1, 2, 3)
        assert is_array_like(data) is True

    def test_is_array_like_numpy(self):
        """Test with numpy array."""
        data = np.array([1, 2, 3])
        assert is_array_like(data) is True

    def test_is_array_like_integer(self):
        """Test with integer (not array-like)."""
        data = 42
        assert is_array_like(data) is False

    def test_is_array_like_string(self):
        """Test with string (not array-like)."""
        data = "not an array"
        assert is_array_like(data) is False

    def test_is_array_like_dict(self):
        """Test with dict (not array-like)."""
        data = {"key": "value"}
        assert is_array_like(data) is False

    def test_is_array_like_none(self):
        """Test with None."""
        assert is_array_like(None) is False

    def test_is_array_like_nested_list(self):
        """Test with nested list."""
        data = [[1, 2], [3, 4]]
        assert is_array_like(data) is True

    def test_is_array_like_2d_numpy(self):
        """Test with 2D numpy array."""
        data = np.array([[1, 2], [3, 4]])
        assert is_array_like(data) is True

    def test_is_array_like_empty_list(self):
        """Test with empty list."""
        data = []
        assert is_array_like(data) is True

    def test_is_array_like_empty_tuple(self):
        """Test with empty tuple."""
        data = ()
        assert is_array_like(data) is True

    def test_is_array_like_empty_numpy(self):
        """Test with empty numpy array."""
        data = np.array([])
        assert is_array_like(data) is True


class TestArrayLikeType:
    """Test ArrayLike type hint."""

    def test_function_accepts_list(self):
        """Test function with ArrayLike accepts list."""

        def process(data: ArrayLike) -> int:
            return len(data)

        result = process([1, 2, 3])
        assert result == 3

    def test_function_accepts_tuple(self):
        """Test function with ArrayLike accepts tuple."""

        def process(data: ArrayLike) -> int:
            return len(data)

        result = process((1, 2, 3))
        assert result == 3

    def test_function_accepts_numpy(self):
        """Test function with ArrayLike accepts numpy array."""

        def process(data: ArrayLike) -> int:
            return len(data)

        result = process(np.array([1, 2, 3]))
        assert result == 3


# Skip torch tests if torch not available
@pytest.mark.skipif(
    not _has_torch(), reason="torch not available"
)
class TestArrayLikeTorch:
    """Test is_array_like with torch (if available)."""

    def test_is_array_like_torch_tensor(self):
        """Test with torch tensor."""
        import torch

        data = torch.tensor([1, 2, 3])
        assert is_array_like(data) is True

    def test_is_array_like_torch_2d(self):
        """Test with 2D torch tensor."""
        import torch

        data = torch.tensor([[1, 2], [3, 4]])
        assert is_array_like(data) is True


def _has_torch():
    """Check if torch is available."""
    try:
        import torch

        return True
    except ImportError:
        return False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
