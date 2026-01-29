"""Command-line interface for cookiecutter-uv template generation."""

from __future__ import annotations

import os
from pathlib import Path


def main() -> None:
    """Execute cookiecutter using the package directory as the template source.

    This function determines the package directory location relative to this module
    and invokes cookiecutter with that directory as the template.
    """
    cwd = Path(__file__).parent
    package_dir = (cwd / "..").resolve()
    os.system(f"cookiecutter {package_dir}")  # noqa: S605 | No injection, retrieving path in OS
