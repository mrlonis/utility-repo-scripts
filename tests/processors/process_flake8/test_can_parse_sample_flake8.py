"""Test that we can parse the sample .flake8 file."""

from configupdater import ConfigUpdater

from src.constants.flake8 import SAMPLE_FLAKE8
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME


def test_can_parse_sample_flake8():
    """Test that we can parse the sample .flake8."""
    updater = ConfigUpdater()
    updater.read_string(SAMPLE_FLAKE8)
    assert updater is not None

    assert updater["flake8"]["exclude"].value == f".git,__pycache__,{REPO_NAME}"
    assert updater["flake8"]["max-line-length"].value == f"{DEFAULT_LINE_LENGTH}"
