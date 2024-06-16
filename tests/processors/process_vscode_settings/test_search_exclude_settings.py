"""Tests for process_vscode_settings.py with no existing data."""

from src.processors.process_vscode_settings import process_vscode_settings
from tests.processors.process_vscode_settings.assert_utils import assert_search_exclude_settings


def test_process_vscode_settings_search_exclude_includes_repo():
    """Test that the python.defaultInterpreterPath is set correctly."""
    result = process_vscode_settings(vscode_settings={}, test=True, debug=True)
    assert result is not None

    assert_search_exclude_settings(data=result)
