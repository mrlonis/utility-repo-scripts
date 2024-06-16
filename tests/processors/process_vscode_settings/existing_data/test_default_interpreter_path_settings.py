"""Tests for process_vscode_settings.py with existing data."""

from copy import deepcopy

from src.constants.vscode_settings import SAMPLE_VSCODE_SETTINGS
from src.processors.process_vscode_settings import process_vscode_settings
from tests.processors.process_vscode_settings.assert_utils import assert_python_default_interpreter_settings


def test_process_vscode_settings_python_default_interpreter_path():
    """Test that the python.defaultInterpreterPath is set correctly."""
    result = process_vscode_settings(vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS), test=True, debug=True)
    assert result is not None

    assert_python_default_interpreter_settings(data=result)
