"""Tests for process_vscode_settings.py with no existing data."""

from src.processors.process_vscode_settings import process_vscode_settings
from tests.processors.process_vscode_settings.assert_utils import assert_python_default_interpreter_settings


def test_process_vscode_settings_python_default_interpreter_path():
    """Test that the python.defaultInterpreterPath is set correctly."""
    result = process_vscode_settings(vscode_settings={}, test=True, debug=True)
    assert result is not None

    assert_python_default_interpreter_settings(data=result)
