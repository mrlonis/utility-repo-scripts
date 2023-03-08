"""Test the process_flake8.py file."""
from configupdater import ConfigUpdater

from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME
from src.process_flake8 import process_flake8

FULL_EXCLUDE = f".git,__pycache__,{REPO_NAME}"


def test_process_flake8():
    """Test the process_flake8 function."""
    line_length = 110

    result = process_flake8(flake8_config=ConfigUpdater(), debug=False, line_length=line_length, test=True)
    assert result is not None

    assert result.get("flake8", "max-line-length").value == str(line_length)
    assert result.get("flake8", "exclude").value == REPO_NAME


def test_process_flake8_existing_line_length():
    """Test the process_flake8 function."""
    line_length = 110
    flake8_config = ConfigUpdater()
    flake8_config.add_section("flake8")
    flake8_config.set("flake8", "max-line-length", str(DEFAULT_LINE_LENGTH))
    assert flake8_config.get("flake8", "max-line-length").value == str(DEFAULT_LINE_LENGTH)

    result = process_flake8(flake8_config=flake8_config, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert result.get("flake8", "max-line-length").value == str(line_length)
    assert result.get("flake8", "exclude").value == REPO_NAME


def test_process_flake8_existing_exclude():
    """Test the process_flake8 function."""
    line_length = 110
    flake8_config = ConfigUpdater()
    flake8_config.add_section("flake8")
    flake8_config.set("flake8", "exclude", ".git,__pycache__")
    assert flake8_config.get("flake8", "exclude").value == ".git,__pycache__"

    result = process_flake8(flake8_config=flake8_config, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert result.get("flake8", "max-line-length").value == str(line_length)
    assert result.get("flake8", "exclude").value == FULL_EXCLUDE


def test_process_flake8_existing_exclude_is_none():
    """Test the process_flake8 function."""
    line_length = 110
    flake8_config = ConfigUpdater()
    flake8_config.add_section("flake8")
    flake8_config.set("flake8", "exclude", "")
    assert flake8_config.get("flake8", "exclude").value == ""

    result = process_flake8(flake8_config=flake8_config, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert result.get("flake8", "max-line-length").value == str(line_length)
    assert result.get("flake8", "exclude").value == f"{REPO_NAME}"


def test_process_flake8_existing_exclude_already_has_submodule():
    """Test the process_flake8 function."""
    line_length = 110
    flake8_config = ConfigUpdater()
    flake8_config.add_section("flake8")
    flake8_config.set("flake8", "exclude", FULL_EXCLUDE)
    assert flake8_config.get("flake8", "exclude").value == FULL_EXCLUDE

    result = process_flake8(flake8_config=flake8_config, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert result.get("flake8", "max-line-length").value == str(line_length)
    assert result.get("flake8", "exclude").value == FULL_EXCLUDE


def test_process_flake8_existing_other_data():
    """Test the process_flake8 function."""
    line_length = 110
    flake8_config = ConfigUpdater()
    flake8_config.add_section("FAKE")
    flake8_config.set("FAKE", "fake", "fake")
    assert flake8_config.get("FAKE", "fake").value == "fake"

    result = process_flake8(flake8_config=flake8_config, debug=True, line_length=line_length, test=True)
    assert result is not None

    assert result.get("flake8", "max-line-length").value == str(line_length)
    assert result.get("flake8", "exclude").value == REPO_NAME
    assert result.get("FAKE", "fake").value == "fake"
