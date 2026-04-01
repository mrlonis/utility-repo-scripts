"""Integration tests for shell helpers in scripts/functions.sh."""

import subprocess
from pathlib import Path
from typing import Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS_SCRIPT = REPO_ROOT / "scripts" / "functions.sh"
TEST_EXTENSION = "ms-python.python"
STATE_MARKER = "state="
STATUS_MARKER = "find_status="


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


def run_find_site_package_flow(
    tmp_path: Path,
    package_probe_result: str,
    debug_enabled: int = 0,
    pip_install_status: int = 0,
) -> Tuple[subprocess.CompletedProcess[str], str]:
    """Run the find/uninstall helper flow and capture pip invocations."""
    calls_file = tmp_path / "pip_calls.txt"
    normalized_functions_script = write_normalized_functions_script(tmp_path)
    command = f"""
source "{normalized_functions_script}"
debug={debug_enabled}
python() {{
\tcase "{package_probe_result}" in
\tpresent)
\t\tprintf 'present:/tmp/fake_package.py\\n'
\t\treturn 0
\t\t;;
\tmissing)
\t\tprintf 'missing\\n'
\t\treturn 0
\t\t;;
\terror)
\t\techo 'unexpected package probe error' >&2
\t\treturn 1
\t\t;;
\tesac
\treturn 1
}}
pip() {{
\tprintf '%s\\n' "$*" >> "{calls_file}"
\tif [ "$1" = "install" ]; then
\t\treturn {pip_install_status}
\tfi
\treturn 0
}}
state="$(find_site_package fake_package fake-package)"
find_status=$?
printf '{STATE_MARKER}%s\\n' "$state"
printf '{STATUS_MARKER}%s\\n' "$find_status"
if [ "$find_status" -eq 0 ]; then
\tuninstall_site_package fake-package "$state"
fi
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


def run_find_site_distribution_flow(
    tmp_path: Path, distribution_probe_result: str, debug_enabled: int = 0
) -> subprocess.CompletedProcess[str]:
    """Run the distribution-state helper and capture its markers."""
    normalized_functions_script = write_normalized_functions_script(tmp_path)
    command = f"""
source "{normalized_functions_script}"
debug={debug_enabled}
python() {{
\tcase "{distribution_probe_result}" in
\tpresent)
\t\tprintf 'present\\n'
\t\treturn 0
\t\t;;
\tmissing)
\t\tprintf 'missing\\n'
\t\treturn 0
\t\t;;
\terror)
\t\techo 'unexpected distribution probe error' >&2
\t\treturn 1
\t\t;;
\tesac
\treturn 1
}}
state="$(find_site_distribution fake-distribution)"
find_status=$?
printf '{STATE_MARKER}%s\\n' "$state"
printf '{STATUS_MARKER}%s\\n' "$find_status"
"""

    return subprocess.run(
        ["bash", "--noprofile", "--norc", "-c", command],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def extract_marker_value(stdout: str, marker: str) -> str:
    """Extract a single marker value from captured stdout."""
    for line in stdout.splitlines():
        if line.startswith(marker):
            return line[len(marker) :]  # noqa: E203
    raise AssertionError(f"Missing marker {marker!r} in stdout: {stdout!r}")


def test_install_vscode_extension_helper_skips_existing_extension(tmp_path: Path) -> None:
    """Existing extensions should not be reinstalled."""
    installed_extensions = "\n".join(["bungcip.better-toml", TEST_EXTENSION, "ms-python.flake8"])

    result, calls = run_install_extension_helper(tmp_path=tmp_path, installed_extensions=installed_extensions)

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert calls == ""


def test_find_site_package_returns_existing_state_without_installing(tmp_path: Path) -> None:
    """Existing packages should report state=1 and skip install/uninstall calls."""
    result, calls = run_find_site_package_flow(tmp_path=tmp_path, package_probe_result="present")

    assert result.returncode == 0
    assert extract_marker_value(result.stdout, STATE_MARKER) == "1"
    assert extract_marker_value(result.stdout, STATUS_MARKER) == "0"
    assert result.stderr == ""
    assert calls == ""


def test_find_site_package_reports_temporary_install_and_uninstalls_afterward(tmp_path: Path) -> None:
    """Missing packages should report state=0 and uninstall after temporary install."""
    result, calls = run_find_site_package_flow(tmp_path=tmp_path, package_probe_result="missing")

    assert result.returncode == 0
    assert extract_marker_value(result.stdout, STATE_MARKER) == "0"
    assert extract_marker_value(result.stdout, STATUS_MARKER) == "0"
    assert "Uninstalling fake-package" in result.stdout
    assert result.stderr == ""
    assert calls == "install fake-package\nuninstall -y fake-package\n"


def test_find_site_package_debug_logs_do_not_pollute_captured_state(tmp_path: Path) -> None:
    """Debug logging should go to stderr so command substitution captures only the state value."""
    result, calls = run_find_site_package_flow(tmp_path=tmp_path, package_probe_result="present", debug_enabled=1)

    assert result.returncode == 0
    assert extract_marker_value(result.stdout, STATE_MARKER) == "1"
    assert extract_marker_value(result.stdout, STATUS_MARKER) == "0"
    assert "find_site_package(): fake-package found" in result.stderr
    assert calls == ""


def test_find_site_package_propagates_install_failure(tmp_path: Path) -> None:
    """A temporary install failure should surface as a nonzero helper status."""
    result, calls = run_find_site_package_flow(
        tmp_path=tmp_path,
        package_probe_result="missing",
        pip_install_status=1,
    )

    assert result.returncode == 0
    assert extract_marker_value(result.stdout, STATE_MARKER) == ""
    assert extract_marker_value(result.stdout, STATUS_MARKER) == "1"
    assert calls == "install fake-package\n"


def test_find_site_package_propagates_unexpected_probe_errors(tmp_path: Path) -> None:
    """Unexpected probe errors should not be treated as missing packages."""
    result, calls = run_find_site_package_flow(tmp_path=tmp_path, package_probe_result="error")

    assert result.returncode == 0
    assert extract_marker_value(result.stdout, STATE_MARKER) == ""
    assert extract_marker_value(result.stdout, STATUS_MARKER) == "1"
    assert "unexpected package probe error" in result.stderr
    assert calls == ""


def test_find_site_distribution_reports_existing_state(tmp_path: Path) -> None:
    """Existing distributions should report state=1."""
    result = run_find_site_distribution_flow(tmp_path=tmp_path, distribution_probe_result="present")

    assert result.returncode == 0
    assert extract_marker_value(result.stdout, STATE_MARKER) == "1"
    assert extract_marker_value(result.stdout, STATUS_MARKER) == "0"
    assert result.stderr == ""


def test_find_site_distribution_reports_missing_state(tmp_path: Path) -> None:
    """Missing distributions should report state=0."""
    result = run_find_site_distribution_flow(tmp_path=tmp_path, distribution_probe_result="missing")

    assert result.returncode == 0
    assert extract_marker_value(result.stdout, STATE_MARKER) == "0"
    assert extract_marker_value(result.stdout, STATUS_MARKER) == "0"
    assert result.stderr == ""


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


def test_ensure_vscode_launch_file_is_noop_when_sample_is_missing(tmp_path: Path) -> None:
    """A missing launch sample should leave launch.json untouched."""
    result, launch_contents = run_ensure_vscode_launch_file(
        tmp_path=tmp_path,
        sample_exists=False,
        launch_exists=False,
        overwrite_launch=0,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert launch_contents == ""


def test_ensure_vscode_launch_file_preserves_existing_launch_without_overwrite_flag(tmp_path: Path) -> None:
    """An existing launch.json should be preserved unless overwrite is requested."""
    result, launch_contents = run_ensure_vscode_launch_file(
        tmp_path=tmp_path,
        sample_exists=True,
        launch_exists=True,
        overwrite_launch=0,
    )

    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    assert launch_contents == '{"version":"existing"}\n'
