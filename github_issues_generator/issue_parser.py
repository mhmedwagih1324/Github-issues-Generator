"""This module contains the parser of issues"""

import os
from github_issues_generator.utils import create_issue_body_file, create_github_command


def generate_github_cli_commands_from_md(
    md_file_path,
    output_dir="issue_files",
    issue_prefix="###",
    milestone_parser="milestone:",
):
    """Generate GitHub CLI commands from markdown file based on custom prefix."""
    commands = []

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file=md_file_path, mode="r", encoding="UTF-8") as file:
        lines = file.readlines()

    issue_title = None
    issue_body = []
    current_milestone = None

    for line in lines:
        # Detect milestones (lines starting with 'milestone:')
        if line.startswith(milestone_parser):
            current_milestone = line[len(milestone_parser) :].strip()
            # commands.append(f'gh milestone create --title "{current_milestone}"')

        # If we encounter a new issue starting with the provided prefix
        elif line.startswith(issue_prefix):
            # If there was a previous issue, save its body to a .md file and store the command
            if issue_title is not None:
                file_path = create_issue_body_file(issue_title, issue_body, output_dir)

                # Create the GitHub CLI command
                command = create_github_command(
                    issue_title, file_path, current_milestone
                )
                commands.append(command)

            # Extract the issue title from this line and reset the issue body
            issue_title = line[len(issue_prefix) :].strip()
            issue_body = []

        # Collect body text for the current issue (keeping indentation)
        else:
            issue_body.append(line)

    # Handle the last issue if it exists
    if issue_title is not None:
        file_path = create_issue_body_file(issue_title, issue_body, output_dir)

        # Create the GitHub CLI command
        command = create_github_command(issue_title, file_path, current_milestone)
        commands.append(command)

    return commands
