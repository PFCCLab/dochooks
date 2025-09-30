from __future__ import annotations

import argparse
import os
import subprocess
from collections.abc import Sequence

from dochooks import __version__

from ..utils.return_code import FAIL, PASS, ReturnCode

DEFAULT_ERROR_MESSAGE = """\
The following files would conflict on case-insensitive filesystems (e.g., APFS, NTFS):

{conflicts}

To fix this, you can:
1. Rename one of the conflicting files to have a different name
2. Use a case-sensitive filesystem
3. Avoid using files that differ only in case

Example conflict:
  existing: README.md
  new file: readme.md  # This would conflict!

Fix by renaming to: readme_lower.md or README_upper.md
"""


def get_all_git_files() -> list[str]:
    """Get all tracked files in the git repository.

    Returns:
        List of all file paths in the git repository, empty list if not in a git repo
    """
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Not in a git repository or git is not available
        return []


def find_case_conflicts(file_paths: Sequence[str]) -> dict[str, list[str]]:
    """Detect case conflicts in file paths.

    Args:
        file_paths: List of file paths to check

    Returns:
        Dictionary mapping lowercase paths to lists of conflicting original paths
    """
    # Build lowercase path mapping
    path_map: dict[str, list[str]] = {}

    for file_path in file_paths:
        # Normalize path
        normalized_path = os.path.normpath(file_path)
        # Convert to lowercase for comparison
        lower_path = normalized_path.lower()

        if lower_path not in path_map:
            path_map[lower_path] = []
        path_map[lower_path].append(normalized_path)

    # Find conflicting paths
    conflicts: dict[str, list[str]] = {}
    for lower_path, original_paths in path_map.items():
        if len(original_paths) > 1:
            conflicts[lower_path] = original_paths

    return conflicts


def format_conflicts(conflicts: dict[str, list[str]], input_files: Sequence[str]) -> str:
    """Format conflicts for display.

    Args:
        conflicts: Dictionary of conflicts from find_case_conflicts
        input_files: List of files being checked (from pre-commit)

    Returns:
        Formatted string showing the conflicts
    """
    lines: list[str] = []
    for lower_path, original_paths in conflicts.items():
        lines.append(f"Conflict group (lowercase: {lower_path}):")
        # Sort paths: lowercase first, then uppercase
        sorted_paths = sorted(original_paths, key=lambda p: (p.lower() != p, p))

        for path in sorted_paths:
            # Mark files from current commit
            is_new = path in input_files
            marker = " [current commit]" if is_new else ""
            lines.append(f"  - {path}{marker}")

        lines.append("")

    return "\n".join(lines)


def check_files(file_paths: Sequence[str], error_message: str = DEFAULT_ERROR_MESSAGE) -> ReturnCode:
    """Check file list for case conflicts.

    Args:
        file_paths: List of file paths to check (usually files from pre-commit)
        error_message: Custom error message template, use {conflicts} as placeholder

    Returns:
        FAIL if conflicts found, PASS otherwise
    """
    # Get all tracked files in git repository
    all_git_files = get_all_git_files()

    # Merge input files and git files, remove duplicates
    all_files = list(set(file_paths) | set(all_git_files))

    # Check for conflicts
    conflicts = find_case_conflicts(all_files)

    if not conflicts:
        return PASS

    # Filter to only conflicts involving input files
    relevant_conflicts: dict[str, list[str]] = {}
    for lower_path, original_paths in conflicts.items():
        # Check if conflict group contains any input files
        has_input_file = any(path in file_paths for path in original_paths)
        if has_input_file:
            relevant_conflicts[lower_path] = original_paths

    if not relevant_conflicts:
        return PASS

    # Format and display conflicts
    conflicts_text = format_conflicts(relevant_conflicts, file_paths)
    print(error_message.format(conflicts=conflicts_text.rstrip()))

    return FAIL


def main(argv: Sequence[str] | None = None) -> ReturnCode:
    parser = argparse.ArgumentParser(
        prog="check-case-conflict",
        description="Check for filename conflicts on case-insensitive filesystems",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "--error-message",
        default=DEFAULT_ERROR_MESSAGE,
        help="Custom error message template (use {conflicts} as placeholder)",
    )
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    args = parser.parse_args(argv)

    if not args.filenames:
        return PASS

    return check_files(args.filenames, error_message=args.error_message)


if __name__ == "__main__":
    raise SystemExit(main())
