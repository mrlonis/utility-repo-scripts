"""Do processing of the pylintrc file."""

from typing import List

from configupdater import AssignMultilineValueError, ConfigUpdater, Option, Section

from src.constants.pylintrc import (
    PYLINTRC_FILENAME,
    PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY,
    PYLINTRC_FORMAT_SECTION_KEY,
    PYLINTRC_MASTER_IGNORE_KEY,
    PYLINTRC_MASTER_SECTION_KEY,
)
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME

INDENT = " " * 7


def process_pylintrc(
    pylintrc: ConfigUpdater, debug: bool = False, line_length: int = DEFAULT_LINE_LENGTH, test: bool = False
):
    """Do processing of the pylintrc file."""
    if debug:
        print("process_pylintrc.py CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --test: {test}")
        print(f"    --line_length: {line_length}")
        print("")

    # Master Settings
    master_section = pylintrc.get_section(PYLINTRC_MASTER_SECTION_KEY, None)
    if master_section is None:
        master_section = Section(name=PYLINTRC_MASTER_SECTION_KEY)
        pylintrc.add_section(master_section)

    ignore_settings = master_section.get(PYLINTRC_MASTER_IGNORE_KEY, None)
    if ignore_settings is None:
        ignore_settings = Option(key=PYLINTRC_MASTER_IGNORE_KEY, value="")
        master_section.add_option(ignore_settings)
    if not ignore_settings.value:
        ignore_settings.value = ""
    if REPO_NAME not in ignore_settings.value:
        try:
            ignore_settings.value = f"{ignore_settings.value}{',' if ignore_settings.value != '' else ''}{REPO_NAME}"
        except AssignMultilineValueError:
            existing_values = ignore_settings.as_list()
            new_values: List[str] = []
            for value in existing_values:
                if not value.endswith(","):
                    value = f"{value},"
                new_values.append(value)
            new_values.append(REPO_NAME)
            ignore_settings.set_values(values=new_values, separator="\n", indent=INDENT)

    # Format Settings
    format_section = pylintrc.get_section(PYLINTRC_FORMAT_SECTION_KEY, None)
    if format_section is None:
        format_section = Section(name=PYLINTRC_FORMAT_SECTION_KEY)
        pylintrc.add_section(format_section)
    format_section.set(PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY, str(line_length))

    # Create File
    if not test:  # pragma: no cover
        if debug:  # pragma: no cover
            print(f"Writing {PYLINTRC_FILENAME} file")  # pragma: no cover
        with open(PYLINTRC_FILENAME, "w", encoding="utf-8") as pylintrc_file:  # pragma: no cover
            pylintrc.write(pylintrc_file)  # pragma: no cover
    else:
        if debug:
            print(f"TESTING: Not Writing {PYLINTRC_FILENAME} file")

    return pylintrc
