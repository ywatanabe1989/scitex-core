#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/path/test_find.py

"""Tests for scitex_core.path find utilities."""

import os
import tempfile
from pathlib import Path

import pytest

from scitex_core.path import find_dir, find_file, find_git_root


class TestFindFile:
    """Test find_file function."""

    def test_find_file_basic(self, tmp_path):
        """Test basic file finding."""
        # Create test files
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()
        (tmp_path / "file3.py").touch()

        # Find all txt files
        results = find_file(str(tmp_path), "*.txt")
        assert len(results) == 2
        assert all(".txt" in r for r in results)

    def test_find_file_pattern(self, tmp_path):
        """Test pattern matching."""
        # Create test files
        (tmp_path / "test_file.py").touch()
        (tmp_path / "main_file.py").touch()
        (tmp_path / "data.txt").touch()

        # Find Python files
        results = find_file(str(tmp_path), "*.py")
        assert len(results) == 2

        # Find specific pattern
        results = find_file(str(tmp_path), "test_*.py")
        assert len(results) == 1

    def test_find_file_nested(self, tmp_path):
        """Test finding in nested directories."""
        # Create nested structure
        (tmp_path / "dir1").mkdir()
        (tmp_path / "dir1" / "file1.txt").touch()
        (tmp_path / "dir2").mkdir()
        (tmp_path / "dir2" / "file2.txt").touch()

        # Find all txt files
        results = find_file(str(tmp_path), "*.txt")
        assert len(results) == 2

    def test_find_file_multiple_patterns(self, tmp_path):
        """Test with multiple patterns."""
        (tmp_path / "file.txt").touch()
        (tmp_path / "file.md").touch()
        (tmp_path / "file.py").touch()

        # Find txt and md files
        results = find_file(str(tmp_path), ["*.txt", "*.md"])
        assert len(results) == 2

    def test_find_file_no_match(self, tmp_path):
        """Test when no files match."""
        (tmp_path / "file.txt").touch()

        results = find_file(str(tmp_path), "*.nonexistent")
        assert len(results) == 0

    def test_find_file_exclusions(self, tmp_path):
        """Test that default exclusions work."""
        # Create files in excluded directories
        (tmp_path / "lib").mkdir()
        (tmp_path / "lib" / "file.txt").touch()
        (tmp_path / "env").mkdir()
        (tmp_path / "env" / "file.txt").touch()
        (tmp_path / "normal.txt").touch()

        results = find_file(str(tmp_path), "*.txt")
        # Should only find the non-excluded file
        assert len(results) == 1
        assert "normal.txt" in results[0]


class TestFindDir:
    """Test find_dir function."""

    def test_find_dir_basic(self, tmp_path):
        """Test basic directory finding."""
        # Create test directories
        (tmp_path / "dir1").mkdir()
        (tmp_path / "dir2").mkdir()
        (tmp_path / "test_dir").mkdir()

        results = find_dir(str(tmp_path), "dir*")
        assert len(results) == 2

    def test_find_dir_pattern(self, tmp_path):
        """Test pattern matching for directories."""
        (tmp_path / "test_one").mkdir()
        (tmp_path / "test_two").mkdir()
        (tmp_path / "other").mkdir()

        results = find_dir(str(tmp_path), "test_*")
        assert len(results) == 2

    def test_find_dir_nested(self, tmp_path):
        """Test finding nested directories."""
        (tmp_path / "parent").mkdir()
        (tmp_path / "parent" / "child1").mkdir()
        (tmp_path / "parent" / "child2").mkdir()

        results = find_dir(str(tmp_path), "child*")
        assert len(results) == 2

    def test_find_dir_multiple_patterns(self, tmp_path):
        """Test with multiple patterns."""
        (tmp_path / "src").mkdir()
        (tmp_path / "lib").mkdir()
        (tmp_path / "tests").mkdir()

        results = find_dir(str(tmp_path), ["src", "tests"])
        assert len(results) == 2

    def test_find_dir_no_match(self, tmp_path):
        """Test when no directories match."""
        (tmp_path / "existing").mkdir()

        results = find_dir(str(tmp_path), "nonexistent")
        assert len(results) == 0


class TestFindGitRoot:
    """Test find_git_root function."""

    def test_find_git_root_in_repo(self, tmp_path):
        """Test finding git root when in a repository."""
        # Create fake git repository
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        # Create nested directory
        nested = tmp_path / "src" / "module"
        nested.mkdir(parents=True)

        # Should find git root from nested directory
        result = find_git_root(str(nested))
        assert result == str(tmp_path)

    def test_find_git_root_at_root(self, tmp_path):
        """Test when already at git root."""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        result = find_git_root(str(tmp_path))
        assert result == str(tmp_path)

    def test_find_git_root_not_in_repo(self, tmp_path):
        """Test when not in a git repository."""
        result = find_git_root(str(tmp_path))
        assert result is None

    def test_find_git_root_current_directory(self):
        """Test with current directory."""
        # This will succeed if we're in a git repo, otherwise None
        result = find_git_root(".")
        # Just check it doesn't crash
        assert result is None or isinstance(result, str)

    def test_find_git_root_deeply_nested(self, tmp_path):
        """Test with deeply nested directory."""
        git_dir = tmp_path / ".git"
        git_dir.mkdir()

        # Create deep nesting
        deep = tmp_path / "a" / "b" / "c" / "d" / "e"
        deep.mkdir(parents=True)

        result = find_git_root(str(deep))
        assert result == str(tmp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
