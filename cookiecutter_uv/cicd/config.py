"""Configuration for dependency updates."""

from __future__ import annotations

from cookiecutter_uv.cicd.fetchers import GitHubRepo

# PyPI packages to track
PYPI_PACKAGES = [
    "pytest",
    "prek",
    "tox-uv",
    "deptry",
    "mypy",
    "ty",
    "pytest-cov",
    "ruff",
    "mkdocs",
    "mkdocs-material",
    "mkdocstrings",
    "cookiecutter",
    "pytest-cookies",
    "hatchling",
]

# GitHub repository for uv
UV_REPO = GitHubRepo(owner="astral-sh", repo="uv")

# Prek hooks: (repo_url, GitHubRepo)
# Note: prek is compatible with standard pre-commit hooks
PREK_HOOKS = [
    ("https://github.com/pre-commit/pre-commit-hooks", GitHubRepo(owner="pre-commit", repo="pre-commit-hooks")),
    ("https://github.com/astral-sh/ruff-pre-commit", GitHubRepo(owner="astral-sh", repo="ruff-pre-commit")),
]
