#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/logging/test_config.py

"""Tests for scitex_core.logging configuration functions."""

import pytest
import logging

try:
    from scitex_core.logging._config import (
        set_level,
        get_level,
        enable_file_logging,
        is_file_logging_enabled,
        configure,
        get_log_path,
    )
    from scitex_core.logging._levels import INFO, DEBUG, WARNING
    CONFIG_AVAILABLE = True
except ImportError as e:
    CONFIG_AVAILABLE = False
    skip_reason = f"Config module not available: {e}"

skip_if_no_config = pytest.mark.skipif(
    not CONFIG_AVAILABLE,
    reason=skip_reason if not CONFIG_AVAILABLE else ""
)


@skip_if_no_config
class TestSetLevel:
    """Test set_level function."""

    def test_set_level_callable(self):
        """Test that set_level is callable."""
        assert callable(set_level)

    def test_set_level_accepts_int(self):
        """Test set_level accepts integer levels."""
        # Should not raise
        set_level(INFO)
        set_level(DEBUG)
        set_level(WARNING)

    def test_set_level_accepts_string(self):
        """Test set_level accepts string levels."""
        # Should not raise
        set_level("INFO")
        set_level("DEBUG")
        set_level("WARNING")


@skip_if_no_config
class TestGetLevel:
    """Test get_level function."""

    def test_get_level_callable(self):
        """Test that get_level is callable."""
        assert callable(get_level)

    def test_get_level_returns_int(self):
        """Test get_level returns integer."""
        level = get_level()
        assert isinstance(level, int)

    def test_get_set_level_roundtrip(self):
        """Test setting and getting level."""
        original = get_level()
        set_level(DEBUG)
        assert get_level() == DEBUG
        set_level(original)  # Restore


@skip_if_no_config
class TestFileLogging:
    """Test file logging configuration."""

    def test_enable_file_logging_callable(self):
        """Test that enable_file_logging is callable."""
        assert callable(enable_file_logging)

    def test_is_file_logging_enabled_callable(self):
        """Test that is_file_logging_enabled is callable."""
        assert callable(is_file_logging_enabled)

    def test_is_file_logging_enabled_returns_bool(self):
        """Test is_file_logging_enabled returns boolean."""
        result = is_file_logging_enabled()
        assert isinstance(result, bool)

    def test_get_log_path_callable(self):
        """Test that get_log_path is callable."""
        assert callable(get_log_path)

    def test_get_log_path_returns_string_or_none(self):
        """Test get_log_path returns string or None."""
        result = get_log_path()
        assert result is None or isinstance(result, str)


@skip_if_no_config
class TestConfigure:
    """Test configure function."""

    def test_configure_callable(self):
        """Test that configure is callable."""
        assert callable(configure)

    def test_configure_with_level(self):
        """Test configure with level parameter."""
        # Should not raise
        configure(level="INFO")
        configure(level=INFO)

    def test_configure_with_enable_file(self):
        """Test configure with enable_file parameter."""
        # Should not raise
        configure(enable_file=False)
        configure(enable_file=True)

    def test_configure_with_enable_console(self):
        """Test configure with enable_console parameter."""
        # Should not raise
        configure(enable_console=True)
        configure(enable_console=False)

    def test_configure_with_all_params(self):
        """Test configure with all parameters."""
        # Should not raise
        configure(
            level="INFO",
            enable_file=False,
            enable_console=True,
            capture_prints=False
        )


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
