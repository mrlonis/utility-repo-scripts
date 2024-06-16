"""Do processing of the .pre-commit-config.yaml file."""

from typing import Any, Dict, List, cast

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from src.constants.pre_commit_config import (
    AUTOPEP8_HOOK,
    AUTOPEP8_HOOK_ID,
    AUTOPEP8_REPO,
    AUTOPEP8_REPO_URL,
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
    PYLINT_HOOK,
    PYLINT_HOOK_ID,
    SHELL_FORMAT_HOOK,
    SHELL_FORMAT_HOOK_ID,
    SHELLCHECK_HOOK,
    SHELLCHECK_HOOK_ID,
    TRAILING_WHITESPACE_HOOK,
    TRAILING_WHITESPACE_HOOK_ID,
)
from src.constants.shared import REPO_NAME
from src.utils.core import validate_python_formatter_option
from src.utils.ruamel.yaml import find_hook_id_index, find_repo_index, remove_hooks, update_hook


class PreCommitConfigProcessor:
    # pylint: disable=too-many-instance-attributes too-few-public-methods
    """Process the .pre-commit-config.yaml file."""

    def __init__(
        self,
        pre_commit_config: CommentedMap,
        debug: bool = False,
        test: bool = False,
        include_jumanji_house: bool = False,
        include_prettier: bool = False,
        include_isort: bool = False,
        python_formatter: str = "",
        pylint_enabled: bool = False,
        flake8_enabled: bool = False,
        pre_commit_pylint_entry_prefix: str = f"{REPO_NAME}/",
    ):  # pylint: disable=too-many-arguments
        """Initialize the PreCommitConfigProcessor class."""
        self.pre_commit_config = pre_commit_config
        self.debug = debug
        self.test = test
        self.include_jumanji_house = include_jumanji_house
        self.include_prettier = include_prettier
        self.include_isort = include_isort
        self.python_formatter = python_formatter
        self.pylint_enabled = pylint_enabled
        self.flake8_enabled = flake8_enabled
        self.pre_commit_pylint_entry_prefix = pre_commit_pylint_entry_prefix

        if self.debug:
            print("process_pre_commit_config.py CLI Arguments:")
            print(f"    --debug: {self.debug}")
            print(f"    --test: {self.test}")
            print(f"    --include_jumanji_house: {self.include_jumanji_house}")
            print(f"    --include_prettier: {self.include_prettier}")
            print(f"    --include_isort: {self.include_isort}")
            print(f"    --python_formatter: {self.python_formatter}")
            print(f"    --pylint_enabled: {self.pylint_enabled}")
            print(f"    --flake8_enabled: {self.flake8_enabled}")
            print(f"    --pylint_entry_prefix: {self.pre_commit_pylint_entry_prefix}")
            print("")

    def process_pre_commit_config(self):
        """Do processing of the .pre-commit-config.yaml file."""
        # Validate String Inputs
        validate_python_formatter_option(python_formatter=self.python_formatter)

        # pre commit base hooks
        self._process_pre_commit_repo()

        # include_jumanji_house
        self._process_jumanji_house_repo()

        # include_prettier
        if not self.include_prettier:
            remove_hooks(pre_commit_config=self.pre_commit_config, repo_urls=[PRETTIER_REPO_URL])
        else:
            update_hook(
                pre_commit_config=self.pre_commit_config,
                repo_url=PRETTIER_REPO_URL,
                repo_default=PRETTIER_REPO,
                hooks=[(PRETTIER_HOOK_ID, PRETTIER_HOOK)],
            )

        # include_isort
        if not self.include_isort:
            remove_hooks(pre_commit_config=self.pre_commit_config, repo_urls=[ISORT_REPO_URL])
        else:
            update_hook(
                pre_commit_config=self.pre_commit_config,
                repo_url=ISORT_REPO_URL,
                repo_default=ISORT_REPO,
                hooks=[(ISORT_HOOK_ID, ISORT_HOOK)],
            )

        # python_formatter
        self._process_python_formatter_option()

        # Process Linter Options
        self._process_python_linter_options()

        # Write .pre-commit-config.yaml
        if not self.test:  # pragma: no cover
            if self.debug:  # pragma: no cover
                print("Creating .pre-commit-config.yaml")  # pragma: no cover
            with open(".pre-commit-config.yaml", "w", encoding="utf-8") as file:  # pragma: no cover
                yaml = YAML()  # pragma: no cover
                yaml.default_flow_style = False  # pragma: no cover
                yaml.dump(self.pre_commit_config, file)  # pragma: no cover
        else:
            if self.debug:
                print("TESTING: Not Creating .pre-commit-config.yaml")
                print(self.pre_commit_config)

        return self.pre_commit_config

    def _process_pre_commit_repo(self):
        update_hook(
            pre_commit_config=self.pre_commit_config,
            repo_url=PRE_COMMIT_REPO_URL,
            repo_default=PRE_COMMIT_REPO,
            hooks=[
                (CHECK_YAML_HOOK_ID, CHECK_YAML_HOOK),
                (END_OF_FILE_FIXER_HOOK_ID, END_OF_FILE_FIXER_HOOK),
                (TRAILING_WHITESPACE_HOOK_ID, TRAILING_WHITESPACE_HOOK),
            ],
        )

    def _process_jumanji_house_repo(self):
        if not self.include_jumanji_house:
            remove_hooks(
                pre_commit_config=self.pre_commit_config,
                repo_urls=[JUMANJI_HOUSE_REPO_URL],
            )
        else:
            update_hook(
                pre_commit_config=self.pre_commit_config,
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

    def _process_python_formatter_option(self):
        if self.python_formatter == "autopep8":
            update_hook(
                pre_commit_config=self.pre_commit_config,
                repo_url=AUTOPEP8_REPO_URL,
                repo_default=AUTOPEP8_REPO,
                hooks=[(AUTOPEP8_HOOK_ID, AUTOPEP8_HOOK)],
            )

            remove_hooks(
                pre_commit_config=self.pre_commit_config,
                repo_urls=[BLACK_REPO_URL],
            )
        elif self.python_formatter == "black":
            update_hook(
                pre_commit_config=self.pre_commit_config,
                repo_url=BLACK_REPO_URL,
                repo_default=BLACK_REPO,
                hooks=[(BLACK_HOOK_ID, BLACK_HOOK)],
            )

            remove_hooks(
                pre_commit_config=self.pre_commit_config,
                repo_urls=[AUTOPEP8_REPO_URL],
            )
        else:
            remove_hooks(
                pre_commit_config=self.pre_commit_config,
                repo_urls=[AUTOPEP8_REPO_URL, BLACK_REPO_URL],
            )

    def _update_pylint_config(self):
        local_repo_index = find_repo_index(self.pre_commit_config, LOCAL_REPO_URL)
        repos = cast(List[Dict[str, Any]], self.pre_commit_config.get("repos", []))
        local_repo = repos[local_repo_index]

        pylint_hook_id = find_hook_id_index(pre_commit_repo=local_repo, hook_id=PYLINT_HOOK_ID)
        hooks = cast(List[Dict[str, Any]], local_repo.get("hooks", []))
        hooks[pylint_hook_id]["entry"] = f"{self.pre_commit_pylint_entry_prefix}ensure_venv.sh"

    def _process_python_linter_options(self):
        if self.pylint_enabled:
            update_hook(
                pre_commit_config=self.pre_commit_config,
                repo_url=LOCAL_REPO_URL,
                repo_default=LOCAL_REPO,
                hooks=[(PYLINT_HOOK_ID, PYLINT_HOOK)],
            )
            self._update_pylint_config()
        else:
            print("Pylint disabled! Attempting to remove it from the local repo...")
            remove_hooks(
                pre_commit_config=self.pre_commit_config,
                repo_urls=[LOCAL_REPO_URL],
                local_ids=[PYLINT_HOOK_ID],
            )

        if not self.flake8_enabled:
            remove_hooks(pre_commit_config=self.pre_commit_config, repo_urls=[FLAKE8_REPO_URL])
        else:
            update_hook(
                pre_commit_config=self.pre_commit_config,
                repo_url=FLAKE8_REPO_URL,
                repo_default=FLAKE8_REPO,
                hooks=[(FLAKE8_HOOK_ID, FLAKE8_HOOK)],
            )
