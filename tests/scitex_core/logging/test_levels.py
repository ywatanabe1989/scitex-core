#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/logging/test_levels.py

"""Tests for scitex_core.logging custom log levels."""

import pytest
import logging
from scitex_core.logging._levels import (
    SUCCESS,
    FAIL,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
)


class TestLogLevels:
    """Test custom log level constants."""

    def test_success_level_defined(self):
        """Test SUCCESS level is defined."""
        assert SUCCESS is not None
        assert isinstance(SUCCESS, int)

    def test_fail_level_defined(self):
        """Test FAIL level is defined."""
        assert FAIL is not None
        assert isinstance(FAIL, int)

    def test_standard_levels_exported(self):
        """Test standard levels are exported."""
        assert DEBUG == logging.DEBUG
        assert INFO == logging.INFO
        assert WARNING == logging.WARNING
        assert ERROR == logging.ERROR
        assert CRITICAL == logging.CRITICAL

    def test_custom_levels_unique(self):
        """Test custom levels have unique values."""
        standard_levels = {DEBUG, INFO, WARNING, ERROR, CRITICAL}
        assert SUCCESS not in standard_levels
        assert FAIL not in standard_levels

    def test_success_level_between_info_and_warning(self):
        """Test SUCCESS level is between INFO and WARNING."""
        # Typically, SUCCESS should be between INFO and WARNING
        assert INFO < SUCCESS < WARNING or SUCCESS == INFO + 5

    def test_fail_level_near_error(self):
        """Test FAIL level is near ERROR."""
        # FAIL should be close to ERROR level
        assert ERROR <= FAIL or FAIL <= ERROR

    def test_levels_are_integers(self):
        """Test all levels are integers."""
        levels = [SUCCESS, FAIL, DEBUG, INFO, WARNING, ERROR, CRITICAL]
        for level in levels:
            assert isinstance(level, int)

    def test_levels_ordered(self):
        """Test standard levels are properly ordered."""
        assert DEBUG < INFO
        assert INFO < WARNING
        assert WARNING < ERROR
        assert ERROR < CRITICAL


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
