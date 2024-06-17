"""Do processing of the .flake8 file."""

from json import dump
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from src.constants.pre_commit_config import PRETTIER_REPO, PRETTIER_REPO_URL
from src.constants.prettier import PRINT_WIDTH_KEY
from src.constants.shared import DEFAULT_LINE_LENGTH
from src.utils.ruamel.yaml import update_repo_rev


def process_prettierrc(
    prettierrc_data: dict[str, Any],
    debug: bool = False,
    test: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
):
    """Do processing for prettierrc file."""
    if debug:
        print("process_prettier.py: process_prettierrc(): CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --test: {test}")
        print(f"    --line_length: {line_length}")
        print(f"    --prettierrc_data: {prettierrc_data}")
        print("")

    if prettierrc_data[PRINT_WIDTH_KEY] != line_length:
        prettierrc_data[PRINT_WIDTH_KEY] = line_length

    if not test:  # pragma: no cover
        if debug:  # pragma: no cover
            print("Writing .prettierrc file")  # pragma: no cover
        with open(".prettierrc", "w", encoding="utf-8") as prettierrc_file:  # pragma: no cover
            dump(prettierrc_data, prettierrc_file, indent=2)
    else:
        if debug:
            print("TESTING: Not Writing .prettierrc file")

    return prettierrc_data


def process_pre_commit_config(
    pre_commit_config: CommentedMap,
    debug: bool = False,
    test: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
):
    """Do processing for prettier file."""
    if debug:
        print("process_prettier.py: process_pre_commit_config(): CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --test: {test}")
        print(f"    --line_length: {line_length}")
        print(f"    --pre_commit_config: {pre_commit_config}")
        print("")

    # Fixing prettier pre-commit hook since it updates to an alpha version
    if debug:
        print("Updating prettier pre-commit hook")
    update_repo_rev(
        pre_commit_config=pre_commit_config,
        repo_url=PRETTIER_REPO_URL,
        repo_default=PRETTIER_REPO,
        rev="v3.1.0",
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
