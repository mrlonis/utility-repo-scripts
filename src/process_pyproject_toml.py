"""Do processing of the pyproject.toml file."""
from pathlib import Path
from typing import Optional, cast

from tomlkit import TOMLDocument, array, document, dump, table
from tomlkit.items import Array, Table

from src.constants.pyproject_toml import (
    PYPROJECT_AUTOPEP8_KEY,
    PYPROJECT_BANDIT_KEY,
    PYPROJECT_BLACK_KEY,
    PYPROJECT_ISORT_KEY,
    PYPROJECT_PYCODESTYLE_MATCH_VALUE,
    PYPROJECT_PYDOCSTYLE_KEY,
    PYPROJECT_PYTEST_INI_OPTIONS_KEY,
    PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE,
    PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE,
    PYPROJECT_PYTEST_KEY,
    PYPROJECT_TOML_FILENAME,
    PYPROJECT_TOOL_KEY,
)
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME
from src.utils.core import validate_python_formatter_option


def _process_python_formatter(tools: Table, python_formatter: str, line_length: int):
    if python_formatter == "autopep8":
        autopep8_tool = cast(Optional[Table], tools.get(PYPROJECT_AUTOPEP8_KEY))
        if autopep8_tool is None:
            autopep8_tool = table()
            tools[PYPROJECT_AUTOPEP8_KEY] = autopep8_tool
        autopep8_tool["max_line_length"] = line_length
        autopep8_tool["experimental"] = True

        tools.pop(PYPROJECT_BLACK_KEY, None)
    elif python_formatter == "black":
        black_tool = cast(Optional[Table], tools.get(PYPROJECT_BLACK_KEY))
        if black_tool is None:
            black_tool = table()
            tools[PYPROJECT_BLACK_KEY] = black_tool
        black_tool["line-length"] = line_length

        tools.pop(PYPROJECT_AUTOPEP8_KEY, None)
    else:
        tools.pop(PYPROJECT_AUTOPEP8_KEY, None)
        tools.pop(PYPROJECT_BLACK_KEY, None)


def _process_pydocstyle(tools: Table, pydocstyle_enabled: bool):
    if not pydocstyle_enabled:
        tools.pop(PYPROJECT_PYDOCSTYLE_KEY, None)
    else:
        pydocstyle_tool = cast(Optional[Table], tools.get(PYPROJECT_PYDOCSTYLE_KEY))

        if pydocstyle_tool is None:
            pydocstyle_tool = table()
            tools[PYPROJECT_PYDOCSTYLE_KEY] = pydocstyle_tool

        pydocstyle_tool["inherit"] = False
        pydocstyle_tool["match"] = PYPROJECT_PYCODESTYLE_MATCH_VALUE


def _process_bandit(tools: Table, bandit_enabled: bool):
    if not bandit_enabled:
        tools.pop(PYPROJECT_BANDIT_KEY, None)
    else:
        bandit_tool = cast(Optional[Table], tools.get(PYPROJECT_BANDIT_KEY))

        if bandit_tool is None:
            bandit_tool = table()
            tools[PYPROJECT_BANDIT_KEY] = bandit_tool

        # Special processing for exclude_dirs
        existing_exclude_dirs = cast(Optional[Array], bandit_tool.get("exclude_dirs"))
        if existing_exclude_dirs is None:
            existing_exclude_dirs = array()

        if REPO_NAME not in existing_exclude_dirs:
            existing_exclude_dirs.insert(0, REPO_NAME)

        bandit_tool["exclude_dirs"] = existing_exclude_dirs


def _process_isort(
    tools: Table, include_isort: bool, line_length: int, python_formatter: str, isort_profile: str
):
    if not include_isort:
        tools.pop(PYPROJECT_ISORT_KEY, None)
    else:
        isort_tool = cast(Optional[Table], tools.get(PYPROJECT_ISORT_KEY))
        if isort_tool is None:
            isort_tool = table()
            tools[PYPROJECT_ISORT_KEY] = isort_tool
        isort_tool["line_length"] = line_length

        if python_formatter == "black":
            isort_tool["profile"] = "black"
        elif isort_profile:
            isort_tool["profile"] = isort_profile
        else:
            if "profile" in isort_tool:
                isort_tool.pop("profile")


def _process_pytest(tools: Table, pytest_enabled: bool):
    if not pytest_enabled:
        tools.pop(PYPROJECT_PYTEST_KEY, None)
    else:
        pytest_tool = cast(Optional[Table], tools.get(PYPROJECT_PYTEST_KEY))
        if pytest_tool is None:
            pytest_tool = table()
            tools[PYPROJECT_PYTEST_KEY] = pytest_tool

        ini_options = cast(Optional[Table], pytest_tool.get(PYPROJECT_PYTEST_INI_OPTIONS_KEY))
        if ini_options is None:
            ini_options = table()

        # Special processing for addopts
        ignore_utility_repo_scripts = f"--ignore=./{REPO_NAME}"
        existing_addopts = cast(Optional[str], ini_options.get("addopts"))
        if existing_addopts is None:
            existing_addopts = ""

        if ignore_utility_repo_scripts not in existing_addopts:
            existing_addopts += f" {ignore_utility_repo_scripts}"
            existing_addopts = existing_addopts.strip()

        ini_options["addopts"] = existing_addopts

        # Remaining Options
        ini_options["log_cli"] = False
        ini_options["log_cli_level"] = "WARNING"
        ini_options["log_cli_format"] = PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE
        ini_options["log_cli_date_format"] = PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE

        pytest_tool["ini_options"] = ini_options


def _handle_removing_file(pyproject_toml: TOMLDocument, tools: Table, debug: bool, test: bool):
    if not tools:
        pyproject_toml = document()

        if not test:  # pragma: no cover
            if debug:  # pragma: no cover
                print("Not Creating pyproject.toml")  # pragma: no cover
                print("Deleting it if it exists")  # pragma: no cover
            if Path(PYPROJECT_TOML_FILENAME).exists():  # pragma: no cover
                Path(PYPROJECT_TOML_FILENAME).unlink()  # pragma: no cover
    return pyproject_toml


def _handle_create(pyproject_toml: TOMLDocument, tools: Table, debug: bool, test: bool):
    pyproject_toml = _handle_removing_file(pyproject_toml=pyproject_toml, tools=tools, debug=debug, test=test)

    if pyproject_toml:
        if not test:  # pragma: no cover
            if debug:  # pragma: no cover
                print(f"Creating {PYPROJECT_TOML_FILENAME}")  # pragma: no cover
            with open(PYPROJECT_TOML_FILENAME, "w", encoding="utf-8") as file:  # pragma: no cover
                dump(pyproject_toml, file)  # pragma: no cover
        else:
            if debug:
                print(f"TESTING: Not Creating {PYPROJECT_TOML_FILENAME}")

    return pyproject_toml


def process_pyproject_toml(
    pyproject_toml: TOMLDocument,
    debug: bool = False,
    test: bool = False,
    include_isort: bool = False,
    python_formatter="",
    pydocstyle_enabled: bool = False,
    pytest_enabled: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
    isort_profile: str = "",
    bandit_enabled: bool = False,
):
    """Do processing of the pyproject.toml file."""
    if debug:
        print("process_pyproject_toml.py CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --test: {test}")
        print(f"    --include_isort: {include_isort}")
        print(f"    --python_formatter: {python_formatter}")
        print(f"    --pydocstyle_enabled: {pydocstyle_enabled}")
        print(f"    --pytest_enabled: {pytest_enabled}")
        print(f"    --line_length: {line_length}")
        print(f"    --isort_profile: {isort_profile}")
        print(f"    --bandit_enabled: {bandit_enabled}")
        print("")

    # Validate String Inputs
    validate_python_formatter_option(python_formatter=python_formatter)

    # Fetch tools
    tools = cast(Optional[Table], pyproject_toml.get(PYPROJECT_TOOL_KEY))
    if tools is None:
        tools = table()
        pyproject_toml[PYPROJECT_TOOL_KEY] = tools

    # python_formatter
    _process_python_formatter(tools=tools, python_formatter=python_formatter, line_length=line_length)

    # pydocstyle_enabled
    _process_pydocstyle(tools=tools, pydocstyle_enabled=pydocstyle_enabled)

    # bandit_enabled
    _process_bandit(tools=tools, bandit_enabled=bandit_enabled)

    # include_isort
    _process_isort(
        tools=tools,
        include_isort=include_isort,
        line_length=line_length,
        python_formatter=python_formatter,
        isort_profile=isort_profile,
    )

    # pytest_enabled
    _process_pytest(tools=tools, pytest_enabled=pytest_enabled)

    # Create pyproject.toml file
    pyproject_toml = _handle_create(pyproject_toml=pyproject_toml, tools=tools, debug=debug, test=test)

    # Return
    return pyproject_toml
