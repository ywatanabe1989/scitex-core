#!/usr/bin/env python3
"""Tests for scitex_core.dict._DotDict.DotDict."""

import pytest

from scitex_core.dict._DotDict import DotDict


class TestConstruction:
    def test_empty_dotdict(self):
        d = DotDict()
        # No public attributes on an empty DotDict.
        assert "x" not in d._data

    def test_from_plain_dict(self):
        d = DotDict({"a": 1, "b": "two"})
        assert d.a == 1
        assert d.b == "two"

    def test_nested_dicts_become_dotdict(self):
        d = DotDict({"outer": {"inner": 42}})
        assert isinstance(d.outer, DotDict)
        assert d.outer.inner == 42

    def test_already_dotdict_input_works(self):
        inner = DotDict({"x": 1})
        outer = DotDict(inner)
        assert outer.x == 1

    def test_non_dict_input_raises(self):
        with pytest.raises(TypeError, match="dictionary"):
            DotDict([("a", 1)])  # list of tuples is not a dict


class TestAccess:
    def test_attribute_access_for_valid_identifier(self):
        d = DotDict({"foo": 1})
        assert d.foo == 1

    def test_missing_attribute_raises_attribute_error(self):
        d = DotDict({"foo": 1})
        with pytest.raises(AttributeError):
            _ = d.bar

    def test_attribute_set_persists_via_item_access(self):
        d = DotDict({"a": 1})
        d.b = 2
        assert d._data["b"] == 2

    def test_dict_set_with_attribute_assigns_dotdict(self):
        d = DotDict()
        d.nested = {"x": 1}
        assert isinstance(d.nested, DotDict)
        assert d.nested.x == 1


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
