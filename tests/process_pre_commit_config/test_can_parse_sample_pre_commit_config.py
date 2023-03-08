"""Test that we can parse the sample .pre-commit-config file."""
from ruamel.yaml import YAML

from src.constants.pre_commit_config import SAMPLE_PRE_COMMIT_CONFIG


def test_can_parse_sample_flake8():
    """Test that we can parse the sample .flake8."""
    yaml = YAML()
    data = yaml.load(SAMPLE_PRE_COMMIT_CONFIG)
    assert data is not None
