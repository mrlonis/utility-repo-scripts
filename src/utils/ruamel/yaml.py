"""ruamel.yaml utility functions."""
from copy import deepcopy
from os import getenv
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


def load_yaml_file(debug: bool, exists: bool, filename: str, sample: str):
    """Load a yaml file or create it from a sample."""
    yaml = YAML()

    if exists:
        if debug:
            print(f"{filename} already exists...")
            print(f"Loading {filename}...")
        pwd = getenv("PWD")
        if pwd is None:
            raise RuntimeError("PWD environment variable is not set.")
        filepath = f"{pwd}/{filename}"
        if debug:
            print(f"filepath: {filepath}")
        with open(Path(filepath).resolve(), "r", encoding="utf-8") as file:
            data = cast(CommentedMap, yaml.load(file))
    else:
        data = cast(CommentedMap, yaml.load(sample))
    return data


def find_repo_index(pre_commit_config: Dict[str, Any], repo_url: str) -> int:
    """Find the hook index of a given `repo_url` in the .pre-commit-config.yaml file."""
    for index, repo in enumerate(pre_commit_config.get("repos", cast(List[Dict[str, Any]], []))):
        if repo.get("repo") == repo_url:
            return index
    raise ValueError(f"Could not find repo: {repo_url}")


def find_hook_id_index(pre_commit_repo: Dict[str, Any], hook_id: str):
    """Find the hook index of a given `hook_id` in the .pre-commit-config.yaml file."""
    for index, hook in enumerate(pre_commit_repo.get("hooks", cast(List[Dict[str, Any]], []))):
        if hook.get("id") == hook_id:
            return index
    raise ValueError(f"Could not find hook with id {hook_id} in repo: {pre_commit_repo.get('repo')}")


def _remove_local_hook(
    pre_commit_config: Dict[str, Any],
    repos: List[Dict[str, Any]],
    repo_url: str,
    local_ids: Optional[List[str]],
):
    test_log = False
    if local_ids:
        test_log = True
    if test_log:
        print(f"Removing local hook(s) {local_ids} from repo: {repo_url}")
    try:
        hook_index = find_repo_index(pre_commit_config, repo_url)
    except ValueError:
        # If the local repo doesn't exist, we don't need to do anything
        return

    pre_commit_repo = repos[hook_index]

    if not local_ids:
        raise ValueError("Unable to remove local hooks without specifying the hook id(s) to remove.")

    for local_id in local_ids:
        try:
            hook_id_index = find_hook_id_index(pre_commit_repo, local_id)
        except ValueError:
            # If the local hook doesn't exist, we don't need to do anything
            continue

        hooks = cast(List[Dict[str, Any]], pre_commit_repo.get("hooks", []))
        hooks.pop(hook_id_index)

        if len(hooks) == 0:
            repos.pop(hook_index)
        else:
            pre_commit_repo["hooks"] = hooks
            repos[hook_index] = pre_commit_repo


def remove_hooks(
    pre_commit_config: Dict[str, Any], repo_urls: List[str], local_ids: Optional[List[str]] = None
) -> None:
    """Remove hooks from the .pre-commit-config.yaml file."""
    repos = cast(List[Dict[str, Any]], pre_commit_config.get("repos", []))

    for repo_url in repo_urls:
        if repo_url == "local":
            _remove_local_hook(
                pre_commit_config=pre_commit_config, repos=repos, repo_url=repo_url, local_ids=local_ids
            )
        else:
            try:
                hook_index = find_repo_index(pre_commit_config, repo_url)
            except ValueError:
                # If the repo doesn't exist, we don't need to do anything
                continue

            repos.pop(hook_index)

    pre_commit_config["repos"] = repos


def deep_update(source: dict, updates: dict):
    """Recursively update a dictionary."""
    for key, value in updates.items():
        if isinstance(value, dict):
            source[key] = deep_update(source.get(key, {}), value)
        elif isinstance(value, list):
            existing_list = source.get(key, [])
            if not isinstance(existing_list, list):
                existing_list = []
            for item in value:
                if item not in existing_list:
                    existing_list.append(item)
            source[key] = existing_list
        else:
            source[key] = value
    return source


def update_hook(
    pre_commit_config: CommentedMap,
    repo_url: str,
    repo_default: Dict[str, Any],
    hooks: List[Tuple[str, Dict[str, Any]]],
):
    """Update a hook in the .pre-commit-config.yaml file."""
    try:
        existing_repo_index = find_repo_index(pre_commit_config, repo_url)
    except ValueError:
        existing_repo_index = None

    repos = cast(List[Dict[str, Any]], pre_commit_config.get("repos", []))
    if existing_repo_index is None:
        repos.append(deepcopy(repo_default))
        pre_commit_config["repos"] = repos
    else:
        existing_repo = repos[existing_repo_index]
        for hook_id, hook_default in hooks:
            try:
                index = find_hook_id_index(existing_repo, hook_id)
                existing_hook = existing_repo["hooks"][index]
                existing_hook = deep_update(existing_hook, deepcopy(hook_default))
                existing_repo["hooks"][index] = existing_hook
            except ValueError:
                existing_hooks = cast(List[Dict[str, Any]], existing_repo.get("hooks", []))
                existing_hooks.append(deepcopy(hook_default))
                existing_repo["hooks"] = existing_hooks
    pre_commit_config["repos"] = repos
