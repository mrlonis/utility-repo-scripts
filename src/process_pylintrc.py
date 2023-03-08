"""Do processing of the pylintrc file."""
from configupdater import ConfigUpdater

from src.constants.pylintrc import (
    PYLINTRC_FILENAME,
    PYLINTRC_FORMAT_MAX_LINE_LENGTH_KEY,
    PYLINTRC_FORMAT_SECTION_KEY,
    PYLINTRC_MASTER_IGNORE_KEY,
    PYLINTRC_MASTER_SECTION_KEY,
)
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME


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
        pylintrc.add_section(PYLINTRC_MASTER_SECTION_KEY)
        master_section = pylintrc.get_section(PYLINTRC_MASTER_SECTION_KEY)
        if master_section is None:
            raise RuntimeError(f"Unable to add MASTER section to the {PYLINTRC_FILENAME} file")

    ignore_settings = master_section.get(PYLINTRC_MASTER_IGNORE_KEY, None)
    if ignore_settings is None:
        pylintrc.set(PYLINTRC_MASTER_SECTION_KEY, PYLINTRC_MASTER_IGNORE_KEY, "")
        ignore_settings = master_section.get(PYLINTRC_MASTER_IGNORE_KEY, None)
        if ignore_settings is None:
            raise RuntimeError(
                f"Unable to add ignore settings to the {PYLINTRC_MASTER_SECTION_KEY} "
                + f"section of the {PYLINTRC_FILENAME} file"
            )
    if not ignore_settings.value:
        ignore_settings.value = ""

    if REPO_NAME not in ignore_settings.value:
        ignore_settings.value = f"{ignore_settings.value}{',' if ignore_settings.value else ''}{REPO_NAME}"

    # Format Settings
    format_section = pylintrc.get_section(PYLINTRC_FORMAT_SECTION_KEY, None)
    if format_section is None:
        pylintrc.add_section(PYLINTRC_FORMAT_SECTION_KEY)
        format_section = pylintrc.get_section(PYLINTRC_FORMAT_SECTION_KEY)
        if format_section is None:
            raise RuntimeError(f"Unable to add FORMAT section to the {PYLINTRC_FILENAME} file")
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
