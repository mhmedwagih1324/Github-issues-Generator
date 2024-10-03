"""App setup file"""

from setuptools import setup, find_packages

setup(
    name="Github-issues-Generator",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "github-issues-generator=github_issues_generator.cli:main",
        ],
    },
    install_requires=[],
    description="A tool to generate GitHub issue CLI commands from a markdown file.",
    author="Mohamed Wagih",
    author_email="mhmedwagih1324@gmail.com",
    url="https://github.com/mhmedwagih1324/Github-issues-Generator",
)
