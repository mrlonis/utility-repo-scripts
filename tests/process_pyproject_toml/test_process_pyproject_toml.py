"""Test the src/process_pyproject_toml.py file."""
from typing import Any, Dict, cast

from tomlkit import document, parse

from src.constants.pyproject_toml import (
    PYPROJECT_AUTOPEP8_KEY,
    PYPROJECT_BLACK_KEY,
    PYPROJECT_ISORT_KEY,
    PYPROJECT_PYCODESTYLE_MATCH_VALUE,
    PYPROJECT_PYDOCSTYLE_KEY,
    PYPROJECT_PYTEST_INI_OPTIONS_KEY,
    PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE,
    PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE,
    PYPROJECT_PYTEST_KEY,
    PYPROJECT_TOOL_KEY,
)
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME
from src.process_pyproject_toml import process_pyproject_toml

TEST_PYPROJECT_PYTEST_INI_OPTIONS_ADDOPTS_VALUE = f"-m fake_mark --ignore=./{REPO_NAME}"


# No Options
def test_process_pyproject_toml_no_options():
    """Test the process_pyproject_toml function with no options set."""
    result = process_pyproject_toml(pyproject_toml=document(), debug=True, test=True)
    assert result is not None
    assert not result


# Test Python Formatter Options
def test_process_pyproject_toml_no_python_formatter():
    """Test the process_pyproject_toml function with no python formatter."""
    python_formatter = ""
    result = process_pyproject_toml(
        pyproject_toml=document(), python_formatter=python_formatter, debug=True, test=True
    )
    assert result is not None
    assert not result


def test_process_pyproject_toml_autopep8_python_formatter():
    """Test the process_pyproject_toml function with autopep8 python formatter."""
    python_formatter = "autopep8"
    result = process_pyproject_toml(
        pyproject_toml=document(), python_formatter=python_formatter, debug=True, test=True
    )
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
    result = process_pyproject_toml(
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
    )
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
    result = process_pyproject_toml(
        pyproject_toml=document(), python_formatter=python_formatter, debug=True, test=True
    )
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
    result = process_pyproject_toml(
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
    )
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    black_tool = cast(Dict[str, Any], tool.get(PYPROJECT_BLACK_KEY))
    assert black_tool is not None

    assert len(black_tool.keys()) == 2
    assert black_tool.get("line-length") == DEFAULT_LINE_LENGTH
    assert black_tool.get("test") == "test"


# Test pydocstyle Options
def test_process_pyproject_toml_no_pydocstyle():
    """Test the process_pyproject_toml function with no pydocstyle."""
    pydocstyle_enabled = False
    result = process_pyproject_toml(
        pyproject_toml=document(), pydocstyle_enabled=pydocstyle_enabled, debug=True, test=True
    )
    assert result is not None
    assert not result


def test_process_pyproject_toml_pydocstyle():
    """Test the process_pyproject_toml function with pydocstyle."""
    pydocstyle_enabled = True
    result = process_pyproject_toml(
        pyproject_toml=document(), pydocstyle_enabled=pydocstyle_enabled, debug=True, test=True
    )
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    pydocstyle_tool = cast(Dict[str, Any], tool.get(PYPROJECT_PYDOCSTYLE_KEY))
    assert pydocstyle_tool is not None

    assert len(pydocstyle_tool.keys()) == 2
    assert pydocstyle_tool.get("inherit") is False
    assert pydocstyle_tool.get("match") == PYPROJECT_PYCODESTYLE_MATCH_VALUE


def test_process_pyproject_toml_pydocstyle_existing_values():
    """Test the process_pyproject_toml function with pydocstyle."""
    pydocstyle_enabled = True
    result = process_pyproject_toml(
        pyproject_toml=parse(
            f"""
[{PYPROJECT_TOOL_KEY}.{PYPROJECT_PYDOCSTYLE_KEY}]
inherit = true
match = "{PYPROJECT_PYCODESTYLE_MATCH_VALUE}"
test = "test"
        """
        ),
        pydocstyle_enabled=pydocstyle_enabled,
        debug=True,
        test=True,
    )
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    pydocstyle_tool = cast(Dict[str, Any], tool.get(PYPROJECT_PYDOCSTYLE_KEY))
    assert pydocstyle_tool is not None

    assert len(pydocstyle_tool.keys()) == 3
    assert pydocstyle_tool.get("inherit") is False
    assert pydocstyle_tool.get("match") == PYPROJECT_PYCODESTYLE_MATCH_VALUE
    assert pydocstyle_tool.get("test") == "test"


# Test isort Options
def test_process_pyproject_toml_no_isort():
    """Test the process_pyproject_toml function with no isort."""
    include_isort = False
    result = process_pyproject_toml(
        pyproject_toml=document(), include_isort=include_isort, debug=True, test=True
    )
    assert result is not None
    assert not result


def test_process_pyproject_toml_isort():
    """Test the process_pyproject_toml function with isort."""
    include_isort = True
    result = process_pyproject_toml(
        pyproject_toml=document(), include_isort=include_isort, debug=True, test=True
    )
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    isort_tool = cast(Dict[str, Any], tool.get(PYPROJECT_ISORT_KEY))
    assert isort_tool is not None

    assert len(isort_tool.keys()) == 1
    assert isort_tool.get("line_length") == DEFAULT_LINE_LENGTH


def test_process_pyproject_toml_isort_with_profile():
    """Test the process_pyproject_toml function with isort."""
    include_isort = True
    isort_profile = "django"
    result = process_pyproject_toml(
        pyproject_toml=document(),
        include_isort=include_isort,
        isort_profile=isort_profile,
        debug=True,
        test=True,
    )
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    isort_tool = cast(Dict[str, Any], tool.get(PYPROJECT_ISORT_KEY))
    assert isort_tool is not None

    assert len(isort_tool.keys()) == 2
    assert isort_tool.get("line_length") == DEFAULT_LINE_LENGTH
    assert isort_tool.get("profile") == "django"


def test_process_pyproject_toml_isort_with_profile_with_black_python_formatter():
    """Test the process_pyproject_toml function with isort."""
    include_isort = True
    isort_profile = "django"
    python_formatter = "black"
    result = process_pyproject_toml(
        pyproject_toml=document(),
        include_isort=include_isort,
        isort_profile=isort_profile,
        python_formatter=python_formatter,
        debug=True,
        test=True,
    )
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    isort_tool = cast(Dict[str, Any], tool.get(PYPROJECT_ISORT_KEY))
    assert isort_tool is not None

    assert len(isort_tool.keys()) == 2
    assert isort_tool.get("line_length") == DEFAULT_LINE_LENGTH
    assert isort_tool.get("profile") == python_formatter


def test_process_pyproject_toml_isort_existing_values():
    """Test the process_pyproject_toml function with isort."""
    include_isort = True
    result = process_pyproject_toml(
        pyproject_toml=parse(
            f"""
[{PYPROJECT_TOOL_KEY}.{PYPROJECT_ISORT_KEY}]
line_length = 100
test = "test"
        """
        ),
        include_isort=include_isort,
        debug=True,
        test=True,
    )
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    isort_tool = cast(Dict[str, Any], tool.get(PYPROJECT_ISORT_KEY))
    assert isort_tool is not None

    assert len(isort_tool.keys()) == 2
    assert isort_tool.get("line_length") == DEFAULT_LINE_LENGTH
    assert isort_tool.get("test") == "test"


def test_process_pyproject_toml_isort_existing_values_no_isort_profile_but_existing_profile():
    """Test the process_pyproject_toml function with isort."""
    include_isort = True
    result = process_pyproject_toml(
        pyproject_toml=parse(
            f"""
[{PYPROJECT_TOOL_KEY}.{PYPROJECT_ISORT_KEY}]
line_length = 100
profile = "django"
test = "test"
        """
        ),
        include_isort=include_isort,
        debug=True,
        test=True,
    )
    assert result is not None

    tool = cast(Dict[str, Any], result.get(PYPROJECT_TOOL_KEY))
    assert tool is not None

    isort_tool = cast(Dict[str, Any], tool.get(PYPROJECT_ISORT_KEY))
    assert isort_tool is not None

    assert len(isort_tool.keys()) == 2
    assert isort_tool.get("line_length") == DEFAULT_LINE_LENGTH
    assert isort_tool.get("test") == "test"


# Test pytest Options
def test_process_pyproject_toml_pytest():
    """Test the process_pyproject_toml function with pytest."""
    pytest_enabled = True
    result = process_pyproject_toml(
        pyproject_toml=document(), pytest_enabled=pytest_enabled, debug=True, test=True
    )
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
    pytest_enabled = True
    result = process_pyproject_toml(
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
        pytest_enabled=pytest_enabled,
        debug=True,
        test=True,
    )
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
    pytest_enabled = True
    result = process_pyproject_toml(
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
        pytest_enabled=pytest_enabled,
        debug=True,
        test=True,
    )
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
    result = process_pyproject_toml(
        pyproject_toml=document(),
        include_isort=True,
        python_formatter="black",
        pydocstyle_enabled=True,
        pytest_enabled=True,
        line_length=DEFAULT_LINE_LENGTH,
        test=True,
    )
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

    pydocstyle_tool = cast(Dict[str, Any], tools.get(PYPROJECT_PYDOCSTYLE_KEY))
    assert pydocstyle_tool is not None
    assert pydocstyle_tool.get("inherit") is False
    assert pydocstyle_tool.get("match") == PYPROJECT_PYCODESTYLE_MATCH_VALUE

    pytest_tool = cast(Dict[str, Any], tools.get(PYPROJECT_PYTEST_KEY))
    assert pytest_tool is not None

    ini_options = cast(Dict[str, Any], pytest_tool.get(PYPROJECT_PYTEST_INI_OPTIONS_KEY))
    assert ini_options is not None

    assert ini_options.get("addopts") == f"--ignore=./{REPO_NAME}"
    assert ini_options.get("log_cli") is False
    assert ini_options.get("log_cli_level") == "WARNING"
    assert ini_options.get("log_cli_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE
    assert ini_options.get("log_cli_date_format") == PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE
