"""Tests for process_vscode_settings.py with no existing data."""

from src.processors.process_vscode_settings import process_vscode_settings
from tests.processors.process_vscode_settings.assert_utils import assert_isort_settings


def test_process_vscode_settings_include_isort():
    """Test the process_vscode_settings function when isort is enabled."""
    include_isort = True

    result = process_vscode_settings(vscode_settings={}, include_isort=include_isort, test=True, debug=True)
    assert result is not None

    assert_isort_settings(data=result, isort_enabled=include_isort)


def test_process_vscode_settings_no_include_isort():
    """Test the process_vscode_settings function when pytest is disabled."""
    include_isort = False

    result = process_vscode_settings(vscode_settings={}, include_isort=include_isort, test=True, debug=True)
    assert result is not None

    assert_isort_settings(data=result, isort_enabled=include_isort)
