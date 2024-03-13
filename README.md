# utility-repo-scripts

This repository holds common scripts for use in python repositories. The main script of note is [setup_python_app.sh](./setup_python_app.sh).

## Table of Contents

- [utility-repo-scripts](#utility-repo-scripts)
  - [Table of Contents](#table-of-contents)
  - [TODO](#todo)
  - [Usage](#usage)
    - [How Python is Determined](#how-python-is-determined)
      - [pyenv](#pyenv)
      - [Brew](#brew)
    - [CLI Flags](#cli-flags)
    - [Supported Package Managers](#supported-package-managers)
      - [pip](#pip)
        - [pip: Dev, Test \& Prod Requirements](#pip-dev-test--prod-requirements)
      - [pip-tools](#pip-tools)
        - [pip-tools: Setup](#pip-tools-setup)
        - [pip-tools: Dev, Test \& Prod Requirements](#pip-tools-dev-test--prod-requirements)
        - [pip-tools: Rebuilding Virtual Environment](#pip-tools-rebuilding-virtual-environment)
      - [poetry](#poetry)
        - [Poetry: Setup](#poetry-setup)
        - [poetry: Rebuilding Virtual Environment](#poetry-rebuilding-virtual-environment)
  - [Testing](#testing)
  - [Linting](#linting)
  - [Brew Packages](#brew-packages)
    - [shfmt](#shfmt)
    - [shellcheck](#shellcheck)
      - [shellcheck VS Code Extension](#shellcheck-vs-code-extension)
    - [Ruby](#ruby)
      - [Markdownlint](#markdownlint)
    - [(Optional) pyenv](#optional-pyenv)

## TODO

- Add `.prettierrc` file if it doesn't exist
- Fix for new VS Code extensions and settings
- Create `pyproject.toml` if it doesn't exist

## Usage

This repo should be added to another repo as a submodule

```sh
git submodule add -b main https://github.com/mrlonis/utility-repo-scripts.git
git commit -m "Adding utility-repo-scripts"
```

This will add the `utility-repo-scripts` repository as a submodule in the `utility-repo-scripts` folder within your project. Submodules are not cloned by default so you should add a step to your `setup` script in the project to initialize it if it wasn't cloned already. This `setup` script should work for most projects:

```sh
#!/bin/bash
git submodule update --init --remote --force
source utility-repo-scripts/setup_python_app.sh --package_manager="pip" --python_version="3.8"
```

### How Python is Determined

#### pyenv

If you have [pyenv](https://github.com/pyenv/pyenv) installed, the `setup_python_app.sh` script will use `pyenv` commands to make and setup the virtual environment.

The `--python_version` flag will be used to set the version of python to use for the virtual environment in `pyenv`.

#### Brew

If `pyenv` is not installed, the `setup_python_app.sh` script will assume `brew` is being used to install `python`. The `--python_version` flag will be used to set the version of python to use for the virtual environment. This flag is a python version such as `"3.8"`. This will result in the `setup_python_app.sh` script attempting to call the `brew` symlinked `python3.8` command. If this version of python was, for some reason, not installed by `brew`, the script will fail. Installing the version of python you want to use with `brew` is outside the scope of this script. Installing the missing version and re-running the `./setup` script will resolve the issue.

When `brew` is assumed as the python source, the `setup_python_app.sh` script will default to create the virtual environment at your exported `WORKON_HOME` environment variable.

If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation), the `setup_python_app.sh` script will default to create the virtual environment at your exported `WORKON_HOME` environment variable.

If this variable is not set or you don't use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation), it will default to `$HOME/.venvs/<project-name>`.

You can change this by adding an environment variable to your `.zshrc` or `.bashrc` file:

```shell
export WORKON_HOME="$HOME/SOME/CUSTOM/PATH/FOR/VIRTUAL/ENVIRONMENTS"
```

This `WORKON_HOME` variable is used by [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation) to determine where to look for virtual environments when invoking `workon <project-name>`.

[Back to Top](#utility-repo-scripts)

### CLI Flags

The `setup` script accepts a few flags to customize the setup process:

**Note**: `0` is False and `1` is True

| Flag                               | Description                                                                     | Default                 | Valid Values                    |
| :--------------------------------- | :------------------------------------------------------------------------------ | :---------------------- | :------------------------------ |
| `-d` or `--debug`                  | Enables or disables debug echo statements                                       | `False`                 |                                 |
| `--package_manager`                | Specifies which package manager to use                                          | `pip`                   | [`pip`, `pip-tools`, `poetry`]  |
| `-r` or `--rebuild_venv`           | Specifies whether or not to delete and re-create the virtual environment or not | `False`                 |                                 |
| `--python_version`                 | Specifies the python version to use                                             | `3.8`                   | [`3.8`, `3.9`, `3.10`, `3.11`]  |
| `--is_package`                     | Specifies whether or not the project is a package                               | `False`                 |                                 |
| `--include_jumanji_house`          | Specifies whether or not to include the `jumanjihouse` `pre-commit` hooks       | `False`                 |                                 |
| `--include_prettier`               | Specifies whether or not to include the `prettier` `pre-commit` hooks           | `False`                 |                                 |
| `--include_isort`                  | Specifies whether or not to include the `isort` `pre-commit` hooks              | `False`                 |                                 |
| `--python_formatter`               | Specifies which python formatter to use                                         | `''`                    | [`''`, `autopep8`, `black`]     |
| `--pylint_enabled`                 | Specifies whether or not to enable `pylint`                                     | `False`                 |                                 |
| `--flake8_enabled`                 | Specifies whether or not to enable `flake8`                                     | `False`                 |                                 |
| `--pytest_enabled`                 | Specifies whether or not to enable `pytest`                                     | `False`                 |                                 |
| `--unittest_enabled`               | Specifies whether or not to enable `unittest`                                   | `False`                 |                                 |
| `--overwrite_vscode_launch`        | Enables or disables the overriding of the `.vscode/launch.json` file            | `False`                 |                                 |
| `--line_length`                    | Specifies the line length to use for various settings                           | `125`                   | `Any non-zero positive integer` |
| `--pre_commit_pylint_entry_prefix` | Specifies the prefix to use for the `pylint` pre-commit hook entry              | `utility-repo-scripts/` |                                 |

[Back to Top](#utility-repo-scripts)

### Supported Package Managers

#### pip

Version 1 of the setup script uses `pip` to manage the python dependencies. This is the default version of the setup script. To use version 1 of the setup script, add the following to your `setup` script:

```sh
#!/bin/bash
git submodule update --init --remote --force
source utility-repo-scripts/setup_python_app.sh \
    --package_manager="pip" \
    --rebuild_venv="$rebuild_venv" \
    --python_version="3.8" \
    --python_formatter="" \
    --pylint_enabled \
    --pytest_enabled \
    --overwrite_vscode_launch \
    --line_length=125
```

[Back to Top](#utility-repo-scripts)

##### pip: Dev, Test & Prod Requirements

We can separate our requirements into different files to make it easier to manage them. For example, we can have a `requirements-dev.txt` file that contains the dependencies needed for development and testing. We can then have a `requirements-test.txt` file that contains the dependencies needed for testing. We can then have a `requirements.txt` file that contains the dependencies needed for production.

```text
# requirements-dev.txt
-r requirements-test.txt
pre-commit
```

```text
# requirements-test.txt
-r requirements.txt
pylint
```

```text
# requirements.txt
pydantic[dotenv]
```

The version 1 of the `setup` script looks for the above files starting with `requirements-dev.txt` and then `requirements-test.txt` and then `requirements.txt`.

If you wish to have `dev` dependencies but not `test` dependencies, you can create a `requirements-dev.txt` file that points the `-r` flag to `requirements.txt` instead of `requirements-test.txt`.

If you wish to only have `test` dependencies, you can create a `requirements-test.txt` file that points the `-r` flag to `requirements.txt` and remove the `requirements-dev.txt` file from the repo.

As shown in the example files above, if you run `./setup` in your project, the resulting command the `setup` script would run is `pip install -r requirements-dev.txt` which would end up installing all the dependencies in `requirements-dev.txt`, `requirements-test.txt` and `requirements.txt`.

This is because the `-r requirements-test.txt` line in `requirements-dev.txt` and the `-r requirements.txt` line in `requirements-test.txt` will ensure that the dependencies in `requirements-test.txt` and `requirements.txt` are also installed when calling the command `pip install -r requirements-dev.txt`.

[Back to Top](#utility-repo-scripts)

#### pip-tools

Version 2 of the setup script uses [pip-tools](https://github.com/jazzband/pip-tools) to manage the python dependencies. To use version 2 of the setup script, modify your `setup` script to the following:

```sh
#!/bin/bash
git submodule update --init --remote --force
rebuild_venv=$1
rebuild_venv="${rebuild_venv:-0}"
source utility-repo-scripts/setup_python_app.sh \
    --package_manager="pip-tools" \
    --rebuild_venv="$rebuild_venv" \
    --python_version="3.8" \
    --python_formatter="" \
    --pylint_enabled \
    --pytest_enabled \
    --overwrite_vscode_launch \
    --line_length=125
```

[Back to Top](#utility-repo-scripts)

##### pip-tools: Setup

To ensure your project will work with version 2 of the setup script, we must first setup at least a `requirements.in` file. This file will contain the direct dependencies of your project. For now, this file should at least contain `pip-tools`.

`requirements.in`:

```requirements
pip-tools
```

Since the newly created virtual environment might not have `pip-tools`:

1. Run: `pip install pip-tools`
1. Then run, `pip-compile -U` to build the `requirements.txt` file.

You can now run `./setup` to setup your project.

[Back to Top](#utility-repo-scripts)

##### pip-tools: Dev, Test & Prod Requirements

We can separate our requirements into different files to make it easier to manage them. For example, we can have a `requirements-dev.in` file that contains the dependencies needed for development and testing. We can then have a `requirements-test.in` file that contains the dependencies needed for testing. We can then have a `requirements.in` file that contains the dependencies needed for production.

```text
# requirements-dev.in
-c requirements.txt
-c requirements-test.txt
pip-tools
pre-commit
```

```text
# requirements-test.in
-c requirements.txt
pylint
```

```text
# requirements.in
pydantic[dotenv]
```

We can then compile these files into their respective `.txt` files:

```shell
pip-compile -U --resolver=backtracking --strip-extras requirements.in
pip-compile -U --resolver=backtracking --strip-extras requirements-test.in
pip-compile -U --resolver=backtracking requirements-dev.in
```

The version 2 of the `setup` script looks for the compiled output of the above commands (aka the `requirements-dev.txt`, `requirements-test.txt`, and `requirements.txt`).

- If `dev`, `test`, and `prod` requirements are found, the resulting command the `setup` script would run is `pip-sync requirements-dev.txt requirements-test.txt requirements.txt`.
- If only `dev` and `prod` requirements are found, the resulting command the `setup` script would run is `pip-sync requirements-dev.txt requirements.txt`.
- If only `test` and `prod` requirements are found, the resulting command the `setup` script would run is `pip-sync requirements-test.txt requirements.txt`.
- If only `prod` requirements are found, the resulting command the `setup` script would run is `pip-sync requirements.txt`.

[Back to Top](#utility-repo-scripts)

##### pip-tools: Rebuilding Virtual Environment

The goal of Version 2 of the setup script is to make it faster to setup and install dependencies. A core part of this is to not rebuild the virtual environment every time the `setup` script is run. This done by checking if the virtual environment destination directory already exists. If it does, we assume that this environment is in a healthy state (i.e. the `python` and `pip` executables and other site-packages are intact). If the folder exists, we can speed up setup by leveraging `pip-sync` on the `requirements` files in the repository. If the virtual environment does not exist, we create one prior to performing `pip-sync`.

Since the virtual environment is built and linked to the system executables at creation, we must rebuild the virtual environment whenever our system changes. One example that would prompt a rebuild of the virtual environment is `python` being updated by `brew`. This would result in the previously linked `python` executable to no longer exist, and this the virtual environment would be in an unhealthy state. To rebuild the virtual environment, run the `setup` script with the `--rebuild_venv` flag set to `1`.

Alternatively, you can set the setup script to accept input for easy ad-hoc re-building. To do this, set your `setup` script to the following:

```sh
#!/bin/bash
git submodule update --init --remote --force
rebuild_venv=$1
rebuild_venv="${rebuild_venv:-0}"
source utility-repo-scripts/setup_python_app.sh \
    --package_manager="pip-tools" \
    --rebuild_venv="$rebuild_venv" \
    --python_version="3.8" \
    --python_formatter="" \
    --pylint_enabled \
    --pytest_enabled \
    --overwrite_vscode_launch \
    --line_length=125
```

To then easily run and re-build the virtual environment on the fly without modifying the `setup` script, run the following:

```sh
./setup 1
```

[Back to Top](#utility-repo-scripts)

#### poetry

Version 3 of the `setup` script uses [Poetry](https://python-poetry.org/docs/) to manage the python dependencies. To use version 3 of the setup script, modify your `setup` script to the following:

```sh
#!/bin/bash
git submodule update --init --remote --force
rebuild_venv=$1
rebuild_venv="${rebuild_venv:-0}"
source utility-repo-scripts/setup_python_app.sh \
    --package_manager="poetry" \
    --rebuild_venv="$rebuild_venv" \
    --python_version="3.8" \
    --python_formatter="" \
    --pylint_enabled \
    --pytest_enabled \
    --overwrite_vscode_launch \
    --line_length=125
```

[Back to Top](#utility-repo-scripts)

##### Poetry: Setup

To setup a project for version 3 of the `setup` script, we must first install `Poetry`. To install `Poetry`, view the [Poetry installation instructions](https://python-poetry.org/docs/#installation).

Once `Poetry` is installed, we can then run the following command to setup the project:

```shell
poetry init
```

This will create a `pyproject.toml` file in the root of the project. This file will contain the project's dependencies. To add a dependency, run the following command:

```shell
poetry add <dependency>
```

For more information about `Poetry`, view the [Poetry documentation](https://python-poetry.org/docs/).

[Back to Top](#utility-repo-scripts)

##### poetry: Rebuilding Virtual Environment

The goal of Version 3 of the setup script is to make it faster to setup and install dependencies. A core part of this is to not rebuild the virtual environment every time the `setup` script is run. This done by checking if the virtual environment destination directory already exists. If it does, we assume that this environment is in a healthy state (i.e. the `python` and `pip` executables and other site-packages are intact). If the folder exists, we can speed up setup by leveraging `poetry install --sync` in the repository. If the virtual environment does not exist, we create one prior to performing `poetry install --sync`.

Since the virtual environment is built and linked to the system executables at creation, we must rebuild the virtual environment whenever our system changes. One example that would prompt a rebuild of the virtual environment is `python` being updated by `brew`. This would result in the previously linked `python` executable to no longer exist, and this the virtual environment would be in an unhealthy state. To rebuild the virtual environment, run the `setup` script with the `--rebuild_venv` flag set to `1`.

Alternatively, you can set the setup script to accept input for easy ad-hoc re-building. To do this, set your `setup` script to the following:

```sh
#!/bin/bash
git submodule update --init --remote --force
rebuild_venv=$1
rebuild_venv="${rebuild_venv:-0}"
source utility-repo-scripts/setup_python_app.sh \
    --package_manager="poetry" \
    --rebuild_venv="$rebuild_venv" \
    --python_version="3.8" \
    --python_formatter="" \
    --pylint_enabled \
    --pytest_enabled \
    --overwrite_vscode_launch \
    --line_length=125
```

To then easily run and re-build the virtual environment on the fly without modifying the `setup` script, run the following:

```sh
./setup 1
```

[Back to Top](#utility-repo-scripts)

## Testing

To test this repo, run the following command:

```shell
poetry run pytest --cov -n auto
```

## Linting

To lint this repo, run the following command:

```shell
poetry run pylint src tests setup_flake8.py setup_pre_commit_config.py setup_pylintrc.py setup_pyproject_toml.py setup_vscode.py
poetry run flake8 src tests setup_flake8.py setup_pre_commit_config.py setup_pylintrc.py setup_pyproject_toml.py setup_vscode.py
```

## Brew Packages

The following section details recommended `brew` packages to install. **Note:** These packages are required for the `pre-commit` to function.

[Back to Top](#utility-repo-scripts)

### shfmt

To format shell files, install `shfmt` with brew:

```shell
brew install shfmt
```

and then run the following command to format all shell files in the repo:

```shell
shfmt -l -w setup_python_app.sh
```

[Back to Top](#utility-repo-scripts)

### shellcheck

To lint shell files, install `shellcheck` with brew:

```shell
brew install shellcheck
```

and then run the following command to lint a shell file changing out the file name/path as needed:

```shell
shellcheck setup_python_app.sh
```

[Back to Top](#utility-repo-scripts)

#### shellcheck VS Code Extension

To get integrated shellcheck linting in VS Code, install the [shellcheck extension](https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck)

[Back to Top](#utility-repo-scripts)

### Ruby

```shell
brew install openssl@3 readline libyaml gmp
brew install rust
brew install rbenv ruby-build
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.zprofile
echo 'eval "$(rbenv init -)"' >> ~/.zprofile
rbenv install 3.2.1
rbenv global 3.2.1
rbenv local 3.2.1
rbenv rehash
gem update --system
gem install mdl
```

[Back to Top](#utility-repo-scripts)

#### Markdownlint

```shell
gem install mdl
```

[Back to Top](#utility-repo-scripts)

### (Optional) pyenv

To install `pyenv`, run the following command:

```shell
brew install pyenv pyenv-virtualenv
```

[Back to Top](#utility-repo-scripts)
