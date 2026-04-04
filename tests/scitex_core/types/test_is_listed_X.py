#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/types/test_is_listed_X.py

"""Tests for scitex_core.types is_listed_X utilities."""

import pytest

from scitex_core.types import is_list_of_type, is_listed_X


class TestIsListedX:
    """Test is_listed_X function."""

    def test_is_listed_X_integers(self):
        """Test with list of integers."""
        data = [1, 2, 3, 4, 5]
        assert is_listed_X(data, int) is True

    def test_is_listed_X_strings(self):
        """Test with list of strings."""
        data = ["a", "b", "c"]
        assert is_listed_X(data, str) is True

    def test_is_listed_X_floats(self):
        """Test with list of floats."""
        data = [1.0, 2.0, 3.0]
        assert is_listed_X(data, float) is True

    def test_is_listed_X_mixed_fail(self):
        """Test that mixed types fail."""
        data = [1, "a", 3]
        assert is_listed_X(data, int) is False

    def test_is_listed_X_empty_list(self):
        """Test with empty list."""
        data = []
        # Empty list should return True (vacuously true)
        assert is_listed_X(data, int) is True

    def test_is_listed_X_not_list(self):
        """Test with non-list."""
        data = (1, 2, 3)  # Tuple, not list
        assert is_listed_X(data, int) is False

    def test_is_listed_X_multiple_types_int_or_float(self):
        """Test with multiple allowed types."""
        data = [1, 2.0, 3, 4.0]
        # Note: in Python, 2.0 is float, not int
        assert is_listed_X(data, (int, float)) is True

    def test_is_listed_X_multiple_types_list(self):
        """Test with list of types."""
        data = [1, 2, 3]
        assert is_listed_X(data, [int, float]) is True

    def test_is_listed_X_none_in_list(self):
        """Test with None in list."""
        data = [1, None, 3]
        assert is_listed_X(data, int) is False

    def test_is_listed_X_nested_lists(self):
        """Test with nested lists."""
        data = [[1, 2], [3, 4]]
        assert is_listed_X(data, list) is True

    def test_is_listed_X_single_element(self):
        """Test with single element list."""
        data = [42]
        assert is_listed_X(data, int) is True

    def test_is_listed_X_booleans(self):
        """Test with booleans."""
        data = [True, False, True]
        assert is_listed_X(data, bool) is True

    def test_is_listed_X_wrong_type(self):
        """Test with wrong type."""
        data = [1, 2, 3]
        assert is_listed_X(data, str) is False


class TestIsListOfType:
    """Test is_list_of_type function (alias)."""

    def test_is_list_of_type_integers(self):
        """Test with list of integers."""
        data = [1, 2, 3, 4, 5]
        assert is_list_of_type(data, int) is True

    def test_is_list_of_type_strings(self):
        """Test with list of strings."""
        data = ["a", "b", "c"]
        assert is_list_of_type(data, str) is True

    def test_is_list_of_type_same_as_is_listed_X(self):
        """Test that is_list_of_type gives same results as is_listed_X."""
        data = [1, 2, 3]
        result1 = is_listed_X(data, int)
        result2 = is_list_of_type(data, int)
        assert result1 == result2

    def test_is_list_of_type_mixed_fail(self):
        """Test that mixed types fail."""
        data = [1, 2.0, "3"]
        assert is_list_of_type(data, int) is False

    def test_is_list_of_type_multiple_types(self):
        """Test with multiple allowed types."""
        data = [1, 2.0, 3]
        assert is_list_of_type(data, (int, float)) is True


class TestIsListedXEdgeCases:
    """Test edge cases for is_listed_X."""

    def test_is_listed_X_dict_values(self):
        """Test with dict (not a list)."""
        data = {1: "a", 2: "b"}
        assert is_listed_X(data, dict) is False

    def test_is_listed_X_set(self):
        """Test with set (not a list)."""
        data = {1, 2, 3}
        assert is_listed_X(data, int) is False

    def test_is_listed_X_string(self):
        """Test with string (not a list of chars)."""
        data = "abc"
        assert is_listed_X(data, str) is False

    def test_is_listed_X_numpy_array(self):
        """Test with numpy array (not a list)."""
        import numpy as np

        data = np.array([1, 2, 3])
        assert is_listed_X(data, int) is False

    def test_is_listed_X_custom_class(self):
        """Test with custom class."""

        class MyClass:
            pass

        obj1 = MyClass()
        obj2 = MyClass()
        data = [obj1, obj2]

        assert is_listed_X(data, MyClass) is True

    def test_is_listed_X_inheritance(self):
        """Test with class inheritance."""

        class Parent:
            pass

        class Child(Parent):
            pass

        obj = Child()
        data = [obj]

        # Should work with exact type
        assert is_listed_X(data, Child) is True

        # Should NOT work with parent type (isinstance would, but we're checking exact type)
        # Actually, isinstance in the implementation will return True
        assert is_listed_X(data, Parent) is True

    def test_is_listed_X_large_list(self):
        """Test with large list."""
        data = list(range(10000))
        assert is_listed_X(data, int) is True

    def test_is_listed_X_exception_handling(self):
        """Test that exceptions are handled gracefully."""
        # Some weird object that might cause issues
        data = object()
        # Should return False, not crash
        assert is_listed_X(data, int) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
