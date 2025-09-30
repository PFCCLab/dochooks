from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from dochooks.check_case_conflict.check import (
    check_files,
    find_case_conflicts,
    format_conflicts,
    get_all_git_files,
)
from dochooks.utils.return_code import FAIL, PASS


class TestGetAllGitFiles:
    def test_get_git_files_success(self) -> None:
        """Test successfully getting git file list"""
        mock_result = MagicMock()
        mock_result.stdout = "file1.txt\nfile2.txt\ndir/file3.txt\n"

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            files = get_all_git_files()
            assert files == ["file1.txt", "file2.txt", "dir/file3.txt"]
            mock_run.assert_called_once()

    def test_get_git_files_empty_repo(self) -> None:
        """Test empty repository"""
        mock_result = MagicMock()
        mock_result.stdout = ""

        with patch("subprocess.run", return_value=mock_result):
            files = get_all_git_files()
            assert files == []

    def test_get_git_files_not_a_repo(self) -> None:
        """Test not in a git repository"""
        with patch("subprocess.run", side_effect=FileNotFoundError()):
            files = get_all_git_files()
            assert files == []


class TestFindCaseConflicts:
    def test_no_conflicts(self) -> None:
        """Test no conflicts case"""
        file_paths = ["path/to/file1.txt", "path/to/file2.txt", "other/file3.txt"]
        conflicts = find_case_conflicts(file_paths)
        assert len(conflicts) == 0

    def test_simple_conflict(self) -> None:
        """Test simple case conflict"""
        file_paths = ["path/to/file.txt", "path/to/File.txt"]
        conflicts = find_case_conflicts(file_paths)
        assert len(conflicts) == 1
        assert "path/to/file.txt" in conflicts
        assert set(conflicts["path/to/file.txt"]) == {"path/to/file.txt", "path/to/File.txt"}

    def test_multiple_conflicts(self) -> None:
        """Test multiple conflicts"""
        file_paths = [
            "a/b/c/d.ext",
            "a/b/c/D.ext",
            "x/y/Z.txt",
            "x/y/z.txt",
        ]
        conflicts = find_case_conflicts(file_paths)
        assert len(conflicts) == 2
        assert "a/b/c/d.ext" in conflicts
        assert "x/y/z.txt" in conflicts

    def test_three_way_conflict(self) -> None:
        """Test three-way conflict"""
        file_paths = ["file.txt", "File.txt", "FILE.txt"]
        conflicts = find_case_conflicts(file_paths)
        assert len(conflicts) == 1
        assert "file.txt" in conflicts
        assert len(conflicts["file.txt"]) == 3

    def test_path_normalization(self) -> None:
        """Test path normalization"""
        file_paths = ["./path/to/file.txt", "path/to/File.txt"]
        conflicts = find_case_conflicts(file_paths)
        assert len(conflicts) == 1


class TestFormatConflicts:
    def test_format_simple_conflict(self) -> None:
        """Test formatting simple conflict"""
        conflicts = {"file.txt": ["file.txt", "File.txt"]}
        result = format_conflicts(conflicts, ["File.txt"])
        assert "Conflict group (lowercase: file.txt):" in result
        assert "file.txt" in result
        assert "File.txt [current commit]" in result

    def test_format_multiple_conflicts(self) -> None:
        """Test formatting multiple conflicts"""
        conflicts = {
            "a/b/file.txt": ["a/b/file.txt", "a/b/File.txt"],
            "x.md": ["x.md", "X.md"],
        }
        result = format_conflicts(conflicts, ["a/b/File.txt", "X.md"])
        assert "a/b/file.txt" in result
        assert "a/b/File.txt [current commit]" in result
        assert "x.md" in result
        assert "X.md [current commit]" in result


class TestCheckFiles:
    @patch("dochooks.check_case_conflict.check.get_all_git_files")
    def test_no_conflicts(self, mock_git_files: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Test no conflicts returns PASS"""
        mock_git_files.return_value = []
        file_paths = ["file1.txt", "file2.txt"]
        result = check_files(file_paths)
        assert result == PASS
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("dochooks.check_case_conflict.check.get_all_git_files")
    def test_with_conflicts(self, mock_git_files: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Test with conflicts returns FAIL and shows message"""
        mock_git_files.return_value = []
        file_paths = ["a/b/c/d.ext", "a/b/c/D.ext"]
        result = check_files(file_paths)
        assert result == FAIL
        captured = capsys.readouterr()
        assert "case-insensitive filesystems" in captured.out
        assert "a/b/c/d.ext" in captured.out
        assert "a/b/c/D.ext" in captured.out

    @patch("dochooks.check_case_conflict.check.get_all_git_files")
    def test_conflict_with_existing_file(self, mock_git_files: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Test new file conflicts with existing file"""
        # Mock existing file.txt in repository
        mock_git_files.return_value = ["file.txt"]
        # Pre-commit passes new File.txt
        file_paths = ["File.txt"]
        result = check_files(file_paths)
        assert result == FAIL
        captured = capsys.readouterr()
        assert "case-insensitive filesystems" in captured.out
        assert "file.txt" in captured.out
        assert "File.txt" in captured.out
        assert "[current commit]" in captured.out

    @patch("dochooks.check_case_conflict.check.get_all_git_files")
    def test_no_conflict_with_existing_files(
        self, mock_git_files: MagicMock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test new file doesn't conflict with existing files"""
        # Repository has some files
        mock_git_files.return_value = ["old_file.txt", "another.md"]
        # New file has no conflict
        file_paths = ["new_file.txt"]
        result = check_files(file_paths)
        assert result == PASS
        captured = capsys.readouterr()
        assert captured.out == ""

    @patch("dochooks.check_case_conflict.check.get_all_git_files")
    def test_custom_error_message(self, mock_git_files: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Test custom error message"""
        mock_git_files.return_value = []
        file_paths = ["file.txt", "File.txt"]
        custom_msg = "Custom error: {conflicts}"
        result = check_files(file_paths, error_message=custom_msg)
        assert result == FAIL
        captured = capsys.readouterr()
        assert "Custom error:" in captured.out
        assert "file.txt" in captured.out

    @patch("dochooks.check_case_conflict.check.get_all_git_files")
    def test_empty_file_list(self, mock_git_files: MagicMock) -> None:
        """Test empty file list"""
        mock_git_files.return_value = []
        result = check_files([])
        assert result == PASS

    @patch("dochooks.check_case_conflict.check.get_all_git_files")
    def test_existing_conflict_not_in_input(
        self, mock_git_files: MagicMock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test existing conflict not in current commit"""
        # Repository already has conflicting files, but current commit doesn't involve them
        mock_git_files.return_value = ["old.txt", "Old.txt"]
        file_paths = ["new.txt"]
        result = check_files(file_paths)
        assert result == PASS
        captured = capsys.readouterr()
        assert captured.out == ""
