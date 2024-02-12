#!/bin/bash
echo "Pylint:"
poetry run pylint src tests setup_flake8.py setup_pre_commit_config.py setup_pylintrc.py setup_pyproject_toml.py setup_vscode.py
echo "Flake8:"
poetry run flake8 src tests setup_flake8.py setup_pre_commit_config.py setup_pylintrc.py setup_pyproject_toml.py setup_vscode.py
echo "Mypy:"
poetry run mypy src tests setup_flake8.py setup_pre_commit_config.py setup_pylintrc.py setup_pyproject_toml.py setup_vscode.py
echo "Pytest:"
poetry run pytest --cov -n auto
