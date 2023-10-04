""".vscode/settings.json file constants."""
# region .vscode/settings.json Constants
from src.constants.pylintrc import PYLINTRC_FILENAME
from src.constants.pyproject_toml import PYPROJECT_TOML_FILENAME
from src.constants.shared import REPO_NAME

VSCODE_SETTINGS_JSON_FILENAME = ".vscode/settings.json"
REPO_IGNORE_PATTERN = f"./{REPO_NAME}/**"

PYTHON_LANGUAGE_KEY = "[python]"
EDITOR_CODE_ACTIONS_ON_SAVE_KEY = "editor.codeActionsOnSave"
SOURCE_ORGANIZE_IMPORTS_KEY = "source.organizeImports"
EDITOR_DEFAULT_FORMATTER_KEY = "editor.defaultFormatter"
EDITOR_FORMAT_ON_SAVE_KEY = "editor.formatOnSave"
AUTOPEP8_ARGS_KEY = "autopep8.args"
BLACK_FORMATTER_ARGS_KEY = "black-formatter.args"
BLACK_FORMATTER_ARGS_VALUE = f"--config={PYPROJECT_TOML_FILENAME}"
FLAKE8_ARGS_KEY = "flake8.args"
FLAKE8_ARGS_RCFILE_VALUE = "--rcfile=.flake8"
ISORT_ARGS_KEY = "isort.args"
ISORT_ARGS_VALUE = f"--settings={PYPROJECT_TOML_FILENAME}"
MYPY_ARGS_KEY = "mypy-type-checker.args"
PYLINT_ARGS_KEY = "pylint.args"
PYLINT_ARGS_RCFILE_VALUE = f"--rcfile={PYLINTRC_FILENAME}"

PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY = "python.analysis.autoImportCompletions"
PYTHON_ANALYSIS_AUTO_SEARCH_PATHS_KEY = "python.analysis.autoSearchPaths"
PYTHON_ANALYSIS_DIAGNOSTIC_MODE_KEY = "python.analysis.diagnosticMode"
PYTHON_ANALYSIS_EXCLUDE_KEY = "python.analysis.exclude"
PYTHON_ANALYSIS_IMPORT_FORMAT_KEY = "python.analysis.importFormat"
PYTHON_ANALYSIS_INDEXING_KEY = "python.analysis.indexing"
PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY = "python.analysis.inlayHints.functionReturnTypes"
PYTHON_ANALYSIS_INLAY_HINTS_PYTEST_PARAMETERS_KEY = "python.analysis.inlayHints.pytestParameters"
PYTHON_ANALYSIS_INLAY_HINTS_VARIABLE_TYPES_KEY = "python.analysis.inlayHints.variableTypes"

PYTHON_ANALYSIS_PACKAGE_INDEX_DEPTHS_KEY = "python.analysis.packageIndexDepths"
DEPTH_KEY = "depth"
INCLUDE_ALL_SYMBOLS_KEY = "includeAllSymbols"
NAME_KEY = "name"
INDEX_NAMES = [
    "alembic",
    "boto3",
    "django",
    "environ",
    "httpx",
    "matplotlib",
    "moto",
    "fastapi",
    "pydantic",
    "requests",
    "rest_framework",
    "scipy",
    "sklearn",
    "sqlalchemy",
    "sqlmodel",
]
DEFAULT_DEPTH = 2

PYTHON_ANALYSIS_TYPE_CHECKING_MODE_KEY = "python.analysis.typeCheckingMode"
PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY = "python.analysis.useLibraryCodeForTypes"

PYTHON_DEFAULT_INTERPRETER_KEY = "python.defaultInterpreterPath"
PYTHON_TESTING_PYTEST_ARGS_KEY = "python.testing.pytestArgs"
PYTHON_TESTING_PYTEST_ENABLED_KEY = "python.testing.pytestEnabled"
PYTHON_TESTING_UNITTEST_ARGS_KEY = "python.testing.unittestArgs"
PYTHON_TESTING_UNITTEST_ENABLED_KEY = "python.testing.unittestEnabled"
SEARCH_EXCLUDE_KEY = "search.exclude"

SAMPLE_VSCODE_SETTINGS = {
    PYTHON_LANGUAGE_KEY: {
        EDITOR_CODE_ACTIONS_ON_SAVE_KEY: {SOURCE_ORGANIZE_IMPORTS_KEY: True},
        EDITOR_DEFAULT_FORMATTER_KEY: "<python_formatter>",
        EDITOR_FORMAT_ON_SAVE_KEY: True,
    },
    AUTOPEP8_ARGS_KEY: [],
    BLACK_FORMATTER_ARGS_KEY: [BLACK_FORMATTER_ARGS_VALUE],
    FLAKE8_ARGS_KEY: [FLAKE8_ARGS_RCFILE_VALUE],
    ISORT_ARGS_KEY: [ISORT_ARGS_VALUE],
    PYLINT_ARGS_KEY: [PYLINT_ARGS_RCFILE_VALUE],
    PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY: True,
    PYTHON_ANALYSIS_AUTO_SEARCH_PATHS_KEY: True,
    PYTHON_ANALYSIS_DIAGNOSTIC_MODE_KEY: "workspace",
    PYTHON_ANALYSIS_EXCLUDE_KEY: ["**/node_modules", "**/__pycache__", ".git", REPO_IGNORE_PATTERN],
    PYTHON_ANALYSIS_IMPORT_FORMAT_KEY: "absolute",
    PYTHON_ANALYSIS_INDEXING_KEY: True,
    PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY: True,
    PYTHON_ANALYSIS_INLAY_HINTS_PYTEST_PARAMETERS_KEY: True,
    PYTHON_ANALYSIS_INLAY_HINTS_VARIABLE_TYPES_KEY: True,
    PYTHON_ANALYSIS_TYPE_CHECKING_MODE_KEY: "basic",
    PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY: True,
    PYTHON_DEFAULT_INTERPRETER_KEY: "~/.venvs/<project>/bin/python",
    PYTHON_TESTING_PYTEST_ARGS_KEY: [f"--ignore={REPO_IGNORE_PATTERN}"],
    PYTHON_TESTING_PYTEST_ENABLED_KEY: False,
    PYTHON_TESTING_UNITTEST_ARGS_KEY: ["-v", "-s", ".", "-p", "*test*.py"],
    PYTHON_TESTING_UNITTEST_ENABLED_KEY: False,
    SEARCH_EXCLUDE_KEY: {
        "**/.git/**": True,
        "**/node_modules/**": True,
        "**/__pycache__/**": True,
        ".coverage": True,
        ".pytest_cache/**": True,
        "htmlcov/**": True,
        "poetry.lock": True,
        f"{REPO_NAME}/**": True,
    },
}

# endregion
