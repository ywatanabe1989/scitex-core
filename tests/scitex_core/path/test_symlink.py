#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: ./tests/scitex_core/path/test_symlink.py

"""Tests for scitex_core.path symlink utilities."""

import os
from pathlib import Path

import pytest

from scitex_core.path import (
    create_relative_symlink,
    fix_broken_symlinks,
    is_symlink,
    list_symlinks,
    readlink,
    resolve_symlinks,
    symlink,
    unlink_symlink,
)


class TestSymlink:
    """Test symlink creation."""

    def test_symlink_basic(self, tmp_path):
        """Test basic symlink creation."""
        source = tmp_path / "source.txt"
        source.write_text("content")
        link = tmp_path / "link.txt"

        result = symlink(source, link)
        assert result == link
        assert link.is_symlink()
        assert link.read_text() == "content"

    def test_symlink_to_directory(self, tmp_path):
        """Test symlinking to a directory."""
        source_dir = tmp_path / "source_dir"
        source_dir.mkdir()
        (source_dir / "file.txt").write_text("content")

        link = tmp_path / "link_dir"
        symlink(source_dir, link)

        assert link.is_symlink()
        assert (link / "file.txt").read_text() == "content"

    def test_symlink_overwrite_false(self, tmp_path):
        """Test that overwrite=False raises error."""
        source = tmp_path / "source.txt"
        source.write_text("content")
        link = tmp_path / "link.txt"
        link.write_text("existing")

        with pytest.raises(FileExistsError):
            symlink(source, link, overwrite=False)

    def test_symlink_overwrite_true(self, tmp_path):
        """Test that overwrite=True replaces existing file."""
        source = tmp_path / "source.txt"
        source.write_text("new content")
        link = tmp_path / "link.txt"
        link.write_text("old content")

        symlink(source, link, overwrite=True)
        assert link.is_symlink()
        assert link.read_text() == "new content"

    def test_symlink_relative(self, tmp_path):
        """Test creating relative symlink."""
        source = tmp_path / "source.txt"
        source.write_text("content")
        link = tmp_path / "link.txt"

        symlink(source, link, relative=True)
        assert link.is_symlink()
        # The link target should be relative
        target = readlink(link)
        assert not target.is_absolute()

    def test_symlink_creates_parent_dirs(self, tmp_path):
        """Test that parent directories are created."""
        source = tmp_path / "source.txt"
        source.write_text("content")
        link = tmp_path / "nested" / "dirs" / "link.txt"

        symlink(source, link)
        assert link.is_symlink()
        assert link.read_text() == "content"

    def test_symlink_to_nonexistent(self, tmp_path):
        """Test symlink to non-existent target."""
        source = tmp_path / "nonexistent.txt"
        link = tmp_path / "link.txt"

        # Should succeed (broken symlink)
        symlink(source, link)
        assert link.is_symlink()


class TestIsSymlink:
    """Test is_symlink function."""

    def test_is_symlink_true(self, tmp_path):
        """Test with actual symlink."""
        source = tmp_path / "source.txt"
        source.touch()
        link = tmp_path / "link.txt"
        symlink(source, link)

        assert is_symlink(link) is True

    def test_is_symlink_false_file(self, tmp_path):
        """Test with regular file."""
        file = tmp_path / "file.txt"
        file.touch()

        assert is_symlink(file) is False

    def test_is_symlink_false_dir(self, tmp_path):
        """Test with directory."""
        dir_path = tmp_path / "dir"
        dir_path.mkdir()

        assert is_symlink(dir_path) is False

    def test_is_symlink_nonexistent(self, tmp_path):
        """Test with non-existent path."""
        path = tmp_path / "nonexistent"

        assert is_symlink(path) is False


class TestReadlink:
    """Test readlink function."""

    def test_readlink_basic(self, tmp_path):
        """Test reading symlink target."""
        source = tmp_path / "source.txt"
        source.touch()
        link = tmp_path / "link.txt"
        symlink(source, link)

        target = readlink(link)
        assert isinstance(target, Path)

    def test_readlink_not_symlink(self, tmp_path):
        """Test that readlink fails on non-symlink."""
        file = tmp_path / "file.txt"
        file.touch()

        with pytest.raises(OSError):
            readlink(file)

    def test_readlink_relative(self, tmp_path):
        """Test reading relative symlink."""
        source = tmp_path / "source.txt"
        source.touch()
        link = tmp_path / "link.txt"
        symlink(source, link, relative=True)

        target = readlink(link)
        # Should be relative
        assert not target.is_absolute()


class TestResolveSymlinks:
    """Test resolve_symlinks function."""

    def test_resolve_symlinks_basic(self, tmp_path):
        """Test resolving symlink."""
        source = tmp_path / "source.txt"
        source.touch()
        link = tmp_path / "link.txt"
        symlink(source, link)

        resolved = resolve_symlinks(link)
        assert resolved == source.resolve()

    def test_resolve_symlinks_chain(self, tmp_path):
        """Test resolving chain of symlinks."""
        source = tmp_path / "source.txt"
        source.touch()
        link1 = tmp_path / "link1.txt"
        link2 = tmp_path / "link2.txt"

        symlink(source, link1)
        symlink(link1, link2)

        resolved = resolve_symlinks(link2)
        assert resolved == source.resolve()

    def test_resolve_symlinks_regular_file(self, tmp_path):
        """Test with regular file."""
        file = tmp_path / "file.txt"
        file.touch()

        resolved = resolve_symlinks(file)
        assert resolved == file.resolve()


class TestCreateRelativeSymlink:
    """Test create_relative_symlink function."""

    def test_create_relative_symlink(self, tmp_path):
        """Test creating relative symlink."""
        source = tmp_path / "source.txt"
        source.write_text("content")
        link = tmp_path / "link.txt"

        create_relative_symlink(source, link)
        assert link.is_symlink()
        assert link.read_text() == "content"

        # Verify it's relative
        target = readlink(link)
        assert not target.is_absolute()

    def test_create_relative_symlink_overwrite(self, tmp_path):
        """Test overwriting with relative symlink."""
        source = tmp_path / "source.txt"
        source.write_text("content")
        link = tmp_path / "link.txt"
        link.write_text("old")

        create_relative_symlink(source, link, overwrite=True)
        assert link.is_symlink()


class TestUnlinkSymlink:
    """Test unlink_symlink function."""

    def test_unlink_symlink_basic(self, tmp_path):
        """Test unlinking symlink."""
        source = tmp_path / "source.txt"
        source.touch()
        link = tmp_path / "link.txt"
        symlink(source, link)

        unlink_symlink(link)
        assert not link.exists()
        assert source.exists()  # Source should still exist

    def test_unlink_symlink_missing_ok_true(self, tmp_path):
        """Test with missing_ok=True."""
        link = tmp_path / "nonexistent"

        # Should not raise
        unlink_symlink(link, missing_ok=True)

    def test_unlink_symlink_missing_ok_false(self, tmp_path):
        """Test with missing_ok=False."""
        link = tmp_path / "nonexistent"

        with pytest.raises(FileNotFoundError):
            unlink_symlink(link, missing_ok=False)

    def test_unlink_symlink_not_symlink(self, tmp_path):
        """Test that unlinking regular file raises error."""
        file = tmp_path / "file.txt"
        file.touch()

        with pytest.raises(OSError):
            unlink_symlink(file)


class TestListSymlinks:
    """Test list_symlinks function."""

    def test_list_symlinks_basic(self, tmp_path):
        """Test listing symlinks."""
        source = tmp_path / "source.txt"
        source.touch()
        link1 = tmp_path / "link1.txt"
        link2 = tmp_path / "link2.txt"
        file = tmp_path / "regular.txt"
        file.touch()

        symlink(source, link1)
        symlink(source, link2)

        links = list_symlinks(tmp_path)
        assert len(links) == 2
        assert all(p.is_symlink() for p in links)

    def test_list_symlinks_recursive(self, tmp_path):
        """Test recursive symlink listing."""
        source = tmp_path / "source.txt"
        source.touch()
        nested_dir = tmp_path / "nested"
        nested_dir.mkdir()

        link1 = tmp_path / "link1.txt"
        link2 = nested_dir / "link2.txt"

        symlink(source, link1)
        symlink(source, link2)

        # Non-recursive
        links = list_symlinks(tmp_path, recursive=False)
        assert len(links) == 1

        # Recursive
        links = list_symlinks(tmp_path, recursive=True)
        assert len(links) == 2

    def test_list_symlinks_empty(self, tmp_path):
        """Test with no symlinks."""
        file = tmp_path / "file.txt"
        file.touch()

        links = list_symlinks(tmp_path)
        assert len(links) == 0


class TestFixBrokenSymlinks:
    """Test fix_broken_symlinks function."""

    def test_fix_broken_symlinks_find(self, tmp_path):
        """Test finding broken symlinks."""
        source = tmp_path / "nonexistent.txt"
        link = tmp_path / "link.txt"
        symlink(source, link)

        result = fix_broken_symlinks(tmp_path)
        assert len(result["found"]) == 1
        assert len(result["fixed"]) == 0
        assert len(result["removed"]) == 0

    def test_fix_broken_symlinks_remove(self, tmp_path):
        """Test removing broken symlinks."""
        source = tmp_path / "nonexistent.txt"
        link = tmp_path / "link.txt"
        symlink(source, link)

        result = fix_broken_symlinks(tmp_path, remove=True)
        assert len(result["found"]) == 1
        assert len(result["removed"]) == 1
        assert not link.exists()

    def test_fix_broken_symlinks_repoint(self, tmp_path):
        """Test repointing broken symlinks."""
        old_source = tmp_path / "old.txt"
        new_source = tmp_path / "new.txt"
        new_source.write_text("content")
        link = tmp_path / "link.txt"
        symlink(old_source, link)

        result = fix_broken_symlinks(tmp_path, new_target=new_source)
        assert len(result["found"]) == 1
        assert len(result["fixed"]) == 1
        assert link.read_text() == "content"

    def test_fix_broken_symlinks_valid_ignored(self, tmp_path):
        """Test that valid symlinks are ignored."""
        source = tmp_path / "source.txt"
        source.write_text("content")
        link = tmp_path / "link.txt"
        symlink(source, link)

        result = fix_broken_symlinks(tmp_path)
        assert len(result["found"]) == 0

    def test_fix_broken_symlinks_recursive(self, tmp_path):
        """Test recursive broken symlink finding."""
        nested_dir = tmp_path / "nested"
        nested_dir.mkdir()

        source1 = tmp_path / "nonexistent1.txt"
        source2 = nested_dir / "nonexistent2.txt"
        link1 = tmp_path / "link1.txt"
        link2 = nested_dir / "link2.txt"

        symlink(source1, link1)
        symlink(source2, link2)

        # Non-recursive
        result = fix_broken_symlinks(tmp_path, recursive=False)
        assert len(result["found"]) == 1

        # Recursive
        result = fix_broken_symlinks(tmp_path, recursive=True)
        assert len(result["found"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
