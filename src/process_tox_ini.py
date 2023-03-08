"""Do processing of the tox.ini file."""
from configupdater import ConfigUpdater

from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME
from src.constants.tox_ini import (
    TOX_COUNT_KEY,
    TOX_COUNT_VALUE,
    TOX_EXCLUDE_KEY,
    TOX_EXCLUDE_VALUE,
    TOX_INDENT_SIZE_KEY,
    TOX_INDENT_SIZE_VALUE,
    TOX_INI_FILENAME,
    TOX_MAX_DOC_LENGTH_KEY,
    TOX_MAX_LINE_LENGTH_KEY,
    TOX_PYCODESTYLE_KEY,
    TOX_STATISTICS_KEY,
    TOX_STATISTICS_VALUE,
)


def _process_pycodestyle_settings(tox_ini: ConfigUpdater, pycodestyle_enabled: bool, line_length: int):
    # pylint: disable=too-many-branches, too-many-statements
    # pycodestyle Settings
    if pycodestyle_enabled:
        pycodestyle_section = tox_ini.get_section(TOX_PYCODESTYLE_KEY, None)
        if pycodestyle_section is None:
            tox_ini.add_section(TOX_PYCODESTYLE_KEY)
            pycodestyle_section = tox_ini.get_section(TOX_PYCODESTYLE_KEY)
            if pycodestyle_section is None:
                raise RuntimeError(f"Unable to add {TOX_PYCODESTYLE_KEY} section to tox.ini file")

        # count
        count_settings = pycodestyle_section.get(TOX_COUNT_KEY, None)
        if count_settings is None:
            tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_COUNT_KEY, str(TOX_COUNT_VALUE))
            count_settings = pycodestyle_section.get(TOX_COUNT_KEY, None)
            if count_settings is None:
                raise RuntimeError(
                    f"Unable to add {TOX_COUNT_KEY} settings to the "
                    + f"{TOX_PYCODESTYLE_KEY} section of the tox.ini file"
                )
        if count_settings.value is None:
            count_settings.value = str(TOX_COUNT_VALUE)

        # exclude
        exclude_settings = pycodestyle_section.get(TOX_EXCLUDE_KEY, None)
        if exclude_settings is None:
            tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_EXCLUDE_KEY, TOX_EXCLUDE_VALUE)
            exclude_settings = pycodestyle_section.get(TOX_EXCLUDE_KEY, None)
            if exclude_settings is None:
                raise RuntimeError(
                    f"Unable to add {TOX_EXCLUDE_KEY} settings to the "
                    + f"{TOX_PYCODESTYLE_KEY} section of the tox.ini file"
                )
        if not exclude_settings.value:
            exclude_settings.value = TOX_EXCLUDE_VALUE
        elif REPO_NAME not in exclude_settings.value:
            exclude_settings.value = (
                f"{exclude_settings.value},{REPO_NAME}" if exclude_settings.value != "" else REPO_NAME
            )

        # indent size
        indent_size_settings = pycodestyle_section.get(TOX_INDENT_SIZE_KEY, None)
        if indent_size_settings is None:
            tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_INDENT_SIZE_KEY, str(TOX_INDENT_SIZE_VALUE))
            indent_size_settings = pycodestyle_section.get(TOX_INDENT_SIZE_KEY, None)
            if indent_size_settings is None:
                raise RuntimeError(
                    f"Unable to add {TOX_INDENT_SIZE_KEY} settings to the "
                    + f"{TOX_PYCODESTYLE_KEY} section of the tox.ini file"
                )
        indent_size_settings.value = str(TOX_INDENT_SIZE_VALUE)

        # max doc length
        max_doc_length_settings = pycodestyle_section.get(TOX_MAX_DOC_LENGTH_KEY, None)
        if max_doc_length_settings is None:
            tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_MAX_DOC_LENGTH_KEY, str(line_length))
            max_doc_length_settings = pycodestyle_section.get(TOX_MAX_DOC_LENGTH_KEY, None)
            if max_doc_length_settings is None:
                raise RuntimeError(
                    f"Unable to add {TOX_MAX_DOC_LENGTH_KEY} settings to the "
                    + f"{TOX_PYCODESTYLE_KEY} section of the tox.ini file"
                )
        max_doc_length_settings.value = str(line_length)

        # max line length
        max_line_length_settings = pycodestyle_section.get(TOX_MAX_LINE_LENGTH_KEY, None)
        if max_line_length_settings is None:
            tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_MAX_LINE_LENGTH_KEY, str(line_length))
            max_line_length_settings = pycodestyle_section.get(TOX_MAX_LINE_LENGTH_KEY, None)
            if max_line_length_settings is None:
                raise RuntimeError(
                    f"Unable to add {TOX_MAX_LINE_LENGTH_KEY} settings to the "
                    + f"{TOX_PYCODESTYLE_KEY} section of the tox.ini file"
                )
        max_line_length_settings.value = str(line_length)

        # statistics
        statistics_settings = pycodestyle_section.get(TOX_STATISTICS_KEY, None)
        if statistics_settings is None:
            tox_ini.set(TOX_PYCODESTYLE_KEY, TOX_STATISTICS_KEY, str(TOX_STATISTICS_VALUE))
            statistics_settings = pycodestyle_section.get(TOX_STATISTICS_KEY, None)
            if statistics_settings is None:
                raise RuntimeError(
                    f"Unable to add {TOX_STATISTICS_KEY} settings to the "
                    + f"{TOX_PYCODESTYLE_KEY} section of the tox.ini file"
                )
        if statistics_settings.value is None:
            statistics_settings.value = str(TOX_STATISTICS_VALUE)


def process_tox_ini(
    tox_ini: ConfigUpdater,
    debug: bool = False,
    pycodestyle_enabled: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
    test: bool = False,
):
    """Do processing of the tox.ini file."""
    if debug:
        print("process_tox_ini.py CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --pycodestyle_enabled: {pycodestyle_enabled}")
        print(f"    --line_length: {line_length}")
        print(f"    --test: {test}")
        print("")

    # pycodestyle Settings
    _process_pycodestyle_settings(
        tox_ini=tox_ini, pycodestyle_enabled=pycodestyle_enabled, line_length=line_length
    )

    # Create File
    if not test:  # pragma: no cover
        if debug:  # pragma: no cover
            print(f"Writing {TOX_INI_FILENAME} file")  # pragma: no cover
        with open(TOX_INI_FILENAME, "w", encoding="utf-8") as tox_ini_file:  # pragma: no cover
            tox_ini.write(tox_ini_file)  # pragma: no cover
    else:
        if debug:
            print(f"TESTING: Not Writing {TOX_INI_FILENAME} file")

    return tox_ini
