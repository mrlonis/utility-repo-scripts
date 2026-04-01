"""Tests for process_vscode_settings.py flag-driven optional behavior with existing data."""

from copy import deepcopy

from src.constants.vscode_settings import (
    FLAKE8_ARGS_KEY,
    ISORT_ARGS_KEY,
    MYPY_ARGS_KEY,
    PYLINT_ARGS_KEY,
    PYTHON_TESTING_PYTEST_ARGS_KEY,
    PYTHON_TESTING_PYTEST_ENABLED_KEY,
    PYTHON_TESTING_UNITTEST_ARGS_KEY,
    PYTHON_TESTING_UNITTEST_ENABLED_KEY,
    SAMPLE_VSCODE_SETTINGS,
)
from src.process_vscode_settings import process_vscode_settings


def test_process_vscode_settings_disable_optional_features_and_enable_unittest():
    """Existing optional VS Code settings should be removable and unittest can be enabled."""
    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        include_isort=False,
        pylint_enabled=False,
        flake8_enabled=False,
        mypy_enabled=False,
        pytest_enabled=False,
        unittest_enabled=True,
        test=True,
        debug=True,
    )
    assert result is not None

    assert result.get(ISORT_ARGS_KEY) is None
    assert result.get(PYLINT_ARGS_KEY) is None
    assert result.get(FLAKE8_ARGS_KEY) is None
    assert result.get(MYPY_ARGS_KEY) is None
    assert result.get(PYTHON_TESTING_PYTEST_ARGS_KEY) is None
    assert result.get(PYTHON_TESTING_PYTEST_ENABLED_KEY) is False
    assert result.get(PYTHON_TESTING_UNITTEST_ARGS_KEY) == ["-v", "-s", ".", "-p", "*test*.py"]
    assert result.get(PYTHON_TESTING_UNITTEST_ENABLED_KEY) is True
