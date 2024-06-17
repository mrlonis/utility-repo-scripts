"""Do processing of the .pre-commit-config.yaml file."""

from argparse import ArgumentParser

from src.constants.pre_commit_config import PRE_COMMIT_CONFIG_FILENAME, SAMPLE_PRE_COMMIT_CONFIG
from src.constants.shared import REPO_NAME
from src.process_pre_commit_config import PreCommitConfigProcessor
from src.utils.core import str2bool
from src.utils.ruamel.yaml import load_yaml_file


def main(
    debug: bool = False,
    python_formatter="black",
    pre_commit_pylint_entry_prefix=f"{REPO_NAME}/",
    test: bool = False,
    exists: bool = False,
):  # pylint: disable=too-many-arguments
    """Do processing of the .pre-commit-config.yaml file."""
    pre_commit_config = load_yaml_file(
        debug=debug, exists=exists, filename=PRE_COMMIT_CONFIG_FILENAME, sample=SAMPLE_PRE_COMMIT_CONFIG
    )

    processor = PreCommitConfigProcessor(
        pre_commit_config=pre_commit_config,
        debug=debug,
        test=test,
        python_formatter=python_formatter,
        pre_commit_pylint_entry_prefix=pre_commit_pylint_entry_prefix,
    )
    processor.process_pre_commit_config()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--python_formatter", default="black", type=str)
    parser.add_argument("--pre_commit_pylint_entry_prefix", default=f"{REPO_NAME}/", type=str)
    parser.add_argument("--exists", type=str2bool, default=False)

    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        test=args.test,
        python_formatter=args.python_formatter,
        pre_commit_pylint_entry_prefix=args.pre_commit_pylint_entry_prefix,
        exists=args.exists,
    )
