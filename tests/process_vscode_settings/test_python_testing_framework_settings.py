"""Tests for process_vscode_settings.py with no existing data."""
from src.process_vscode_settings import process_vscode_settings
from tests.process_vscode_settings.assert_utils import assert_python_testing_settings


def test_process_vscode_settings_no_python_testing_framework():
    """Test the process_vscode_settings function when no testing framework is enabled."""
    pytest_enabled = False
    unittest_enabled = False

    result = process_vscode_settings(
        vscode_settings={},
        pytest_enabled=pytest_enabled,
        unittest_enabled=unittest_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

    assert_python_testing_settings(
        data=result, pytest_enabled=pytest_enabled, unittest_enabled=unittest_enabled
    )


def test_process_vscode_settings_pytest_python_testing_framework():
    """Test the process_vscode_settings function when pytest is enabled."""
    pytest_enabled = True
    unittest_enabled = False

    result = process_vscode_settings(
        vscode_settings={},
        pytest_enabled=pytest_enabled,
        unittest_enabled=unittest_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

    assert_python_testing_settings(
        data=result, pytest_enabled=pytest_enabled, unittest_enabled=unittest_enabled
    )


def test_process_vscode_settings_unittest_python_testing_framework():
    """Test the process_vscode_settings function when unittest is enabled."""
    pytest_enabled = False
    unittest_enabled = True

    result = process_vscode_settings(
        vscode_settings={},
        pytest_enabled=pytest_enabled,
        unittest_enabled=unittest_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

    assert_python_testing_settings(
        data=result, pytest_enabled=pytest_enabled, unittest_enabled=unittest_enabled
    )


def test_process_vscode_settings_all_python_testing_framework():
    """Test the process_vscode_settings function when pytest and unittest is enabled."""
    pytest_enabled = True
    unittest_enabled = True

    result = process_vscode_settings(
        vscode_settings={},
        pytest_enabled=pytest_enabled,
        unittest_enabled=unittest_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

    assert_python_testing_settings(
        data=result, pytest_enabled=pytest_enabled, unittest_enabled=unittest_enabled
    )
