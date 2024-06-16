"""Tests for process_vscode_settings.py with existing data."""

from copy import deepcopy

from src.constants.vscode_settings import SAMPLE_VSCODE_SETTINGS
from src.processors.process_vscode_settings import process_vscode_settings
from tests.processors.process_vscode_settings.assert_utils import assert_search_exclude_settings


def test_process_vscode_settings_search_exclude_includes_repo():
    """Test that the python.defaultInterpreterPath is set correctly."""
    result = process_vscode_settings(vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS), test=True, debug=True)
    assert result is not None

    assert_search_exclude_settings(data=result)
