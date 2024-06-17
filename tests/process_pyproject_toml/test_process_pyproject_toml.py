"""Test the src/process_pyproject_toml.py file."""

from typing import Any, Dict, cast

from tomlkit import document, parse

from src.constants.pyproject_toml import (
    PYPROJECT_AUTOPEP8_KEY,
    PYPROJECT_BLACK_KEY,
    PYPROJECT_ISORT_KEY,
    PYPROJECT_PYTEST_INI_OPTIONS_KEY,
    PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE,
    PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE,
    PYPROJECT_PYTEST_KEY,
    PYPROJECT_TOOL_KEY,
)
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME
from src.process_pyproject_toml import PyProjectTomlProcessor

TEST_PYPROJECT_PYTEST_INI_OPTIONS_ADDOPTS_VALUE = f"-m fake_mark --ignore=./{REPO_NAME}"


# Test Python Formatter Options
def test_process_pyproject_toml_no_python_formatter():
    """Test the process_pyproject_toml function with no python formatter."""
    python_formatter = ""
    result = PyProjectTomlProcessor(
        pyproject_toml=document(), python_formatter=python_formatter, debug=True, test=True
    ).process_pyproject_toml()
    assert result is not None


def test_process_pyproject_toml_autopep8_python_formatter():
    """Test the process_pyproject_toml function with autopep8 python formatter."""
    python_formatter = "autopep8"
    result = PyProjectTomlProcessor(
        pyproject_toml=document(), python_formatter=python_formatter, debug=True, test=True
    ).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    autopep8_tool = cast(Dict[str, Any], tool.get(PYPROJECT_AUTOPEP8_KEY))
    assert autopep8_tool is not None

    assert len(autopep8_tool.keys()) == 2
    assert autopep8_tool.get("experimental") is True
    assert autopep8_tool.get("max_line_length") == DEFAULT_LINE_LENGTH


def test_process_pyproject_toml_autopep8_python_formatter_existing_values():
    """Test the process_pyproject_toml function with autopep8 python formatter."""
    python_formatter = "autopep8"
    result = PyProjectTomlProcessor(
        pyproject_toml=parse(
            f"""
[{PYPROJECT_TOOL_KEY}.{PYPROJECT_AUTOPEP8_KEY}]
experimental = false
max_line_length = 100
test = "test"
        """
        ),
        python_formatter=python_formatter,
        debug=True,
        test=True,
    ).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    autopep8_tool = cast(Dict[str, Any], tool.get(PYPROJECT_AUTOPEP8_KEY))
    assert autopep8_tool is not None

    assert len(autopep8_tool.keys()) == 3
    assert autopep8_tool.get("experimental") is True
    assert autopep8_tool.get("max_line_length") == DEFAULT_LINE_LENGTH
    assert autopep8_tool.get("test") == "test"


def test_process_pyproject_toml_black_python_formatter():
    """Test the process_pyproject_toml function with black python formatter."""
    python_formatter = "black"
    result = PyProjectTomlProcessor(
        pyproject_toml=document(), python_formatter=python_formatter, debug=True, test=True
    ).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    black_tool = cast(Dict[str, Any], tool.get(PYPROJECT_BLACK_KEY))
    assert black_tool is not None

    assert len(black_tool.keys()) == 1
    assert black_tool.get("line-length") == DEFAULT_LINE_LENGTH


def test_process_pyproject_toml_black_python_formatter_existing_values():
    """Test the process_pyproject_toml function with black python formatter."""
    python_formatter = "black"
    result = PyProjectTomlProcessor(
        pyproject_toml=parse(
            f"""
[{PYPROJECT_TOOL_KEY}.{PYPROJECT_BLACK_KEY}]
line-length = 100
test = "test"
        """
        ),
        python_formatter=python_formatter,
        debug=True,
        test=True,
    ).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    black_tool = cast(Dict[str, Any], tool.get(PYPROJECT_BLACK_KEY))
    assert black_tool is not None

    assert len(black_tool.keys()) == 2
    assert black_tool.get("line-length") == DEFAULT_LINE_LENGTH
    assert black_tool.get("test") == "test"


# Test isort Options
def test_process_pyproject_toml_isort():
    """Test the process_pyproject_toml function with isort."""
    result = PyProjectTomlProcessor(pyproject_toml=document(), debug=True, test=True).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    isort_tool = cast(Dict[str, Any], tool.get(PYPROJECT_ISORT_KEY))
    assert isort_tool is not None

    assert len(isort_tool.keys()) == 2
    assert isort_tool.get("line_length") == DEFAULT_LINE_LENGTH
    assert isort_tool.get("profile") == "black"


def test_process_pyproject_toml_isort_existing_values():
    """Test the process_pyproject_toml function with isort."""
    result = PyProjectTomlProcessor(
        pyproject_toml=parse(
            f"""
[{PYPROJECT_TOOL_KEY}.{PYPROJECT_ISORT_KEY}]
line_length = 100
test = "test"
        """
        ),
        debug=True,
        test=True,
    ).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    isort_tool = cast(Dict[str, Any], tool.get(PYPROJECT_ISORT_KEY))
    assert isort_tool is not None

    assert len(isort_tool.keys()) == 3
    assert isort_tool.get("line_length") == DEFAULT_LINE_LENGTH
    assert isort_tool.get("test") == "test"


# Test pytest Options
def test_process_pyproject_toml_pytest():
    """Test the process_pyproject_toml function with pytest."""
    result = PyProjectTomlProcessor(pyproject_toml=document(), debug=True, test=True).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    pytest_tool = cast(Dict[str, Any], tool.get(PYPROJECT_PYTEST_KEY))
    assert pytest_tool is not None
    assert len(pytest_tool.keys()) == 1

    ini_options = cast(Dict[str, Any], pytest_tool.get("ini_options"))
    assert ini_options is not None
    assert len(ini_options.keys()) == 5

    assert ini_options.get("addopts") == f"--ignore=./{REPO_NAME}"
    assert ini_options.get("log_cli") is False
    assert ini_options.get("log_cli_level") == "WARNING"
    assert ini_options.get("log_cli_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE
    assert ini_options.get("log_cli_date_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE


def test_process_pyproject_toml_pytest_existing_values():
    """Test the process_pyproject_toml function with pytest."""
    result = PyProjectTomlProcessor(
        pyproject_toml=parse(
            f"""
[{PYPROJECT_TOOL_KEY}.{PYPROJECT_PYTEST_KEY}.{PYPROJECT_PYTEST_INI_OPTIONS_KEY}]
addopts = "-m fake_mark"
log_cli = true
log_cli_level = "INFO"
log_cli_format = "{PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE}"
log_cli_date_format = "{PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE}"
test = "test"
        """
        ),
        debug=True,
        test=True,
    ).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    pytest_tool = cast(Dict[str, Any], tool.get(PYPROJECT_PYTEST_KEY))
    assert pytest_tool is not None
    assert len(pytest_tool.keys()) == 1

    ini_options = cast(Dict[str, Any], pytest_tool.get("ini_options"))
    assert ini_options is not None
    assert len(ini_options.keys()) == 6

    assert ini_options.get("addopts") == TEST_PYPROJECT_PYTEST_INI_OPTIONS_ADDOPTS_VALUE
    assert ini_options.get("log_cli") is False
    assert ini_options.get("log_cli_level") == "WARNING"
    assert ini_options.get("log_cli_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE
    assert ini_options.get("log_cli_date_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE
    assert ini_options.get("test") == "test"


def test_process_pyproject_toml_pytest_existing_value_addopts_has_ignore():
    """Test the process_pyproject_toml function with pytest."""
    result = PyProjectTomlProcessor(
        pyproject_toml=parse(
            f"""
[{PYPROJECT_TOOL_KEY}.{PYPROJECT_PYTEST_KEY}.{PYPROJECT_PYTEST_INI_OPTIONS_KEY}]
addopts = "{TEST_PYPROJECT_PYTEST_INI_OPTIONS_ADDOPTS_VALUE}"
log_cli = true
log_cli_level = "INFO"
log_cli_format = "{PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE}"
log_cli_date_format = "{PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE}"
test = "test"
        """
        ),
        debug=True,
        test=True,
    ).process_pyproject_toml()
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    pytest_tool = cast(Dict[str, Any], tool.get(PYPROJECT_PYTEST_KEY))
    assert pytest_tool is not None
    assert len(pytest_tool.keys()) == 1

    ini_options = cast(Dict[str, Any], pytest_tool.get("ini_options"))
    assert ini_options is not None
    assert len(ini_options.keys()) == 6

    assert ini_options.get("addopts") == TEST_PYPROJECT_PYTEST_INI_OPTIONS_ADDOPTS_VALUE
    assert ini_options.get("log_cli") is False
    assert ini_options.get("log_cli_level") == "WARNING"
    assert ini_options.get("log_cli_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE
    assert ini_options.get("log_cli_date_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE
    assert ini_options.get("test") == "test"


# Happy Path Test
def test_process_pyproject_toml():
    """Test the process_pyproject_toml function with all options set."""
    result = PyProjectTomlProcessor(
        pyproject_toml=document(), python_formatter="black", line_length=DEFAULT_LINE_LENGTH, test=True
    ).process_pyproject_toml()
    assert result is not None

    tools = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tools is not None

    print(result)

    black_tool = cast(Dict[str, Any], tools.get(PYPROJECT_BLACK_KEY))
    assert black_tool is not None
    assert black_tool.get("line-length") == DEFAULT_LINE_LENGTH

    isort_tool = cast(Dict[str, Any], tools.get(PYPROJECT_ISORT_KEY))
    assert isort_tool is not None
    assert isort_tool.get("line_length") == DEFAULT_LINE_LENGTH
    assert isort_tool.get("profile") == "black"

    pytest_tool = cast(Dict[str, Any], tools.get(PYPROJECT_PYTEST_KEY))
    assert pytest_tool is not None

    ini_options = cast(Dict[str, Any], pytest_tool.get(PYPROJECT_PYTEST_INI_OPTIONS_KEY))
    assert ini_options is not None

    assert ini_options.get("addopts") == f"--ignore=./{REPO_NAME}"
    assert ini_options.get("log_cli") is False
    assert ini_options.get("log_cli_level") == "WARNING"
    assert ini_options.get("log_cli_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE
    assert ini_options.get("log_cli_date_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE
