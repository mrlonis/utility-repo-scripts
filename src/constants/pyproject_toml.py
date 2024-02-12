"""pyproject.toml file constants."""

# region pyproject.toml Constants
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME

PYPROJECT_TOML_FILENAME = "pyproject.toml"
PYPROJECT_TOOL_KEY = "tool"
PYPROJECT_AUTOPEP8_KEY = "autopep8"
PYPROJECT_BLACK_KEY = "black"
PYPROJECT_ISORT_KEY = "isort"
PYPROJECT_PYCODESTYLE_MATCH_VALUE = ".*.py"
PYPROJECT_PYTEST_KEY = "pytest"
PYPROJECT_PYTEST_INI_OPTIONS_KEY = "ini_options"
PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE = "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE = "%Y-%m-%d %H:%M:%S"

SAMPLE_PYPROJECT_TOML = f"""[{PYPROJECT_TOOL_KEY}.{PYPROJECT_AUTOPEP8_KEY}]
max_line_length = {DEFAULT_LINE_LENGTH}
experimental = true

[{PYPROJECT_TOOL_KEY}.{PYPROJECT_BLACK_KEY}]
line-length = {DEFAULT_LINE_LENGTH}

[{PYPROJECT_TOOL_KEY}.{PYPROJECT_ISORT_KEY}]
line_length = {DEFAULT_LINE_LENGTH}
profile = "black"

[{PYPROJECT_TOOL_KEY}.{PYPROJECT_PYTEST_KEY}.{PYPROJECT_PYTEST_INI_OPTIONS_KEY}]
addopts = "--ignore=./{REPO_NAME}"
log_cli = false
log_cli_level = "WARNING"
log_cli_format = "{PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_VALUE}"
log_cli_date_format = "{PYPROJECT_PYTEST_INI_OPTIONS_LOG_CLI_DATE_FORMAT_VALUE}"
markers = [
    "example_mark_with_description: marks tests as example_mark_with_description (deselect with '-m \\"not example_mark_with_description\\"')",
    "example_mark_without_description",
]
"""  # noqa: E501
# endregion
