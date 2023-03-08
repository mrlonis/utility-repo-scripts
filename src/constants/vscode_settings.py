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
PYLINT_ARGS_KEY = "pylint.args"
PYLINT_ARGS_RCFILE_VALUE = f"--rcfile={PYLINTRC_FILENAME}"

PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY = "python.analysis.autoImportCompletions"
PYTHON_ANALYSIS_AUTO_IMPORT_USER_SYMBOLS_KEY = "python.analysis.autoImportUserSymbols"
PYTHON_ANALYSIS_AUTO_SEARCH_PATHS_KEY = "python.analysis.autoSearchPaths"
PYTHON_ANALYSIS_DIAGNOSTIC_MODE_KEY = "python.analysis.diagnosticMode"
PYTHON_ANALYSIS_EXCLUDE_KEY = "python.analysis.exclude"
PYTHON_ANALYSIS_IMPORT_FORMAT_KEY = "python.analysis.importFormat"
PYTHON_ANALYSIS_INDEXING_KEY = "python.analysis.indexing"
PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY = "python.analysis.inlayHints.functionReturnTypes"
PYTHON_ANALYSIS_INLAY_HINTS_PYTEST_PARAMETERS_KEY = "python.analysis.inlayHints.pytestParameters"
PYTHON_ANALYSIS_INLAY_HINTS_VARIABLE_TYPES_KEY = "python.analysis.inlayHints.variableTypes"
PYTHON_ANALYSIS_TYPE_CHECKING_MODE_KEY = "python.analysis.typeCheckingMode"
PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY = "python.analysis.useLibraryCodeForTypes"

PYTHON_DEFAULT_INTERPRETER_KEY = "python.defaultInterpreterPath"
PYTHON_FORMATTING_PROVIDER_KEY = "python.formatting.provider"
PYTHON_LINTING_BANDIT_ARGS_KEY = "python.linting.banditArgs"
PYTHON_LINTING_BANDIT_ENABLED_KEY = "python.linting.banditEnabled"
PYTHON_LINTING_ENABLED_KEY = "python.linting.enabled"
PYTHON_LINTING_FLAKE8_ARGS_KEY = "python.linting.flake8Args"
PYTHON_LINTING_FLAKE8_ENABLED_KEY = "python.linting.flake8Enabled"
PYTHON_LINTING_IGNORE_PATTERNS_KEY = "python.linting.ignorePatterns"
PYTHON_LINTING_MYPY_ARGS_KEY = "python.linting.mypyArgs"
PYTHON_LINTING_MYPY_ENABLED_KEY = "python.linting.mypyEnabled"
PYTHON_LINTING_PROSPECTOR_ARGS_KEY = "python.linting.prospectorArgs"
PYTHON_LINTING_PROSPECTOR_ENABLED_KEY = "python.linting.prospectorEnabled"
PYTHON_LINTING_PYCODESTYLE_ARGS_KEY = "python.linting.pycodestyleArgs"
PYTHON_LINTING_PYCODESTYLE_ENABLED_KEY = "python.linting.pycodestyleEnabled"
PYTHON_LINTING_PYDOCSTYLE_ARGS_KEY = "python.linting.pydocstyleArgs"
PYTHON_LINTING_PYDOCSTYLE_ARGS_VALUE = f"--config=./{PYPROJECT_TOML_FILENAME}"
PYTHON_LINTING_PYDOCSTYLE_ENABLED_KEY = "python.linting.pydocstyleEnabled"
PYTHON_LINTING_PYLAMA_ARGS_KEY = "python.linting.pylamaArgs"
PYTHON_LINTING_PYLAMA_ENABLED_KEY = "python.linting.pylamaEnabled"
PYTHON_LINTING_PYLINT_ARGS_KEY = "python.linting.pylintArgs"
PYTHON_LINTING_PYLINT_ENABLED_KEY = "python.linting.pylintEnabled"
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
    PYTHON_ANALYSIS_AUTO_IMPORT_USER_SYMBOLS_KEY: True,
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
    PYTHON_FORMATTING_PROVIDER_KEY: "none",
    PYTHON_LINTING_BANDIT_ARGS_KEY: [],
    PYTHON_LINTING_BANDIT_ENABLED_KEY: False,
    PYTHON_LINTING_ENABLED_KEY: False,
    PYTHON_LINTING_FLAKE8_ARGS_KEY: [FLAKE8_ARGS_RCFILE_VALUE],
    PYTHON_LINTING_FLAKE8_ENABLED_KEY: False,
    PYTHON_LINTING_IGNORE_PATTERNS_KEY: [
        ".vscode/*.py",
        "**/site-packages/**/*.py",
        REPO_IGNORE_PATTERN,
    ],
    PYTHON_LINTING_MYPY_ARGS_KEY: ["--ignore-missing-imports", "--follow-imports=silent"],
    PYTHON_LINTING_MYPY_ENABLED_KEY: False,
    PYTHON_LINTING_PROSPECTOR_ARGS_KEY: [],
    PYTHON_LINTING_PROSPECTOR_ENABLED_KEY: False,
    PYTHON_LINTING_PYCODESTYLE_ARGS_KEY: [],
    PYTHON_LINTING_PYCODESTYLE_ENABLED_KEY: False,
    PYTHON_LINTING_PYDOCSTYLE_ARGS_KEY: [PYTHON_LINTING_PYDOCSTYLE_ARGS_VALUE],
    PYTHON_LINTING_PYDOCSTYLE_ENABLED_KEY: False,
    PYTHON_LINTING_PYLAMA_ARGS_KEY: [],
    PYTHON_LINTING_PYLAMA_ENABLED_KEY: False,
    PYTHON_LINTING_PYLINT_ARGS_KEY: [PYLINT_ARGS_RCFILE_VALUE],
    PYTHON_LINTING_PYLINT_ENABLED_KEY: False,
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
