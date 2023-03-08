"""Test that we can parse the sample pylintrc file."""
from configupdater import ConfigUpdater

from src.constants.pylintrc import (
    PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY,
    PYLINTRC_FORMAT_SECTION_KEY,
    PYLINTRC_MASTER_IGNORE_KEY,
    PYLINTRC_MASTER_SECTION_KEY,
    SAMPLE_PYLINTRC,
)
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME


def test_can_parse_sample_flake8():
    """Test that we can parse the sample .flake8."""
    updater = ConfigUpdater()
    updater.read_string(SAMPLE_PYLINTRC)
    assert updater is not None

    assert updater[PYLINTRC_MASTER_SECTION_KEY][PYLINTRC_MASTER_IGNORE_KEY].value == f"CVS,{REPO_NAME}"
    assert (
        updater[PYLINTRC_FORMAT_SECTION_KEY][PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY].value
        == f"{DEFAULT_LINE_LENGTH}"
    )
