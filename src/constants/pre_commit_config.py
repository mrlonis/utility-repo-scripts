""".pre-commit-config.yaml file constants."""

# region .pre-commit-config.yaml Constants
from src.constants.pylintrc import PYLINTRC_FILENAME
from src.constants.pyproject_toml import PYPROJECT_TOML_FILENAME

PRE_COMMIT_CONFIG_FILENAME = ".pre-commit-config.yaml"

PRE_COMMIT_REPO_URL = "https://github.com/pre-commit/pre-commit-hooks"
PRE_COMMIT_REV = "v4.4.0"
CHECK_YAML_HOOK_ID = "check-yaml"
CHECK_YAML_HOOK = {"id": CHECK_YAML_HOOK_ID}
END_OF_FILE_FIXER_HOOK_ID = "end-of-file-fixer"
END_OF_FILE_FIXER_HOOK = {"id": END_OF_FILE_FIXER_HOOK_ID}
TRAILING_WHITESPACE_HOOK_ID = "trailing-whitespace"
TRAILING_WHITESPACE_HOOK = {"id": TRAILING_WHITESPACE_HOOK_ID}
PRE_COMMIT_REPO = {
    "repo": PRE_COMMIT_REPO_URL,
    "rev": PRE_COMMIT_REV,
    "hooks": [CHECK_YAML_HOOK, END_OF_FILE_FIXER_HOOK, TRAILING_WHITESPACE_HOOK],
}

JUMANJI_HOUSE_REPO_URL = "https://github.com/jumanjihouse/pre-commit-hooks"
JUMANJI_HOUSE_REV = "3.0.0"
GIT_CHECK_HOOK_ID = "git-check"
GIT_CHECK_HOOK = {"id": GIT_CHECK_HOOK_ID}
GIT_DIRTY_HOOK_ID = "git-dirty"
GIT_DIRTY_HOOK = {"id": GIT_DIRTY_HOOK_ID}
MARKDOWN_LINT_HOOK_ID = "markdownlint"
MARKDOWN_LINT_HOOK = {"id": MARKDOWN_LINT_HOOK_ID}
SHELLCHECK_HOOK_ID = "shellcheck"
SHELLCHECK_HOOK = {"id": SHELLCHECK_HOOK_ID}
SHELL_FORMAT_HOOK_ID = "shfmt"
SHELL_FORMAT_HOOK = {"id": SHELL_FORMAT_HOOK_ID}
JUMANJI_HOUSE_REPO = {
    "repo": JUMANJI_HOUSE_REPO_URL,
    "rev": JUMANJI_HOUSE_REV,
    "hooks": [GIT_CHECK_HOOK, GIT_DIRTY_HOOK, MARKDOWN_LINT_HOOK, SHELLCHECK_HOOK, SHELL_FORMAT_HOOK],
}

PRETTIER_REPO_URL = "https://github.com/pre-commit/mirrors-prettier"
PRETTIER_HOOK_ID = "prettier"
PRETTIER_HOOK = {"id": PRETTIER_HOOK_ID, "args": ["--write", "--config=.prettierrc"]}
PRETTIER_REPO = {"repo": PRETTIER_REPO_URL, "rev": "v3.1.0", "hooks": [PRETTIER_HOOK]}

ISORT_REPO_URL = "https://github.com/pycqa/isort"
ISORT_HOOK_ID = "isort"
ISORT_HOOK = {
    "id": ISORT_HOOK_ID,
    "name": "isort (python)",
    "args": [f"--settings-file={PYPROJECT_TOML_FILENAME}"],
}
ISORT_REPO = {"repo": ISORT_REPO_URL, "rev": "5.12.0", "hooks": [ISORT_HOOK]}

AUTOPEP8_REPO_URL = "https://github.com/pre-commit/mirrors-autopep8"
AUTOPEP8_HOOK_ID = "autopep8"
AUTOPEP8_HOOK = {"id": AUTOPEP8_HOOK_ID}
AUTOPEP8_REPO = {"repo": AUTOPEP8_REPO_URL, "rev": "v2.0.1", "hooks": [AUTOPEP8_HOOK]}

BLACK_REPO_URL = "https://github.com/psf/black"
BLACK_HOOK_ID = "black"
BLACK_HOOK = {"id": BLACK_HOOK_ID}
BLACK_REPO = {"repo": BLACK_REPO_URL, "rev": "23.1.0", "hooks": [BLACK_HOOK]}

LOCAL_REPO_URL = "local"
PYLINT_HOOK_ID = "pylint"
PYLINT_HOOK = {
    "id": PYLINT_HOOK_ID,
    "name": "pylint",
    "entry": "ensure_venv.sh",
    "language": "script",
    "types": ["python"],
    "args": ["pylint", "-v", f"--rcfile={PYLINTRC_FILENAME}"],
}
LOCAL_REPO = {"repo": LOCAL_REPO_URL, "hooks": [PYLINT_HOOK]}

FLAKE8_REPO_URL = "https://github.com/pycqa/flake8"
FLAKE8_HOOK_ID = "flake8"
FLAKE8_HOOK = {"id": FLAKE8_HOOK_ID, "args": ["--config=.flake8"]}
FLAKE8_REPO = {"repo": FLAKE8_REPO_URL, "rev": "6.0.0", "hooks": [FLAKE8_HOOK]}

SAMPLE_PRE_COMMIT_CONFIG = f"""
repos:
  - repo: {PRE_COMMIT_REPO_URL}
    rev: {PRE_COMMIT_REV}
    hooks:
      - id: {CHECK_YAML_HOOK_ID}
      - id: {END_OF_FILE_FIXER_HOOK_ID}
      - id: {TRAILING_WHITESPACE_HOOK_ID}
  - repo: {JUMANJI_HOUSE_REPO_URL}
    rev: {JUMANJI_HOUSE_REV}
    hooks:
      - id: {GIT_CHECK_HOOK_ID} # Configure in .gitattributes
      - id: {GIT_DIRTY_HOOK_ID} # Configure in .gitignore
      - id: {MARKDOWN_LINT_HOOK_ID} # Configure in .mdlrc
      - id: {SHELLCHECK_HOOK_ID}
      - id: {SHELL_FORMAT_HOOK_ID}
  - repo: {PRETTIER_REPO_URL}
    rev: v3.0.0-alpha.4
    hooks:
      - id: {PRETTIER_HOOK_ID}
        args: [--write, --config=.prettierrc]
  - repo: {ISORT_REPO_URL}
    rev: 5.12.0
    hooks:
      - id: {ISORT_HOOK_ID}
        name: isort (python)
        args: [--settings-file={PYPROJECT_TOML_FILENAME}]
  - repo: {AUTOPEP8_REPO_URL}
    rev: v2.0.1
    hooks:
      - id: {AUTOPEP8_HOOK_ID} # Configure in {PYPROJECT_TOML_FILENAME}
  - repo: {BLACK_REPO_URL}
    rev: 23.1.0
    hooks:
      - id: {BLACK_HOOK_ID} # Configure in {PYPROJECT_TOML_FILENAME}
  - repo: {LOCAL_REPO_URL}
    hooks:
      - id: {PYLINT_HOOK_ID}
        name: pylint
        entry: ensure_venv.sh
        language: script
        types: [python]
        args: [pylint, -v, --rcfile={PYLINTRC_FILENAME}]
  - repo: {FLAKE8_REPO_URL}
    rev: 6.0.0
    hooks:
      - id: {FLAKE8_HOOK_ID}
        args: [--config=.flake8]
"""
# endregion
