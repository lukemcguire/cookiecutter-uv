<p align="center">
  <img width="600" src="https://raw.githubusercontent.com/lukemcguire/cookiecutter-uv/main/docs/static/cookiecutter.svg">
</p style = "margin-bottom: 2rem;">

---

[![Build status](https://img.shields.io/github/actions/workflow/status/lukemcguire/cookiecutter-uv/main.yml?branch=main)](https://github.com/lukemcguire/cookiecutter-uv/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-_3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/lukemcguire/cookiecutter-uv/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://lukemcguire.github.io/cookiecutter-uv/)
[![License](https://img.shields.io/github/license/lukemcguire/cookiecutter-uv)](https://img.shields.io/github/license/lukemcguire/cookiecutter-uv)

This is a modern Cookiecutter template that can be used to initiate a Python project with all the necessary tools for development, testing, and deployment. It supports the following features:

- [uv](https://docs.astral.sh/uv/) for dependency management
- Supports both [src and flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
- CI/CD with [GitHub Actions](https://github.com/features/actions)
- Pre-commit hooks with [prek](https://github.com/RobertCraigie/prek)
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/)/[ty](https://docs.astral.sh/ty/) and [deptry](https://github.com/fpgmaas/deptry/).
- Publishing to [PyPI](https://pypi.org) by creating a new release on GitHub
- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [codecov](https://about.codecov.io/)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Containerization with [Docker](https://www.docker.com/) or [Podman](https://podman.io/)
- Development environment with [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers)

---

<p align="center">
  <a href="https://lukemcguire.github.io/cookiecutter-uv/">Documentation</a> - <a href="https://github.com/lukemcguire/cookiecutter-uv-example">Example</a>
</p>

---

## Quickstart

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/lukemcguire/cookiecutter-uv.git
```

or if you don't have `uv` installed yet:

```bash
pip install cookiecutter
cookiecutter https://github.com/lukemcguire/cookiecutter-uv.git
```

Follow the prompts to configure your project. You'll be asked to select a Python version from your uv-managed installations. The template will verify the version is available.

Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

### Python Version Selection

The template will prompt you to select from Python 3.10, 3.11, 3.12, 3.13, or 3.14. If your selected version isn't installed, install it with:

```bash
uv python install 3.13  # or your preferred version
```

## Acknowledgements

This project is a fork of [Florian Maas'](https://github.com/fpgmaas/cookiecutter-uv) project which is partially based on [Audrey
Feldroy\'s](https://github.com/audreyfeldroy)\'s great
[cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage)
repository.
