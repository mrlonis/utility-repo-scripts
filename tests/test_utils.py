"""Test the src/utils.py file."""
import pytest

from src.utils.core import validate_python_formatter_option


# Testing python_formatter options
def test_process_vs_code_settings_invalid_python_formatter():
    """Test the validate_python_formatter_option function with an invalid python_formatter."""
    python_formatter = "fake-formatter"

    with pytest.raises(ValueError) as exception_info:
        validate_python_formatter_option(python_formatter=python_formatter)

    assert exception_info is not None
    assert exception_info.value.args[0] == (
        f"Invalid python_formatter: {python_formatter}. "
        + "Valid Options are: ['', 'autopep8', 'black', 'yapf']"
    )
