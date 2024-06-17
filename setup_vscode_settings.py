"""Do processing of the .vscode/settings.json file."""

from argparse import ArgumentParser

from src.constants.vscode_settings import SAMPLE_VSCODE_SETTINGS, VSCODE_SETTINGS_JSON_FILENAME
from src.process_vscode_settings import process_vscode_settings
from src.utils.core import load_json_file, str2bool


def main(
    debug: bool = False,
    include_isort: bool = False,
    python_formatter="",
    pylint_enabled: bool = False,
    flake8_enabled: bool = False,
    mypy_enabled: bool = False,
    pytest_enabled: bool = False,
    unittest_enabled: bool = False,
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
        include_isort=include_isort,
        python_formatter=python_formatter,
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        mypy_enabled=mypy_enabled,
        pytest_enabled=pytest_enabled,
        unittest_enabled=unittest_enabled,
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--include_isort", action="store_true")
    parser.add_argument("--python_formatter", default="black", type=str)
    parser.add_argument("--pylint_enabled", action="store_true")
    parser.add_argument("--flake8_enabled", action="store_true")
    parser.add_argument("--mypy_enabled", action="store_true")
    parser.add_argument("--pytest_enabled", action="store_true")
    parser.add_argument("--unittest_enabled", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--exists", type=str2bool, default=False)
    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        include_isort=args.include_isort,
        python_formatter=args.python_formatter,
        pylint_enabled=args.pylint_enabled,
        flake8_enabled=args.flake8_enabled,
        mypy_enabled=args.mypy_enabled,
        pytest_enabled=args.pytest_enabled,
        unittest_enabled=args.unittest_enabled,
        test=args.test,
        exists=args.exists,
    )
