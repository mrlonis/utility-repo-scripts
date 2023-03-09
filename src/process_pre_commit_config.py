"""Do processing of the .pre-commit-config.yaml file."""
from typing import Any, Dict, List, cast

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from src.constants.pre_commit_config import (
    AUTOPEP8_HOOK,
    AUTOPEP8_HOOK_ID,
    AUTOPEP8_REPO,
    AUTOPEP8_REPO_URL,
    BANDIT_HOOK,
    BANDIT_HOOK_ID,
    BANDIT_REPO,
    BANDIT_REPO_URL,
    BLACK_HOOK,
    BLACK_HOOK_ID,
    BLACK_REPO,
    BLACK_REPO_URL,
    CHECK_YAML_HOOK,
    CHECK_YAML_HOOK_ID,
    END_OF_FILE_FIXER_HOOK,
    END_OF_FILE_FIXER_HOOK_ID,
    FLAKE8_HOOK,
    FLAKE8_HOOK_ID,
    FLAKE8_REPO,
    FLAKE8_REPO_URL,
    GIT_CHECK_HOOK,
    GIT_CHECK_HOOK_ID,
    GIT_DIRTY_HOOK,
    GIT_DIRTY_HOOK_ID,
    ISORT_HOOK,
    ISORT_HOOK_ID,
    ISORT_REPO,
    ISORT_REPO_URL,
    JUMANJI_HOUSE_REPO,
    JUMANJI_HOUSE_REPO_URL,
    LOCAL_REPO,
    LOCAL_REPO_URL,
    MARKDOWN_LINT_HOOK,
    MARKDOWN_LINT_HOOK_ID,
    PRE_COMMIT_REPO,
    PRE_COMMIT_REPO_URL,
    PRETTIER_HOOK,
    PRETTIER_HOOK_ID,
    PRETTIER_REPO,
    PRETTIER_REPO_URL,
    PYDOCSTYLE_HOOK,
    PYDOCSTYLE_HOOK_ID,
    PYDOCSTYLE_REPO,
    PYDOCSTYLE_REPO_URL,
    PYLINT_HOOK,
    PYLINT_HOOK_ID,
    SHELL_FORMAT_HOOK,
    SHELL_FORMAT_HOOK_ID,
    SHELLCHECK_HOOK,
    SHELLCHECK_HOOK_ID,
    TRAILING_WHITESPACE_HOOK,
    TRAILING_WHITESPACE_HOOK_ID,
    YAPF_HOOK,
    YAPF_HOOK_ID,
    YAPF_REPO,
    YAPF_REPO_URL,
)
from src.constants.shared import REPO_NAME
from src.utils.core import validate_python_formatter_option
from src.utils.ruamel.yaml import find_hook_id_index, find_repo_index, remove_hooks, update_hook


def _process_pre_commit_repo(pre_commit_config: CommentedMap):
    update_hook(
        pre_commit_config=pre_commit_config,
        repo_url=PRE_COMMIT_REPO_URL,
        repo_default=PRE_COMMIT_REPO,
        hooks=[
            (CHECK_YAML_HOOK_ID, CHECK_YAML_HOOK),
            (END_OF_FILE_FIXER_HOOK_ID, END_OF_FILE_FIXER_HOOK),
            (TRAILING_WHITESPACE_HOOK_ID, TRAILING_WHITESPACE_HOOK),
        ],
    )


def _process_jumanji_house_repo(pre_commit_config: CommentedMap, include_jumanji_house: bool):
    if not include_jumanji_house:
        remove_hooks(
            pre_commit_config=pre_commit_config,
            repo_urls=[JUMANJI_HOUSE_REPO_URL],
        )
    else:
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=JUMANJI_HOUSE_REPO_URL,
            repo_default=JUMANJI_HOUSE_REPO,
            hooks=[
                (GIT_CHECK_HOOK_ID, GIT_CHECK_HOOK),
                (GIT_DIRTY_HOOK_ID, GIT_DIRTY_HOOK),
                (MARKDOWN_LINT_HOOK_ID, MARKDOWN_LINT_HOOK),
                (SHELLCHECK_HOOK_ID, SHELLCHECK_HOOK),
                (SHELL_FORMAT_HOOK_ID, SHELL_FORMAT_HOOK),
            ],
        )


def _process_python_formatter_option(pre_commit_config: CommentedMap, python_formatter: str):
    if python_formatter == "autopep8":
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=AUTOPEP8_REPO_URL,
            repo_default=AUTOPEP8_REPO,
            hooks=[(AUTOPEP8_HOOK_ID, AUTOPEP8_HOOK)],
        )

        remove_hooks(
            pre_commit_config=pre_commit_config,
            repo_urls=[BLACK_REPO_URL, YAPF_REPO_URL],
        )
    elif python_formatter == "black":
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=BLACK_REPO_URL,
            repo_default=BLACK_REPO,
            hooks=[(BLACK_HOOK_ID, BLACK_HOOK)],
        )

        remove_hooks(
            pre_commit_config=pre_commit_config,
            repo_urls=[
                AUTOPEP8_REPO_URL,
                YAPF_REPO_URL,
            ],
        )
    elif python_formatter == "yapf":
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=YAPF_REPO_URL,
            repo_default=YAPF_REPO,
            hooks=[(YAPF_HOOK_ID, YAPF_HOOK)],
        )

        remove_hooks(
            pre_commit_config=pre_commit_config,
            repo_urls=[
                AUTOPEP8_REPO_URL,
                BLACK_REPO_URL,
            ],
        )
    else:
        remove_hooks(
            pre_commit_config=pre_commit_config,
            repo_urls=[
                AUTOPEP8_REPO_URL,
                BLACK_REPO_URL,
                YAPF_REPO_URL,
            ],
        )


def _update_pylint_config(pre_commit_config: CommentedMap, pre_commit_pylint_entry_prefix: str):
    local_repo_index = find_repo_index(pre_commit_config, LOCAL_REPO_URL)
    repos = cast(List[Dict[str, Any]], pre_commit_config.get("repos", []))
    local_repo = repos[local_repo_index]

    pylint_hook_id = find_hook_id_index(pre_commit_repo=local_repo, hook_id=PYLINT_HOOK_ID)
    hooks = cast(List[Dict[str, Any]], local_repo.get("hooks", []))
    hooks[pylint_hook_id]["entry"] = f"{pre_commit_pylint_entry_prefix}ensure_venv.sh"


def _process_python_linter_options(
    pre_commit_config: CommentedMap,
    pylint_enabled: bool,
    flake8_enabled: bool,
    pydocstyle_enabled: bool,
    bandit_enabled: bool,
    pre_commit_pylint_entry_prefix: str = f"{REPO_NAME}/",
):
    if pylint_enabled:
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=LOCAL_REPO_URL,
            repo_default=LOCAL_REPO,
            hooks=[(PYLINT_HOOK_ID, PYLINT_HOOK)],
        )
        _update_pylint_config(
            pre_commit_config=pre_commit_config, pre_commit_pylint_entry_prefix=pre_commit_pylint_entry_prefix
        )
    else:
        print("Pylint disabled! Attempting to remove it from the local repo...")
        remove_hooks(
            pre_commit_config=pre_commit_config,
            repo_urls=[LOCAL_REPO_URL],
            local_ids=[PYLINT_HOOK_ID],
        )

    if not flake8_enabled:
        remove_hooks(pre_commit_config=pre_commit_config, repo_urls=[FLAKE8_REPO_URL])
    else:
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=FLAKE8_REPO_URL,
            repo_default=FLAKE8_REPO,
            hooks=[(FLAKE8_HOOK_ID, FLAKE8_HOOK)],
        )

    if not pydocstyle_enabled:
        remove_hooks(pre_commit_config=pre_commit_config, repo_urls=[PYDOCSTYLE_REPO_URL])
    else:
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=PYDOCSTYLE_REPO_URL,
            repo_default=PYDOCSTYLE_REPO,
            hooks=[(PYDOCSTYLE_HOOK_ID, PYDOCSTYLE_HOOK)],
        )

    if not bandit_enabled:
        remove_hooks(pre_commit_config=pre_commit_config, repo_urls=[BANDIT_REPO_URL])
    else:
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=BANDIT_REPO_URL,
            repo_default=BANDIT_REPO,
            hooks=[(BANDIT_HOOK_ID, BANDIT_HOOK)],
        )


def process_pre_commit_config(
    pre_commit_config: CommentedMap,
    debug: bool = False,
    test: bool = False,
    include_jumanji_house: bool = False,
    include_prettier: bool = False,
    include_isort: bool = False,
    python_formatter: str = "",
    pylint_enabled: bool = False,
    flake8_enabled: bool = False,
    pydocstyle_enabled: bool = False,
    bandit_enabled: bool = False,
    pre_commit_pylint_entry_prefix: str = f"{REPO_NAME}/",
):
    """Do processing of the .pre-commit-config.yaml file."""
    # pylint: disable=too-many-arguments
    if debug:
        print("process_pre_commit_config.py CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --test: {test}")
        print(f"    --include_jumanji_house: {include_jumanji_house}")
        print(f"    --include_prettier: {include_prettier}")
        print(f"    --include_isort: {include_isort}")
        print(f"    --python_formatter: {python_formatter}")
        print(f"    --pylint_enabled: {pylint_enabled}")
        print(f"    --flake8_enabled: {flake8_enabled}")
        print(f"    --pydocstyle_enabled: {pydocstyle_enabled}")
        print(f"    --pylint_entry_prefix: {pre_commit_pylint_entry_prefix}")
        print(f"    --bandit_enabled: {bandit_enabled}")
        print("")

    # Validate String Inputs
    validate_python_formatter_option(python_formatter=python_formatter)

    # pre commit base hooks
    _process_pre_commit_repo(pre_commit_config=pre_commit_config)

    # include_jumanji_house
    _process_jumanji_house_repo(
        pre_commit_config=pre_commit_config, include_jumanji_house=include_jumanji_house
    )

    # include_prettier
    if not include_prettier:
        remove_hooks(pre_commit_config=pre_commit_config, repo_urls=[PRETTIER_REPO_URL])
    else:
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=PRETTIER_REPO_URL,
            repo_default=PRETTIER_REPO,
            hooks=[(PRETTIER_HOOK_ID, PRETTIER_HOOK)],
        )

    # include_isort
    if not include_isort:
        remove_hooks(pre_commit_config=pre_commit_config, repo_urls=[ISORT_REPO_URL])
    else:
        update_hook(
            pre_commit_config=pre_commit_config,
            repo_url=ISORT_REPO_URL,
            repo_default=ISORT_REPO,
            hooks=[(ISORT_HOOK_ID, ISORT_HOOK)],
        )

    # python_formatter
    _process_python_formatter_option(pre_commit_config=pre_commit_config, python_formatter=python_formatter)

    # Process Linter Options
    _process_python_linter_options(
        pre_commit_config=pre_commit_config,
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        bandit_enabled=bandit_enabled,
        pre_commit_pylint_entry_prefix=pre_commit_pylint_entry_prefix,
    )

    # Write .pre-commit-config.yaml
    if not test:  # pragma: no cover
        if debug:  # pragma: no cover
            print("Creating .pre-commit-config.yaml")  # pragma: no cover
        with open(".pre-commit-config.yaml", "w", encoding="utf-8") as file:  # pragma: no cover
            yaml = YAML()  # pragma: no cover
            yaml.default_flow_style = False  # pragma: no cover
            yaml.dump(pre_commit_config, file)  # pragma: no cover
    else:
        if debug:
            print("TESTING: Not Creating .pre-commit-config.yaml")
            print(pre_commit_config)

    return pre_commit_config
