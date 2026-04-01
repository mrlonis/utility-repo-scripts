"""Integration tests for setup_python_app.sh using PATH-based command shims."""

import os
import stat
import subprocess
import textwrap
from pathlib import Path
from typing import Collection, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
SETUP_PYTHON_APP_SCRIPT = REPO_ROOT / "setup_python_app.sh"
CALLS_FILE_ENV = "SETUP_PYTHON_APP_TEST_CALLS_FILE"
BIN_DIR_ENV = "SETUP_PYTHON_APP_TEST_BIN_DIR"
CODE_EXTENSIONS_ENV = "SETUP_PYTHON_APP_TEST_CODE_EXTENSIONS"


def write_executable(path: Path, contents: str) -> None:
    """Write an executable shell script to disk."""
    path.write_text(textwrap.dedent(contents), encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def write_fake_tools(bin_dir: Path, unavailable: Collection[str] = ()) -> None:
    """Create fake executables used to isolate setup_python_app.sh from external tools."""
    unavailable_tools = set(unavailable)

    if "python" not in unavailable_tools:
        write_executable(
            bin_dir / "python",
            """\
            #!/bin/bash
            set -eu
            printf '%s\\n' "python $*" >> "$SETUP_PYTHON_APP_TEST_CALLS_FILE"
            if [ "${1:-}" = "-m" ] && [ "${2:-}" = "pip" ]; then
                exit 0
            fi

            if [ "${1:-}" = "-c" ]; then
                case "${2:-}" in
                *"importlib.util.find_spec"*)
                    printf 'present:/fake/site-packages/%s.py\\n' "${3:-package}"
                    exit 0
                    ;;
                *"metadata.distribution"*)
                    printf 'present\\n'
                    exit 0
                    ;;
                esac

                echo "unexpected python -c invocation: $*" >&2
                exit 1
            fi

            script_name="$(basename -- "${1:-}")"
            case "$script_name" in
            setup_prettierrc.py)
                printf '{"semi": true}\\n' > .prettierrc
                ;;
            setup_pre_commit_config.py)
                printf 'repos: []\\n' > .pre-commit-config.yaml
                ;;
            setup_pyproject_toml.py)
                if [ ! -f pyproject.toml ]; then
                    printf '[tool.poetry]\\nname = "sample-project"\\nversion = "0.1.0"\\n' > pyproject.toml
                fi
                ;;
            setup_pylintrc.py)
                printf '[MASTER]\\n' > .pylintrc
                ;;
            setup_flake8.py)
                printf '[flake8]\\n' > .flake8
                ;;
            setup_fix_prettier_pre_commit.py)
                if [ ! -f .pre-commit-config.yaml ]; then
                    printf 'repos: []\\n' > .pre-commit-config.yaml
                fi
                printf '# prettier hook fixed\\n' >> .pre-commit-config.yaml
                ;;
            setup_vscode_settings.py)
                mkdir -p .vscode
                printf '{"python.testing.pytestEnabled": true}\\n' > .vscode/settings.json
                ;;
            *)
                echo "unexpected python invocation: $*" >&2
                exit 1
                ;;
            esac
            """,
        )

    if "pyenv" not in unavailable_tools:
        write_executable(
            bin_dir / "pyenv",
            """\
            #!/bin/bash
            set -eu
            printf '%s\\n' "pyenv $*" >> "$SETUP_PYTHON_APP_TEST_CALLS_FILE"
            subcommand="${1:-}"
            case "$subcommand" in
            init)
                printf 'export PYENV_SHELL=bash\\n'
                ;;
            install | virtualenv-delete | virtualenv | local | shell | activate)
                exit 0
                ;;
            which)
                printf '%s/.fake-pyenv/versions/%s/bin/python\\n' "$PWD" "$(basename "$PWD")"
                ;;
            *)
                echo "unexpected pyenv invocation: $*" >&2
                exit 1
                ;;
            esac
            """,
        )

    for command_name in ["pip", "pip-sync", "poetry", "pre-commit", "prettier", "sort-json"]:
        if command_name in unavailable_tools:
            continue

        write_executable(
            bin_dir / command_name,
            f"""\
            #!/bin/bash
            set -eu
            printf '%s\\n' "{command_name} $*" >> "$SETUP_PYTHON_APP_TEST_CALLS_FILE"
            exit 0
            """,
        )

    if "code" not in unavailable_tools:
        write_executable(
            bin_dir / "code",
            """\
            #!/bin/bash
            set -eu
            printf '%s\\n' "code $*" >> "$SETUP_PYTHON_APP_TEST_CALLS_FILE"
            if [ "${1:-}" = "--list-extensions" ]; then
                printf '%s' "${SETUP_PYTHON_APP_TEST_CODE_EXTENSIONS:-}"
            fi
            exit 0
            """,
        )

    if "npm" not in unavailable_tools:
        write_executable(
            bin_dir / "npm",
            """#!/bin/bash
set -eu
printf '%s\\n' "npm $*" >> "$SETUP_PYTHON_APP_TEST_CALLS_FILE"

if [ "${1:-}" = "install" ] && [ "${2:-}" = "-g" ] && [ "${3:-}" = "prettier" ]; then
    target="$SETUP_PYTHON_APP_TEST_BIN_DIR/prettier"
    cat > "$target" <<'EOF'
#!/bin/bash
set -eu
printf '%s\\n' "prettier $*" >> "$SETUP_PYTHON_APP_TEST_CALLS_FILE"
exit 0
EOF
    chmod +x "$target"
    exit 0
fi

if [ "${1:-}" = "install" ] && [ "${2:-}" = "-g" ] && [ "${3:-}" = "sort-json" ]; then
    target="$SETUP_PYTHON_APP_TEST_BIN_DIR/sort-json"
    cat > "$target" <<'EOF'
#!/bin/bash
set -eu
printf '%s\\n' "sort-json $*" >> "$SETUP_PYTHON_APP_TEST_CALLS_FILE"
exit 0
EOF
    chmod +x "$target"
    exit 0
fi

exit 0
""",
        )


def run_setup_python_app(
    project_dir: Path,
    tmp_path: Path,
    args: Sequence[str] = (),
    unavailable_tools: Collection[str] = (),
    code_extensions: str = "",
) -> Tuple[subprocess.CompletedProcess[str], str, Path]:
    """Run setup_python_app.sh with isolated fake tools and return command logs."""
    home_dir = tmp_path / "home"
    home_dir.mkdir()
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    calls_file = tmp_path / "calls.log"
    write_fake_tools(bin_dir=bin_dir, unavailable=unavailable_tools)

    env = os.environ.copy()
    env["HOME"] = str(home_dir)
    env["PATH"] = f"{bin_dir}:/usr/bin:/bin"
    env["SHELL"] = "/bin/bash"
    env[CALLS_FILE_ENV] = str(calls_file)
    env[BIN_DIR_ENV] = str(bin_dir)
    env[CODE_EXTENSIONS_ENV] = code_extensions

    result = subprocess.run(
        ["bash", "--noprofile", "--norc", str(SETUP_PYTHON_APP_SCRIPT), *args],
        cwd=project_dir,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    calls = calls_file.read_text(encoding="utf-8") if calls_file.exists() else ""
    return result, calls, home_dir


def test_setup_python_app_rejects_invalid_package_manager(tmp_path: Path) -> None:
    """Invalid package_manager values should fail during argument validation."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()

    env = os.environ.copy()
    env["PATH"] = "/usr/bin:/bin"
    env["HOME"] = str(tmp_path / "home")
    env["SHELL"] = "/bin/bash"

    result = subprocess.run(
        [
            "bash",
            "--noprofile",
            "--norc",
            str(SETUP_PYTHON_APP_SCRIPT),
            "--package_manager=invalid",
        ],
        cwd=project_dir,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 2
    assert "Invalid package_manager option: (invalid)" in result.stderr


def test_setup_python_app_requires_pyenv_when_missing(tmp_path: Path) -> None:
    """The script should stop with a clear message when pyenv is unavailable."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()
    (project_dir / "pyproject.toml").write_text(
        '[tool.poetry]\nname = "sample-project"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )

    result, calls, _home_dir = run_setup_python_app(
        project_dir=project_dir,
        tmp_path=tmp_path,
        unavailable_tools={"pyenv"},
    )

    assert result.returncode == 1
    assert "pyenv not installed!" in result.stdout
    assert "Please install pyenv to use this setup script." in result.stdout
    assert calls == ""


def test_setup_python_app_poetry_happy_path_uses_mocked_tools(tmp_path: Path) -> None:
    """The poetry flow should complete while calling only fake external tools."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()
    (project_dir / "pyproject.toml").write_text(
        '[tool.poetry]\nname = "sample-project"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )
    vscode_dir = project_dir / ".vscode"
    vscode_dir.mkdir()
    (vscode_dir / "launch.sample.json").write_text('{"version":"sample"}\n', encoding="utf-8")

    result, calls, home_dir = run_setup_python_app(
        project_dir=project_dir,
        tmp_path=tmp_path,
        args=["--package_manager=poetry", "--pre_commit_autoupdate=1", "--python_formatter=black"],
    )

    assert result.returncode == 0
    assert "Project setup complete" in result.stdout
    assert (project_dir / ".prettierrc").exists()
    assert (project_dir / ".pre-commit-config.yaml").exists()
    assert (project_dir / ".pylintrc").exists()
    assert (project_dir / ".flake8").exists()
    assert (project_dir / ".vscode" / "settings.json").exists()
    assert (project_dir / ".vscode" / "launch.json").read_text(encoding="utf-8") == '{"version":"sample"}\n'
    custom_script = home_dir / ".python_after_setup.sh"
    assert custom_script.exists()
    assert os.access(custom_script, os.X_OK)

    assert "pyenv install -s 3.13.9" in calls
    assert "pyenv virtualenv -f 3.13.9 sample-project" in calls
    assert "pyenv virtualenv-delete -f sample-project" not in calls
    assert "poetry env remove --all" in calls
    assert "poetry sync" in calls
    assert "poetry show -o" in calls
    assert "python " in calls
    assert "setup_prettierrc.py" in calls
    assert "setup_pre_commit_config.py" in calls
    assert "setup_pyproject_toml.py" in calls
    assert "setup_pylintrc.py" in calls
    assert "setup_flake8.py" in calls
    assert "setup_fix_prettier_pre_commit.py" in calls
    assert "setup_vscode_settings.py" in calls
    assert "pre-commit install" in calls
    assert "pre-commit autoupdate" in calls
    assert "code --install-extension ms-python.black-formatter --force" in calls


def test_setup_python_app_pip_flow_rebuilds_virtualenv_and_installs_requirements(tmp_path: Path) -> None:
    """The pip flow should rebuild the virtualenv and install requirements-dev.txt."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()
    (project_dir / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")

    result, calls, _home_dir = run_setup_python_app(
        project_dir=project_dir,
        tmp_path=tmp_path,
        args=["--package_manager=pip"],
        code_extensions="ms-python.python\n",
    )

    assert result.returncode == 0
    assert "Project setup complete" in result.stdout
    assert "pyenv virtualenv-delete -f sample-project" in calls
    assert "python -m pip install --upgrade pip" in calls
    assert "pip install --upgrade setuptools" in calls
    assert "pip install wheel" in calls
    assert "pip install -r requirements-dev.txt" in calls
    assert "poetry sync" not in calls


def test_setup_python_app_can_mock_npm_fallback_for_formatting_tools(tmp_path: Path) -> None:
    """Missing prettier and sort-json commands should fall back to fake npm installs."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()
    (project_dir / "pyproject.toml").write_text(
        '[tool.poetry]\nname = "sample-project"\nversion = "0.1.0"\n',
        encoding="utf-8",
    )

    result, calls, _home_dir = run_setup_python_app(
        project_dir=project_dir,
        tmp_path=tmp_path,
        args=["--package_manager=poetry"],
        unavailable_tools={"prettier", "sort-json"},
    )

    assert result.returncode == 0
    assert "npm install -g prettier" in calls
    assert "npm install -g sort-json" in calls
    assert "prettier .prettierrc --write --ignore-path .prettierignore" in calls
    assert "sort-json .vscode/settings.json" in calls
