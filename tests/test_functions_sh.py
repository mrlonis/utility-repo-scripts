"""Integration tests for shell helpers in scripts/functions.sh."""

import subprocess
from pathlib import Path
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS_SCRIPT = REPO_ROOT / "scripts" / "functions.sh"
TEST_EXTENSION = "ms-python.python"


def run_install_extension_helper(
    tmp_path: Path, installed_extensions: str, extension_name: str = TEST_EXTENSION
) -> Tuple[subprocess.CompletedProcess[str], str]:
    """Run the VS Code extension helper and capture attempted installs."""
    calls_file = tmp_path / "code_calls.txt"
    normalized_functions_script = write_normalized_functions_script(tmp_path)
    command = f"""
source "{normalized_functions_script}"
code() {{
\tprintf '%s\\n' "$*" >> "{calls_file}"
}}
install_vscode_Extension_if_not_installed "{extension_name}" "{installed_extensions}"
"""

    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-c", command],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    calls = calls_file.read_text(encoding="utf-8") if calls_file.exists() else ""
    return result, calls


def write_normalized_functions_script(tmp_path: Path) -> Path:
    """Write an LF-normalized copy of scripts/functions.sh for shell tests."""
    normalized_functions_script = tmp_path / "functions.sh"
    normalized_functions_script.write_text(
        FUNCTIONS_SCRIPT.read_text(encoding="utf-8").replace("\r\n", "\n"),
        encoding="utf-8",
    )
    return normalized_functions_script


def run_ensure_vscode_launch_file(
    tmp_path: Path, sample_exists: bool, launch_exists: bool, overwrite_launch: int
) -> Tuple[subprocess.CompletedProcess[str], str]:
    """Run the VS Code launch helper and return the resulting launch file content."""
    sample_launch_path = tmp_path / "launch.sample.json"
    launch_path = tmp_path / "launch.json"

    if sample_exists:
        sample_launch_path.write_text('{"version":"sample"}\n', encoding="utf-8")

    if launch_exists:
        launch_path.write_text('{"version":"existing"}\n', encoding="utf-8")

    normalized_functions_script = write_normalized_functions_script(tmp_path)
    command = f"""
source "{normalized_functions_script}"
ensure_vscode_launch_file "{sample_launch_path}" "{launch_path}" "{overwrite_launch}" 0
"""

    result = subprocess.run(
        ["bash", "--noprofile", "--norc", "-c", command],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    launch_contents = launch_path.read_text(encoding="utf-8") if launch_path.exists() else ""
    return result, launch_contents


def test_install_vscode_extension_helper_skips_existing_extension(tmp_path: Path) -> None:
    """Existing extensions should not be reinstalled."""
    installed_extensions = "\n".join(["bungcip.better-toml", TEST_EXTENSION, "ms-python.flake8"])

    result, calls = run_install_extension_helper(tmp_path=tmp_path, installed_extensions=installed_extensions)

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert calls == ""


def test_install_vscode_extension_helper_installs_missing_extension(tmp_path: Path) -> None:
    """Missing extensions should trigger a VS Code install command."""
    installed_extensions = "\n".join(["bungcip.better-toml", "ms-python.flake8"])

    result, calls = run_install_extension_helper(tmp_path=tmp_path, installed_extensions=installed_extensions)

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert calls == f"--install-extension {TEST_EXTENSION} --force\n"


def test_install_vscode_extension_helper_skips_dash_prefixed_existing_extension(tmp_path: Path) -> None:
    """Dash-prefixed extension names should be treated as literal patterns."""
    extension_name = "-custom.extension"
    installed_extensions = "\n".join(["bungcip.better-toml", extension_name, "ms-python.flake8"])

    result, calls = run_install_extension_helper(
        tmp_path=tmp_path,
        installed_extensions=installed_extensions,
        extension_name=extension_name,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert calls == ""


def test_ensure_vscode_launch_file_creates_missing_launch_without_overwrite_flag(tmp_path: Path) -> None:
    """A missing launch.json should be created from the sample by default."""
    result, launch_contents = run_ensure_vscode_launch_file(
        tmp_path=tmp_path,
        sample_exists=True,
        launch_exists=False,
        overwrite_launch=0,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert launch_contents == '{"version":"sample"}\n'


def test_ensure_vscode_launch_file_overwrites_existing_launch_when_requested(tmp_path: Path) -> None:
    """The overwrite flag should replace an existing launch.json from the sample."""
    result, launch_contents = run_ensure_vscode_launch_file(
        tmp_path=tmp_path,
        sample_exists=True,
        launch_exists=True,
        overwrite_launch=1,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert launch_contents == '{"version":"sample"}\n'
