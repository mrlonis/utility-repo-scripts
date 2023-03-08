"""Tests for process_vscode_settings.py with no existing data."""
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
    isort_enabled = True
    python_formatter = "black"
    pylint_enabled = True
    flake8_enabled = True
    pydocstyle_enabled = True
    pycodestyle_enabled = True
    bandit_enabled = True
    mypy_enabled = True
    prospector_enabled = True
    pylama_enabled = True
    pytest_enabled = True
    unittest_enabled = True

    result = process_vscode_settings(
        vscode_settings={},
        test=True,
        include_isort=isort_enabled,
        python_formatter=python_formatter,
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        pycodestyle_enabled=pycodestyle_enabled,
        bandit_enabled=bandit_enabled,
        mypy_enabled=mypy_enabled,
        prospector_enabled=prospector_enabled,
        pylama_enabled=pylama_enabled,
        pytest_enabled=pytest_enabled,
        unittest_enabled=unittest_enabled,
    )
    assert result is not None

    assert_python_default_interpreter_settings(data=result)
    assert_python_analysis_settings(data=result)
    assert_python_formatter_settings(data=result, python_formatter=python_formatter)
    assert_isort_settings(data=result, isort_enabled=isort_enabled)
    assert_python_linting_settings(
        data=result,
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        pycodestyle_enabled=pycodestyle_enabled,
        bandit_enabled=bandit_enabled,
        mypy_enabled=mypy_enabled,
        prospector_enabled=prospector_enabled,
        pylama_enabled=pylama_enabled,
    )
    assert_python_testing_settings(
        data=result, pytest_enabled=pytest_enabled, unittest_enabled=unittest_enabled
    )
