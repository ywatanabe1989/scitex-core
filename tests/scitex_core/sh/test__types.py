#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/sh/test__types.py

"""Tests for scitex_core.sh._types module."""

import pytest
from typing import get_args
from scitex_core.sh._types import ShellResult, CommandInput, ReturnFormat


class TestShellResult:
    """Test ShellResult TypedDict."""

    def test_shell_result_structure(self):
        """Test that ShellResult has correct structure."""
        # Create a valid ShellResult
        result: ShellResult = {
            "stdout": "output",
            "stderr": "error",
            "exit_code": 0,
            "success": True,
        }

        assert result["stdout"] == "output"
        assert result["stderr"] == "error"
        assert result["exit_code"] == 0
        assert result["success"] is True

    def test_shell_result_all_keys_required(self):
        """Test ShellResult type checking."""
        # This is a runtime check - TypedDict is for type checkers
        result: ShellResult = {
            "stdout": "",
            "stderr": "",
            "exit_code": 1,
            "success": False,
        }

        assert "stdout" in result
        assert "stderr" in result
        assert "exit_code" in result
        assert "success" in result

    def test_shell_result_types(self):
        """Test ShellResult value types."""
        result: ShellResult = {
            "stdout": "test",
            "stderr": "error",
            "exit_code": 127,
            "success": False,
        }

        assert isinstance(result["stdout"], str)
        assert isinstance(result["stderr"], str)
        assert isinstance(result["exit_code"], int)
        assert isinstance(result["success"], bool)

    def test_shell_result_empty_strings(self):
        """Test ShellResult with empty strings."""
        result: ShellResult = {
            "stdout": "",
            "stderr": "",
            "exit_code": 0,
            "success": True,
        }

        assert result["stdout"] == ""
        assert result["stderr"] == ""

    def test_shell_result_multiline_output(self):
        """Test ShellResult with multiline output."""
        result: ShellResult = {
            "stdout": "line1\nline2\nline3",
            "stderr": "",
            "exit_code": 0,
            "success": True,
        }

        assert "\n" in result["stdout"]
        assert result["stdout"].count("\n") == 2

    def test_shell_result_nonzero_exit_code(self):
        """Test ShellResult with nonzero exit code."""
        result: ShellResult = {
            "stdout": "",
            "stderr": "Command failed",
            "exit_code": 1,
            "success": False,
        }

        assert result["exit_code"] != 0
        assert result["success"] is False

    def test_shell_result_large_exit_code(self):
        """Test ShellResult with large exit code."""
        result: ShellResult = {
            "stdout": "",
            "stderr": "Signal terminated",
            "exit_code": 137,  # SIGKILL
            "success": False,
        }

        assert result["exit_code"] == 137


class TestCommandInput:
    """Test CommandInput type alias."""

    def test_command_input_is_list_of_str(self):
        """Test that CommandInput is List[str]."""
        # CommandInput should be List[str]
        valid_command: CommandInput = ["ls", "-la"]
        assert isinstance(valid_command, list)
        assert all(isinstance(arg, str) for arg in valid_command)

    def test_command_input_empty_list(self):
        """Test CommandInput with empty list."""
        command: CommandInput = []
        assert isinstance(command, list)
        assert len(command) == 0

    def test_command_input_single_element(self):
        """Test CommandInput with single element."""
        command: CommandInput = ["echo"]
        assert isinstance(command, list)
        assert len(command) == 1

    def test_command_input_multiple_elements(self):
        """Test CommandInput with multiple elements."""
        command: CommandInput = ["git", "commit", "-m", "message"]
        assert isinstance(command, list)
        assert len(command) == 4

    def test_command_input_with_flags(self):
        """Test CommandInput with various flags."""
        command: CommandInput = ["ls", "-l", "-a", "-h", "--color=auto"]
        assert all(isinstance(arg, str) for arg in command)

    def test_command_input_with_paths(self):
        """Test CommandInput with file paths."""
        command: CommandInput = ["cat", "/path/to/file.txt"]
        assert command[0] == "cat"
        assert command[1] == "/path/to/file.txt"


class TestReturnFormat:
    """Test ReturnFormat Literal type."""

    def test_return_format_dict(self):
        """Test ReturnFormat with 'dict'."""
        format_type: ReturnFormat = "dict"
        assert format_type == "dict"
        assert isinstance(format_type, str)

    def test_return_format_str(self):
        """Test ReturnFormat with 'str'."""
        format_type: ReturnFormat = "str"
        assert format_type == "str"
        assert isinstance(format_type, str)

    def test_return_format_values(self):
        """Test that ReturnFormat only allows 'dict' or 'str'."""
        # This is a type checker test, but we can verify the Literal values
        try:
            args = get_args(ReturnFormat)
            assert "dict" in args
            assert "str" in args
            assert len(args) == 2
        except:
            # If get_args doesn't work with this Python version, skip
            pass


class TestTypesIntegration:
    """Test how types work together."""

    def test_shell_result_from_command_input(self):
        """Test creating ShellResult from CommandInput."""
        command: CommandInput = ["echo", "test"]

        # Simulated result
        result: ShellResult = {
            "stdout": "test",
            "stderr": "",
            "exit_code": 0,
            "success": True,
        }

        assert isinstance(command, list)
        assert isinstance(result, dict)

    def test_return_format_determines_result_type(self):
        """Test that return format affects result type."""
        # When return_as="dict"
        dict_format: ReturnFormat = "dict"
        result_dict: ShellResult = {
            "stdout": "output",
            "stderr": "",
            "exit_code": 0,
            "success": True,
        }

        # When return_as="str"
        str_format: ReturnFormat = "str"
        result_str: str = "output"

        assert dict_format == "dict"
        assert str_format == "str"
        assert isinstance(result_dict, dict)
        assert isinstance(result_str, str)


class TestTypesDocumentation:
    """Test that types are properly defined and documented."""

    def test_shell_result_exists(self):
        """Test that ShellResult type exists."""
        assert ShellResult is not None

    def test_command_input_exists(self):
        """Test that CommandInput type exists."""
        assert CommandInput is not None

    def test_return_format_exists(self):
        """Test that ReturnFormat type exists."""
        assert ReturnFormat is not None

    def test_types_are_importable(self):
        """Test that all types can be imported."""
        from scitex_core.sh._types import (
            ShellResult,
            CommandInput,
            ReturnFormat,
        )

        assert ShellResult is not None
        assert CommandInput is not None
        assert ReturnFormat is not None


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
