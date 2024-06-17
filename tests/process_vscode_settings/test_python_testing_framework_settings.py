"""Tests for process_vscode_settings.py with no existing data."""

from src.process_vscode_settings import process_vscode_settings
from tests.process_vscode_settings.assert_utils import assert_python_testing_settings


def test_process_vscode_settings_pytest_python_testing_framework():
    """Test the process_vscode_settings function when pytest is enabled."""
    result = process_vscode_settings(vscode_settings={}, test=True, debug=True)
    assert result is not None

    assert_python_testing_settings(data=result)
