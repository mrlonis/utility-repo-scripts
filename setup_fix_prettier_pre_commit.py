"""Do processing of the .pre-commit-config.yaml file."""

from argparse import ArgumentParser

from src.constants.pre_commit_config import PRE_COMMIT_CONFIG_FILENAME, SAMPLE_PRE_COMMIT_CONFIG
from src.constants.shared import DEFAULT_LINE_LENGTH
from src.process_prettier import process_pre_commit_config
from src.utils.core import str2bool
from src.utils.ruamel.yaml import load_yaml_file


def main(
    debug: bool = False,
    test: bool = False,
    pre_commit_config_exists: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
):  # pylint: disable=too-many-arguments
    """Do processing for prettier file."""
    pre_commit_config = load_yaml_file(
        debug=debug,
        exists=pre_commit_config_exists,
        filename=PRE_COMMIT_CONFIG_FILENAME,
        sample=SAMPLE_PRE_COMMIT_CONFIG,
    )
    process_pre_commit_config(
        debug=debug,
        test=test,
        line_length=line_length,
        pre_commit_config=pre_commit_config,
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--pre_commit_config_exists", type=str2bool, default=False)
    parser.add_argument("--line_length", default=DEFAULT_LINE_LENGTH, type=int)

    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        test=args.test,
        pre_commit_config_exists=args.pre_commit_config_exists,
        line_length=args.line_length,
    )
