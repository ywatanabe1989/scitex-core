#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/repro/test_gen_id.py

"""Tests for scitex_core.repro gen_id utilities."""

import re

import pytest

from scitex_core.repro import gen_ID, gen_id


class TestGenId:
    """Test gen_id function."""

    def test_gen_id_default(self):
        """Test gen_id with default parameters."""
        result = gen_id()
        assert isinstance(result, str)
        assert "_" in result  # Should have timestamp_random format

    def test_gen_id_format(self):
        """Test that gen_id follows expected format."""
        result = gen_id()
        # Should have timestamp and random parts
        parts = result.split("_")
        assert len(parts) >= 2

    def test_gen_id_uniqueness(self):
        """Test that consecutive calls generate different IDs."""
        id1 = gen_id()
        id2 = gen_id()
        # Random parts should differ
        assert id1 != id2

    def test_gen_id_custom_time_format(self):
        """Test with custom time format."""
        result = gen_id(time_format="%Y%m%d")
        # Should contain 8-digit date
        assert re.search(r"\d{8}_", result)

    def test_gen_id_custom_length(self):
        """Test with custom random string length."""
        result = gen_id(N=4)
        parts = result.split("_")
        random_part = parts[-1]
        assert len(random_part) == 4

    def test_gen_id_zero_length(self):
        """Test with zero length random string."""
        result = gen_id(N=0)
        assert result.endswith("_")

    def test_gen_id_large_length(self):
        """Test with large random string length."""
        result = gen_id(N=32)
        parts = result.split("_")
        random_part = parts[-1]
        assert len(random_part) == 32

    def test_gen_id_alphanumeric(self):
        """Test that random part is alphanumeric."""
        result = gen_id()
        parts = result.split("_")
        random_part = parts[-1]
        assert random_part.isalnum()

    def test_gen_id_backward_compat(self):
        """Test gen_ID backward compatibility alias."""
        result = gen_ID()
        assert isinstance(result, str)
        assert "_" in result


class TestGenIdEdgeCases:
    """Test edge cases for gen_id."""

    def test_gen_id_special_time_format(self):
        """Test with special characters in time format."""
        result = gen_id(time_format="%Y-%m-%d_%H:%M:%S")
        assert isinstance(result, str)
        assert "_" in result

    def test_gen_id_consistency_same_time(self):
        """Test that IDs generated at same time differ only in random part."""
        # This is probabilistic - generate many and check
        ids = [gen_id() for _ in range(10)]
        # All should be unique (probability of collision is extremely low)
        assert len(set(ids)) == len(ids)

    def test_gen_id_minimum_length(self):
        """Test with minimum random length."""
        result = gen_id(N=1)
        parts = result.split("_")
        random_part = parts[-1]
        assert len(random_part) == 1

    def test_gen_id_contains_letters_and_digits(self):
        """Test that random part can contain both letters and digits."""
        # Generate many IDs and check at least one has both
        has_letter = False
        has_digit = False

        for _ in range(100):
            result = gen_id()
            random_part = result.split("_")[-1]
            if any(c.isalpha() for c in random_part):
                has_letter = True
            if any(c.isdigit() for c in random_part):
                has_digit = True

        assert has_letter
        assert has_digit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
