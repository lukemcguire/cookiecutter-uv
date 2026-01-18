from __future__ import annotations

import re
import subprocess
import sys

PROJECT_NAME_REGEX = r"^[-a-zA-Z][-a-zA-Z0-9]+$"
project_name = "{{cookiecutter.project_name}}"
if not re.match(PROJECT_NAME_REGEX, project_name):
    print(
        f"ERROR: The project name {project_name} is not a valid Python module name. Please do not use a _ and use - instead"
    )
    # Exit to cancel project
    sys.exit(1)

PROJECT_SLUG_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
project_slug = "{{cookiecutter.project_slug}}"
if not re.match(PROJECT_SLUG_REGEX, project_slug):
    print(
        f"ERROR: The project slug {project_slug} is not a valid Python module name. Please do not use a - and use _ instead"
    )
    # Exit to cancel project
    sys.exit(1)

# Validate Python version is available via uv
python_version = "{{cookiecutter.python_version}}"
try:
    result = subprocess.run(
        ["uv", "python", "list"],
        capture_output=True,
        text=True,
        check=True,
    )
    installed_versions = result.stdout

    # Check if the requested version is installed
    if python_version not in installed_versions:
        print(f"\nERROR: Python {python_version} is not installed via uv.")
        print(f"\nTo install Python {python_version}, run:")
        print(f"  uv python install {python_version}")
        print("\nInstalled Python versions:")
        print(installed_versions)
        sys.exit(1)
    else:
        print(f"✓ Using Python {python_version} (uv-managed)")

except subprocess.CalledProcessError:
    print("\nWARNING: Could not verify Python version with uv.")
    print(f"Proceeding with Python {python_version}...")
except FileNotFoundError:
    print("\nWARNING: uv command not found.")
    print(f"Proceeding with Python {python_version}...")
    print("Make sure uv is installed and in your PATH.")
