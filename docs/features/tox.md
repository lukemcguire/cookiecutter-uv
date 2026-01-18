# Python Version Testing

This template has been optimized for web application development. Unlike library projects that need to test compatibility across multiple Python versions, web applications typically run on a single Python version in production.

## Single Version Approach

When you generate a project from this template, you'll be prompted to select a Python version from your uv-managed installations. The template will:

- Use the Python version you select during project creation
- Validate that the version is installed via `uv python list`
- Configure `pyproject.toml` with that specific Python version
- Set up CI/CD to test against that single version

This approach simplifies development and testing while being perfectly suitable for web applications.

## Testing

Testing is done automatically in the CI/CD pipeline on every pull request and merge to main using the Python version specified in your project configuration.

## If You Need Multi-Version Testing

If you're building a library or need to test against multiple Python versions, you can manually add [tox-uv](https://github.com/tox-dev/tox-uv) to your project:

```sh
uv add --dev tox-uv
```

Then create a `tox.ini` file and configure the GitHub Actions workflow to use a matrix strategy for testing multiple versions.
