#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/logging/test_tee.py

"""Tests for scitex_core.logging Tee functionality."""

import pytest
import sys
import io
import tempfile
import os

try:
    from scitex_core.logging._Tee import Tee, tee
    TEE_AVAILABLE = True
except ImportError as e:
    TEE_AVAILABLE = False
    skip_reason = f"Tee module not available: {e}"

skip_if_no_tee = pytest.mark.skipif(
    not TEE_AVAILABLE,
    reason=skip_reason if not TEE_AVAILABLE else ""
)


@skip_if_no_tee
class TestTeeClass:
    """Test Tee class."""

    def test_tee_class_exists(self):
        """Test that Tee class exists."""
        assert Tee is not None

    def test_tee_with_file(self):
        """Test Tee with file output."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tf:
            temp_path = tf.name

        try:
            original_stdout = sys.stdout
            with open(temp_path, 'w') as f:
                sys.stdout = Tee(original_stdout, f)
                print("Test message")
                sys.stdout = original_stdout

            # Read back the file
            with open(temp_path, 'r') as f:
                content = f.read()

            assert "Test message" in content
        finally:
            os.unlink(temp_path)
            sys.stdout = original_stdout

    def test_tee_writes_to_both_streams(self):
        """Test that Tee writes to both streams."""
        stream1 = io.StringIO()
        stream2 = io.StringIO()

        tee_obj = Tee(stream1, stream2)
        tee_obj.write("Test\n")
        tee_obj.flush()

        assert "Test" in stream1.getvalue()
        assert "Test" in stream2.getvalue()

    def test_tee_has_write_method(self):
        """Test that Tee has write method."""
        stream = io.StringIO()
        tee_obj = Tee(stream, stream)
        assert hasattr(tee_obj, 'write')
        assert callable(tee_obj.write)

    def test_tee_has_flush_method(self):
        """Test that Tee has flush method."""
        stream = io.StringIO()
        tee_obj = Tee(stream, stream)
        assert hasattr(tee_obj, 'flush')
        assert callable(tee_obj.flush)


@skip_if_no_tee
class TestTeeFunction:
    """Test tee context manager function."""

    def test_tee_function_exists(self):
        """Test that tee function exists."""
        assert tee is not None
        assert callable(tee)

    def test_tee_as_context_manager(self):
        """Test tee as context manager."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tf:
            temp_path = tf.name

        try:
            with tee(temp_path):
                print("Context manager test")

            # Read back the file
            with open(temp_path, 'r') as f:
                content = f.read()

            assert "Context manager test" in content
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_tee_restores_stdout(self):
        """Test that tee restores original stdout."""
        original = sys.stdout

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tf:
            temp_path = tf.name

        try:
            with tee(temp_path):
                assert sys.stdout != original

            assert sys.stdout == original
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
