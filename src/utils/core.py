"""Core Python utility functions for the project."""

import json
from argparse import ArgumentTypeError
from copy import deepcopy
from os import getenv
from pathlib import Path
from typing import Any, Dict, Union, cast


def validate_python_formatter_option(python_formatter: str):
    """Validate the python_formatter option."""
    if python_formatter not in ["", "autopep8", "black"]:
        raise ValueError(
            f"Invalid python_formatter: {python_formatter}. " + "Valid Options are: ['', 'autopep8', 'black']"
        )


def str2bool(value: Union[str, bool, Any]):
    """Convert shell script string to boolean."""
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    if value.lower() in ("no", "false", "f", "n", "0"):
        return False
    raise ArgumentTypeError("Boolean value expected.")


def load_json_file(debug: bool, exists: bool, filename: str, sample: Dict[str, Any]):
    """Load a json file or create it from a sample."""
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
            data = cast(Dict[str, Any], json.load(file))
    else:
        data = cast(Dict[str, Any], deepcopy(sample))
    return data
