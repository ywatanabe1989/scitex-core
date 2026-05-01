#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/repro/test_hash_array.py

"""Tests for scitex_core.repro hash_array utilities."""

import numpy as np
import pytest

from scitex_core.repro import hash_array


class TestHashArray:
    """Test hash_array function."""

    def test_hash_array_basic(self):
        """Test basic hash_array functionality."""
        data = np.array([1, 2, 3, 4, 5])
        result = hash_array(data)
        assert isinstance(result, str)
        assert len(result) == 16

    def test_hash_array_deterministic(self):
        """Test that same data produces same hash."""
        data = np.array([1, 2, 3, 4, 5])
        hash1 = hash_array(data)
        hash2 = hash_array(data)
        assert hash1 == hash2

    def test_hash_array_different_data(self):
        """Test that different data produces different hash."""
        data1 = np.array([1, 2, 3, 4, 5])
        data2 = np.array([1, 2, 3, 4, 6])
        hash1 = hash_array(data1)
        hash2 = hash_array(data2)
        assert hash1 != hash2

    def test_hash_array_2d(self):
        """Test with 2D array."""
        data = np.array([[1, 2], [3, 4]])
        result = hash_array(data)
        assert isinstance(result, str)
        assert len(result) == 16

    def test_hash_array_float(self):
        """Test with float array."""
        data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = hash_array(data)
        assert isinstance(result, str)
        assert len(result) == 16

    def test_hash_array_complex(self):
        """Test with complex array."""
        data = np.array([1 + 2j, 3 + 4j])
        result = hash_array(data)
        assert isinstance(result, str)
        assert len(result) == 16

    def test_hash_array_3d(self):
        """Test with 3D array."""
        data = np.random.random((3, 4, 5))
        result = hash_array(data)
        assert isinstance(result, str)
        assert len(result) == 16

    def test_hash_array_empty(self):
        """Test with empty array."""
        data = np.array([])
        result = hash_array(data)
        assert isinstance(result, str)
        assert len(result) == 16

    def test_hash_array_single_element(self):
        """Test with single element array."""
        data = np.array([42])
        result = hash_array(data)
        assert isinstance(result, str)
        assert len(result) == 16

    def test_hash_array_dtype_matters(self):
        """Test that dtype affects hash."""
        data_int = np.array([1, 2, 3], dtype=np.int32)
        data_float = np.array([1, 2, 3], dtype=np.float64)
        hash_int = hash_array(data_int)
        hash_float = hash_array(data_float)
        # Different dtypes should produce different hashes
        assert hash_int != hash_float

    def test_hash_array_order_matters(self):
        """Test that order of elements matters."""
        data1 = np.array([1, 2, 3])
        data2 = np.array([3, 2, 1])
        hash1 = hash_array(data1)
        hash2 = hash_array(data2)
        assert hash1 != hash2

    def test_hash_array_shape_matters(self):
        """Test that shape affects hash."""
        data1 = np.array([[1, 2], [3, 4]])
        data2 = np.array([1, 2, 3, 4])
        hash1 = hash_array(data1)
        hash2 = hash_array(data2)
        # Different shapes should produce different hashes
        # (even if same values)
        assert hash1 != hash2

    def test_hash_array_hexadecimal(self):
        """Test that hash is hexadecimal."""
        data = np.array([1, 2, 3])
        result = hash_array(data)
        # Should only contain hex characters
        assert all(c in "0123456789abcdef" for c in result)

    def test_hash_array_large_array(self):
        """Test with large array."""
        data = np.random.random((1000, 1000))
        result = hash_array(data)
        assert isinstance(result, str)
        assert len(result) == 16

    def test_hash_array_reproducibility_across_runs(self):
        """Test that hash is same across multiple calls."""
        data = np.array([1, 2, 3, 4, 5])
        hashes = [hash_array(data) for _ in range(10)]
        # All should be identical
        assert len(set(hashes)) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
