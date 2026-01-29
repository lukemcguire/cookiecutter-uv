from __future__ import annotations

from tests.utils import run_within_dir


def test_full_structure(cookies, tmp_path):
    """
    Test to verify the correct structure of a generated project.

    The test checks that all expected files and directories exist in the
    generated project directory and that the project creation process
    completes without errors.

    Note: Tests with all optional features enabled (devcontainer, dockerfile, etc.)
    """

    expected_files = [
        ".devcontainer",  # Enabled with devcontainer='y'
        ".github",
        ".gitignore",
        ".pre-commit-config.yaml",
        "CONTRIBUTING.md",
        "Dockerfile",  # Enabled with dockerfile='y'
        "LICENSE",
        "Makefile",
        "README.md",
        "codecov.yaml",
        "docs",
        "mkdocs.yml",
        "pyproject.toml",
        "tests",
    ]

    with run_within_dir(tmp_path):
        # Test with flat layout (default)
        result = cookies.bake(extra_context={"devcontainer": "y", "dockerfile": "y", "mkdocs": "y", "layout": "flat"})

        # Check that all expected files and folders are present
        for file in expected_files:
            file_path = result.project_path / file
            assert file_path.exists(), f"Missing file or folder: {file_path}"

        # Check for package directory in flat layout
        assert (result.project_path / "example_project").exists(), "Package directory should exist in flat layout"

        # Verify tox.ini is NOT present (removed in this fork)
        assert not (result.project_path / "tox.ini").exists(), "tox.ini should not exist"

        # Final assertions
        assert result.exit_code == 0
        assert result.exception is None
