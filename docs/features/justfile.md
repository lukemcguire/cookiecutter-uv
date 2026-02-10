# Justfile

The generated repository will have a `justfile` available. A list of all
available commands (called "recipes" in Just) can be obtained by running
`just --list` or simply `just` in the terminal. Initially, if all features are selected, the following commands are
available:

```
install              Install the virtual environment and install the prek hooks
check                Run code quality tools
test                 Test the code with pytest
build                Build wheel file
clean-build          Clean build artifacts
publish              Publish a release to PyPI
build-and-publish    Build and publish
docs-test            Test if documentation can be built without warnings or errors
docs                 Build and serve the documentation
```

## What is Just?

[Just](https://just.systems/) is a modern command runner written in Rust. It provides a cleaner, more intuitive alternative to Make for task automation with several advantages:

- **Built-in help system**: `just --list` automatically shows all available recipes with their descriptions
- **Cleaner syntax**: More readable and maintainable than Makefile syntax
- **Better cross-platform support**: Works consistently on Linux, macOS, and Windows
- **No legacy baggage**: Designed from scratch for command running, not building software
- **Growing ecosystem**: Increasingly adopted in modern development workflows

## Installation

Just can be installed using various methods:

```bash
# macOS
brew install just

# Linux (using cargo)
cargo install just

# Or download from GitHub releases
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

# Windows (using cargo)
cargo install just

# Windows (using Scoop)
scoop install just
```

For more installation options, see the [official installation guide](https://github.com/casey/just#installation).

## Usage Examples

Run any recipe by name:

```bash
just install        # Set up development environment
just check          # Run all code quality checks
just test           # Run tests
just build          # Build distribution package
just docs           # Serve documentation locally
```

The default recipe (when you run `just` with no arguments) shows the list of available recipes, making it easy to discover what commands are available in your project.

## Recipe Details

### Development Workflow

**`just install`**
- Creates a virtual environment using uv
- Installs all project dependencies
- Installs prek hooks (if in a git repository)
- Generates `uv.lock` file

**`just check`**
- Verifies `uv.lock` is consistent with `pyproject.toml`
- Runs prek (ruff linting and formatting)
- Runs type checker (mypy or ty, depending on configuration)
- Runs deptry to check for obsolete dependencies (if enabled)

**`just test`**
- Runs pytest test suite
- With coverage reporting if codecov is enabled
- With doctest support if codecov is disabled

### Build and Publish

**`just build`**
- Cleans previous build artifacts
- Creates a wheel distribution file using uv

**`just publish`** (if `publish_to_pypi` is enabled)
- Publishes the package to PyPI using twine
- Requires `PYPI_TOKEN` to be configured

**`just build-and-publish`** (if `publish_to_pypi` is enabled)
- Convenience recipe that runs `build` then `publish`

### Documentation

**`just docs`** (if `mkdocs` is enabled)
- Builds and serves documentation locally at `http://localhost:8000`
- Auto-reloads on file changes

**`just docs-test`** (if `mkdocs` is enabled)
- Tests if documentation can be built without warnings or errors
- Useful for CI/CD validation

## Why Just instead of Make?

This template uses Just instead of Make for several reasons:

1. **Simpler syntax**: No tab vs. space issues, clearer recipe definitions
2. **Built-in help**: No need for custom Python scripts to parse comments
3. **Better error messages**: Clear indication of which recipe failed
4. **Cross-platform**: Works identically on Linux, macOS, and Windows
5. **Modern tooling**: Active development and growing community
6. **No implicit rules**: Explicit is better than implicit

## Common Workflows

### Initial Setup
```bash
git clone <your-repo>
cd <your-repo>
just install
```

### Development Cycle
```bash
# Make changes to code
just check          # Verify code quality
just test           # Run tests
git commit -m "..."
```

### Release Process
```bash
just check          # Ensure quality
just test           # Ensure tests pass
just build          # Build package
# Create GitHub release to trigger publishing
```

### Documentation Preview
```bash
just docs           # Preview locally at localhost:8000
just docs-test      # Validate docs build
