"""Test the process_tox_ini.py file."""
from configupdater import ConfigUpdater

from src.constants.shared import REPO_NAME
from src.constants.tox_ini import (
    TOX_COUNT_KEY,
    TOX_EXCLUDE_KEY,
    TOX_EXCLUDE_VALUE,
    TOX_INDENT_SIZE_KEY,
    TOX_INDENT_SIZE_VALUE,
    TOX_MAX_DOC_LENGTH_KEY,
    TOX_MAX_LINE_LENGTH_KEY,
    TOX_PYCODESTYLE_KEY,
    TOX_STATISTICS_KEY,
)
from src.process_tox_ini import process_tox_ini


def assert_tox_ini(data: ConfigUpdater, pycodestyle_enabled: bool, line_length: int):
    """Assert the pylintrc file is correct."""
    # pycodestyle
    if pycodestyle_enabled:
        # count
        count_value = data.get(TOX_PYCODESTYLE_KEY, TOX_COUNT_KEY).value
        assert count_value is not None

        # exclude
        exclude_value = data.get(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY).value
        assert exclude_value is not None

        # indent size
        indent_size_value = data.get(TOX_PYCODESTYLE_KEY, TOX_INDENT_SIZE_KEY).value
        assert indent_size_value is not None
        assert indent_size_value == str(TOX_INDENT_SIZE_VALUE)

        # max doc length
        max_doc_length_value = data.get(TOX_PYCODESTYLE_KEY, TOX_MAX_DOC_LENGTH_KEY).value
        assert max_doc_length_value is not None
        assert max_doc_length_value == str(line_length)

        # max line length
        max_line_length_value = data.get(TOX_PYCODESTYLE_KEY, TOX_MAX_LINE_LENGTH_KEY).value
        assert max_line_length_value is not None
        assert max_line_length_value == str(line_length)

        # statistics
        statistics_value = data.get(TOX_PYCODESTYLE_KEY, TOX_STATISTICS_KEY).value
        assert statistics_value is not None
    else:
        assert data.get_section(TOX_PYCODESTYLE_KEY) is None


def test_process_tox_ini():
    """Test the process_tox_ini function."""
    pycodestyle_enabled = True
    line_length = 110

    result = process_tox_ini(
        tox_ini=ConfigUpdater(),
        debug=False,
        pycodestyle_enabled=pycodestyle_enabled,
        line_length=line_length,
        test=True,
    )
    assert result is not None

    assert_tox_ini(data=result, pycodestyle_enabled=pycodestyle_enabled, line_length=line_length)


# exclude
def test_process_tox_ini_existing_exclude():
    """Test the process_tox_ini function."""
    pycodestyle_enabled = True
    line_length = 110
    tox_ini = ConfigUpdater()
    tox_ini.add_section(TOX_PYCODESTYLE_KEY)
    tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY, ".svn,CVS,.bzr,.hg,.git,__pycache__,.tox")
    assert (
        tox_ini.get(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY).value == ".svn,CVS,.bzr,.hg,.git,__pycache__,.tox"
    )

    result = process_tox_ini(
        tox_ini=tox_ini,
        debug=True,
        pycodestyle_enabled=pycodestyle_enabled,
        line_length=line_length,
        test=True,
    )
    assert result is not None

    assert_tox_ini(data=result, pycodestyle_enabled=pycodestyle_enabled, line_length=line_length)
    exclude_value = tox_ini.get(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY).value
    assert exclude_value is not None
    assert exclude_value == TOX_EXCLUDE_VALUE
    assert REPO_NAME in exclude_value


def test_process_tox_ini_existing_exclude_is_none():
    """Test the process_tox_ini function."""
    pycodestyle_enabled = True
    line_length = 110
    tox_ini = ConfigUpdater()
    tox_ini.add_section(TOX_PYCODESTYLE_KEY)
    tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY, "")
    assert tox_ini.get(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY).value == ""

    result = process_tox_ini(
        tox_ini=tox_ini,
        debug=True,
        pycodestyle_enabled=pycodestyle_enabled,
        line_length=line_length,
        test=True,
    )
    assert result is not None

    assert_tox_ini(data=result, pycodestyle_enabled=pycodestyle_enabled, line_length=line_length)
    assert tox_ini.get(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY).value == TOX_EXCLUDE_VALUE


def test_process_tox_ini_existing_exclude_includes_repo_name():
    """Test the process_tox_ini function."""
    pycodestyle_enabled = True
    line_length = 110
    tox_ini = ConfigUpdater()
    tox_ini.add_section(TOX_PYCODESTYLE_KEY)
    tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY, TOX_EXCLUDE_VALUE)
    assert tox_ini.get(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY).value == TOX_EXCLUDE_VALUE

    result = process_tox_ini(
        tox_ini=tox_ini,
        debug=True,
        pycodestyle_enabled=pycodestyle_enabled,
        line_length=line_length,
        test=True,
    )
    assert result is not None

    assert_tox_ini(data=result, pycodestyle_enabled=pycodestyle_enabled, line_length=line_length)
    assert tox_ini.get(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY).value == TOX_EXCLUDE_VALUE


# max doc length
def test_process_tox_ini_existing_line_length():
    """Test the process_tox_ini function."""
    pycodestyle_enabled = True
    line_length = 110
    tox_ini = ConfigUpdater()
    tox_ini.add_section(TOX_PYCODESTYLE_KEY)
    tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_MAX_DOC_LENGTH_KEY, "199")
    assert tox_ini.get(TOX_PYCODESTYLE_KEY, TOX_MAX_DOC_LENGTH_KEY).value == "199"

    result = process_tox_ini(
        tox_ini=tox_ini,
        debug=True,
        pycodestyle_enabled=pycodestyle_enabled,
        line_length=line_length,
        test=True,
    )
    assert result is not None

    assert_tox_ini(data=result, pycodestyle_enabled=pycodestyle_enabled, line_length=line_length)


# other
def test_process_tox_ini_existing_other_data():
    """Test the process_tox_ini function."""
    pycodestyle_enabled = True
    line_length = 110
    tox_ini = ConfigUpdater()
    tox_ini.add_section("FAKE")
    tox_ini.set("FAKE", "fake", "fake")
    assert tox_ini.get("FAKE", "fake").value == "fake"

    result = process_tox_ini(
        tox_ini=tox_ini,
        debug=True,
        pycodestyle_enabled=pycodestyle_enabled,
        line_length=line_length,
        test=True,
    )
    assert result is not None

    assert_tox_ini(data=result, pycodestyle_enabled=pycodestyle_enabled, line_length=line_length)
    assert tox_ini.get("FAKE", "fake").value == "fake"
