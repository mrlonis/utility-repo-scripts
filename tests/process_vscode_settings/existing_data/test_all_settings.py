"""Tests for process_vscode_settings.py with existing data."""

from copy import deepcopy

from src.constants.vscode_settings import SAMPLE_VSCODE_SETTINGS
from src.process_vscode_settings import process_vscode_settings
from tests.process_vscode_settings.assert_utils import (
    assert_isort_settings,
    assert_python_analysis_settings,
    assert_python_default_interpreter_settings,
    assert_python_formatter_settings,
    assert_python_linting_settings,
    assert_python_testing_settings,
)


# Happy Path Test
def test_process_vscode_settings():
    """Test the process_vscode_settings function with all values set."""
    python_formatter = "black"

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS), test=True, python_formatter=python_formatter
    )
    assert result is not None

    assert_python_default_interpreter_settings(data=result)
    assert_python_analysis_settings(data=result)
    assert_python_formatter_settings(data=result, python_formatter=python_formatter)
    assert_isort_settings(data=result)
    assert_python_linting_settings(data=result)
    assert_python_testing_settings(data=result)
