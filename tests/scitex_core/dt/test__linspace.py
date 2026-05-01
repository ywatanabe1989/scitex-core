#!/usr/bin/env python3
"""Tests for scitex_core.dt._linspace.linspace (datetime linspace)."""

import datetime

import numpy as np
import pytest

from scitex_core.dt._linspace import linspace


@pytest.fixture
def dt_pair():
    return datetime.datetime(2026, 1, 1, 0, 0, 0), datetime.datetime(
        2026, 1, 1, 1, 0, 0
    )


class TestNSamples:
    def test_returns_correct_length(self, dt_pair):
        start, end = dt_pair
        out = linspace(start, end, n_samples=5)
        assert len(out) == 5

    def test_endpoints_match(self, dt_pair):
        start, end = dt_pair
        out = linspace(start, end, n_samples=5)
        assert out[0] == start
        assert out[-1] == end

    def test_returns_ndarray_of_datetimes(self, dt_pair):
        start, end = dt_pair
        out = linspace(start, end, n_samples=3)
        assert isinstance(out, np.ndarray)
        assert isinstance(out[0], datetime.datetime)


class TestSamplingRate:
    def test_uses_sampling_rate_correctly(self, dt_pair):
        start, end = dt_pair  # 1 hour = 3600 seconds
        out = linspace(start, end, sampling_rate=1)  # 1 Hz → 3601 samples
        assert len(out) == 3601

    def test_sampling_rate_must_be_positive(self, dt_pair):
        start, end = dt_pair
        with pytest.raises(ValueError, match="positive"):
            linspace(start, end, sampling_rate=-1)


class TestErrors:
    def test_start_must_be_datetime(self):
        with pytest.raises(TypeError, match="start_dt"):
            linspace("2026-01-01", datetime.datetime(2026, 1, 2), n_samples=3)

    def test_end_must_be_datetime(self):
        with pytest.raises(TypeError, match="end_dt"):
            linspace(datetime.datetime(2026, 1, 1), "2026-01-02", n_samples=3)

    def test_start_must_precede_end(self, dt_pair):
        start, end = dt_pair
        with pytest.raises(ValueError, match="earlier"):
            linspace(end, start, n_samples=3)

    def test_must_provide_one_of_n_samples_or_sampling_rate(self, dt_pair):
        start, end = dt_pair
        with pytest.raises(ValueError, match="must be provided"):
            linspace(start, end)

    def test_cannot_provide_both(self, dt_pair):
        start, end = dt_pair
        with pytest.raises(ValueError, match="not both"):
            linspace(start, end, n_samples=5, sampling_rate=1)


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
