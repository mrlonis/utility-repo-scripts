"""Do processing of the pyproject.toml file."""

from pathlib import Path
from typing import Optional, cast

from tomlkit import TOMLDocument, document, dump, table
from tomlkit.items import Table

from src.constants.pyproject_toml import (
    PYPROJECT_AUTOPEP8_KEY,
    PYPROJECT_BLACK_KEY,
    PYPROJECT_ISORT_KEY,
    PYPROJECT_POETRY_KEY,
    PYPROJECT_PYTEST_INI_OPTIONS_KEY,
    PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE,
    PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE,
    PYPROJECT_PYTEST_KEY,
    PYPROJECT_TOML_FILENAME,
    PYPROJECT_TOOL_KEY,
)
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME
from src.utils.core import validate_python_formatter_option


class PyProjectTomlProcessor:
    # pylint: disable=too-many-instance-attributes too-few-public-methods
    """Do processing of the pyproject.toml file."""

    def __init__(
        self,
        pyproject_toml: TOMLDocument,
        include_isort: bool = False,
        python_formatter="",
        isort_profile: str = "",
        pytest_enabled: bool = False,
        line_length: int = DEFAULT_LINE_LENGTH,
        package_manager: str = "pip",
        is_package: bool = False,
        debug: bool = False,
        test: bool = False,
    ):
        # pylint: disable=too-many-arguments
        """Initialize the class."""
        self.pyproject_toml = pyproject_toml
        self.include_isort = include_isort
        self.python_formatter = python_formatter
        self.isort_profile = isort_profile
        self.pytest_enabled = pytest_enabled
        self.line_length = line_length
        self.package_manager = package_manager
        self.is_package = is_package
        self.debug = debug
        self.test = test

        if self.debug:
            print("process_pyproject_toml.py CLI Arguments:")
            print(f"    --include-isort: {self.include_isort}")
            print(f"    --python-formatter: {self.python_formatter}")
            print(f"    --isort-profile: {self.isort_profile}")
            print(f"    --pytest-enabled: {self.pytest_enabled}")
            print(f"    --line-length: {self.line_length}")
            print(f"    --package-manager: {self.package_manager}")
            print(f"    --is-package: {self.is_package}")
            print(f"    --debug: {self.debug}")
            print(f"    --test: {self.test}")
            print("")

    def process_pyproject_toml(self):
        """Do processing of the pyproject.toml file."""
        # Validate String Inputs
        validate_python_formatter_option(python_formatter=self.python_formatter)

        # Fetch tools
        tools = cast(Optional[Table], self.pyproject_toml.get(PYPROJECT_TOOL_KEY))
        if tools is None:
            tools = table()
            self.pyproject_toml[PYPROJECT_TOOL_KEY] = tools

        # python_formatter
        self._process_python_formatter(tools=tools)

        # include_isort
        self._process_isort(tools=tools)

        # pytest_enabled
        self._process_pytest(tools=tools)

        # Poetry package-mode
        self._poetry_package_mode(tools=tools)

        # Create pyproject.toml file
        self._handle_create(tools=tools)

        # Return
        return self.pyproject_toml

    def _process_python_formatter(self, tools: Table):
        if self.python_formatter == "autopep8":
            autopep8_tool = cast(Optional[Table], tools.get(PYPROJECT_AUTOPEP8_KEY))
            if autopep8_tool is None:
                autopep8_tool = table()
                tools[PYPROJECT_AUTOPEP8_KEY] = autopep8_tool
            autopep8_tool["max_line_length"] = self.line_length
            autopep8_tool["experimental"] = True

            tools.pop(PYPROJECT_BLACK_KEY, None)
        elif self.python_formatter == "black":
            black_tool = cast(Optional[Table], tools.get(PYPROJECT_BLACK_KEY))
            if black_tool is None:
                black_tool = table()
                tools[PYPROJECT_BLACK_KEY] = black_tool
            black_tool["line-length"] = self.line_length

            tools.pop(PYPROJECT_AUTOPEP8_KEY, None)
        else:
            tools.pop(PYPROJECT_AUTOPEP8_KEY, None)
            tools.pop(PYPROJECT_BLACK_KEY, None)

    def _process_isort(self, tools: Table):
        if not self.include_isort:
            tools.pop(PYPROJECT_ISORT_KEY, None)
        else:
            isort_tool = cast(Optional[Table], tools.get(PYPROJECT_ISORT_KEY))
            if isort_tool is None:
                isort_tool = table()
                tools[PYPROJECT_ISORT_KEY] = isort_tool
            isort_tool["line_length"] = self.line_length

            if self.python_formatter == "black":
                isort_tool["profile"] = "black"
            elif self.isort_profile:
                isort_tool["profile"] = self.isort_profile
            else:
                if "profile" in isort_tool:
                    isort_tool.pop("profile")

    def _process_pytest(self, tools: Table):
        if not self.pytest_enabled:
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

    def _poetry_package_mode(self, tools: Table):
        if self.package_manager == "poetry" and not self.is_package:
            poetry_tool: Table | None = cast(Optional[Table], tools.get(PYPROJECT_POETRY_KEY))
            if poetry_tool is None:
                poetry_tool = table()
                tools[PYPROJECT_POETRY_KEY] = poetry_tool
            poetry_tool["package-mode"] = False

    def _handle_removing_file(self, tools: Table):
        if not tools:
            self.pyproject_toml = document()

            if not self.test:  # pragma: no cover
                if self.debug:  # pragma: no cover
                    print("Not Creating pyproject.toml")  # pragma: no cover
                    print("Deleting it if it exists")  # pragma: no cover
                if Path(PYPROJECT_TOML_FILENAME).exists():  # pragma: no cover
                    Path(PYPROJECT_TOML_FILENAME).unlink()  # pragma: no cover

    def _handle_create(self, tools: Table):
        self._handle_removing_file(tools=tools)

        if self.pyproject_toml:
            if not self.test:  # pragma: no cover
                if self.debug:  # pragma: no cover
                    print(f"Creating {PYPROJECT_TOML_FILENAME}")  # pragma: no cover
                with open(PYPROJECT_TOML_FILENAME, "w", encoding="utf-8") as file:  # pragma: no cover
                    dump(self.pyproject_toml, file)  # pragma: no cover
            else:
                if self.debug:
                    print(f"TESTING: Not Creating {PYPROJECT_TOML_FILENAME}")
