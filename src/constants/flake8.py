""".flake8 file constants."""
# region .flake8 Constants
from src.constants.shared import DEFAULT_LINE_LENGTH, REPO_NAME

FLAKE8_FILENAME = ".flake8"

SAMPLE_FLAKE8 = f"""[flake8]
exclude = .git,__pycache__,{REPO_NAME}
max-line-length = {DEFAULT_LINE_LENGTH}
"""
# endregion
