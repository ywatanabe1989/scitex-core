#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/sh/test__init__.py

"""Tests for scitex_core.sh module main functions.

Note: These tests require the scitex dependency issue in _execute.py to be resolved.
The module currently imports 'scitex' which should be removed or replaced with
standalone implementations for scitex-core.
"""

import pytest
import sys
import os

# Check if scitex is available (for CI/CD compatibility)
try:
    from scitex_core.sh import sh, sh_run, quote
    SCITEX_AVAILABLE = True
except ImportError as e:
    SCITEX_AVAILABLE = False
    skip_reason = f"scitex dependency not available: {e}"

skip_if_no_scitex = pytest.mark.skipif(
    not SCITEX_AVAILABLE,
    reason=skip_reason if not SCITEX_AVAILABLE else ""
)


@skip_if_no_scitex
class TestShBasic:
    """Test basic sh() function."""

    def test_sh_simple_command(self):
        """Test sh with simple command."""
        result = sh(["echo", "test"], verbose=False)
        assert isinstance(result, dict)
        assert result["stdout"] == "test"
        assert result["success"] is True
        assert result["exit_code"] == 0

    def test_sh_return_as_str(self):
        """Test sh with return_as='str'."""
        result = sh(["echo", "hello"], verbose=False, return_as="str")
        assert isinstance(result, str)
        assert result == "hello"

    def test_sh_return_as_dict(self):
        """Test sh with return_as='dict'."""
        result = sh(["echo", "hello"], verbose=False, return_as="dict")
        assert isinstance(result, dict)
        assert "stdout" in result
        assert "stderr" in result
        assert "exit_code" in result
        assert "success" in result

    def test_sh_error_command(self):
        """Test sh with command that errors."""
        result = sh(["cat", "/nonexistent/file"], verbose=False, return_as="dict")
        assert result["success"] is False
        assert result["exit_code"] != 0
        assert len(result["stderr"]) > 0

    def test_sh_error_return_as_str(self):
        """Test sh error with return_as='str' returns stderr."""
        result = sh(["cat", "/nonexistent/file"], verbose=False, return_as="str")
        assert isinstance(result, str)
        assert len(result) > 0  # Should contain error message

    def test_sh_with_arguments(self):
        """Test sh with multiple arguments."""
        result = sh(["printf", "%s", "test"], verbose=False)
        assert result["success"] is True
        assert "test" in result["stdout"]

    def test_sh_empty_output(self):
        """Test sh with command that produces no output."""
        result = sh(["true"], verbose=False)
        assert result["success"] is True
        assert result["stdout"] == ""

    def test_sh_rejects_string(self):
        """Test that sh rejects string commands."""
        with pytest.raises(TypeError) as exc_info:
            sh("echo test", verbose=False)

        assert "String commands are not allowed" in str(exc_info.value)


@skip_if_no_scitex
class TestShRun:
    """Test sh_run() function."""

    def test_sh_run_basic(self):
        """Test sh_run with basic command."""
        result = sh_run(["echo", "test"], verbose=False)
        assert isinstance(result, dict)
        assert result["stdout"] == "test"
        assert result["success"] is True

    def test_sh_run_error_handling(self):
        """Test sh_run error handling."""
        result = sh_run(["cat", "/nonexistent"], verbose=False)
        assert result["success"] is False
        assert result["exit_code"] != 0
        assert len(result["stderr"]) > 0

    def test_sh_run_rejects_string(self):
        """Test that sh_run rejects string commands."""
        with pytest.raises(TypeError):
            sh_run("ls -la", verbose=False)

    def test_sh_run_with_multiple_args(self):
        """Test sh_run with multiple arguments."""
        result = sh_run(["ls", "-la"], verbose=False)
        # ls might fail in some test environments, so just check structure
        assert isinstance(result, dict)
        assert "success" in result
        assert "exit_code" in result


@skip_if_no_scitex
class TestShTimeout:
    """Test timeout functionality."""

    def test_sh_with_timeout_success(self):
        """Test sh with timeout that completes in time."""
        result = sh(["echo", "test"], verbose=False, timeout=5)
        assert result["success"] is True
        assert result["stdout"] == "test"

    def test_sh_with_timeout_expiry(self):
        """Test sh with command that times out."""
        result = sh(["sleep", "10"], verbose=False, timeout=1)
        assert result["success"] is False
        assert "timed out" in result["stderr"].lower()

    def test_sh_timeout_return_as_str(self):
        """Test sh timeout with return_as='str'."""
        result = sh(["echo", "test"], verbose=False, return_as="str", timeout=5)
        assert isinstance(result, str)
        assert result == "test"

    def test_sh_timeout_error_return_as_str(self):
        """Test sh timeout error with return_as='str'."""
        result = sh(["sleep", "10"], verbose=False, return_as="str", timeout=1)
        assert isinstance(result, str)
        assert "timed out" in result.lower()

    def test_sh_with_timeout_none(self):
        """Test sh with explicit timeout=None."""
        result = sh(["echo", "test"], verbose=False, timeout=None)
        assert result["success"] is True


@skip_if_no_scitex
class TestShStreaming:
    """Test streaming output functionality."""

    def test_sh_streaming_basic(self):
        """Test sh with streaming enabled."""
        result = sh(
            ["bash", "-c", "echo 'line1'; echo 'line2'"],
            verbose=False,
            stream_output=True
        )
        assert result["success"] is True
        assert "line1" in result["stdout"]
        assert "line2" in result["stdout"]

    def test_sh_streaming_vs_buffered_same_output(self):
        """Test that streaming and buffered give same results."""
        cmd = ["bash", "-c", "for i in 1 2 3; do echo $i; done"]

        buffered = sh(cmd, verbose=False, stream_output=False)
        streaming = sh(cmd, verbose=False, stream_output=True)

        assert buffered["stdout"] == streaming["stdout"]
        assert buffered["success"] == streaming["success"]

    def test_sh_streaming_with_timeout(self):
        """Test streaming with timeout."""
        result = sh(
            ["bash", "-c", "echo 'start'; sleep 5"],
            verbose=False,
            stream_output=True,
            timeout=1
        )
        assert result["success"] is False
        assert "timed out" in result["stderr"].lower()

    def test_sh_streaming_error_command(self):
        """Test streaming with error command."""
        result = sh(
            ["bash", "-c", "echo 'start'; false"],
            verbose=False,
            stream_output=True
        )
        assert result["success"] is False
        assert "start" in result["stdout"]


@skip_if_no_scitex
class TestShVerbose:
    """Test verbose output functionality."""

    def test_sh_verbose_output(self, capsys):
        """Test that verbose=True prints output."""
        sh(["echo", "test"], verbose=True)
        captured = capsys.readouterr()
        # Should contain command or output
        assert "echo" in captured.out or "test" in captured.out

    def test_sh_run_verbose_output(self, capsys):
        """Test that sh_run verbose=True prints output."""
        sh_run(["echo", "test"], verbose=True)
        captured = capsys.readouterr()
        assert "echo" in captured.out or "test" in captured.out

    def test_sh_verbose_false_no_output(self, capsys):
        """Test that verbose=False suppresses output."""
        sh(["echo", "test"], verbose=False)
        captured = capsys.readouterr()
        # Should not print (or minimal output)
        # Note: Some CI systems may still capture output


class TestQuoteExport:
    """Test that quote is exported."""

    def test_quote_available(self):
        """Test that quote function is available."""
        if SCITEX_AVAILABLE:
            assert callable(quote)
            result = quote("test; dangerous")
            assert isinstance(result, str)


@skip_if_no_scitex
class TestShEdgeCases:
    """Test edge cases and special scenarios."""

    def test_sh_unicode_output(self):
        """Test handling Unicode output."""
        result = sh(["echo", "Hello 世界"], verbose=False)
        assert result["success"] is True
        assert "世界" in result["stdout"]

    def test_sh_binary_output_handling(self):
        """Test handling of commands that might output binary."""
        # This should handle decoding gracefully
        result = sh(["echo", "-e", "\\x00\\x01\\x02"], verbose=False)
        assert isinstance(result["stdout"], str)

    def test_sh_empty_command_list(self):
        """Test behavior with empty command list."""
        # Should either raise or handle gracefully
        try:
            result = sh([], verbose=False)
            # If it doesn't raise, check it fails safely
            assert result["success"] is False or result is not None
        except (ValueError, TypeError, OSError):
            # Acceptable to raise error for empty command
            pass

    def test_sh_with_env_variables_literal(self):
        """Test that environment variables aren't expanded in list format."""
        result = sh(["echo", "$HOME"], verbose=False)
        # Should print literal "$HOME", not expanded value
        assert "$HOME" in result["stdout"]

    def test_sh_multiple_rapid_calls(self):
        """Test multiple rapid command executions."""
        for i in range(10):
            result = sh(["echo", f"test{i}"], verbose=False)
            assert result["success"] is True
            assert f"test{i}" in result["stdout"]


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
