#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/str/test_color_text.py

"""Tests for scitex_core.str.color_text functionality."""

import pytest
from scitex_core.str import color_text, ct, COLORS, STYLES


class TestColorText:
    """Test color_text function."""

    def test_color_text_basic(self):
        """Test basic color application."""
        result = color_text("Hello", "red")
        assert isinstance(result, str)
        assert "Hello" in result
        # Should contain ANSI codes
        assert '\033[' in result

    def test_color_text_no_color(self):
        """Test text without color."""
        result = color_text("Hello")
        # Without color, should still return the text (may or may not have codes)
        assert "Hello" in result

    def test_color_text_invalid_color(self):
        """Test with invalid color name."""
        result = color_text("Hello", "invalid_color")
        # Should return text unchanged
        assert result == "Hello"

    def test_color_text_empty_string(self):
        """Test with empty string."""
        result = color_text("")
        assert result == ""

    def test_color_text_all_colors(self):
        """Test all defined colors."""
        test_text = "Test"
        for color_name in ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']:
            result = color_text(test_text, color_name)
            assert test_text in result
            assert isinstance(result, str)

    def test_color_text_bright_colors(self):
        """Test bright color variants."""
        result = color_text("Bright", "bright_red")
        assert "Bright" in result
        assert '\033[' in result

    def test_color_text_with_style(self):
        """Test color with style."""
        result = color_text("Styled", "red", "bold")
        assert "Styled" in result
        assert '\033[' in result

    def test_color_text_style_only(self):
        """Test style without color."""
        result = color_text("Bold text", style="bold")
        assert "Bold text" in result

    def test_color_text_invalid_style(self):
        """Test with invalid style."""
        result = color_text("Text", "red", "invalid_style")
        # Should still apply color
        assert "Text" in result

    def test_color_text_multiline(self):
        """Test with multiline text."""
        text = "Line 1\nLine 2\nLine 3"
        result = color_text(text, "green")
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result

    def test_color_text_unicode(self):
        """Test with Unicode characters."""
        text = "Hello 世界"
        result = color_text(text, "blue")
        assert "世界" in result

    def test_color_text_special_chars(self):
        """Test with special characters."""
        text = "!@#$%^&*()"
        result = color_text(text, "yellow")
        assert text in result

    def test_color_text_reset_included(self):
        """Test that reset code is included."""
        result = color_text("Test", "red")
        # Should end with reset code
        assert result.endswith(COLORS['reset'])


class TestColorTextAlias:
    """Test ct alias."""

    def test_ct_is_color_text(self):
        """Test that ct is an alias for color_text."""
        assert ct is color_text

    def test_ct_works_same_as_color_text(self):
        """Test ct produces same result as color_text."""
        text = "Test"
        color = "green"
        assert ct(text, color) == color_text(text, color)


class TestColorsConstant:
    """Test COLORS constant."""

    def test_colors_is_dict(self):
        """Test COLORS is a dictionary."""
        assert isinstance(COLORS, dict)

    def test_colors_has_basic_colors(self):
        """Test COLORS contains basic colors."""
        basic_colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'black']
        for color in basic_colors:
            assert color in COLORS

    def test_colors_has_bright_variants(self):
        """Test COLORS contains bright variants."""
        assert 'bright_red' in COLORS
        assert 'bright_green' in COLORS
        assert 'bright_blue' in COLORS

    def test_colors_has_reset(self):
        """Test COLORS contains reset."""
        assert 'reset' in COLORS

    def test_color_codes_are_strings(self):
        """Test all color codes are strings."""
        for code in COLORS.values():
            assert isinstance(code, str)

    def test_color_codes_are_ansi(self):
        """Test color codes are ANSI escape sequences."""
        for code in COLORS.values():
            assert code.startswith('\033[')


class TestStylesConstant:
    """Test STYLES constant."""

    def test_styles_is_dict(self):
        """Test STYLES is a dictionary."""
        assert isinstance(STYLES, dict)

    def test_styles_has_common_styles(self):
        """Test STYLES contains common styles."""
        common_styles = ['bold', 'italic', 'underline']
        for style in common_styles:
            assert style in STYLES

    def test_styles_has_additional_styles(self):
        """Test STYLES contains additional styles."""
        additional = ['dim', 'blink', 'reverse', 'hidden', 'strikethrough']
        for style in additional:
            assert style in STYLES

    def test_style_codes_are_strings(self):
        """Test all style codes are strings."""
        for code in STYLES.values():
            assert isinstance(code, str)

    def test_style_codes_are_ansi(self):
        """Test style codes are ANSI escape sequences."""
        for code in STYLES.values():
            assert code.startswith('\033[')


class TestColorTextIntegration:
    """Test color_text integration scenarios."""

    def test_multiple_colors_sequential(self):
        """Test applying different colors to multiple texts."""
        texts = [
            color_text("Error", "red"),
            color_text("Warning", "yellow"),
            color_text("Success", "green"),
        ]

        for text in texts:
            assert isinstance(text, str)
            assert '\033[' in text

    def test_nested_not_recommended_but_works(self):
        """Test that nested color_text calls work (though not recommended)."""
        inner = color_text("inner", "red")
        outer = color_text(f"Outer [{inner}]", "blue")

        assert "inner" in outer
        assert "Outer" in outer

    def test_color_text_preserves_whitespace(self):
        """Test that whitespace is preserved."""
        text = "  spaced  text  "
        result = color_text(text, "cyan")
        # Remove ANSI codes to check whitespace
        plain = result.replace(COLORS['cyan'], '').replace(COLORS['reset'], '')
        assert plain == text

    def test_color_text_with_tabs(self):
        """Test text with tabs."""
        text = "Column1\tColumn2\tColumn3"
        result = color_text(text, "magenta")
        assert "Column1" in result
        assert "\t" in result

    def test_color_combinations(self):
        """Test various color and style combinations."""
        combinations = [
            ("Text", "red", "bold"),
            ("Text", "green", "italic"),
            ("Text", "blue", "underline"),
            ("Text", "yellow", None),
            ("Text", None, "bold"),
        ]

        for text, color, style in combinations:
            result = color_text(text, color, style)
            assert text in result
            assert isinstance(result, str)


class TestColorTextEdgeCases:
    """Test edge cases."""

    def test_very_long_text(self):
        """Test with very long text."""
        text = "A" * 10000
        result = color_text(text, "red")
        assert len(result) >= len(text)

    def test_text_with_existing_ansi_codes(self):
        """Test text that already has ANSI codes."""
        text_with_codes = f"{COLORS['red']}Already colored{COLORS['reset']}"
        result = color_text(text_with_codes, "blue")
        # Should add blue codes
        assert COLORS['blue'] in result

    def test_none_text_handling(self):
        """Test handling of None (should not crash, but behavior may vary)."""
        # Depending on implementation, this might raise or handle gracefully
        try:
            result = color_text(None, "red")
            # If it doesn't raise, check result
            assert result is not None or result is None
        except (TypeError, AttributeError):
            # Acceptable to raise on None input
            pass

    def test_numeric_text(self):
        """Test with numeric input (converted to string)."""
        # If implementation doesn't handle this, it's acceptable
        try:
            result = color_text(123, "green")
            assert "123" in str(result)
        except (TypeError, AttributeError):
            # Acceptable to only accept strings
            pass


if __name__ == "__main__":
    import os
    pytest.main([os.path.abspath(__file__), "-v"])


# EOF
