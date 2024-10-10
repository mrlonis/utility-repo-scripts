"""Do processing of the pyproject.toml file."""

from argparse import ArgumentParser

from src.constants.pyproject_toml import PYPROJECT_TOML_FILENAME, SAMPLE_PYPROJECT_TOML
from src.constants.shared import DEFAULT_LINE_LENGTH
from src.process_pyproject_toml import PyProjectTomlProcessor
from src.utils.core import str2bool
from src.utils.tomlkit import load_toml_file


def main(  # pylint: disable=too-many-positional-arguments
    debug: bool = False,
    test: bool = False,
    python_formatter="black",
    line_length: int = DEFAULT_LINE_LENGTH,
    exists: bool = False,
    isort_profile: str = "black",
    package_manager: str = "poetry",
    is_package: bool = False,
):
    """Do processing of the pyproject.toml file."""
    pyproject_toml = load_toml_file(
        debug=debug, exists=exists, filename=PYPROJECT_TOML_FILENAME, sample=SAMPLE_PYPROJECT_TOML
    )
    PyProjectTomlProcessor(
        pyproject_toml=pyproject_toml,
        python_formatter=python_formatter,
        isort_profile=isort_profile,
        line_length=line_length,
        package_manager=package_manager,
        is_package=is_package,
        debug=debug,
        test=test,
    ).process_pyproject_toml()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("--python_formatter", default="black", type=str)
    parser.add_argument("--line_length", default=DEFAULT_LINE_LENGTH, type=int)
    parser.add_argument("--exists", type=str2bool, default=False)
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--isort_profile", default="black", type=str)
    parser.add_argument("--package_manager", default="pip", type=str)
    parser.add_argument("--is_package", type=str2bool, default=False)

    args, unknown = parser.parse_known_args()

    main(
        debug=args.debug,
        python_formatter=args.python_formatter,
        line_length=args.line_length,
        exists=args.exists,
        test=args.test,
        isort_profile=args.isort_profile,
        package_manager=args.package_manager,
        is_package=args.is_package,
    )
