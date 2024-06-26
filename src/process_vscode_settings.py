"""Do processing of the .vscode/settings.json file."""

import json
import os
from copy import deepcopy
from typing import Any, Dict, List, Optional, cast

from src.constants.shared import REPO_NAME
from src.constants.vscode_settings import (
    AUTOPEP8_ARGS_KEY,
    BLACK_FORMATTER_ARGS_KEY,
    BLACK_FORMATTER_ARGS_VALUE,
    DEFAULT_DEPTH,
    DEPTH_KEY,
    EDITOR_CODE_ACTIONS_ON_SAVE_KEY,
    EDITOR_DEFAULT_FORMATTER_KEY,
    EDITOR_FORMAT_ON_SAVE_KEY,
    FLAKE8_ARGS_KEY,
    FLAKE8_ARGS_RCFILE_VALUE,
    INCLUDE_ALL_SYMBOLS_KEY,
    INDEX_NAMES,
    ISORT_ARGS_KEY,
    ISORT_ARGS_VALUE,
    MYPY_ARGS_KEY,
    NAME_KEY,
    PYLINT_ARGS_KEY,
    PYLINT_ARGS_RCFILE_VALUE,
    PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY,
    PYTHON_ANALYSIS_AUTO_SEARCH_PATHS_KEY,
    PYTHON_ANALYSIS_DIAGNOSTIC_MODE_KEY,
    PYTHON_ANALYSIS_EXCLUDE_KEY,
    PYTHON_ANALYSIS_IMPORT_FORMAT_KEY,
    PYTHON_ANALYSIS_INDEXING_KEY,
    PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY,
    PYTHON_ANALYSIS_INLAY_HINTS_PYTEST_PARAMETERS_KEY,
    PYTHON_ANALYSIS_INLAY_HINTS_VARIABLE_TYPES_KEY,
    PYTHON_ANALYSIS_PACKAGE_INDEX_DEPTHS_KEY,
    PYTHON_ANALYSIS_TYPE_CHECKING_MODE_KEY,
    PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY,
    PYTHON_DEFAULT_INTERPRETER_KEY,
    PYTHON_LANGUAGE_KEY,
    PYTHON_TESTING_PYTEST_ARGS_KEY,
    PYTHON_TESTING_PYTEST_ENABLED_KEY,
    PYTHON_TESTING_UNITTEST_ARGS_KEY,
    PYTHON_TESTING_UNITTEST_ENABLED_KEY,
    REPO_IGNORE_PATTERN,
    SEARCH_EXCLUDE_KEY,
    SOURCE_ORGANIZE_IMPORTS_KEY,
)
from src.utils.core import validate_python_formatter_option


def process_vscode_settings(
    vscode_settings: Dict[str, Any], debug: bool = False, test: bool = False, python_formatter: str = "black"
):
    """Do processing of the .vscode/settings.json file."""
    # pylint: disable=too-many-arguments too-many-locals
    if debug:
        print("process_vs_code_settings.py CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --test: {test}")
        print(f"    --python_formatter: {python_formatter}")
        print("")

    # Validate String Inputs
    validate_python_formatter_option(python_formatter=python_formatter)

    # python.defaultInterpreterPath
    _process_python_default_interpreter(data=vscode_settings)

    # python.analysis
    _process_python_analysis(data=vscode_settings)

    # search.exclude
    _process_search_exclude(data=vscode_settings)

    # python_formatter
    _process_python_formatter_option(data=vscode_settings, python_formatter=python_formatter)

    # Process Linter Options
    _process_python_linter_options(data=vscode_settings)

    # python_testing_framework
    _process_python_testing_options(data=vscode_settings)

    # include_isort
    _process_isort_options(data=vscode_settings)

    # python.analysis.packageIndexDepths
    _process_python_analysis_package_index_depths(data=vscode_settings)

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


def _process_python_default_interpreter(data: Dict[str, Any]):
    project_name = os.path.basename(os.getenv("PWD", ""))
    venv_location = f"~/.pyenv/versions/{project_name}"
    data[PYTHON_DEFAULT_INTERPRETER_KEY] = venv_location


def _process_python_analysis(data: Dict[str, Any]):
    # pylint: disable=too-many-branches
    auto_import_completions = cast(Optional[bool], data.get(PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY))
    if auto_import_completions is None:
        data[PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY] = True

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

    function_return_types = cast(Optional[bool], data.get(PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY))
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

    use_library_code_for_types = cast(Optional[bool], data.get(PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY))
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
        data[AUTOPEP8_ARGS_KEY] = []
        data.pop(BLACK_FORMATTER_ARGS_KEY, None)
    elif python_formatter == "black":
        python_language[EDITOR_DEFAULT_FORMATTER_KEY] = "ms-python.black-formatter"
        data.pop(AUTOPEP8_ARGS_KEY, None)
        data[BLACK_FORMATTER_ARGS_KEY] = [BLACK_FORMATTER_ARGS_VALUE]
    else:
        python_language[EDITOR_DEFAULT_FORMATTER_KEY] = "ms-python.python"
        data.pop(AUTOPEP8_ARGS_KEY, None)
        data.pop(BLACK_FORMATTER_ARGS_KEY, None)

    python_language[EDITOR_FORMAT_ON_SAVE_KEY] = True

    code_actions_on_save = cast(Optional[Dict[str, Any]], python_language.get(EDITOR_CODE_ACTIONS_ON_SAVE_KEY))
    if code_actions_on_save is None:
        code_actions_on_save = {}
        python_language[EDITOR_CODE_ACTIONS_ON_SAVE_KEY] = code_actions_on_save

    code_actions_on_save[SOURCE_ORGANIZE_IMPORTS_KEY] = "explicit"


def _process_python_linter_options(data: Dict[str, Any]):
    data[PYLINT_ARGS_KEY] = [PYLINT_ARGS_RCFILE_VALUE]
    data[FLAKE8_ARGS_KEY] = [FLAKE8_ARGS_RCFILE_VALUE]
    data[MYPY_ARGS_KEY] = ["--ignore-missing-imports", "--follow-imports=silent"]


def _process_python_testing_options(data: Dict[str, Any]):
    data[PYTHON_TESTING_PYTEST_ARGS_KEY] = [f"--ignore=./{REPO_NAME}"]
    data[PYTHON_TESTING_PYTEST_ENABLED_KEY] = True
    data.pop(PYTHON_TESTING_UNITTEST_ARGS_KEY, None)
    data[PYTHON_TESTING_UNITTEST_ENABLED_KEY] = False


def _process_isort_options(data: Dict[str, Any]):
    data[ISORT_ARGS_KEY] = [ISORT_ARGS_VALUE]


def _process_python_analysis_package_index_depths(data: Dict[str, Any]):
    existing_package_index_depths = cast(
        Optional[List[Dict[str, Any]]], data.get(PYTHON_ANALYSIS_PACKAGE_INDEX_DEPTHS_KEY, None)
    )

    if existing_package_index_depths is None:
        existing_package_index_depths = cast(List[Dict[str, Any]], [])

    index_names_copy = deepcopy(INDEX_NAMES)

    for item in existing_package_index_depths:
        name = cast(Optional[str], item.get(NAME_KEY))
        if name is not None and name in index_names_copy:
            # Depth
            existing_depth = cast(Optional[int], item.get(DEPTH_KEY))
            if existing_depth is None or existing_depth < DEFAULT_DEPTH:
                existing_depth = DEFAULT_DEPTH
            item[DEPTH_KEY] = existing_depth

            # includeAllSymbols
            item[INCLUDE_ALL_SYMBOLS_KEY] = True

            index_names_copy.remove(name)

    for name in index_names_copy:
        existing_package_index_depths.append(
            {
                NAME_KEY: name,
                DEPTH_KEY: DEFAULT_DEPTH,
                INCLUDE_ALL_SYMBOLS_KEY: True,
            }
        )

    data[PYTHON_ANALYSIS_PACKAGE_INDEX_DEPTHS_KEY] = existing_package_index_depths
