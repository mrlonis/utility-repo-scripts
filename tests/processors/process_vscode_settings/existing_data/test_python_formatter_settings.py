"""Tests for process_vscode_settings.py with existing data."""

from copy import deepcopy

from src.constants.vscode_settings import SAMPLE_VSCODE_SETTINGS
from src.processors.process_vscode_settings import process_vscode_settings
from tests.processors.process_vscode_settings.assert_utils import assert_python_formatter_settings


def test_process_vscode_settings_no_python_formatter():
    """Test the process_vscode_settings function when no formatter is enabled."""
    python_formatter = ""

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        python_formatter=python_formatter,
        test=True,
        debug=True,
    )
    assert result is not None

    assert_python_formatter_settings(data=result, python_formatter=python_formatter)


def test_process_vscode_settings_autopep8_python_formatter():
    """Test the process_vscode_settings function when autopep8 is enabled."""
    python_formatter = "autopep8"

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        python_formatter=python_formatter,
        test=True,
        debug=True,
    )
    assert result is not None

    assert_python_formatter_settings(data=result, python_formatter=python_formatter)


def test_process_vscode_settings_black_python_formatter():
    """Test the process_vscode_settings function when black is enabled."""
    python_formatter = "black"

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        python_formatter=python_formatter,
        test=True,
        debug=True,
    )
    assert result is not None

    assert_python_formatter_settings(data=result, python_formatter=python_formatter)
