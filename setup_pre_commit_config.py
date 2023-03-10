"""Do processing of the .pre-commit-config.yaml file."""
from argparse import ArgumentParser

from src.constants.pre_commit_config import PRE_COMMIT_CONFIG_FILENAME, SAMPLE_PRE_COMMIT_CONFIG
from src.constants.shared import REPO_NAME
from src.process_pre_commit_config import PreCommitConfigProcessor
from src.utils.core import str2bool
from src.utils.ruamel.yaml import load_yaml_file


def main(
    debug: bool = False,
    include_jumanji_house: bool = False,
    include_prettier: bool = False,
    include_isort: bool = False,
    python_formatter="",
    pylint_enabled: bool = False,
    flake8_enabled: bool = False,
    pydocstyle_enabled: bool = False,
    pre_commit_pylint_entry_prefix=f"{REPO_NAME}/",
    test: bool = False,
    exists: bool = False,
    bandit_enabled: bool = False,
):  # pylint: disable=too-many-arguments
    """Do processing of the .pre-commit-config.yaml file."""
    pre_commit_config = load_yaml_file(
        debug=debug, exists=exists, filename=PRE_COMMIT_CONFIG_FILENAME, sample=SAMPLE_PRE_COMMIT_CONFIG
    )

    processor = PreCommitConfigProcessor(
        pre_commit_config=pre_commit_config,
        debug=debug,
        test=test,
        include_jumanji_house=include_jumanji_house,
        include_prettier=include_prettier,
        include_isort=include_isort,
        python_formatter=python_formatter,
        pylint_enabled=pylint_enabled,
        flake8_enabled=flake8_enabled,
        pydocstyle_enabled=pydocstyle_enabled,
        pre_commit_pylint_entry_prefix=pre_commit_pylint_entry_prefix,
        bandit_enabled=bandit_enabled,
    )
    processor.process_pre_commit_config()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--include_jumanji_house", action="store_true")
    parser.add_argument("--include_prettier", action="store_true")
    parser.add_argument("--include_isort", action="store_true")
    parser.add_argument("--python_formatter", default="black", type=str)
    parser.add_argument("--pylint_enabled", action="store_true")
    parser.add_argument("--flake8_enabled", action="store_true")
    parser.add_argument("--pydocstyle_enabled", action="store_true")
    parser.add_argument("--pre_commit_pylint_entry_prefix", default=f"{REPO_NAME}/", type=str)
    parser.add_argument("--exists", type=str2bool, default=False)
    parser.add_argument("--bandit_enabled", action="store_true")

    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        test=args.test,
        include_jumanji_house=args.include_jumanji_house,
        include_prettier=args.include_prettier,
        include_isort=args.include_isort,
        python_formatter=args.python_formatter,
        pylint_enabled=args.pylint_enabled,
        flake8_enabled=args.flake8_enabled,
        pydocstyle_enabled=args.pydocstyle_enabled,
        pre_commit_pylint_entry_prefix=args.pre_commit_pylint_entry_prefix,
        exists=args.exists,
        bandit_enabled=args.bandit_enabled,
    )
