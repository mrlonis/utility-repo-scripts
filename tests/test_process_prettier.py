"""Tests for src/process_prettier.py."""

from typing import Any, Dict, List, cast

from ruamel.yaml.comments import CommentedMap

from src.constants.pre_commit_config import PRETTIER_REPO_URL
from src.process_prettier import process_pre_commit_config


def _find_repo(pre_commit_config: Dict[str, Any], repo_url: str):
    repos = cast(List[Dict[str, Any]], pre_commit_config.get("repos", []))
    for repo in repos:
        if repo.get("repo") == repo_url:
            return repo
    return None


def test_process_prettier_pre_commit_config_does_not_add_missing_repo():
    """The prettier fixer should not add the repo when it is not already configured."""
    result = process_pre_commit_config(pre_commit_config=cast(CommentedMap, {"repos": []}), test=True, debug=True)

    assert result is not None
    assert _find_repo(result, PRETTIER_REPO_URL) is None


def test_process_prettier_pre_commit_config_updates_existing_repo_rev():
    """The prettier fixer should still pin the rev when the repo already exists."""
    result = process_pre_commit_config(
        pre_commit_config=cast(
            CommentedMap,
            {
                "repos": [
                    {
                        "repo": PRETTIER_REPO_URL,
                        "rev": "v3.0.0-alpha.4",
                        "hooks": [{"id": "prettier"}],
                    }
                ]
            },
        ),
        test=True,
        debug=True,
    )

    assert result is not None
    repo = _find_repo(result, PRETTIER_REPO_URL)
    assert repo is not None
    assert repo["rev"] == "v3.1.0"
