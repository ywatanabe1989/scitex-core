#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/types/test_ColorLike.py

"""Tests for scitex_core.types ColorLike."""

import pytest

from scitex_core.types import ColorLike


class TestColorLikeType:
    """Test ColorLike type hint."""

    def test_function_accepts_string(self):
        """Test function with ColorLike accepts string."""

        def get_color(color: ColorLike) -> str:
            if isinstance(color, str):
                return color
            return "tuple"

        result = get_color("red")
        assert result == "red"

    def test_function_accepts_hex(self):
        """Test function with ColorLike accepts hex string."""

        def get_color(color: ColorLike) -> str:
            if isinstance(color, str):
                return color
            return "tuple"

        result = get_color("#FF0000")
        assert result == "#FF0000"

    def test_function_accepts_rgb_tuple(self):
        """Test function with ColorLike accepts RGB tuple."""

        def get_color(color: ColorLike) -> str:
            if isinstance(color, str):
                return "string"
            return "tuple"

        result = get_color((1.0, 0.0, 0.0))
        assert result == "tuple"

    def test_function_accepts_rgba_tuple(self):
        """Test function with ColorLike accepts RGBA tuple."""

        def get_color(color: ColorLike) -> str:
            if isinstance(color, str):
                return "string"
            return "tuple"

        result = get_color((1.0, 0.0, 0.0, 0.5))
        assert result == "tuple"

    def test_function_accepts_rgb_list(self):
        """Test function with ColorLike accepts RGB list."""

        def get_color(color: ColorLike) -> str:
            if isinstance(color, str):
                return "string"
            return "list"

        result = get_color([1.0, 0.0, 0.0])
        assert result == "list"

    def test_function_accepts_rgba_list(self):
        """Test function with ColorLike accepts RGBA list."""

        def get_color(color: ColorLike) -> str:
            if isinstance(color, str):
                return "string"
            return "list"

        result = get_color([1.0, 0.0, 0.0, 0.5])
        assert result == "list"


class TestColorLikeExamples:
    """Test common color examples."""

    def test_named_colors(self):
        """Test common named colors."""

        def accepts_color(color: ColorLike) -> bool:
            return isinstance(color, (str, tuple, list))

        assert accepts_color("red")
        assert accepts_color("blue")
        assert accepts_color("green")
        assert accepts_color("black")
        assert accepts_color("white")

    def test_hex_colors(self):
        """Test hex color codes."""

        def accepts_color(color: ColorLike) -> bool:
            return isinstance(color, (str, tuple, list))

        assert accepts_color("#FF0000")
        assert accepts_color("#00FF00")
        assert accepts_color("#0000FF")
        assert accepts_color("#000000")
        assert accepts_color("#FFFFFF")

    def test_rgb_ranges(self):
        """Test RGB with different value ranges."""

        def accepts_color(color: ColorLike) -> bool:
            return isinstance(color, (str, tuple, list))

        # 0-1 range (normalized)
        assert accepts_color((0.5, 0.5, 0.5))
        assert accepts_color((1.0, 0.0, 0.5))

        # Could also accept 0-255 range as floats
        assert accepts_color((128.0, 128.0, 128.0))

    def test_rgba_with_alpha(self):
        """Test RGBA with various alpha values."""

        def accepts_color(color: ColorLike) -> bool:
            return isinstance(color, (str, tuple, list))

        assert accepts_color((1.0, 0.0, 0.0, 0.5))  # 50% opacity
        assert accepts_color((0.0, 1.0, 0.0, 1.0))  # Fully opaque
        assert accepts_color((0.0, 0.0, 1.0, 0.0))  # Fully transparent


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
