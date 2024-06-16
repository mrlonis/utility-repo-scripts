"""Do processing of the pylintrc file."""

from argparse import ArgumentParser

from src.constants.pylintrc import PYLINTRC_FILENAME, SAMPLE_PYLINTRC
from src.constants.shared import DEFAULT_LINE_LENGTH
from src.processors.process_pylintrc import process_pylintrc
from src.utils.configupdater import load_ini_file
from src.utils.core import str2bool


def main(
    debug: bool = False,
    test: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
    exists: bool = False,
):
    """Do processing of the pylintrc file."""
    pylintrc = load_ini_file(debug=debug, exists=exists, filename=PYLINTRC_FILENAME, sample=SAMPLE_PYLINTRC)
    process_pylintrc(pylintrc=pylintrc, debug=debug, line_length=line_length, test=test)


def script_entry():
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--line_length", default=DEFAULT_LINE_LENGTH, type=int)
    parser.add_argument("--exists", type=str2bool, default=False)
    parser.add_argument("--test", action="store_true")

    args, _ = parser.parse_known_args()

    main(
        debug=args.debug,
        line_length=args.line_length,
        exists=args.exists,
        test=args.test,
    )
