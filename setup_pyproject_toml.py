"""Do processing of the pyproject.toml file."""
from argparse import ArgumentParser

from src.constants.pyproject_toml import PYPROJECT_TOML_FILENAME, SAMPLE_PYPROJECT_TOML
from src.constants.shared import DEFAULT_LINE_LENGTH
from src.process_pyproject_toml import process_pyproject_toml
from src.utils.core import str2bool
from src.utils.tomlkit import load_toml_file


def main(
    debug: bool = False,
    test: bool = False,
    include_isort: bool = False,
    python_formatter="",
    pydocstyle_enabled: bool = False,
    pytest_enabled: bool = False,
    line_length: int = DEFAULT_LINE_LENGTH,
    exists: bool = False,
    isort_profile: str = "black",
    bandit_enabled: bool = False,
):
    """Do processing of the pyproject.toml file."""
    pyproject_toml = load_toml_file(
        debug=debug, exists=exists, filename=PYPROJECT_TOML_FILENAME, sample=SAMPLE_PYPROJECT_TOML
    )
    process_pyproject_toml(
        pyproject_toml=pyproject_toml,
        debug=debug,
        test=test,
        include_isort=include_isort,
        python_formatter=python_formatter,
        pydocstyle_enabled=pydocstyle_enabled,
        pytest_enabled=pytest_enabled,
        line_length=line_length,
        isort_profile=isort_profile,
        bandit_enabled=bandit_enabled,
    )


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--include_isort", action="store_true")
    parser.add_argument("--python_formatter", default="black", type=str)
    parser.add_argument("--pydocstyle_enabled", action="store_true")
    parser.add_argument("--pytest_enabled", action="store_true")
    parser.add_argument("--line_length", default=DEFAULT_LINE_LENGTH, type=int)
    parser.add_argument("--exists", type=str2bool, default=False)
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--isort_profile", default="black", type=str)
    parser.add_argument("--bandit_enabled", action="store_true")

    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        include_isort=args.include_isort,
        python_formatter=args.python_formatter,
        pydocstyle_enabled=args.pydocstyle_enabled,
        pytest_enabled=args.pytest_enabled,
        line_length=args.line_length,
        exists=args.exists,
        test=args.test,
        isort_profile=args.isort_profile,
        bandit_enabled=args.bandit_enabled,
    )
