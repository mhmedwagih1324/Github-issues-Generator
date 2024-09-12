import os
def escape_backticks(text):
    return text.replace('`', '\\`')

def sanitize_filename(filename):
    """Helper function to sanitize file names by replacing invalid characters."""
    return "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in filename).strip()

def create_github_command(issue_title, file_path):
    escaped_title = escape_backticks(issue_title)
    return f'gh issue create --title "{escaped_title}" --body-file "{file_path}"'

def create_issue_body_file(issue_title, issue_body, output_dir):
    """Create a file for the issue body with a sanitized file name."""
    sanitized_title = sanitize_filename(issue_title)
    file_path = os.path.join(output_dir, f"{sanitized_title}.md")

    with open(file_path, 'w') as issue_file:
        issue_file.write("".join(issue_body))
    
    return file_path
