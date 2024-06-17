"""Do processing of the .vscode/settings.json file."""

from argparse import ArgumentParser

from src.constants.vscode_settings import SAMPLE_VSCODE_SETTINGS, VSCODE_SETTINGS_JSON_FILENAME
from src.process_vscode_settings import process_vscode_settings
from src.utils.core import load_json_file, str2bool


def main(
    debug: bool = False,
    python_formatter="black",
    test: bool = False,
    exists: bool = False,
):
    # pylint: disable=too-many-arguments, too-many-locals
    """Do processing of the .vscode/settings.json file."""
    vscode_settings = load_json_file(
        debug=debug, exists=exists, filename=VSCODE_SETTINGS_JSON_FILENAME, sample=SAMPLE_VSCODE_SETTINGS
    )

    process_vscode_settings(
        vscode_settings=vscode_settings,
        debug=debug,
        test=test,
        python_formatter=python_formatter,
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--python_formatter", default="black", type=str)
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--exists", type=str2bool, default=False)
    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        python_formatter=args.python_formatter,
        test=args.test,
        exists=args.exists,
    )
