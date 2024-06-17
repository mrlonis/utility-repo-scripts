#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"
source "$script_dir"/scripts/functions.sh "$@"

# Configure pyproject.toml
[ ! -f "pyproject.toml" ] && pyproject_toml_exists=0 || pyproject_toml_exists=1
if [ "$debug" = 1 ]; then
	echo "$dash_separator pyproject.toml Setup $dash_separator"
fi

# Install toml if it doesn't exist
tomlkit_installed=$(find_site_package tomlkit tomlkit)

# Create .pre-commit-config.yaml using setup_pyproject_toml.py
python "$script_dir"/setup_pyproject_toml.py "$@" --exists="$pyproject_toml_exists"

# Uninstall tomlkit if it didn't exist prior to running this script
uninstall_site_package tomlkit "$tomlkit_installed"

if [ "$debug" = 1 ]; then
	echo ""
fi
