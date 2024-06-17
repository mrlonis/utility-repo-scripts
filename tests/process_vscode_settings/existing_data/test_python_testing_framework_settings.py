"""Tests for process_vscode_settings.py with existing data."""

from copy import deepcopy

from src.constants.vscode_settings import SAMPLE_VSCODE_SETTINGS
from src.process_vscode_settings import process_vscode_settings
from tests.process_vscode_settings.assert_utils import assert_python_testing_settings


def test_process_vscode_settings_python_testing_framework():
    """Test the process_vscode_settings function when no testing framework is enabled."""
    result = process_vscode_settings(vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS), test=True, debug=True)
    assert result is not None

    assert_python_testing_settings(data=result)
