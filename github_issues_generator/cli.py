"""This module contains the main function"""

import argparse
import os
import subprocess
from github_issues_generator.issue_parser import generate_github_cli_commands_from_md


def main():
    """Application starts here"""

    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="A tool to generate GitHub CLI issue commands from a markdown file"
    )

    # Add arguments
    parser.add_argument(
        "filename",
        type=str,
        help="The markdown file containing issues",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="issue_files",
        help="Directory to save issue files (default: 'issue_files')",
    )
    parser.add_argument(
        "--commands-file",
        type=str,
        default="commands.sh",
        help="File to save GitHub CLI commands (default: 'commands.sh')",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the GitHub CLI commands after generating",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output for debugging",
    )
    parser.add_argument(
        "--issue-prefix",
        type=str,
        default="###",
        help="String that indicates the start of an issue title (default: '###')",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Check if the input markdown file exists
    if not os.path.exists(args.filename):
        print(f"Error: The file '{args.filename}' does not exist.")
        return

    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        if args.verbose:
            print(f"Creating output directory: {args.output_dir}")
        os.makedirs(args.output_dir)

    # Generate GitHub CLI commands from the markdown file with the user-provided prefix
    commands = generate_github_cli_commands_from_md(
        args.filename, args.output_dir, args.issue_prefix
    )

    # Write the commands to the specified file
    with open(args.commands_file, "w", encoding="UTF-8") as cmd_file:
        cmd_file.write("\n".join(commands))

    if args.verbose:
        print(f"GitHub CLI commands have been written to {args.commands_file}")
        print(f"Issue files have been written to the {args.output_dir} directory")

    # Optionally execute the commands
    if args.execute:
        if args.verbose:
            print(f"Executing commands from {args.commands_file}...")

        for command in commands:
            if args.verbose:
                print(f"Running: {command}")
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error: Command failed with error: {e}")
                return

    print("Done.")
