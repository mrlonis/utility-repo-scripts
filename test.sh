#!/bin/bash
poetry run pylint src tests setup_flake8.py setup_pre_commit_config.py setup_pylintrc.py setup_pyproject_toml.py setup_vscode.py
poetry run flake8 src tests setup_flake8.py setup_pre_commit_config.py setup_pylintrc.py setup_pyproject_toml.py setup_vscode.py
poetry run pydocstyle src tests setup_flake8.py setup_pre_commit_config.py setup_pylintrc.py setup_pyproject_toml.py setup_vscode.py
poetry run bandit -c pyproject.toml -r .
poetry run pytest --cov -n auto
