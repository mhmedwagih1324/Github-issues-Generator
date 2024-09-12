import os
from github_issues_generator.utils import create_issue_body_file, create_github_command

def generate_github_cli_commands_from_md(md_file_path, output_dir='issue_files', issue_prefix='###'):
    """Generate GitHub CLI commands from markdown file based on custom prefix."""
    commands = []

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(md_file_path, 'r') as file:
        lines = file.readlines()

    issue_title = None
    issue_body = []

    for line in lines:
        # If we encounter a new issue starting with the provided prefix
        if line.startswith(issue_prefix):
            # If there was a previous issue, save its body to a .md file and store the command
            if issue_title is not None:
                file_path = create_issue_body_file(issue_title, issue_body, output_dir)

                # Create the GitHub CLI command
                command = create_github_command(issue_title, file_path)
                commands.append(command)

            # Extract the issue title from this line and reset the issue body
            issue_title = line[len(issue_prefix):].strip()
            issue_body = []

        # Collect body text for the current issue (keeping indentation)
        else:
            issue_body.append(line)

    # Handle the last issue if it exists
    if issue_title is not None:
        file_path = create_issue_body_file(issue_title, issue_body, output_dir)

        # Create the GitHub CLI command
        command = create_github_command(issue_title, file_path)
        commands.append(command)

    return commands
