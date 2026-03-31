# Copilot Instructions

## Project purpose

This repository provides reusable setup scripts for Python repositories, typically consumed as a git submodule. The main entrypoint is `setup_python_app.sh`, and the convenience wrapper is `./setup`.

The current preferred workflow is Poetry-first. If you make package-management changes, default to Poetry and avoid introducing new package manager support unless the user explicitly asks for it.

## How the repo is structured

- Keep shell scripts as orchestration layers. `setup_python_app.sh` coordinates environment setup, dependency installation, pre-commit setup, and VS Code setup.
- Keep Python logic in the processor modules under `src/`.
- Root-level Python scripts like `setup_pyproject_toml.py` and `setup_pre_commit_config.py` should stay thin CLI wrappers around `src/` logic.
- Tests live under `tests/` and generally mirror the processor modules they cover.

## Preferred change patterns

- Prefer editing the processor in `src/` instead of duplicating logic in a root script.
- Preserve existing user config when updating files. The processors are designed to merge or adjust existing config rather than replace it wholesale.
- When adding or changing CLI options, update all affected layers together:
  - `setup_python_app.sh`
  - the relevant root-level Python wrapper
  - the processor in `src/`
  - tests
  - README if behavior changed
- Keep generated/configured defaults consistent across:
  - `pyproject.toml`
  - `.pre-commit-config.yaml`
  - `.pylintrc`
  - `.flake8`
  - `.vscode/settings.json`

## Poetry and Python expectations

- Prefer `poetry sync`, `poetry install`, `poetry run ...`, and `poetry show -o` workflows.
- Do not add support for new package managers by default.
- Legacy references to `pip` and `pip-tools` may still exist in the codebase and README. Treat those as legacy paths unless the user explicitly asks to maintain or expand them.
- This repo currently targets Python `3.13.9`; keep version changes deliberate and update all related references together.

## Style and implementation notes

- Follow the existing style: small focused functions, explicit names, and minimal hidden behavior.
- Preserve idempotency. Running setup multiple times should converge on the same result without duplicating config entries.
- Respect the existing `test=True` and `debug=True` patterns in processors so logic can be exercised without writing files.
- Keep path handling compatible with submodule usage. `setup_python_app.sh` contains logic for being sourced from another repository; do not break that flow.
- Keep the repo-specific ignore behavior for `utility-repo-scripts` intact unless the user asks to change it.

## Validation

- Preferred full validation command: `./test.sh`
- If running tools individually, use Poetry:
  - `poetry run pylint ...`
  - `poetry run flake8 ...`
  - `poetry run mypy ...`
  - `poetry run pytest --cov -n auto`
- When changing a processor, update or add the corresponding tests under `tests/`.

## When in doubt

- Optimize for safe updates to downstream repositories that consume this repo.
- Prefer backwards-compatible changes to CLI flags and generated file structure.
- If behavior and docs disagree, align the code, tests, and README together instead of fixing only one place.
