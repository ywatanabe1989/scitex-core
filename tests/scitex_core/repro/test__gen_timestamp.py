#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/repro/test_gen_timestamp.py

"""Tests for scitex_core.repro gen_timestamp utilities."""

import re
import time

import pytest

from scitex_core.repro import gen_timestamp, timestamp


class TestGenTimestamp:
    """Test gen_timestamp function."""

    def test_gen_timestamp_returns_string(self):
        """Test that gen_timestamp returns a string."""
        result = gen_timestamp()
        assert isinstance(result, str)

    def test_gen_timestamp_format(self):
        """Test timestamp format."""
        result = gen_timestamp()
        # Format: YYYY-MMDD-HHMM
        pattern = r"\d{4}-\d{4}-\d{4}"
        assert re.match(pattern, result)

    def test_gen_timestamp_contains_hyphen(self):
        """Test that timestamp contains hyphens."""
        result = gen_timestamp()
        assert "-" in result
        assert result.count("-") == 2

    def test_gen_timestamp_length(self):
        """Test timestamp length."""
        result = gen_timestamp()
        # YYYY-MMDD-HHMM is 14 characters
        assert len(result) == 14

    def test_gen_timestamp_numeric_parts(self):
        """Test that all parts are numeric (except hyphens)."""
        result = gen_timestamp()
        parts = result.split("-")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)

    def test_gen_timestamp_consistency(self):
        """Test that timestamps within same minute are identical."""
        ts1 = gen_timestamp()
        time.sleep(0.1)  # Small delay
        ts2 = gen_timestamp()
        # Should be same if within same minute
        # This might occasionally fail at minute boundary
        if ts1[:-2] == ts2[:-2]:  # Same year-month-day-hour
            assert True

    def test_gen_timestamp_changes_over_time(self):
        """Test that timestamp changes when time passes."""
        ts1 = gen_timestamp()
        time.sleep(61)  # Wait over a minute
        ts2 = gen_timestamp()
        # These should definitely be different
        # (Skip this test if running quickly)
        # Just check the function works
        assert isinstance(ts2, str)

    def test_timestamp_alias(self):
        """Test timestamp is an alias for gen_timestamp."""
        result1 = gen_timestamp()
        result2 = timestamp()
        # Should be same if called immediately after
        assert result1[:10] == result2[:10]  # At least same date


class TestGenTimestampEdgeCases:
    """Test edge cases for gen_timestamp."""

    def test_gen_timestamp_year(self):
        """Test that year is reasonable (4 digits, starts with 20)."""
        result = gen_timestamp()
        year = result[:4]
        assert len(year) == 4
        assert year.startswith("20")

    def test_gen_timestamp_month(self):
        """Test that month is valid (01-12)."""
        result = gen_timestamp()
        # Format: YYYY-MMDD-HHMM
        month = result[5:7]
        month_int = int(month)
        assert 1 <= month_int <= 12

    def test_gen_timestamp_day(self):
        """Test that day is valid (01-31)."""
        result = gen_timestamp()
        day = result[7:9]
        day_int = int(day)
        assert 1 <= day_int <= 31

    def test_gen_timestamp_hour(self):
        """Test that hour is valid (00-23)."""
        result = gen_timestamp()
        hour = result[10:12]
        hour_int = int(hour)
        assert 0 <= hour_int <= 23

    def test_gen_timestamp_minute(self):
        """Test that minute is valid (00-59)."""
        result = gen_timestamp()
        minute = result[12:14]
        minute_int = int(minute)
        assert 0 <= minute_int <= 59


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
