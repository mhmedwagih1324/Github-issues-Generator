"""Testing utility functions"""

from unittest.mock import mock_open, patch
import pytest
from github_issues_generator.utils import (
    sanitize_filename,
    escape_backticks,
    create_issue_body_file,
    create_github_command,
)


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("filename has spaces", "filename has spaces"),
        ("filename-has-dashes", "filename-has-dashes"),
        (
            "filename has Special! Characters@#$%^&*()",
            "filename has Special_ Characters_________",
        ),
        ("filename is-already_clean", "filename is-already_clean"),
        ("", ""),  # empty filename
    ],
)
def test_sanitize_filename(filename, expected):
    """Testing sanitize_filename utility"""
    assert sanitize_filename(filename) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("This title has `backticks`", "This title has \\`backticks\\`"),
        ("This title has no backticks", "This title has no backticks"),
        ("", ""),  # empty text
    ],
)
def test_escape_backticks(text, expected):
    """Testing escape_backticks utility"""
    assert escape_backticks(text) == expected


@pytest.mark.parametrize(
    "issue_title, issue_body, output_dir, expected, should_raise",
    [
        (
            "title of issue",
            "This is the body of the issue.",
            "output",
            "output/title of issue.md",
            False,
        ),
        (
            "Issue with / invalid characters",
            "This body will be saved.",
            "output",
            "output/Issue with _ invalid characters.md",
            False,
        ),
        (
            "",
            "This is the body of the issue.",
            "output",
            "",
            True,
        ),
    ],
)
def test_create_issue_body_file(
    issue_title,
    issue_body,
    output_dir,
    expected,
    should_raise,
):
    """Testing create_issue_body_file utility"""
    mocked_open = mock_open()

    if should_raise:
        mocked_open.side_effect = RuntimeError("Failed to write file: File write error")

    with patch("builtins.open", mocked_open):
        if should_raise:
            with pytest.raises(
                RuntimeError,
                match="Failed to write file: File write error",
            ):
                create_issue_body_file(issue_title, issue_body, output_dir)
        else:
            result = create_issue_body_file(issue_title, issue_body, output_dir)

            assert result == expected

            mocked_open.assert_called_once_with(
                file=expected, mode="w", encoding="utf-8"
            )

            mocked_open().write.assert_called_once_with(issue_body)


@pytest.mark.parametrize(
    "issue_title, file_path, current_milestone, expected",
    [
        (
            "Test Issue",
            "path/to/file.md",
            "",
            'gh issue create --title "Test Issue" --body-file "path/to/file.md"',
        ),
        (
            "Issue with `backticks`",
            "path/to/file.md",
            "",
            'gh issue create --title "Issue with \\`backticks\\`" --body-file "path/to/file.md"',
        ),
        (
            "Another Issue",
            "path/to/file.md",
            "Milestone 1",
            'gh issue create --title "Another Issue" --body-file "path/to/file.md" --milestone "Milestone 1"',
        ),
        (
            "Milestone with `backticks`",
            "path/to/file.md",
            "Milestone `two`",
            'gh issue create --title "Milestone with \\`backticks\\`" --body-file "path/to/file.md" --milestone "Milestone \\`two\\`"',  # pylint: disable=line-too-long, useless-suppression
        ),
    ],
)
def test_create_github_command(issue_title, file_path, current_milestone, expected):
    """Tests for the create_github_command function."""
    assert create_github_command(issue_title, file_path, current_milestone) == expected
