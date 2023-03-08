"""Do processing of the .flake8 file."""
from configupdater import ConfigUpdater, Option

from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME


def process_flake8(
    flake8_config: ConfigUpdater,
    debug: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
    test: bool = False,
):
    """Do processing of the .flake8 file."""
    if debug:
        print("process_flake8.py CLI Arguments:")
        print(f"    --debug: {debug}")
        print(f"    --test: {test}")
        print(f"    --line_length: {line_length}")
        print("")

    if flake8_config.get_section("flake8", None) is None:
        flake8_config.add_section("flake8")

    flake8_config.set("flake8", "max-line-length", str(line_length))

    exclude_settings = flake8_config.get("flake8", "exclude", None)
    if not exclude_settings:
        exclude_settings = Option(key="exclude", value="")
    if not exclude_settings.value:
        exclude_settings.value = ""

    if REPO_NAME not in exclude_settings.value:
        exclude_settings.value = f"{exclude_settings.value}{',' if exclude_settings.value else ''}{REPO_NAME}"
    flake8_config.set("flake8", "exclude", exclude_settings.value)

    if not test:  # pragma: no cover
        if debug:  # pragma: no cover
            print("Writing .flake8 file")  # pragma: no cover
        with open(".flake8", "w", encoding="utf-8") as flake8_file:  # pragma: no cover
            flake8_config.write(flake8_file)  # pragma: no cover
    else:
        if debug:
            print("TESTING: Not Writing .flake8 file")

    return flake8_config
