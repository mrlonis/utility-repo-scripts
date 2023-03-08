"""Test that we can parse the sample tox.ini."""
from configupdater import ConfigUpdater

from src.constants.shared import DEFAULT_LINE_LENGTH
from src.constants.tox_ini import (
    SAMPLE_TOX_INI,
    TOX_COUNT_KEY,
    TOX_COUNT_VALUE,
    TOX_EXCLUDE_KEY,
    TOX_EXCLUDE_VALUE,
    TOX_INDENT_SIZE_KEY,
    TOX_INDENT_SIZE_VALUE,
    TOX_MAX_DOC_LENGTH_KEY,
    TOX_MAX_LINE_LENGTH_KEY,
    TOX_PYCODESTYLE_KEY,
    TOX_STATISTICS_KEY,
    TOX_STATISTICS_VALUE,
)


def test_can_parse_sample_tox_ini():
    """Test that we can parse the sample tox.ini."""
    updater = ConfigUpdater()
    updater.read_string(SAMPLE_TOX_INI)
    assert updater is not None

    assert updater[TOX_PYCODESTYLE_KEY][TOX_COUNT_KEY].value == str(TOX_COUNT_VALUE)
    assert updater[TOX_PYCODESTYLE_KEY][TOX_EXCLUDE_KEY].value == TOX_EXCLUDE_VALUE
    assert updater[TOX_PYCODESTYLE_KEY][TOX_INDENT_SIZE_KEY].value == str(TOX_INDENT_SIZE_VALUE)
    assert updater[TOX_PYCODESTYLE_KEY][TOX_MAX_DOC_LENGTH_KEY].value == str(DEFAULT_LINE_LENGTH)
    assert updater[TOX_PYCODESTYLE_KEY][TOX_MAX_LINE_LENGTH_KEY].value == str(DEFAULT_LINE_LENGTH)
    assert updater[TOX_PYCODESTYLE_KEY][TOX_STATISTICS_KEY].value == str(TOX_STATISTICS_VALUE)
