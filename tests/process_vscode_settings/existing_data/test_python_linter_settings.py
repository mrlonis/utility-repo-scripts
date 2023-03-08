"""Tests for process_vscode_settings.py with existing data."""
from copy import deepcopy

from src.constants.vscode_settings import SAMPLE_VSCODE_SETTINGS
from src.process_vscode_settings import process_vscode_settings
from tests.process_vscode_settings.assert_utils import assert_python_linting_settings


def test_process_vscode_settings_no_python_linter():
    """Test the process_vscode_settings function when no linter is enabled."""
    pylint_enabled = False
    flake8_enabled = False
    pydocstyle_enabled = False
    pycodestyle_enabled = False
    bandit_enabled = False
    mypy_enabled = False
    prospector_enabled = False
    pylama_enabled = False

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

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


def test_process_vscode_settings_pylint_python_linter():
    """Test the process_vscode_settings function when pylint is enabled."""
    pylint_enabled = True
    flake8_enabled = False
    pydocstyle_enabled = False
    pycodestyle_enabled = False
    bandit_enabled = False
    mypy_enabled = False
    prospector_enabled = False
    pylama_enabled = False

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

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


def test_process_vscode_settings_flake8_python_linter():
    """Test the process_vscode_settings function when flake8 is enabled."""
    pylint_enabled = False
    flake8_enabled = True
    pydocstyle_enabled = False
    pycodestyle_enabled = False
    bandit_enabled = False
    mypy_enabled = False
    prospector_enabled = False
    pylama_enabled = False

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

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


def test_process_vscode_settings_pydocstyle_python_linter():
    """Test the process_vscode_settings function when pydocstyle is enabled."""
    pylint_enabled = False
    flake8_enabled = False
    pydocstyle_enabled = True
    pycodestyle_enabled = False
    bandit_enabled = False
    mypy_enabled = False
    prospector_enabled = False
    pylama_enabled = False

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

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


def test_process_vscode_settings_all_python_linters():
    """Test the process_vscode_settings function when all linters are enabled."""
    pylint_enabled = True
    flake8_enabled = True
    pydocstyle_enabled = True
    pycodestyle_enabled = False
    bandit_enabled = False
    mypy_enabled = False
    prospector_enabled = False
    pylama_enabled = False

    result = process_vscode_settings(
        vscode_settings=deepcopy(SAMPLE_VSCODE_SETTINGS),
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        test=True,
        debug=True,
    )
    assert result is not None

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
