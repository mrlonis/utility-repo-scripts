"""configupdater utility functions."""
from os import getenv
from pathlib import Path

from configupdater import ConfigUpdater


def load_ini_file(debug: bool, exists: bool, filename: str, sample: str):
    """Load an ini file or create it from a sample."""
    data = ConfigUpdater()

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
        data.read(Path(filepath).resolve())
    else:
        if debug:
            print(f"{filename} doesn't exists...")
            print(f"Creating {filename} from sample...")
        data.read_string(sample)

    return data
