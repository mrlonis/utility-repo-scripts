"""Do processing of the .vscode/settings.json file."""
import json
import os
from typing import Any, Dict, List, Optional, cast

from src.constants.pyproject_toml import PYPROJECT_TOML_FILENAME
from src.constants.shared import REPO_NAME
from src.constants.vscode_settings import (
    AUTOPEP8_ARGS_KEY,
    BLACK_FORMATTER_ARGS_KEY,
    BLACK_FORMATTER_ARGS_VALUE,
    EDITOR_CODE_ACTIONS_ON_SAVE_KEY,
    EDITOR_DEFAULT_FORMATTER_KEY,
    EDITOR_FORMAT_ON_SAVE_KEY,
    FLAKE8_ARGS_KEY,
    FLAKE8_ARGS_RCFILE_VALUE,
    ISORT_ARGS_KEY,
    ISORT_ARGS_VALUE,
    PYLINT_ARGS_KEY,
    PYLINT_ARGS_RCFILE_VALUE,
    PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY,
    PYTHON_ANALYSIS_AUTO_IMPORT_USER_SYMBOLS_KEY,
    PYTHON_ANALYSIS_AUTO_SEARCH_PATHS_KEY,
    PYTHON_ANALYSIS_DIAGNOSTIC_MODE_KEY,
    PYTHON_ANALYSIS_EXCLUDE_KEY,
    PYTHON_ANALYSIS_IMPORT_FORMAT_KEY,
    PYTHON_ANALYSIS_INDEXING_KEY,
    PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY,
    PYTHON_ANALYSIS_INLAY_HINTS_PYTEST_PARAMETERS_KEY,
    PYTHON_ANALYSIS_INLAY_HINTS_VARIABLE_TYPES_KEY,
    PYTHON_ANALYSIS_TYPE_CHECKING_MODE_KEY,
    PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY,
    PYTHON_DEFAULT_INTERPRETER_KEY,
    PYTHON_FORMATTING_PROVIDER_KEY,
    PYTHON_LANGUAGE_KEY,
    PYTHON_LINTING_BANDIT_ARGS_KEY,
    PYTHON_LINTING_BANDIT_ENABLED_KEY,
    PYTHON_LINTING_ENABLED_KEY,
    PYTHON_LINTING_FLAKE8_ARGS_KEY,
    PYTHON_LINTING_FLAKE8_ENABLED_KEY,
    PYTHON_LINTING_IGNORE_PATTERNS_KEY,
    PYTHON_LINTING_MYPY_ARGS_KEY,
    PYTHON_LINTING_MYPY_ENABLED_KEY,
    PYTHON_LINTING_PROSPECTOR_ARGS_KEY,
    PYTHON_LINTING_PROSPECTOR_ENABLED_KEY,
    PYTHON_LINTING_PYCODESTYLE_ARGS_KEY,
    PYTHON_LINTING_PYCODESTYLE_ENABLED_KEY,
    PYTHON_LINTING_PYDOCSTYLE_ARGS_KEY,
    PYTHON_LINTING_PYDOCSTYLE_ARGS_VALUE,
    PYTHON_LINTING_PYDOCSTYLE_ENABLED_KEY,
    PYTHON_LINTING_PYLAMA_ARGS_KEY,
    PYTHON_LINTING_PYLAMA_ENABLED_KEY,
    PYTHON_LINTING_PYLINT_ARGS_KEY,
    PYTHON_LINTING_PYLINT_ENABLED_KEY,
    PYTHON_TESTING_PYTEST_ARGS_KEY,
    PYTHON_TESTING_PYTEST_ENABLED_KEY,
    PYTHON_TESTING_UNITTEST_ARGS_KEY,
    PYTHON_TESTING_UNITTEST_ENABLED_KEY,
    REPO_IGNORE_PATTERN,
    SEARCH_EXCLUDE_KEY,
    SOURCE_ORGANIZE_IMPORTS_KEY,
)
from src.utils.core import validate_python_formatter_option


def _process_python_default_interpreter(data: Dict[str, Any], use_pyenv: bool):
    project_name = os.path.basename(os.getenv("PWD", ""))

    if use_pyenv:
        venv_location = f"~/.pyenv/versions/{project_name}"
        data[PYTHON_DEFAULT_INTERPRETER_KEY] = venv_location
    else:
        venv_folder_location = os.getenv("WORKON_HOME", "~/.venvs")
        venv_location = f"{venv_folder_location.replace(os.getenv('HOME', ''), '~')}/{project_name}"
        data[PYTHON_DEFAULT_INTERPRETER_KEY] = venv_location


def _process_python_analysis(data: Dict[str, Any]):
    # pylint: disable=too-many-branches
    auto_import_completions = cast(Optional[bool], data.get(PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY))
    if auto_import_completions is None:
        data[PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY] = True

    auto_import_user_symbols = cast(Optional[bool], data.get(PYTHON_ANALYSIS_AUTO_IMPORT_USER_SYMBOLS_KEY))
    if auto_import_user_symbols is None:
        data[PYTHON_ANALYSIS_AUTO_IMPORT_USER_SYMBOLS_KEY] = True

    auto_search_paths = cast(Optional[bool], data.get(PYTHON_ANALYSIS_AUTO_SEARCH_PATHS_KEY))
    if auto_search_paths is None:
        data[PYTHON_ANALYSIS_AUTO_SEARCH_PATHS_KEY] = True

    diagnostic_mode = cast(Optional[str], data.get(PYTHON_ANALYSIS_DIAGNOSTIC_MODE_KEY))
    if diagnostic_mode is None:
        data[PYTHON_ANALYSIS_DIAGNOSTIC_MODE_KEY] = "workspace"

    exclude = cast(Optional[List[str]], data.get(PYTHON_ANALYSIS_EXCLUDE_KEY))
    if exclude is None:
        exclude = []
        data[PYTHON_ANALYSIS_EXCLUDE_KEY] = exclude
    if REPO_IGNORE_PATTERN not in exclude:
        exclude.append(REPO_IGNORE_PATTERN)

    import_format = cast(Optional[str], data.get(PYTHON_ANALYSIS_IMPORT_FORMAT_KEY))
    if import_format is None:
        data[PYTHON_ANALYSIS_IMPORT_FORMAT_KEY] = "absolute"

    indexing = cast(Optional[bool], data.get(PYTHON_ANALYSIS_INDEXING_KEY))
    if indexing is None:
        data[PYTHON_ANALYSIS_INDEXING_KEY] = True

    function_return_types = cast(
        Optional[bool], data.get(PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY)
    )
    if function_return_types is None:
        data[PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY] = True

    pytest_parameters = cast(Optional[bool], data.get(PYTHON_ANALYSIS_INLAY_HINTS_PYTEST_PARAMETERS_KEY))
    if pytest_parameters is None:
        data[PYTHON_ANALYSIS_INLAY_HINTS_PYTEST_PARAMETERS_KEY] = True

    variable_types = cast(Optional[bool], data.get(PYTHON_ANALYSIS_INLAY_HINTS_VARIABLE_TYPES_KEY))
    if variable_types is None:
        data[PYTHON_ANALYSIS_INLAY_HINTS_VARIABLE_TYPES_KEY] = True

    type_checking_mode = cast(Optional[str], data.get(PYTHON_ANALYSIS_TYPE_CHECKING_MODE_KEY))
    if type_checking_mode is None:
        data[PYTHON_ANALYSIS_TYPE_CHECKING_MODE_KEY] = "basic"

    use_library_code_for_types = cast(
        Optional[bool], data.get(PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY)
    )
    if use_library_code_for_types is None:
        data[PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY] = True


def _process_search_exclude(data: Dict[str, Any]):
    exclude = cast(Optional[Dict[str, bool]], data.get(SEARCH_EXCLUDE_KEY))
    if exclude is None:
        exclude = cast(Dict[str, bool], {})
        data[SEARCH_EXCLUDE_KEY] = exclude

    exclude[f"{REPO_NAME}/**"] = True


def _process_python_formatter_option(data: Dict[str, Any], python_formatter: str):
    python_language = cast(Optional[Dict[str, Any]], data.get(PYTHON_LANGUAGE_KEY))
    if python_language is None:
        python_language = {}
        data[PYTHON_LANGUAGE_KEY] = python_language

    if python_formatter == "autopep8":
        python_language[EDITOR_DEFAULT_FORMATTER_KEY] = "ms-python.autopep8"
        data[PYTHON_FORMATTING_PROVIDER_KEY] = "none"
        data[AUTOPEP8_ARGS_KEY] = []
        data.pop(BLACK_FORMATTER_ARGS_KEY, None)
    elif python_formatter == "black":
        python_language[EDITOR_DEFAULT_FORMATTER_KEY] = "ms-python.black-formatter"
        data[PYTHON_FORMATTING_PROVIDER_KEY] = "none"
        data.pop(AUTOPEP8_ARGS_KEY, None)
        data[BLACK_FORMATTER_ARGS_KEY] = [BLACK_FORMATTER_ARGS_VALUE]
    else:
        python_language[EDITOR_DEFAULT_FORMATTER_KEY] = "ms-python.python"
        data[PYTHON_FORMATTING_PROVIDER_KEY] = "none"
        data.pop(AUTOPEP8_ARGS_KEY, None)
        data.pop(BLACK_FORMATTER_ARGS_KEY, None)

    python_language[EDITOR_FORMAT_ON_SAVE_KEY] = True

    code_actions_on_save = cast(
        Optional[Dict[str, Any]], python_language.get(EDITOR_CODE_ACTIONS_ON_SAVE_KEY)
    )
    if code_actions_on_save is None:
        code_actions_on_save = {}
        python_language[EDITOR_CODE_ACTIONS_ON_SAVE_KEY] = code_actions_on_save

    code_actions_on_save[SOURCE_ORGANIZE_IMPORTS_KEY] = True


def _process_python_linter_options(
    data: Dict[str, Any],
    pylint_enabled: bool,
    flake8_enabled: bool,
    pydocstyle_enabled: bool,
    pycodestyle_enabled: bool,
    bandit_enabled: bool,
    mypy_enabled: bool,
    prospector_enabled: bool,
    pylama_enabled: bool,
):
    # pylint: disable=too-many-branches too-many-statements
    # General Linting Settings
    if (  # pylint: disable=too-many-boolean-expressions
        pylint_enabled
        or flake8_enabled
        or pydocstyle_enabled
        or pycodestyle_enabled
        or bandit_enabled
        or mypy_enabled
        or prospector_enabled
        or pylama_enabled
    ):
        data[PYTHON_LINTING_ENABLED_KEY] = True
    else:
        data[PYTHON_LINTING_ENABLED_KEY] = False

    ignore_patterns = cast(Optional[List[str]], data.get(PYTHON_LINTING_IGNORE_PATTERNS_KEY))
    if ignore_patterns is None:
        ignore_patterns = []
        data[PYTHON_LINTING_IGNORE_PATTERNS_KEY] = ignore_patterns
    if REPO_IGNORE_PATTERN not in ignore_patterns:
        ignore_patterns.append(REPO_IGNORE_PATTERN)

    # pylint
    if pylint_enabled:
        data[PYTHON_LINTING_PYLINT_ENABLED_KEY] = True
        data[PYLINT_ARGS_KEY] = [PYLINT_ARGS_RCFILE_VALUE]
        data[PYTHON_LINTING_PYLINT_ARGS_KEY] = [PYLINT_ARGS_RCFILE_VALUE]
    else:
        data.pop(PYLINT_ARGS_KEY, None)
        data.pop(PYTHON_LINTING_PYLINT_ARGS_KEY, None)
        data[PYTHON_LINTING_PYLINT_ENABLED_KEY] = False

    # flake8
    if flake8_enabled:
        data[PYTHON_LINTING_FLAKE8_ENABLED_KEY] = True
        data[FLAKE8_ARGS_KEY] = [FLAKE8_ARGS_RCFILE_VALUE]
        data[PYTHON_LINTING_FLAKE8_ARGS_KEY] = [FLAKE8_ARGS_RCFILE_VALUE]
    else:
        data.pop(FLAKE8_ARGS_KEY, None)
        data.pop(PYTHON_LINTING_FLAKE8_ARGS_KEY, None)
        data[PYTHON_LINTING_FLAKE8_ENABLED_KEY] = False

    # pydocstyle
    if pydocstyle_enabled:
        data[PYTHON_LINTING_PYDOCSTYLE_ENABLED_KEY] = True
        data[PYTHON_LINTING_PYDOCSTYLE_ARGS_KEY] = [PYTHON_LINTING_PYDOCSTYLE_ARGS_VALUE]
    else:
        data.pop(PYTHON_LINTING_PYDOCSTYLE_ARGS_KEY, None)
        data[PYTHON_LINTING_PYDOCSTYLE_ENABLED_KEY] = False

    # pycodestyle
    if pycodestyle_enabled:
        data[PYTHON_LINTING_PYCODESTYLE_ARGS_KEY] = ["--config=./tox.ini"]
        data[PYTHON_LINTING_PYCODESTYLE_ENABLED_KEY] = True
    else:
        data.pop(PYTHON_LINTING_PYCODESTYLE_ARGS_KEY, None)
        data[PYTHON_LINTING_PYCODESTYLE_ENABLED_KEY] = False

    # bandit
    if bandit_enabled:
        data[PYTHON_LINTING_BANDIT_ARGS_KEY] = ["-c", PYPROJECT_TOML_FILENAME, "-r", "."]
        data[PYTHON_LINTING_BANDIT_ENABLED_KEY] = True
    else:
        data.pop(PYTHON_LINTING_BANDIT_ARGS_KEY, None)
        data[PYTHON_LINTING_BANDIT_ENABLED_KEY] = False

    # mypy
    if mypy_enabled:
        data[PYTHON_LINTING_MYPY_ARGS_KEY] = ["--ignore-missing-imports", "--follow-imports=silent"]
        data[PYTHON_LINTING_MYPY_ENABLED_KEY] = True
    else:
        data.pop(PYTHON_LINTING_MYPY_ARGS_KEY, None)
        data[PYTHON_LINTING_MYPY_ENABLED_KEY] = False

    # prospector
    if prospector_enabled:
        data[PYTHON_LINTING_PROSPECTOR_ARGS_KEY] = []
        data[PYTHON_LINTING_PROSPECTOR_ENABLED_KEY] = True
    else:
        data.pop(PYTHON_LINTING_PROSPECTOR_ARGS_KEY, None)
        data[PYTHON_LINTING_PROSPECTOR_ENABLED_KEY] = False

    # pylama
    if pylama_enabled:
        data[PYTHON_LINTING_PYLAMA_ARGS_KEY] = []
        data[PYTHON_LINTING_PYLAMA_ENABLED_KEY] = True
    else:
        data.pop(PYTHON_LINTING_PYLAMA_ARGS_KEY, None)
        data[PYTHON_LINTING_PYLAMA_ENABLED_KEY] = False


def _process_python_testing_options(data: Dict[str, Any], pytest_enabled: bool, unittest_enabled: bool):
    if pytest_enabled:
        data[PYTHON_TESTING_PYTEST_ARGS_KEY] = [f"--ignore=./{REPO_NAME}"]
        data[PYTHON_TESTING_PYTEST_ENABLED_KEY] = True
    else:
        data.pop(PYTHON_TESTING_PYTEST_ARGS_KEY, None)
        data[PYTHON_TESTING_PYTEST_ENABLED_KEY] = False

    if unittest_enabled:
        data[PYTHON_TESTING_UNITTEST_ARGS_KEY] = ["-v", "-s", ".", "-p", "*test*.py"]
        data[PYTHON_TESTING_UNITTEST_ENABLED_KEY] = True
    else:
        data.pop(PYTHON_TESTING_UNITTEST_ARGS_KEY, None)
        data[PYTHON_TESTING_UNITTEST_ENABLED_KEY] = False


def _process_isort_options(data: Dict[str, Any], include_isort: bool):
    if include_isort:
        data[ISORT_ARGS_KEY] = [ISORT_ARGS_VALUE]
    else:
        data.pop(ISORT_ARGS_KEY, None)


def process_vscode_settings(
    vscode_settings: Dict[str, Any],
    debug: bool = False,
    test: bool = False,
    include_isort: bool = False,
    python_formatter: str = "",
    pylint_enabled: bool = False,
    flake8_enabled: bool = False,
    pydocstyle_enabled: bool = False,
    pycodestyle_enabled: bool = False,
    bandit_enabled: bool = False,
    mypy_enabled: bool = False,
    prospector_enabled: bool = False,
    pylama_enabled: bool = False,
    pytest_enabled: bool = False,
    unittest_enabled: bool = False,
    use_pyenv: bool = False,
):
    """Do processing of the .vscode/settings.json file."""
    # pylint: disable=too-many-arguments too-many-locals
    if debug:
        print("process_vs_code_settings.py CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --test: {test}")
        print(f"    --include_isort: {include_isort}")
        print(f"    --python_formatter: {python_formatter}")
        print(f"    --pylint_enabled: {pylint_enabled}")
        print(f"    --flake8_enabled: {flake8_enabled}")
        print(f"    --pydocstyle_enabled: {pydocstyle_enabled}")
        print(f"    --pycodestyle_enabled: {pycodestyle_enabled}")
        print(f"    --bandit_enabled: {bandit_enabled}")
        print(f"    --mypy_enabled: {mypy_enabled}")
        print(f"    --prospector_enabled: {prospector_enabled}")
        print(f"    --pylama_enabled: {pylama_enabled}")
        print(f"    --pytest_enabled: {pytest_enabled}")
        print(f"    --unittest_enabled: {unittest_enabled}")
        print(f"    --use_pyenv: {use_pyenv}")
        print("")

    # Validate String Inputs
    validate_python_formatter_option(python_formatter=python_formatter)

    # python.defaultInterpreterPath
    _process_python_default_interpreter(data=vscode_settings, use_pyenv=use_pyenv)

    # python.analysis
    _process_python_analysis(data=vscode_settings)

    # search.exclude
    _process_search_exclude(data=vscode_settings)

    # python_formatter
    _process_python_formatter_option(data=vscode_settings, python_formatter=python_formatter)

    # Process Linter Options
    _process_python_linter_options(
        data=vscode_settings,
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        pycodestyle_enabled=pycodestyle_enabled,
        bandit_enabled=bandit_enabled,
        mypy_enabled=mypy_enabled,
        prospector_enabled=prospector_enabled,
        pylama_enabled=pylama_enabled,
    )

    # python_testing_framework
    _process_python_testing_options(
        data=vscode_settings, pytest_enabled=pytest_enabled, unittest_enabled=unittest_enabled
    )

    # include_isort
    _process_isort_options(data=vscode_settings, include_isort=include_isort)

    # Create .vscode/settings.json file
    if not test:  # pragma: no cover
        if debug:  # pragma: no cover
            print("Creating .vscode/settings.json")  # pragma: no cover
        with open(".vscode/settings.json", "w", encoding="utf-8") as file:  # pragma: no cover
            json.dump(vscode_settings, file)  # pragma: no cover
    else:
        if debug:
            print("TESTING: Not Creating .vscode/settings.json")
            print(vscode_settings)

    # Return
    return vscode_settings
