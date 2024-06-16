#!/bin/bash
echo "Pylint:"
poetry run pylint src tests
echo "Flake8:"
poetry run flake8 src tests
echo "Mypy:"
poetry run mypy src tests
echo "Pytest:"
poetry run pytest --cov -n auto
