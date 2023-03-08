"""Test that we can parse the sample pyproject.toml."""
from tomlkit import parse

from src.constants.pyproject_toml import SAMPLE_PYPROJECT_TOML


def test_can_parse_sample_pyproject_toml():
    """Test that we can parse the sample pyproject.toml."""
    data = parse(SAMPLE_PYPROJECT_TOML)
    assert data is not None
