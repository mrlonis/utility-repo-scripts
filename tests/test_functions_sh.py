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
    normalized_functions_script = tmp_path / "functions.sh"
    normalized_functions_script.write_text(
        FUNCTIONS_SCRIPT.read_text(encoding="utf-8").replace("\r\n", "\n"),
        encoding="utf-8",
    )
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
