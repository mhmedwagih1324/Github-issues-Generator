# Github Issues Generator

**Github Issues Generator** is a command-line tool that helps developers create GitHub issues from a structured `.md` (Markdown) file. Each issue is defined by a title and body, and the tool generates GitHub CLI commands to create these issues programmatically.

A simple use of the generator is this ![explaining](https://github.com/user-attachments/assets/fc9882b0-3efd-4791-ba9e-379a924dcec4)



## Idea Behind

When planning for a new feature or solving a bug you might always make a markdown file listing all the tasks but need to create an issue for each task that can be assigned to someone, the process of creating that issues becomes time consuming when the feature or the bug is complicated.

## Features
- Parses a Markdown file containing issue titles and bodies.
- Generates GitHub CLI commands (`gh issue create`) for each issue.
- Saves issue bodies into `.md` files, organized into a folder.
- Supports customizable prefixes for issue titles.
- Escapes special characters (like backticks) in issue titles.

## Installation

To install the **Github Issues Generator**, first clone the repository:

```bash
git clone https://github.com/your-username/github-issues-generator.git
cd github-issues-generator
```

Then, install the tool using `pip`:

```bash
pip install .
```

If you encounter the warning about the script being installed in a location that is not on `PATH`, you can resolve it by adding the installation path to your system’s `PATH` (explained in the installation notes below).

## Installation Notes (Optional)

If you see this warning:

```
WARNING: The script github-issues-generator is installed in '/home/your_user/.local/bin' which is not on PATH.
```

You can fix this by adding the script installation directory to your `PATH`:

```bash
export PATH="$PATH:/home/your_user/.local/bin"
```

Make this change permanent by adding the export line to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
```

Then, reload the shell configuration:

```bash
source ~/.bashrc
```

## Usage

Once installed, you can use the **Github Issues Generator** from the command line. The tool requires the path to a `.md` file containing issues to generate commands for. Each issue title is defined by a line starting with a customizable prefix (e.g., `###` by default).

### Command Syntax

```bash
github-issues-generator <path_to_md_file> [--prefix <issue_prefix>] [--output-dir <output_dir>]
```

### Arguments

- `<path_to_md_file>`: The path to the Markdown file containing the issues.
- `--prefix <issue_prefix>`: The prefix used to define issue titles in the Markdown file (default: `###`).
- `--output-dir <output_dir>`: The directory where issue files will be saved (default: `issue_files`).
- `--commands-file <commands_file>`: The file where GitHub CLI commands will be saved (default: `commands.sh`).
- `--execute`: Executes the GitHub CLI commands after generating them.
- `--verbose`: Enables verbose output for debugging.

### Example Usage

1. Prepare a file called `issues.md` with the following structure:

```markdown
### First Issue
This is the body of the first issue.

It has multiple lines.

### Second Issue
This is the body of the second issue.

It also has multiple lines and supports markdown.
```

2. Run the **Github Issues Generator**:

```bash
github-issues-generator issues.md
```

This will generate GitHub CLI commands for each issue and save the issue bodies into the `issue_files/` directory.

3. If your issue titles have a different prefix (e.g., `####`), you can specify the prefix with the `--prefix` option:

```bash
github-issues-generator issues.md --prefix '####'
```

4. To save the generated issue files in a custom directory:

```bash
github-issues-generator issues.md --output-dir 'custom_issues_dir'
```

### Generated Commands

The tool will generate GitHub CLI commands like this:

```bash
gh issue create --title "First Issue" --body-file "issue_files/First_Issue.md"
gh issue create --title "Second Issue" --body-file "issue_files/Second_Issue.md"
```

You can run these commands manually or automate them using a script.

### Special Character Handling

The tool escapes special characters in issue titles, such as backticks (`\``). For example, if an issue title contains backticks:

```markdown
### Issue with `backticks`
The issue body text goes here.
```

The generated command will be:

```bash
gh issue create --title "Issue with \`backticks\`" --body-file "issue_files/Issue_with_backticks.md"
```

## Requirements

- Python 3.6 or later.
- `gh` CLI (GitHub CLI) must be installed and authenticated with your GitHub account.

You can install the GitHub CLI by following the instructions here: [GitHub CLI Installation Guide](https://github.com/cli/cli#installation).

## Development

To contribute to this project:

1. Fork the repository.
2. Create a new feature branch.
3. Make your changes and write tests.
4. Submit a pull request for review.

Make sure your code is clean and follows PEP 8 standards.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
