"""Test the src/process_pre_commit_config.py file."""
from typing import Any, Dict, List, cast

from ruamel.yaml.comments import CommentedMap

from src.constants.pre_commit_config import (
    AUTOPEP8_REPO_URL,
    BLACK_REPO_URL,
    CHECK_YAML_HOOK_ID,
    END_OF_FILE_FIXER_HOOK_ID,
    FLAKE8_REPO_URL,
    GIT_CHECK_HOOK_ID,
    GIT_DIRTY_HOOK_ID,
    ISORT_REPO_URL,
    JUMANJI_HOUSE_REPO_URL,
    JUMANJI_HOUSE_REV,
    LOCAL_REPO_URL,
    MARKDOWN_LINT_HOOK_ID,
    PRE_COMMIT_REPO_URL,
    PRE_COMMIT_REV,
    PRETTIER_REPO_URL,
    PYDOCSTYLE_REPO_URL,
    PYLINT_HOOK_ID,
    SHELL_FORMAT_HOOK_ID,
    SHELLCHECK_HOOK_ID,
    TRAILING_WHITESPACE_HOOK_ID,
    YAPF_REPO_URL,
)
from src.constants.pylintrc import PYLINTRC_FILENAME
from src.constants.shared import REPO_NAME
from src.process_pre_commit_config import PreCommitConfigProcessor

PYLINT_PROPER_ENTRY = f"{REPO_NAME}/ensure_venv.sh"
PYLINT_IMPROPER_ENTRY = "ensure_venv.sh"
RC_FILE_ARG = f"--rcfile={PYLINTRC_FILENAME}"
IGNORE_TEST_ARG = "--ignore=tests"
EXCLUDE_STATIC = "^static/"
FAKE_ENTRY = "fake.sh"


def _find_repo(pre_commit_config: Dict[str, Any], repo_url: str):
    repos = cast(List[Dict[str, Any]], pre_commit_config.get("repos", []))
    for repo in repos:
        if repo.get("repo") == repo_url:
            return repo
    return None


# Testing pre-commit base hooks
def test_process_pre_commit_config_include_base_hooks():
    """Test the process_pre_commit_config function with everything False."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}), test=True, debug=True
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=PRE_COMMIT_REPO_URL)
    assert repo is not None

    assert repo["repo"] == PRE_COMMIT_REPO_URL
    assert repo["rev"] == PRE_COMMIT_REV

    hooks = cast(List[Dict[str, Any]], repo.get("hooks", []))
    assert len(hooks) == 3

    assert len(hooks[0].keys()) == 1
    assert hooks[0].get("id") == CHECK_YAML_HOOK_ID

    assert len(hooks[1].keys()) == 1
    assert hooks[1].get("id") == END_OF_FILE_FIXER_HOOK_ID

    assert len(hooks[2].keys()) == 1
    assert hooks[2].get("id") == TRAILING_WHITESPACE_HOOK_ID


def test_process_pre_commit_config_include_base_hooks_retain_existing_fields():
    """Test the process_pre_commit_config function with everything False with existing data."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(
            CommentedMap,
            {
                "repos": [
                    {
                        "repo": PRE_COMMIT_REPO_URL,
                        "rev": "v4.5.0",
                        "hooks": [
                            {"id": CHECK_YAML_HOOK_ID, "test": "test"},
                            {"id": END_OF_FILE_FIXER_HOOK_ID, "test": "test"},
                            {"id": TRAILING_WHITESPACE_HOOK_ID, "test": "test"},
                        ],
                    }
                ]
            },
        ),
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=PRE_COMMIT_REPO_URL)
    assert repo is not None

    assert repo["repo"] == PRE_COMMIT_REPO_URL
    assert repo["rev"] == "v4.5.0"

    hooks = cast(List[Dict[str, Any]], repo.get("hooks", []))
    assert len(hooks) == 3

    assert len(hooks[0].keys()) == 2
    assert hooks[0].get("id") == CHECK_YAML_HOOK_ID
    assert hooks[0].get("test") == "test"

    assert len(hooks[1].keys()) == 2
    assert hooks[1].get("id") == END_OF_FILE_FIXER_HOOK_ID
    assert hooks[1].get("test") == "test"

    assert len(hooks[2].keys()) == 2
    assert hooks[2].get("id") == TRAILING_WHITESPACE_HOOK_ID
    assert hooks[2].get("test") == "test"


# Testing include_jumanji_house options
def test_process_pre_commit_config_include_jumanji_house():
    """Test the process_pre_commit_config function with the include_jumanji_house option set to True."""
    include_jumanji_house = True

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        include_jumanji_house=include_jumanji_house,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=JUMANJI_HOUSE_REPO_URL)
    assert repo is not None

    assert repo["repo"] == JUMANJI_HOUSE_REPO_URL
    assert repo["rev"] == JUMANJI_HOUSE_REV

    hooks = cast(List[Dict[str, Any]], repo.get("hooks", []))
    assert len(hooks) == 5

    assert len(hooks[0].keys()) == 1
    assert hooks[0].get("id") == GIT_CHECK_HOOK_ID

    assert len(hooks[1].keys()) == 1
    assert hooks[1].get("id") == GIT_DIRTY_HOOK_ID

    assert len(hooks[2].keys()) == 1
    assert hooks[2].get("id") == MARKDOWN_LINT_HOOK_ID

    assert len(hooks[3].keys()) == 1
    assert hooks[3].get("id") == SHELLCHECK_HOOK_ID

    assert len(hooks[4].keys()) == 1
    assert hooks[4].get("id") == SHELL_FORMAT_HOOK_ID


def test_process_pre_commit_config_include_jumanji_house_with_existing_data():
    """Test the process_pre_commit_config function with the include_jumanji_house option set to True."""
    include_jumanji_house = True

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(
            CommentedMap,
            {
                "repos": [
                    {
                        "repo": JUMANJI_HOUSE_REPO_URL,
                        "rev": "3.1.0",
                        "hooks": [
                            {"id": GIT_CHECK_HOOK_ID, "test": "test"},
                            {"id": GIT_DIRTY_HOOK_ID, "test": "test"},
                            {"id": MARKDOWN_LINT_HOOK_ID, "test": "test"},
                            {"id": SHELLCHECK_HOOK_ID, "test": "test"},
                            {"id": SHELL_FORMAT_HOOK_ID, "test": "test"},
                        ],
                    }
                ]
            },
        ),
        include_jumanji_house=include_jumanji_house,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=JUMANJI_HOUSE_REPO_URL)
    assert repo is not None

    assert repo["repo"] == JUMANJI_HOUSE_REPO_URL
    assert repo["rev"] == "3.1.0"

    hooks = cast(List[Dict[str, Any]], repo.get("hooks", []))
    assert len(hooks) == 5

    assert len(hooks[0].keys()) == 2
    assert hooks[0].get("id") == GIT_CHECK_HOOK_ID
    assert hooks[0].get("test") == "test"

    assert len(hooks[1].keys()) == 2
    assert hooks[1].get("id") == GIT_DIRTY_HOOK_ID
    assert hooks[1].get("test") == "test"

    assert len(hooks[2].keys()) == 2
    assert hooks[2].get("id") == MARKDOWN_LINT_HOOK_ID
    assert hooks[2].get("test") == "test"

    assert len(hooks[3].keys()) == 2
    assert hooks[3].get("id") == SHELLCHECK_HOOK_ID
    assert hooks[3].get("test") == "test"

    assert len(hooks[4].keys()) == 2
    assert hooks[4].get("id") == SHELL_FORMAT_HOOK_ID
    assert hooks[4].get("test") == "test"


def test_process_pre_commit_config_dont_include_jumanji_house():
    """Test the process_pre_commit_config function with the include_jumanji_house option set to False."""
    include_jumanji_house = False

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        include_jumanji_house=include_jumanji_house,
        include_prettier=True,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=JUMANJI_HOUSE_REPO_URL)
    assert repo is None


# Testing include_prettier options
def test_process_pre_commit_config_include_prettier():
    """Test the process_pre_commit_config function with the include_prettier option set to True."""
    include_prettier = True

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}), include_prettier=include_prettier, test=True, debug=True
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=PRETTIER_REPO_URL)
    assert repo is not None


def test_process_pre_commit_config_dont_include_prettier():
    """Test the process_pre_commit_config function with the include_prettier option set to False."""
    include_prettier = False

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        include_jumanji_house=True,
        include_prettier=include_prettier,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=PRETTIER_REPO_URL)
    assert repo is None


# Testing include_isort options
def test_process_pre_commit_config_include_isort():
    """Test the process_pre_commit_config function with the include_isort option set to True."""
    include_isort = True

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}), include_isort=include_isort, test=True, debug=True
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=ISORT_REPO_URL)
    assert repo is not None


def test_process_pre_commit_config_dont_include_isort():
    """Test the process_pre_commit_config function with the include_isort option set to False."""
    include_isort = False

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        include_jumanji_house=True,
        include_isort=include_isort,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=ISORT_REPO_URL)
    assert repo is None


# Testing python_formatter options
def test_process_pre_commit_config_no_python_formatter():
    """Test the process_pre_commit_config function with the python_formatter option set to an empty string."""
    python_formatter = ""

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        include_jumanji_house=True,
        python_formatter=python_formatter,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=AUTOPEP8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=BLACK_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=YAPF_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_autopep8_python_formatter():
    """Test the process_pre_commit_config function with the python_formatter option set to autopep8."""
    python_formatter = "autopep8"

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}), python_formatter=python_formatter, test=True, debug=True
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=BLACK_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=YAPF_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_black_python_formatter():
    """Test the process_pre_commit_config function with the python_formatter option set to black."""
    python_formatter = "black"

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}), python_formatter=python_formatter, test=True, debug=True
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=AUTOPEP8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=YAPF_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_yapf_python_formatter():
    """Test the process_pre_commit_config function with the python_formatter option set to yapf."""
    python_formatter = "yapf"

    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}), python_formatter=python_formatter, test=True, debug=True
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=AUTOPEP8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=BLACK_REPO_URL)
    assert repo is None


# Testing python_linter options
def test_process_pre_commit_config_no_python_linter():
    """Test the process_pre_commit_config function with all python linters disabled."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        include_jumanji_house=True,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_flake8_python_linter():
    """Test the process_pre_commit_config function with the flake8_enabled option set to True."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        flake8_enabled=True,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is not None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=PYDOCSTYLE_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_pylint_python_linter():
    """Test the process_pre_commit_config function with the pylint_enabled option set to True."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        pylint_enabled=True,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is not None

    repo["url"] = LOCAL_REPO_URL

    hooks = cast(List[Dict[str, Any]], repo.get("hooks", []))
    assert len(hooks) == 1

    hook = hooks[0]
    assert len(hook.keys()) == 6

    assert hook["id"] == PYLINT_HOOK_ID
    assert hook["name"] == "pylint"
    assert hook["entry"] == PYLINT_PROPER_ENTRY
    assert hook["language"] == "script"
    assert hook["types"] == ["python"]
    assert hook["args"] == ["pylint", "-v", RC_FILE_ARG]

    repo = _find_repo(pre_commit_config=result, repo_url=PYDOCSTYLE_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_pylint_python_linter_with_existing_pylint():
    """Test the process_pre_commit_config function with the pylint_enabled option set to True."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(
            CommentedMap,
            {
                "repos": [
                    {
                        "repo": LOCAL_REPO_URL,
                        "hooks": [
                            {
                                "id": PYLINT_HOOK_ID,
                                "name": "pylint",
                                "entry": PYLINT_IMPROPER_ENTRY,
                                "language": "script",
                                "types": ["python"],
                                "args": ["pylint", IGNORE_TEST_ARG, "-v", RC_FILE_ARG],
                                "exclude": EXCLUDE_STATIC,
                            }
                        ],
                    }
                ]
            },
        ),
        pylint_enabled=True,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is not None

    repo["url"] = LOCAL_REPO_URL

    hooks = cast(List[Dict[str, Any]], repo.get("hooks", []))
    assert len(hooks) == 1

    hook = hooks[0]
    assert len(hook.keys()) == 7

    assert hook["id"] == PYLINT_HOOK_ID
    assert hook["name"] == "pylint"
    assert hook["entry"] == PYLINT_PROPER_ENTRY
    assert hook["language"] == "script"
    assert hook["types"] == ["python"]
    assert hook["args"] == ["pylint", IGNORE_TEST_ARG, "-v", RC_FILE_ARG]
    assert hook["exclude"] == EXCLUDE_STATIC

    repo = _find_repo(pre_commit_config=result, repo_url=PYDOCSTYLE_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_no_python_linter_with_existing_pylint():
    """Test the process_pre_commit_config function with the pylint_enabled option set to True."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(
            CommentedMap,
            {
                "repos": [
                    {
                        "repo": LOCAL_REPO_URL,
                        "hooks": [
                            {
                                "id": PYLINT_HOOK_ID,
                                "name": "pylint",
                                "entry": PYLINT_IMPROPER_ENTRY,
                                "language": "script",
                                "types": ["python"],
                                "args": ["pylint", IGNORE_TEST_ARG, "-v", RC_FILE_ARG],
                                "exclude": EXCLUDE_STATIC,
                            }
                        ],
                    }
                ]
            },
        ),
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_no_python_linter_with_existing_pylint_and_other_local():
    """Test the process_pre_commit_config function with the pylint_enabled option set to True."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(
            CommentedMap,
            {
                "repos": [
                    {
                        "repo": LOCAL_REPO_URL,
                        "hooks": [
                            {
                                "id": "fake-local-hook-id",
                                "name": "fake-local-hook",
                                "entry": FAKE_ENTRY,
                                "language": "script",
                                "types": ["python"],
                            },
                            {
                                "id": PYLINT_HOOK_ID,
                                "name": "pylint",
                                "entry": PYLINT_IMPROPER_ENTRY,
                                "language": "script",
                                "types": ["python"],
                                "args": ["pylint", IGNORE_TEST_ARG, "-v", RC_FILE_ARG],
                                "exclude": EXCLUDE_STATIC,
                            },
                        ],
                    }
                ]
            },
        ),
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is not None

    repo["url"] = LOCAL_REPO_URL

    hooks = cast(List[Dict[str, Any]], repo.get("hooks", []))
    assert len(hooks) == 1

    hook = hooks[0]
    assert len(hook.keys()) == 5

    assert hook["id"] == "fake-local-hook-id"
    assert hook["name"] == "fake-local-hook"
    assert hook["entry"] == FAKE_ENTRY
    assert hook["language"] == "script"
    assert hook["types"] == ["python"]

    repo = _find_repo(pre_commit_config=result, repo_url=PYDOCSTYLE_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_pylint_python_linter_with_existing_local():
    """Test the process_pre_commit_config function with the pylint_enabled option set to True."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(
            CommentedMap,
            {
                "repos": [
                    {
                        "repo": LOCAL_REPO_URL,
                        "hooks": [
                            {
                                "id": "fake-local-hook-id",
                                "name": "fake-local-hook",
                                "entry": FAKE_ENTRY,
                                "language": "script",
                                "types": ["python"],
                            }
                        ],
                    }
                ]
            },
        ),
        pylint_enabled=True,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is not None

    repo["url"] = LOCAL_REPO_URL

    hooks = cast(List[Dict[str, Any]], repo.get("hooks", []))
    assert len(hooks) == 2

    hook1 = hooks[0]
    assert len(hook1.keys()) == 5

    assert hook1["id"] == "fake-local-hook-id"
    assert hook1["name"] == "fake-local-hook"
    assert hook1["entry"] == FAKE_ENTRY
    assert hook1["language"] == "script"
    assert hook1["types"] == ["python"]

    hook2 = hooks[1]
    assert len(hook2.keys()) == 6

    assert hook2["id"] == PYLINT_HOOK_ID
    assert hook2["name"] == "pylint"
    assert hook2["entry"] == PYLINT_PROPER_ENTRY
    assert hook2["language"] == "script"
    assert hook2["types"] == ["python"]
    assert hook2["args"] == ["pylint", "-v", RC_FILE_ARG]

    repo = _find_repo(pre_commit_config=result, repo_url=PYDOCSTYLE_REPO_URL)
    assert repo is None


def test_process_pre_commit_config_pydocstyle_python_linter():
    """Test the process_pre_commit_config function with the pylint_enabled option set to True."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        pydocstyle_enabled=True,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is None

    repo = _find_repo(pre_commit_config=result, repo_url=PYDOCSTYLE_REPO_URL)
    assert repo is not None


def test_process_pre_commit_config_all_python_linter():
    """Test the process_pre_commit_config function when all linters are enabled."""
    result = PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        pylint_enabled=True,
        flake8_enabled=True,
        pydocstyle_enabled=True,
        bandit_enabled=True,
        test=True,
        debug=True,
    ).process_pre_commit_config()
    assert result is not None

    repo = _find_repo(pre_commit_config=result, repo_url=FLAKE8_REPO_URL)
    assert repo is not None

    repo = _find_repo(pre_commit_config=result, repo_url=LOCAL_REPO_URL)
    assert repo is not None

    repo = _find_repo(pre_commit_config=result, repo_url=PYDOCSTYLE_REPO_URL)
    assert repo is not None


# Happy Path Test
def test_process_pre_commit_config():
    """Test the process_pre_commit_config function with all options set."""
    PreCommitConfigProcessor(
        pre_commit_config=cast(CommentedMap, {}),
        include_jumanji_house=True,
        include_prettier=True,
        include_isort=True,
        python_formatter="black",
        pylint_enabled=True,
        flake8_enabled=True,
        pydocstyle_enabled=True,
        bandit_enabled=True,
        test=True,
    ).process_pre_commit_config()
