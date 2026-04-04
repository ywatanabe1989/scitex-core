# Testing Guide for scitex-core

## Setup

```bash
pip install -e ".[dev]"
```

This installs:
- pytest>=7.0
- pytest-cov
- black>=22.0
- mypy>=0.950

## Running Tests

### pytest

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src/scitex_core tests/

# Generate HTML coverage report
pytest --cov=src/scitex_core --cov-report=html tests/

# Run specific test file
pytest tests/test_errors.py

# Run specific test function
pytest tests/test_errors.py::test_scitex_error_basic

# Run specific module tests
pytest tests/scitex_core/sh/
```

### Coverage

```bash
# Generate coverage report
pytest --cov=src/scitex_core tests/
coverage report
coverage html  # Creates htmlcov/index.html
```

## Test Structure

Tests mirror the source structure:
```
src/scitex_core/
├── errors.py              → tests/test_errors.py
├── sh/
│   ├── __init__.py        → tests/scitex_core/sh/test___init__.py
│   ├── _execute.py        → tests/scitex_core/sh/test__execute.py
│   ├── _security.py       → tests/scitex_core/sh/test__security.py
│   └── _types.py          → tests/scitex_core/sh/test__types.py
└── logging/
    ├── __init__.py        → tests/scitex_core/logging/test___init__.py
    └── ...
```

## Test Categories

- **Unit tests**: Test individual functions/classes in isolation
- **Integration tests**: Test module interactions
- **Security tests**: Test security features (sh module)
- **Error handling tests**: Test error conditions

## Writing Tests

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from scitex_core.module import function


def test_basic_functionality():
    """Test basic functionality."""
    result = function()
    assert result == expected


class TestClassName:
    """Group related tests together."""

    def test_method_one(self):
        """Test method one."""
        assert True

    def test_method_two(self):
        """Test method two."""
        assert True
```

## Common Pytest Features

```python
# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
])
def test_with_params(input, expected):
    assert function(input) == expected

# Exception testing
def test_raises_error():
    with pytest.raises(ValueError):
        function_that_raises()

# Fixtures
@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"

# Capturing output
def test_output(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert "hello" in captured.out
```

## Running Specific Test Categories

```bash
# Run only sh module tests
pytest tests/scitex_core/sh/

# Run only logging module tests
pytest tests/scitex_core/logging/

# Run only error tests
pytest tests/test_errors.py
```

## Continuous Integration

Tests are designed to run in CI environments. Ensure all tests pass before committing:

```bash
# Run full test suite with coverage
pytest --cov=src/scitex_core --cov-report=term-missing tests/
```

# EOF
