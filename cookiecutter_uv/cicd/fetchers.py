"""Version fetchers for PyPI and GitHub."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, TypeGuard
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

TIMEOUT = 30


@dataclass
class GitHubRepo:
    """A GitHub repository reference."""

    owner: str
    repo: str

    def __str__(self) -> str:
        """Return string representation as owner/repo format."""
        return f"{self.owner}/{self.repo}"


def _is_dict(value: dict[str, Any] | list[Any] | None) -> TypeGuard[dict[str, Any]]:
    """Type guard to check if a value is a dict.

    This helps mypy narrow union types when we expect dict responses.

    Returns:
        True if value is a dict, False otherwise.
    """
    return isinstance(value, dict)


def _is_list(value: dict[str, Any] | list[Any] | None) -> TypeGuard[list[Any]]:
    """Type guard to check if a value is a list.

    This helps mypy narrow union types when we expect list responses.

    Returns:
        True if value is a list, False otherwise.
    """
    return isinstance(value, list)


def get_pypi_version(package: str) -> str | None:
    """Get the latest version of a package from PyPI.

    Returns:
        The latest version string, or None if the package is not found or fetch fails.
    """
    data = _fetch_json(f"https://pypi.org/pypi/{package}/json")
    if _is_dict(data):
        # PyPI API returns a dict with structure: {"info": {"version": "1.2.3", ...}, ...}
        version: str | None = data.get("info", {}).get("version")
        return version
    return None


def get_github_release(repo: GitHubRepo) -> str | None:
    """Get the latest release tag from GitHub.

    Returns:
        The latest release tag (with 'v' prefix stripped), or None if not found or fetch fails.
    """
    data = _fetch_json(f"https://api.github.com/repos/{repo}/releases/latest")
    if _is_dict(data):
        # GitHub API returns a dict with structure: {"tag_name": "v1.2.3", ...}
        tag = data.get("tag_name", "")
        return tag.lstrip("v") if tag else None
    return None


def get_github_tag(repo: GitHubRepo) -> str | None:
    """Get the latest tag from GitHub (for repos without releases).

    Returns:
        The latest tag (with 'v' prefix stripped), or None if not found or fetch fails.
    """
    data = _fetch_json(f"https://api.github.com/repos/{repo}/tags")
    if _is_list(data) and len(data) > 0:
        # GitHub API returns a list of dicts: [{"name": "v1.2.3", ...}, ...]
        first_tag = data[0]
        if isinstance(first_tag, dict):
            tag = first_tag.get("name", "")
            return tag.lstrip("v") if tag else None
    return None


def _fetch_json(url: str) -> dict[str, Any] | list[Any] | None:
    """Fetch JSON from a URL.

    Returns:
        Parsed JSON as dict or list, or None if fetch fails or URL is invalid.
    """
    if not url.startswith(("https://", "http://")):
        return None
    try:
        with urlopen(url, timeout=TIMEOUT) as response:  # noqa: S310
            result: dict[str, Any] | list[Any] = json.loads(response.read().decode())
            return result
    except (HTTPError, URLError, json.JSONDecodeError):
        return None
