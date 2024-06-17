"""This module contains utility functions for asserting vscode settings."""

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


def assert_python_default_interpreter_settings(data: Dict[str, Any]):
    """Assert that the python default interpreter settings are set correctly."""
    assert data.get(PYTHON_DEFAULT_INTERPRETER_KEY) == f"~/.pyenv/versions/{REPO_NAME}"


def assert_python_analysis_package_index_depths_settings(data: Dict[str, Any]):
    """Assert that the python analysis package index depths settings are set correctly."""
    package_index_depths = cast(Optional[List[Dict[str, Any]]], data.get(PYTHON_ANALYSIS_PACKAGE_INDEX_DEPTHS_KEY))
    assert package_index_depths is not None

    index_names_copy = deepcopy(INDEX_NAMES)

    for item in package_index_depths:
        name = cast(Optional[str], item.get(NAME_KEY))
        if name is not None and name in index_names_copy:
            # Depth
            depth = cast(Optional[int], item.get(DEPTH_KEY))
            assert depth is not None
            assert depth >= DEFAULT_DEPTH

            # includeAllSymbols
            include_all_symbols = cast(Optional[bool], item.get(INCLUDE_ALL_SYMBOLS_KEY))
            assert include_all_symbols is not None
            assert include_all_symbols is True

            index_names_copy.remove(name)

    assert len(index_names_copy) == 0


def assert_python_analysis_settings(data: Dict[str, Any]):
    """Assert that the python analysis settings are set correctly."""
    auto_import_completions = cast(Optional[bool], data.get(PYTHON_ANALYSIS_AUTO_IMPORT_COMPLETIONS_KEY))
    assert auto_import_completions is not None

    auto_search_paths = cast(Optional[bool], data.get(PYTHON_ANALYSIS_AUTO_SEARCH_PATHS_KEY))
    assert auto_search_paths is not None

    diagnostic_mode = cast(Optional[str], data.get(PYTHON_ANALYSIS_DIAGNOSTIC_MODE_KEY))
    assert diagnostic_mode is not None

    exclude = cast(Optional[List[str]], data.get(PYTHON_ANALYSIS_EXCLUDE_KEY))
    assert exclude is not None
    assert REPO_IGNORE_PATTERN in exclude

    import_format = cast(Optional[str], data.get(PYTHON_ANALYSIS_IMPORT_FORMAT_KEY))
    assert import_format is not None

    indexing = cast(Optional[bool], data.get(PYTHON_ANALYSIS_INDEXING_KEY))
    assert indexing is not None

    function_return_types = cast(Optional[bool], data.get(PYTHON_ANALYSIS_INLAY_HINTS_FUNCTION_RETURN_TYPES_KEY))
    assert function_return_types is not None

    pytest_parameters = cast(Optional[bool], data.get(PYTHON_ANALYSIS_INLAY_HINTS_PYTEST_PARAMETERS_KEY))
    assert pytest_parameters is not None

    variable_types = cast(Optional[bool], data.get(PYTHON_ANALYSIS_INLAY_HINTS_VARIABLE_TYPES_KEY))
    assert variable_types is not None

    # python.analysis.packageIndexDepths
    assert_python_analysis_package_index_depths_settings(data=data)

    type_checking_mode = cast(Optional[str], data.get(PYTHON_ANALYSIS_TYPE_CHECKING_MODE_KEY))
    assert type_checking_mode is not None
    assert type_checking_mode in ["off", "basic", "strict"]

    use_library_code_for_types = cast(Optional[bool], data.get(PYTHON_ANALYSIS_USE_LIBRARY_CODE_FOR_TYPES_KEY))
    assert use_library_code_for_types is not None


def assert_search_exclude_settings(data: Dict[str, Any]):
    """Assert that the search exclude settings are set correctly."""
    exclude = cast(Optional[Dict[str, bool]], data.get(SEARCH_EXCLUDE_KEY))
    assert exclude is not None

    repo_exclude = cast(Optional[bool], exclude.get(f"{REPO_NAME}/**"))
    assert repo_exclude is not None
    assert repo_exclude is True


def assert_python_formatter_settings(data: Dict[str, Any], python_formatter: str):
    """Assert that the python formatter settings are set correctly."""
    python_language = cast(Optional[Dict[str, Any]], data.get(PYTHON_LANGUAGE_KEY))
    assert python_language is not None

    if python_formatter == "autopep8":
        assert python_language.get(EDITOR_DEFAULT_FORMATTER_KEY) == "ms-python.autopep8"
        assert data.get(AUTOPEP8_ARGS_KEY) == []
        assert data.get(BLACK_FORMATTER_ARGS_KEY) is None
    elif python_formatter == "black":
        assert python_language.get(EDITOR_DEFAULT_FORMATTER_KEY) == "ms-python.black-formatter"
        assert data.get(AUTOPEP8_ARGS_KEY) is None
        assert data.get(BLACK_FORMATTER_ARGS_KEY) == [BLACK_FORMATTER_ARGS_VALUE]
    else:
        assert python_language.get(EDITOR_DEFAULT_FORMATTER_KEY) == "ms-python.python"
        assert data.get(BLACK_FORMATTER_ARGS_KEY) is None
        assert data.get(BLACK_FORMATTER_ARGS_KEY) is None

    format_on_save = cast(Optional[bool], python_language.get(EDITOR_FORMAT_ON_SAVE_KEY))
    assert format_on_save is not None
    assert format_on_save is True

    code_actions_on_save = cast(Optional[Dict[str, Any]], python_language.get(EDITOR_CODE_ACTIONS_ON_SAVE_KEY))
    assert code_actions_on_save is not None

    source_organize_imports = cast(Optional[bool], code_actions_on_save.get(SOURCE_ORGANIZE_IMPORTS_KEY))
    assert source_organize_imports is not None
    assert source_organize_imports == "explicit"


def assert_python_linting_settings(data: Dict[str, Any]):
    # pylint: disable=too-many-branches too-many-statements
    """Assert that the python linting settings are set correctly."""
    assert data.get(PYLINT_ARGS_KEY) == [PYLINT_ARGS_RCFILE_VALUE]
    assert data.get(FLAKE8_ARGS_KEY) == [FLAKE8_ARGS_RCFILE_VALUE]
    assert data.get(MYPY_ARGS_KEY) == ["--ignore-missing-imports", "--follow-imports=silent"]


def assert_python_testing_settings(data: Dict[str, Any]):
    """Assert that the python testing settings are set correctly."""
    assert data.get(PYTHON_TESTING_PYTEST_ARGS_KEY) is not None
    assert data.get(PYTHON_TESTING_PYTEST_ENABLED_KEY) is True
    assert data.get(PYTHON_TESTING_UNITTEST_ARGS_KEY) is None
    assert data.get(PYTHON_TESTING_UNITTEST_ENABLED_KEY) is False


def assert_isort_settings(data: Dict[str, Any]):
    """Assert that the isort settings are set correctly."""
    assert data.get(ISORT_ARGS_KEY) is not None
    assert data.get(ISORT_ARGS_KEY) == [ISORT_ARGS_VALUE]
