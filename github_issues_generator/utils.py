"""This module contains utility functions that are used in the app"""

import os


def escape_backticks(text: str):
    """replaces any backtick (`) with (\\`)

    Args:
        text (str): text needs to be escaped

    Returns:
        str: text wih escaped backticks
    """
    return text.replace("`", "\\`")


def sanitize_filename(filename: str):
    """Sanitizes file names by replacing invalid characters with underscore

    Args:
        filename (str): name of the file to be sanitized

    Returns:
        str: The sanitized filename
    """
    sanitized_chars = []

    for c in filename.strip():
        if c.isalnum() or c in (" ", "-", "_"):
            sanitized_chars.append(c)
        else:
            sanitized_chars.append("_")

    return "".join(sanitized_chars)


def create_issue_body_file(issue_title: str, issue_body: str, output_dir: str) -> str:
    """Creates a file for the issue body with a sanitized file name.

    Args:
        issue_title (str): Title of the issue.
        issue_body (str): Body of the issue.
        output_dir (str): Directory to save the body file.

    Returns:
        str: Path to the issue body file.
    """
    sanitized_title = sanitize_filename(issue_title)

    file_path = os.path.join(output_dir, f"{sanitized_title}.md")

    try:
        with open(file=file_path, mode="w", encoding="utf-8") as issue_file:
            issue_file.write("".join(issue_body))
    except Exception as e:
        raise RuntimeError(f"Failed to write file: {e}") from e

    return file_path


def create_github_command(
    issue_title: str,
    file_path: str,
    current_milestone: str = "",
) -> str:
    """Creates and returns a GitHub command to create an issue.

    Args:
        issue_title (str): Title of the issue for the command.
        file_path (str): Path to the file containing the issue body.
        current_milestone (str, optional): Milestone name to attach the issue to.

    Returns:
        str: The constructed GitHub command.
    """
    command = f'gh issue create --title "{escape_backticks(issue_title)}" --body-file "{file_path}"'

    if current_milestone != "":
        command += f' --milestone "{escape_backticks(current_milestone)}"'

    return command
