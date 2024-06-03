"""Do processing of the .flake8 file."""

from argparse import ArgumentParser

from src.constants.flake8 import FLAKE8_FILENAME, SAMPLE_FLAKE8
from src.constants.shared import DEFAULT_LINE_LENGTH
from src.process_flake8 import process_flake8
from src.utils.configupdater import load_ini_file
from src.utils.core import str2bool


def main(
    debug: bool = False,
    test: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
    exists: bool = False,
):
    """Do processing of the .flake8 file."""
    flake8_config = load_ini_file(debug=debug, exists=exists, filename=FLAKE8_FILENAME, sample=SAMPLE_FLAKE8)
    process_flake8(flake8_config=flake8_config, debug=debug, line_length=line_length, test=test)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--line_length", default=DEFAULT_LINE_LENGTH, type=int)
    parser.add_argument("--exists", type=str2bool, default=False)
    parser.add_argument("--test", action="store_true")

    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        line_length=args.line_length,
        exists=args.exists,
        test=args.test,
    )
