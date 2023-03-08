"""tomlkit utility functions."""
from os import getenv
from pathlib import Path

from tomlkit import load, parse


def load_toml_file(debug: bool, exists: bool, filename: str, sample: str):
    """Load a toml file or create it from a sample."""
    if exists:
        if debug:
            print(f"{filename} already exists...")
            print(f"Loading {filename}...")
        pwd = getenv("PWD")
        if pwd is None:
            raise RuntimeError("PWD environment variable is not set.")
        filepath = f"{pwd}/{filename}"
        if debug:
            print(f"filepath: {filepath}")
        with open(Path(filepath).resolve(), "r", encoding="utf-8") as file:
            data = load(file)
    else:
        if debug:
            print(f"{filename} doesn't exists...")
            print(f"Creating {filename} from sample...")
        data = parse(sample)
    return data
