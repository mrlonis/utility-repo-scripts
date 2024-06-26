"""Do processing of the .prettierrc file."""

from argparse import ArgumentParser

from src.constants.prettier import SAMPLE_PRETTIERRC
from src.constants.shared import DEFAULT_LINE_LENGTH
from src.process_prettier import process_prettierrc
from src.utils.core import load_json_file, str2bool


def main(
    debug: bool = False,
    test: bool = False,
    exists: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
):  # pylint: disable=too-many-arguments
    """Do processing for prettier file."""
    prettierrc_data = load_json_file(debug=debug, exists=exists, filename=".prettierrc", sample=SAMPLE_PRETTIERRC)
    process_prettierrc(debug=debug, test=test, line_length=line_length, prettierrc_data=prettierrc_data)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--exists", type=str2bool, default=False)
    parser.add_argument("--line_length", default=DEFAULT_LINE_LENGTH, type=int)

    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        test=args.test,
        exists=args.exists,
        line_length=args.line_length,
    )
