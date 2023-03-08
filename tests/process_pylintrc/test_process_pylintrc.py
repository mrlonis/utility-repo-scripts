"""Test the process_pylintrc.py file."""
from configupdater import ConfigUpdater

from src.constants.pylintrc import (
    PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY,
    PYLINTRC_FORMAT_SECTION_KEY,
    PYLINTRC_MASTER_IGNORE_KEY,
    PYLINTRC_MASTER_SECTION_KEY,
)
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME
from src.process_pylintrc import process_pylintrc


def assert_pylintrc(data: ConfigUpdater, line_length: int):
    """Assert the pylintrc file is correct."""
    # Check Master Settings
    ignore_value = data.get(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY).value
    assert ignore_value is not None
    assert REPO_NAME in ignore_value

    # Check Format Settings
    max_line_length_value = data.get(PYLINTRC_FORMAT_SECTION_KEY, PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY).value
    assert max_line_length_value is not None
    assert max_line_length_value == str(line_length)


def test_process_pylintrc():
    """Test the process_pylintrc function."""
    line_length = 110

    result = process_pylintrc(pylintrc=ConfigUpdater(), debug=False, line_length=line_length, test=True)
    assert result is not None

    assert_pylintrc(data=result, line_length=line_length)


def test_process_pylintrc_existing_ignore():
    """Test the process_pylintrc function."""
    line_length = 110
    pylintrc = ConfigUpdater()
    pylintrc.add_section(PYLINTRC_MASTER_SECTION_KEY)
    pylintrc.set(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY, "CVS")
    assert pylintrc.get(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY).value == "CVS"

    result = process_pylintrc(pylintrc=pylintrc, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert_pylintrc(data=result, line_length=line_length)
    assert pylintrc.get(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY).value == f"CVS,{REPO_NAME}"


def test_process_pylintrc_existing_ignore_is_none():
    """Test the process_pylintrc function."""
    line_length = 110
    pylintrc = ConfigUpdater()
    pylintrc.add_section(PYLINTRC_MASTER_SECTION_KEY)
    pylintrc.set(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY, "")
    assert pylintrc.get(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY).value == ""

    result = process_pylintrc(pylintrc=pylintrc, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert_pylintrc(data=result, line_length=line_length)
    assert pylintrc.get(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY).value == f"{REPO_NAME}"


def test_process_pylintrc_existing_ignore_includes_repo_name():
    """Test the process_pylintrc function."""
    line_length = 110
    pylintrc = ConfigUpdater()
    pylintrc.add_section(PYLINTRC_MASTER_SECTION_KEY)
    pylintrc.set(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY, f"CVS,{REPO_NAME}")
    assert pylintrc.get(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY).value == f"CVS,{REPO_NAME}"

    result = process_pylintrc(pylintrc=pylintrc, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert_pylintrc(data=result, line_length=line_length)
    assert pylintrc.get(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY).value == f"CVS,{REPO_NAME}"


def test_process_pylintrc_existing_line_length():
    """Test the process_pylintrc function."""
    line_length = 110
    pylintrc = ConfigUpdater()
    pylintrc.add_section(PYLINTRC_FORMAT_SECTION_KEY)
    pylintrc.set(PYLINTRC_FORMAT_SECTION_KEY, PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY, str(DEFAULT_LINE_LENGTH))
    assert pylintrc.get(PYLINTRC_FORMAT_SECTION_KEY, PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY).value == str(
        DEFAULT_LINE_LENGTH
    )

    result = process_pylintrc(pylintrc=pylintrc, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert_pylintrc(data=result, line_length=line_length)


def test_process_pylintrc_existing_other_data():
    """Test the process_pylintrc function."""
    line_length = 110
    pylintrc = ConfigUpdater()
    pylintrc.add_section("FAKE")
    pylintrc.set("FAKE", "fake", "fake")
    assert pylintrc.get("FAKE", "fake").value == "fake"

    result = process_pylintrc(pylintrc=pylintrc, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert_pylintrc(data=result, line_length=line_length)
    assert pylintrc.get("FAKE", "fake").value == "fake"
