#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/conftest.py

from pathlib import Path
import re

# match lines that begin with "def test_"
_pattern_test_def = re.compile(r"^def test_", re.MULTILINE)


def pytest_collect_file(file_path):
    """Only load files that have test functions."""
    if str(file_path).endswith(".py") and (
        file_path.name.startswith("test_")
        or file_path.name.endswith("_test.py")
    ):
        try:
            content = Path(file_path).read_text()
            if "def test_" not in content:
                return None
            print(file_path)
        except:
            pass
    return None


# EOF
