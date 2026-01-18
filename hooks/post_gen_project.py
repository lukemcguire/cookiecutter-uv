#!/usr/bin/env python
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath: str) -> None:
    Path(os.path.join(PROJECT_DIRECTORY, filepath)).unlink()


def remove_dir(filepath: str) -> None:
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


def move_file(filepath: str, target: str) -> None:
    Path(os.path.join(PROJECT_DIRECTORY, filepath)).rename(os.path.join(PROJECT_DIRECTORY, target))


def move_dir(src: str, target: str) -> None:
    shutil.move(os.path.join(PROJECT_DIRECTORY, src), os.path.join(PROJECT_DIRECTORY, target))


def get_python_version() -> str:
    """Get selected Python version from cookiecutter config."""
    return "{{cookiecutter.python_version}}"


def update_python_version_in_file(filepath: Path, python_version: str) -> None:
    """Update Python version in pyproject.toml."""
    content = filepath.read_text()

    # Update requires-python
    content = re.sub(
        r'requires-python = ">=\d+\.\d+,<\d+\.\d+"',
        f'requires-python = ">={python_version},<4.0"',
        content,
    )

    # Remove all specific Python version classifiers
    content = re.sub(
        r'"Programming Language :: Python :: 3\.\d+",?\n',
        "",
        content,
    )

    # Add back the current version classifier
    content = re.sub(
        r'("Programming Language :: Python :: 3",)',
        f'\\1\n    "Programming Language :: Python :: {python_version}",',
        content,
    )

    filepath.write_text(content)


def update_github_action_python_version(python_version: str) -> None:
    """Update default Python version in GitHub Actions setup."""
    action_file = Path(PROJECT_DIRECTORY) / ".github" / "actions" / "setup-python-env" / "action.yml"
    if action_file.exists():
        content = action_file.read_text()
        content = re.sub(
            r'default: "\d+\.\d+"',
            f'default: "{python_version}"',
            content,
            count=1,  # Only update first occurrence (python-version)
        )
        action_file.write_text(content)


def remove_tox_ini() -> None:
    """Remove tox.ini from generated project."""
    tox_file = Path(PROJECT_DIRECTORY) / "tox.ini"
    if tox_file.exists():
        tox_file.unlink()


def check_command_exists(command: str) -> bool:
    """Check if a command exists in the system PATH."""
    return shutil.which(command) is not None


def run_command(
    cmd: list[str],
    description: str,
    *,
    check: bool = True,
    capture_output: bool = False,
    dry_run: bool = False,
) -> subprocess.CompletedProcess | None:
    """Run a command and provide feedback to the user.

    Args:
        cmd: Command and arguments to run
        description: Human-readable description of what the command does
        check: Whether to raise an exception if the command fails
        capture_output: Whether to capture stdout/stderr
        dry_run: If True, only print the command without executing

    Returns:
        CompletedProcess instance with command results, or None if dry_run
    """
    cmd_str = " ".join(cmd)

    if dry_run:
        print(f"[DRY RUN] {description}")
        print(f"          Would run: {cmd_str}")
        return None

    print(f"🚀 {description}...")
    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_DIRECTORY,
            check=check,
            capture_output=capture_output,
            text=True,
        )
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
        if not capture_output and result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        raise


def check_gh_auth() -> bool:
    """Check if GitHub CLI is authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_git_config() -> tuple[bool, str]:
    """Check if git user.name and user.email are configured.

    Returns:
        Tuple of (is_configured, error_message)
    """
    try:
        name_result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            check=False,
        )
        email_result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            check=False,
        )

        missing = []
        if name_result.returncode != 0 or not name_result.stdout.strip():
            missing.append("user.name")
        if email_result.returncode != 0 or not email_result.stdout.strip():
            missing.append("user.email")

        if missing:
            config_missing = " and ".join(missing)
            error_msg = f"Git {config_missing} not configured"
            return False, error_msg

        return True, ""
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, "Unable to check git configuration"


def check_git_connectivity(protocol: str) -> tuple[bool, str]:
    """Check if git can connect to GitHub with the specified protocol.

    Args:
        protocol: Either 'ssh' or 'https'

    Returns:
        Tuple of (can_connect, error_message)
    """
    try:
        if protocol == "ssh":
            # Test SSH connection to GitHub
            result = subprocess.run(
                ["ssh", "-T", "git@github.com"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            # SSH to GitHub returns 1 even on successful auth with message
            # "Hi username! You've successfully authenticated..."
            if "successfully authenticated" in result.stderr.lower():
                return True, ""
            return False, "SSH connection to GitHub failed. Ensure SSH keys are configured."
        else:  # https
            # For HTTPS, check if credential helper is configured
            result = subprocess.run(
                ["git", "config", "--get", "credential.helper"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                return True, ""
            return False, "Git credential helper not configured for HTTPS. You may be prompted for credentials."
    except subprocess.TimeoutExpired:
        return False, f"{protocol.upper()} connection to GitHub timed out"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False, f"Unable to test {protocol.upper()} connectivity"


def validate_repository_name(name: str) -> tuple[bool, str]:
    """Validate repository name meets GitHub requirements.

    Args:
        name: Repository name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    import re

    if not name:
        return False, "Repository name cannot be empty"

    if len(name) > 100:
        return False, "Repository name exceeds 100 characters"

    # GitHub allows alphanumeric, hyphens, underscores, and periods
    # Must not start with a period
    if name.startswith("."):
        return False, "Repository name cannot start with a period"

    # Check for invalid characters
    if not re.match(r"^[a-zA-Z0-9._-]+$", name):
        return False, "Repository name contains invalid characters (only alphanumeric, -, _, . allowed)"

    return True, ""


def setup_github_repository(*, dry_run: bool = False) -> bool:
    """Automate GitHub repository creation and initial setup.

    Args:
        dry_run: If True, only show what commands would be run

    Returns:
        True if setup was successful, False otherwise
    """
    project_name = "{{cookiecutter.project_name}}"
    author_handle = "{{cookiecutter.author_github_handle}}"
    protocol = "{{cookiecutter.git_remote_protocol}}"

    print("\n" + "=" * 60)
    if dry_run:
        print("🔍 DRY RUN: Showing GitHub setup commands (not executing)")
    else:
        print("🚀 Starting automated GitHub setup")
    print("=" * 60 + "\n")

    # Check prerequisites (skip in dry-run mode)
    if not dry_run:
        # Validate repository name
        is_valid, error_msg = validate_repository_name(project_name)
        if not is_valid:
            print(f"❌ Invalid repository name: {error_msg}")
            print(f"   Project name: '{project_name}'")
            print("   Please use a valid name (alphanumeric, -, _, . only)")
            return False

        # Check if git repo already exists
        if Path(PROJECT_DIRECTORY, ".git").exists():
            print("❌ Git repository already initialized in this directory")
            print("   This may conflict with the automation")
            print("   Please run the setup commands manually from the README")
            return False

        if not check_command_exists("gh"):
            print("❌ GitHub CLI (gh) is not installed")
            print("   Install from: https://cli.github.com/")
            print("   Then run the setup commands manually from the README")
            return False

        if not check_command_exists("git"):
            print("❌ Git is not installed")
            print("   Install git first, then run setup commands manually from the README")
            return False

        if not check_gh_auth():
            print("❌ GitHub CLI is not authenticated")
            print("   Run: gh auth login")
            print("   Then run the setup commands manually from the README")
            return False

        # Check git configuration
        config_ok, config_error = check_git_config()
        if not config_ok:
            print(f"❌ {config_error}")
            print("   Configure with:")
            print('   git config --global user.name "Your Name"')
            print('   git config --global user.email "your.email@example.com"')
            return False

        # Check git connectivity for chosen protocol
        can_connect, connect_error = check_git_connectivity(protocol)
        if not can_connect:
            print(f"⚠️  {connect_error}")
            if protocol == "ssh":
                print("   Setup SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh")
            else:
                print("   You may be prompted for credentials during push")
            # Don't fail for HTTPS credential helper - just warn
            if protocol == "ssh":
                return False
    else:
        print("ℹ️  Prerequisite checks would be performed:")
        print("    - Repository name validation")
        print("    - Existing .git directory check")
        print("    - gh, git installation")
        print("    - GitHub authentication")
        print("    - Git user configuration")
        print(f"    - {protocol.upper()} connectivity to GitHub\n")

    try:
        # Initialize git repository
        run_command(
            ["git", "init", "-b", "main"],
            "Initializing git repository",
            dry_run=dry_run,
        )

        # Run make install to set up environment and pre-commit
        run_command(
            ["make", "install"],
            "Setting up development environment",
            dry_run=dry_run,
        )

        # Create GitHub repository
        if not dry_run:
            print(f"🚀 Creating GitHub repository '{author_handle}/{project_name}'...")
        gh_create_cmd = [
            "gh",
            "repo",
            "create",
            project_name,
            "--public",
            "--source",
            ".",
        ]
        result = run_command(
            gh_create_cmd,
            f"Creating GitHub repository",
            check=False,
            capture_output=True,
            dry_run=dry_run,
        )

        if not dry_run and result and result.returncode != 0:
            if "already exists" in result.stderr.lower():
                print(f"⚠️  Repository {author_handle}/{project_name} already exists")
                print("   Continuing with existing repository...")
            else:
                print(f"❌ Failed to create GitHub repository")
                print(f"   Error: {result.stderr}")
                print("   Please create the repository manually and run:")
                print(f"   git remote add origin <your-repo-url>")
                print(f"   git push -u origin main")
                return False

        # Stage all files
        run_command(
            ["git", "add", "."],
            "Staging files for initial commit",
            dry_run=dry_run,
        )

        # First commit attempt
        if not dry_run:
            print("🚀 Creating initial commit...")
        result = run_command(
            ["git", "commit", "-m", "init commit"],
            "Making initial commit",
            check=False,
            capture_output=True,
            dry_run=dry_run,
        )

        # Check if pre-commit modified any files
        if dry_run:
            print("[DRY RUN] Checking if pre-commit modified files")
            print("          Would run: git status --porcelain")
            print("[DRY RUN] If files were modified, would stage and commit again")
        else:
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=PROJECT_DIRECTORY,
                capture_output=True,
                text=True,
                check=True,
            )

            if status_result.stdout.strip():
                print("🔧 Pre-commit hooks modified files, committing changes...")
                run_command(
                    ["git", "add", "."],
                    "Staging pre-commit modifications",
                )
                run_command(
                    ["git", "commit", "-m", "init commit"],
                    "Making final commit",
                )

        # Add remote and push
        if protocol == "ssh":
            remote_url = f"git@github.com:{author_handle}/{project_name}.git"
        else:  # https
            remote_url = f"https://github.com/{author_handle}/{project_name}.git"

        # Check if remote already exists
        if dry_run:
            print(f"[DRY RUN] Checking if remote 'origin' exists")
            print(f"          Would run: git remote get-url origin")
            print(f"[DRY RUN] If remote doesn't exist, would add: {remote_url}")
        else:
            check_remote = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=PROJECT_DIRECTORY,
                capture_output=True,
                check=False,
            )

            if check_remote.returncode != 0:
                run_command(
                    ["git", "remote", "add", "origin", remote_url],
                    f"Adding GitHub remote ({protocol})",
                )

        run_command(
            ["git", "push", "-u", "origin", "main"],
            "Pushing initial commit to GitHub",
            dry_run=dry_run,
        )

        print("\n" + "=" * 60)
        if dry_run:
            print("✅ DRY RUN completed - above commands would be executed")
            print("=" * 60)
            print(f"\n📂 Repository would be: https://github.com/{author_handle}/{project_name}")
            print("💡 To actually run these commands, set dry_run_github_setup to 'n'\n")
        else:
            print("✅ GitHub setup completed successfully!")
            print("=" * 60)
            print(f"\n📂 Repository: https://github.com/{author_handle}/{project_name}")
            print("🎉 Your project is ready to go!\n")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Automated setup failed: {e}")
        print("\nPlease complete the setup manually using the commands in README.md")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        print("\nPlease complete the setup manually using the commands in README.md")
        return False


if __name__ == "__main__":
    # Update Python version to match current environment
    python_version = get_python_version()
    update_python_version_in_file(Path(PROJECT_DIRECTORY) / "pyproject.toml", python_version)
    update_github_action_python_version(python_version)

    # Remove tox.ini (not needed for web apps)
    remove_tox_ini()

    if "{{cookiecutter.include_github_actions}}" != "y":
        remove_dir(".github")
    else:
        if "{{cookiecutter.mkdocs}}" != "y" and "{{cookiecutter.publish_to_pypi}}" == "n":
            remove_file(".github/workflows/on-release-main.yml")

    if "{{cookiecutter.mkdocs}}" != "y":
        remove_dir("docs")
        remove_file("mkdocs.yml")

    if "{{cookiecutter.dockerfile}}" != "y":
        remove_file("Dockerfile")

    if "{{cookiecutter.codecov}}" != "y":
        remove_file("codecov.yaml")
        if "{{cookiecutter.include_github_actions}}" == "y":
            remove_file(".github/workflows/validate-codecov-config.yml")

    if "{{cookiecutter.devcontainer}}" != "y":
        remove_dir(".devcontainer")

    if "{{cookiecutter.open_source_license}}" == "MIT license":
        move_file("LICENSE_MIT", "LICENSE")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "BSD license":
        move_file("LICENSE_BSD", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "ISC license":
        move_file("LICENSE_ISC", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_APACHE")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "Apache Software License 2.0":
        move_file("LICENSE_APACHE", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_GPL")

    if "{{cookiecutter.open_source_license}}" == "GNU General Public License v3":
        move_file("LICENSE_GPL", "LICENSE")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")

    if "{{cookiecutter.open_source_license}}" == "Not open source":
        remove_file("LICENSE_GPL")
        remove_file("LICENSE_MIT")
        remove_file("LICENSE_BSD")
        remove_file("LICENSE_ISC")
        remove_file("LICENSE_APACHE")

    if "{{cookiecutter.layout}}" == "src":
        if Path("src").is_dir():
            remove_dir("src")
        move_dir("{{cookiecutter.project_slug}}", os.path.join("src", "{{cookiecutter.project_slug}}"))

    # Run automated GitHub setup if requested
    if "{{cookiecutter.automate_github_setup}}" == "y":
        dry_run = "{{cookiecutter.dry_run_github_setup}}" == "y"
        setup_github_repository(dry_run=dry_run)
