"""Integration tests for the ensure_venv.sh helper."""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ENSURE_VENV_SCRIPT = REPO_ROOT / "ensure_venv.sh"
VENV_MARKER = "__VIRTUAL_ENV__="


def run_ensure_venv(project_dir: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    """Run ensure_venv.sh and print the active virtual environment."""
    execution_env = env.copy()
    execution_env["PWD"] = str(project_dir)

    return subprocess.run(
        [
            "bash",
            str(ENSURE_VENV_SCRIPT),
            "bash",
            "--noprofile",
            "--norc",
            "-c",
            f'printf "{VENV_MARKER}%s" "${{VIRTUAL_ENV:-}}"',
        ],
        cwd=project_dir,
        env=execution_env,
        text=True,
        capture_output=True,
        check=False,
    )


def write_activate_script(venv_dir: Path) -> None:
    """Create a minimal activate script that exports VIRTUAL_ENV."""
    activate_path = venv_dir / "bin" / "activate"
    activate_path.parent.mkdir(parents=True)
    activate_path.write_text(f'export VIRTUAL_ENV="{venv_dir}"\n', encoding="utf-8")


def extract_virtual_env(stdout: str) -> str:
    """Extract the VIRTUAL_ENV value from the marker output."""
    assert VENV_MARKER in stdout
    return stdout.split(VENV_MARKER, maxsplit=1)[1]


def test_ensure_venv_preserves_existing_virtual_env(tmp_path: Path) -> None:
    """An active virtual environment should not be replaced."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()

    env = os.environ.copy()
    env["VIRTUAL_ENV"] = "/already/active"
    env.pop("WORKON_HOME", None)
    env.pop("PYENV_ROOT", None)

    result = run_ensure_venv(project_dir=project_dir, env=env)

    assert result.returncode == 0
    assert extract_virtual_env(result.stdout) == "/already/active"
    assert result.stderr == ""


def test_ensure_venv_activates_local_project_venv_first(tmp_path: Path) -> None:
    """The helper should activate the in-repo .venv created by setup_python_app.sh."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()

    venv_dir = project_dir / ".venv"
    write_activate_script(venv_dir)

    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    env.pop("WORKON_HOME", None)
    env.pop("PYENV_ROOT", None)

    result = run_ensure_venv(project_dir=project_dir, env=env)

    assert result.returncode == 0
    assert extract_virtual_env(result.stdout) == str(venv_dir)
    assert result.stderr == ""


def test_ensure_venv_prefers_local_project_venv_over_workon_home(tmp_path: Path) -> None:
    """A project-local .venv should win even when WORKON_HOME is configured."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()

    local_venv_dir = project_dir / ".venv"
    write_activate_script(local_venv_dir)

    workon_home = tmp_path / "workon-home"
    workon_venv_dir = workon_home / project_dir.name
    write_activate_script(workon_venv_dir)

    env = os.environ.copy()
    env["WORKON_HOME"] = str(workon_home)
    env.pop("VIRTUAL_ENV", None)
    env.pop("PYENV_ROOT", None)

    result = run_ensure_venv(project_dir=project_dir, env=env)

    assert result.returncode == 0
    assert extract_virtual_env(result.stdout) == str(local_venv_dir)
    assert result.stderr == ""


def test_ensure_venv_uses_workon_home_when_local_project_venv_is_missing(tmp_path: Path) -> None:
    """WORKON_HOME should be the next fallback when a local .venv is unavailable."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()

    workon_home = tmp_path / "workon-home"
    venv_dir = workon_home / project_dir.name
    write_activate_script(venv_dir)

    env = os.environ.copy()
    env["WORKON_HOME"] = str(workon_home)
    env.pop("VIRTUAL_ENV", None)
    env.pop("PYENV_ROOT", None)

    result = run_ensure_venv(project_dir=project_dir, env=env)

    assert result.returncode == 0
    assert extract_virtual_env(result.stdout) == str(venv_dir)
    assert result.stderr == ""


def test_ensure_venv_falls_back_to_pyenv_when_workon_home_cannot_activate(tmp_path: Path) -> None:
    """A non-activatable WORKON_HOME candidate should fall back to the pyenv location."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()

    workon_home = tmp_path / "workon-home"
    (workon_home / project_dir.name).mkdir(parents=True)

    home_dir = tmp_path / "home"
    pyenv_venv_dir = home_dir / ".pyenv" / "versions" / project_dir.name
    write_activate_script(pyenv_venv_dir)

    env = os.environ.copy()
    env["HOME"] = str(home_dir)
    env["WORKON_HOME"] = str(workon_home)
    env.pop("VIRTUAL_ENV", None)
    env.pop("PYENV_ROOT", None)

    result = run_ensure_venv(project_dir=project_dir, env=env)

    assert result.returncode == 0
    assert extract_virtual_env(result.stdout) == str(pyenv_venv_dir)
    assert result.stderr == ""


def test_ensure_venv_warns_and_runs_command_when_virtual_env_is_missing(tmp_path: Path) -> None:
    """Missing fallback environments should warn without blocking the command."""
    project_dir = tmp_path / "sample-project"
    project_dir.mkdir()

    home_dir = tmp_path / "home"

    env = os.environ.copy()
    env["HOME"] = str(home_dir)
    env.pop("VIRTUAL_ENV", None)
    env.pop("WORKON_HOME", None)
    env.pop("PYENV_ROOT", None)

    result = run_ensure_venv(project_dir=project_dir, env=env)

    assert result.returncode == 0
    assert "none of the candidate virtual environments exist or can be activated" in result.stderr
    assert extract_virtual_env(result.stdout) == ""
