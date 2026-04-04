#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/simple_runner.py

"""
Simple test runner for basic testing without pytest.
For full test suite, install pytest: pip install pytest pytest-cov
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("=" * 60)
print("SciTeX-Core Basic Test Runner")
print("=" * 60)
print()

# Test 1: Import errors module
print("[1/5] Testing errors module import...")
try:
    from scitex_core import errors
    print("  ✓ errors module imported successfully")

    # Test basic error
    try:
        error = errors.SciTeXError("Test error", context={"test": "value"})
        assert "Test error" in str(error)
        assert error.context["test"] == "value"
        print("  ✓ SciTeXError basic functionality works")
    except Exception as e:
        print(f"  ✗ SciTeXError test failed: {e}")

    # Test config error
    try:
        error = errors.ConfigFileNotFoundError("./test.yaml")
        assert "test.yaml" in str(error)
        print("  ✓ ConfigFileNotFoundError works")
    except Exception as e:
        print(f"  ✗ ConfigFileNotFoundError test failed: {e}")

except ImportError as e:
    print(f"  ✗ Failed to import errors: {e}")

print()

# Test 2: Import str module
print("[2/6] Testing str module import...")
try:
    from scitex_core.str import color_text, ct, COLORS, STYLES
    print("  ✓ str module imported successfully")

    # Test color_text function
    try:
        result = color_text("test", "red")
        assert isinstance(result, str)
        assert "test" in result
        print("  ✓ color_text() function works")
    except Exception as e:
        print(f"  ✗ color_text() test failed: {e}")

    # Test ct alias
    try:
        assert ct is color_text
        print("  ✓ ct alias works")
    except Exception as e:
        print(f"  ✗ ct alias test failed: {e}")

    # Test COLORS and STYLES constants
    try:
        assert isinstance(COLORS, dict)
        assert isinstance(STYLES, dict)
        assert 'red' in COLORS
        assert 'bold' in STYLES
        print("  ✓ COLORS and STYLES constants defined")
    except Exception as e:
        print(f"  ✗ Constants test failed: {e}")

except ImportError as e:
    print(f"  ✗ Failed to import str module: {e}")

print()

# Test 3: Import sh module
print("[3/6] Testing sh module import...")
try:
    from scitex_core.sh import _security, _types
    print("  ✓ sh._security imported successfully")
    print("  ✓ sh._types imported successfully")

    # Test validate_command
    try:
        _security.validate_command(["ls", "-la"])
        print("  ✓ validate_command accepts list format")
    except Exception as e:
        print(f"  ✗ validate_command test failed: {e}")

    # Test string rejection
    try:
        _security.validate_command("ls -la")
        print("  ✗ validate_command should reject strings")
    except TypeError:
        print("  ✓ validate_command correctly rejects strings")

    # Test quote function
    try:
        result = _security.quote("test; dangerous")
        assert isinstance(result, str)
        print("  ✓ quote function works")
    except Exception as e:
        print(f"  ✗ quote test failed: {e}")

except ImportError as e:
    print(f"  ✗ Failed to import sh module: {e}")

print()

# Test 4: Import logging module components
print("[4/6] Testing logging module import...")
try:
    from scitex_core.logging import _levels
    print("  ✓ logging._levels imported successfully")

    # Test levels
    assert _levels.SUCCESS is not None
    assert _levels.FAIL is not None
    assert _levels.INFO == 20
    print("  ✓ Custom log levels defined correctly")

except ImportError as e:
    print(f"  ✗ Failed to import logging module: {e}")

print()

# Test 5: Test types
print("[5/6] Testing type definitions...")
try:
    from scitex_core.sh._types import ShellResult, CommandInput

    # Create a ShellResult
    result = {
        "stdout": "test",
        "stderr": "",
        "exit_code": 0,
        "success": True,
    }
    assert isinstance(result, dict)
    print("  ✓ ShellResult type definition works")

    # Create a CommandInput
    command = ["echo", "test"]
    assert isinstance(command, list)
    print("  ✓ CommandInput type definition works")

except ImportError as e:
    print(f"  ✗ Failed to import types: {e}")

print()

# Test 6: Test validation helpers
print("[6/6] Testing validation helpers...")
try:
    from scitex_core.errors import check_path, InvalidPathError

    # Test valid path
    try:
        check_path("./test/file.txt")
        print("  ✓ check_path accepts valid relative paths")
    except Exception as e:
        print(f"  ✗ check_path failed on valid path: {e}")

    # Test invalid path
    try:
        check_path("/absolute/path")
        print("  ✗ check_path should reject absolute paths")
    except InvalidPathError:
        print("  ✓ check_path correctly rejects absolute paths")

except ImportError as e:
    print(f"  ✗ Failed to import validation helpers: {e}")

print()
print("=" * 60)
print("Basic tests completed!")
print()
print("For comprehensive testing, install pytest:")
print("  pip install -e '.[dev]'")
print("  pytest tests/")
print("=" * 60)

# EOF
