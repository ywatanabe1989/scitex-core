#!/usr/bin/env python3
"""Tests for scitex_core.parallel._run.run (ThreadPoolExecutor parallel runner)."""

import pytest

from scitex_core.parallel._run import run


def _square(x):
    return x * x


def _add(a, b):
    return a + b


def _boom(_):
    raise RuntimeError("boom")


class TestParallelRun:
    def test_runs_each_args_tuple(self):
        results = run(_square, [(2,), (3,), (4,)], n_jobs=2)
        # Result order is by completion, not args order — sort to compare.
        assert sorted(results) == [4, 9, 16]

    def test_handles_multi_arg_tuples(self):
        results = run(_add, [(1, 2), (3, 4), (5, 6)], n_jobs=2)
        assert sorted(results) == [3, 7, 11]

    def test_empty_args_list_raises(self):
        with pytest.raises(ValueError, match="empty"):
            run(_square, [], n_jobs=2)

    def test_n_jobs_default_uses_all_cores(self):
        # Just verify default doesn't crash and returns the expected length.
        results = run(_square, [(i,) for i in range(5)])
        assert len(results) == 5

    def test_propagates_function_exceptions(self):
        # Worker exceptions should bubble back to the caller.
        with pytest.raises(RuntimeError, match="boom"):
            run(_boom, [(1,), (2,)], n_jobs=2)


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
