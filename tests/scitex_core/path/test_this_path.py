#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/path/test_this_path.py

"""Tests for scitex_core.path this_path utilities."""

import os
from pathlib import Path

import pytest

from scitex_core.path import get_this_path, this_path


class TestThisPath:
    """Test this_path function."""

    def test_this_path_returns_string(self):
        """Test that this_path returns a string."""
        result = this_path()
        assert isinstance(result, str)

    def test_this_path_is_absolute(self):
        """Test that returned path is absolute."""
        result = this_path()
        assert os.path.isabs(result)

    def test_this_path_exists(self):
        """Test that returned path exists."""
        result = this_path()
        # The path should exist (it's this test file)
        assert os.path.exists(result)

    def test_this_path_is_this_file(self):
        """Test that this_path returns this file's path."""
        result = this_path()
        # Should contain the test file name
        assert "test_this_path" in result

    def test_this_path_custom_fake_path(self):
        """Test custom fake path for IPython."""
        # This test will use the real path since we're not in IPython
        result = this_path(ipython_fake_path="/custom/fake/path.py")
        # Should return real path since we're not in IPython
        assert "/custom/fake/path.py" not in result
        assert os.path.exists(result)

    def test_get_this_path_alias(self):
        """Test that get_this_path is an alias for this_path."""
        result1 = this_path()
        result2 = get_this_path()
        assert result1 == result2

    def test_this_path_from_different_locations(self):
        """Test calling this_path from different code locations."""

        def helper_function():
            return this_path()

        # Call from helper function
        result = helper_function()
        # Should still return this test file's path
        assert "test_this_path" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
