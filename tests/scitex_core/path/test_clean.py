#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/path/test_clean.py

"""Tests for scitex_core.path clean utilities."""

from pathlib import Path

import pytest

from scitex_core.path import clean


class TestClean:
    """Test clean function."""

    def test_clean_basic_path(self):
        """Test basic path cleaning."""
        result = clean("/home/user/file.txt")
        assert result == "/home/user/file.txt"

    def test_clean_removes_double_slashes(self):
        """Test that double slashes are removed."""
        result = clean("/home//user//file.txt")
        assert "//" not in result
        assert result == "/home/user/file.txt"

    def test_clean_replaces_spaces(self):
        """Test that spaces are replaced with underscores."""
        result = clean("path with spaces")
        assert " " not in result
        assert result == "path_with_spaces"

    def test_clean_normalizes_dotdot(self):
        """Test that ../ is normalized."""
        result = clean("/home/user/./folder/../file.txt")
        assert result == "/home/user/file.txt"

    def test_clean_normalizes_dot(self):
        """Test that ./ is normalized."""
        result = clean("path/./to/./file.txt")
        assert result == "path/to/file.txt"

    def test_clean_preserves_trailing_slash(self):
        """Test that trailing slash is preserved for directories."""
        result = clean("directory/")
        assert result.endswith("/")

    def test_clean_empty_string(self):
        """Test with empty string."""
        result = clean("")
        assert result == ""

    def test_clean_path_object(self):
        """Test with Path object."""
        path_obj = Path("/home/user/file.txt")
        result = clean(path_obj)
        assert isinstance(result, str)
        assert result == "/home/user/file.txt"

    def test_clean_complex_path(self):
        """Test complex path with multiple issues."""
        result = clean("path with//spaces/./to/../file.txt")
        assert result == "path_with/spaces/file.txt"

    def test_clean_absolute_vs_relative(self):
        """Test that absolute and relative paths are handled correctly."""
        abs_path = clean("/home/user/file.txt")
        assert abs_path.startswith("/")

        rel_path = clean("user/file.txt")
        assert not rel_path.startswith("/")

    def test_clean_multiple_spaces(self):
        """Test multiple consecutive spaces."""
        result = clean("path   with   many   spaces")
        assert result == "path___with___many___spaces"

    def test_clean_windows_path_separators(self):
        """Test handling of Windows-style backslashes."""
        # Note: On Unix, backslashes are valid filename characters
        result = clean("path\\to\\file")
        # The behavior depends on OS, just check it doesn't crash
        assert isinstance(result, str)

    def test_clean_trailing_slash_complex(self):
        """Test trailing slash with normalization."""
        result = clean("path/to/../dir/")
        assert result.endswith("/")
        assert result == "path/dir/"

    def test_clean_multiple_calls_idempotent(self):
        """Test that cleaning multiple times gives same result."""
        path = "/home//user/./file.txt"
        result1 = clean(path)
        result2 = clean(result1)
        assert result1 == result2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
