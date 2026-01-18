# Prompt arguments

When running the command `ccp` a prompt will start which enables you to configure your repository. The
prompt values and their explanation are as follows:

---

**author**

Your full name.

**email**

Your email address.

**author_github_handle**

Your github handle, i.e. `<handle>` in `https://github.com/<handle>`

**project_name**

Your project name. Should be equal to the name of your repository
and it should only contain alphanumeric characters and `-`'s.

**project_slug**

The project slug, will default to the `project_name` with all `-`'s
replaced with `_`. This will be how you import your code later, e.g.

```python
from <project_slug> import foo
```

**project_description**

A short description of your project.

**layout**

`"flat"` or `"src"`, defaults to `"flat"`.

- `"flat"`: Places the Python module in the root directory.
- `"src"`: Organizes the project by placing the Python module inside a `src` directory.

**include_github_actions**

`"y"` or `"n"`. Adds a `.github` directory with various actions and
workflows to setup the environment and run code formatting checks
and unittests.

**publish_to_pypi**

`"y"` or `"n"`. Adds functionality to the
`Makefile` and Github workflows to make publishing your code as
simple as creating a new release release on Github. For more info,
see
[Publishing to PyPI](./features/publishing.md).

**deptry**

`"y"` or `"n"`. Adds [deptry](https://fpgmaas.github.io/deptry/)
to the development dependencies of the project, and adds it to the `make check` command. `deptry` is a command line tool to check for issues with dependencies in a Python project, such as obsolete or missing dependencies.

**mkdocs**

`"y"` or `"n"`. Adds [MkDocs](https://www.mkdocs.org/)
documentation to your project. This includes automatically parsing
your docstrings and adding them to the documentation. Documentation
will be deployed to the `gh-pages` branch.

**codecov**

`"y"` or `"n"`. Adds code coverage checks with [codecov](https://about.codecov.io/).

**dockerfile**

`"y"` or `"n"`. Adds a simple [Dockerfile](https://docker.com).

**devcontainer**

`"y"` or `"n"`. Adds a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) specification to the project along with pre-installed pre-commit hooks and VSCode python extension configuration.

**python_version**

Select the Python version for your project from uv-managed Python installations. Options: `["3.13", "3.12", "3.11", "3.10", "3.14"]`

The template will verify that the selected version is installed via uv. If not, you'll be prompted to install it with `uv python install <version>`.

**open_source_license**

Choose a [license](https://choosealicense.com/). Options:
`["1. MIT License", "2. BSD license", "3. ISC license",  "4. Apache Software License 2.0", "5. GNU General Public License v3", "6. Not open source"]`

**automate_github_setup**

`"y"` or `"n"`, defaults to `"n"`. Automates GitHub repository creation and initial setup after project generation. When enabled:

- Creates a GitHub repository using the GitHub CLI (`gh`)
- Initializes local git repository
- Runs `make install` to set up the development environment
- Makes the initial commit (handling pre-commit hooks automatically)
- Adds the GitHub remote
- Pushes the initial commit to GitHub

**Requirements:** GitHub CLI (`gh`) must be installed and authenticated.

**git_remote_protocol**

`"ssh"` or `"https"`, defaults to `"ssh"`. Specifies the protocol to use for the GitHub remote URL. Only applies when `automate_github_setup` is `"y"`.

- `"ssh"`: Uses SSH protocol (e.g., `git@github.com:user/repo.git`) - requires SSH key setup
- `"https"`: Uses HTTPS protocol (e.g., `https://github.com/user/repo.git`) - uses credential helper

**dry_run_github_setup**

`"y"` or `"n"`, defaults to `"n"`. When enabled, shows all commands that would be executed during automated GitHub setup without actually running them. Only applies when `automate_github_setup` is `"y"`.

Useful for:
- Understanding what the automation will do before committing
- Verifying the setup commands for your specific configuration
- Learning the manual setup process

---
