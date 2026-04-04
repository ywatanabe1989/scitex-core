#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/sh/test__security.py

"""Tests for scitex_core.sh._security module."""

import pytest
from scitex_core.sh._security import validate_command, quote, DANGEROUS_CHARS


class TestValidateCommand:
    """Test the validate_command function."""

    def test_list_command_valid(self):
        """Test that list commands pass validation."""
        # Should not raise
        validate_command(["ls", "-la"])
        validate_command(["echo", "hello"])
        validate_command(["python", "script.py"])

    def test_string_command_rejected(self):
        """Test that string commands are rejected."""
        with pytest.raises(TypeError) as exc_info:
            validate_command("ls -la")

        error_msg = str(exc_info.value)
        assert "String commands are not allowed" in error_msg
        assert "list format" in error_msg

    def test_null_byte_in_argument(self):
        """Test that null bytes in arguments are detected."""
        with pytest.raises(ValueError) as exc_info:
            validate_command(["echo", "test\0malicious"])

        error_msg = str(exc_info.value)
        assert "null byte" in error_msg.lower()
        assert "shell injection" in error_msg.lower()

    def test_null_byte_in_command(self):
        """Test that null bytes in command name are detected."""
        with pytest.raises(ValueError) as exc_info:
            validate_command(["cat\0rm", "file.txt"])

        error_msg = str(exc_info.value)
        assert "null byte" in error_msg.lower()

    def test_empty_list_valid(self):
        """Test that empty list is valid."""
        # Should not raise
        validate_command([])

    def test_list_with_special_chars_valid(self):
        """Test that list with special chars is valid (they're quoted)."""
        # These are safe in list format because each arg is literal
        validate_command(["echo", "file;rm -rf /"])
        validate_command(["cat", "file|grep test"])
        validate_command(["ls", "dir&background"])

    def test_list_with_flags(self):
        """Test lists with various flags."""
        validate_command(["ls", "-la", "-h", "--color=auto"])
        validate_command(["git", "commit", "-m", "Message with spaces"])

    def test_list_with_paths(self):
        """Test lists with file paths."""
        validate_command(["cat", "/path/to/file.txt"])
        validate_command(["cp", "./source", "./destination"])


class TestQuoteFunction:
    """Test the quote function."""

    def test_quote_simple_string(self):
        """Test quoting a simple string."""
        result = quote("hello")
        assert result == "hello" or result == "'hello'"

    def test_quote_string_with_spaces(self):
        """Test quoting string with spaces."""
        result = quote("hello world")
        assert "hello world" in result
        # Should be quoted
        assert "'" in result or '"' in result

    def test_quote_dangerous_string(self):
        """Test quoting string with dangerous characters."""
        dangerous = "file; rm -rf /"
        result = quote(dangerous)

        # Should contain the original text
        assert "rm -rf /" in result
        # Should be quoted to make it safe
        assert "'" in result or '"' in result

    def test_quote_with_pipe(self):
        """Test quoting string with pipe."""
        result = quote("cat file | grep test")
        assert "|" in result
        assert "'" in result or '"' in result

    def test_quote_with_redirect(self):
        """Test quoting string with redirect."""
        result = quote("output > file.txt")
        assert ">" in result
        assert "'" in result or '"' in result

    def test_quote_with_backticks(self):
        """Test quoting string with backticks."""
        result = quote("`malicious command`")
        assert "`" in result
        assert "'" in result or '"' in result

    def test_quote_with_dollar(self):
        """Test quoting string with dollar sign."""
        result = quote("$HOME")
        assert "$" in result
        assert "'" in result or '"' in result

    def test_quote_empty_string(self):
        """Test quoting empty string."""
        result = quote("")
        assert isinstance(result, str)

    def test_quote_with_quotes(self):
        """Test quoting string that contains quotes."""
        result = quote("text with 'single' quotes")
        assert "single" in result
        # Should be properly escaped/quoted

    def test_quote_with_newlines(self):
        """Test quoting string with newlines."""
        result = quote("line1\nline2")
        assert "\n" in result or "\\n" in result

    def test_quote_idempotent(self):
        """Test that quoting is safe to repeat."""
        text = "dangerous; text"
        once = quote(text)
        twice = quote(once)
        # Should still be a string
        assert isinstance(twice, str)


class TestDangerousChars:
    """Test the DANGEROUS_CHARS constant."""

    def test_dangerous_chars_defined(self):
        """Test that dangerous characters are defined."""
        assert isinstance(DANGEROUS_CHARS, list)
        assert len(DANGEROUS_CHARS) > 0

    def test_contains_semicolon(self):
        """Test that semicolon is in dangerous chars."""
        assert ";" in DANGEROUS_CHARS

    def test_contains_pipe(self):
        """Test that pipe is in dangerous chars."""
        assert "|" in DANGEROUS_CHARS

    def test_contains_ampersand(self):
        """Test that ampersand is in dangerous chars."""
        assert "&" in DANGEROUS_CHARS

    def test_contains_redirect(self):
        """Test that redirects are in dangerous chars."""
        assert ">" in DANGEROUS_CHARS
        assert "<" in DANGEROUS_CHARS

    def test_contains_dollar(self):
        """Test that dollar sign is in dangerous chars."""
        assert "$" in DANGEROUS_CHARS

    def test_contains_backtick(self):
        """Test that backtick is in dangerous chars."""
        assert "`" in DANGEROUS_CHARS

    def test_contains_newline(self):
        """Test that newline is in dangerous chars."""
        assert "\n" in DANGEROUS_CHARS

    def test_contains_parentheses(self):
        """Test that parentheses are in dangerous chars."""
        assert "(" in DANGEROUS_CHARS
        assert ")" in DANGEROUS_CHARS

    def test_contains_braces(self):
        """Test that braces are in dangerous chars."""
        assert "{" in DANGEROUS_CHARS
        assert "}" in DANGEROUS_CHARS


class TestSecurityEdgeCases:
    """Test edge cases and security scenarios."""

    def test_unicode_in_command(self):
        """Test Unicode characters in command."""
        # Should not raise - Unicode is allowed
        validate_command(["echo", "Hello 世界"])

    def test_very_long_argument(self):
        """Test very long arguments."""
        long_arg = "a" * 10000
        # Should not raise
        validate_command(["echo", long_arg])

    def test_many_arguments(self):
        """Test command with many arguments."""
        many_args = ["command"] + [f"arg{i}" for i in range(100)]
        # Should not raise
        validate_command(many_args)

    def test_nested_quotes_in_list(self):
        """Test nested quotes are safe in list format."""
        # Safe because each element is treated literally
        validate_command(["echo", "\"nested 'quotes'\""])

    def test_environment_variable_in_list(self):
        """Test environment variables in list format."""
        # Safe because not interpreted in list format
        validate_command(["echo", "$PATH"])


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
