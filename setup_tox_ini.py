"""Do processing of the tox.ini file."""
from argparse import ArgumentParser

from src.constants.shared import DEFAULT_LINE_LENGTH
from src.constants.tox_ini import SAMPLE_TOX_INI, TOX_INI_FILENAME
from src.process_tox_ini import process_tox_ini
from src.utils.configupdater import load_ini_file
from src.utils.core import str2bool


def main(
    debug: bool = False,
    test: bool = False,
    pycodestyle_enabled: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
    exists: bool = False,
):
    """Do processing of the tox.ini file."""
    tox_ini = load_ini_file(debug=debug, exists=exists, filename=TOX_INI_FILENAME, sample=SAMPLE_TOX_INI)
    process_tox_ini(
        tox_ini=tox_ini,
        debug=debug,
        line_length=line_length,
        test=test,
        pycodestyle_enabled=pycodestyle_enabled,
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--pycodestyle_enabled", action="store_true")
    parser.add_argument("--line_length", default=DEFAULT_LINE_LENGTH, type=int)
    parser.add_argument("--exists", type=str2bool, default=False)
    parser.add_argument("--test", action="store_true")

    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        pycodestyle_enabled=args.pycodestyle_enabled,
        line_length=args.line_length,
        exists=args.exists,
        test=args.test,
    )
