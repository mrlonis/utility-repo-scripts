#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"
source "$script_dir"/scripts/functions.sh "$@" # Loads find_site_package & prettier_format functions

# Check if .prettierrc exists
[ ! -f ".prettierrc" ] && prettierrc_exists=0 || prettierrc_exists=1

# Check if .pre-commit-config.yaml exists
[ ! -f ".pre-commit-config.yaml" ] && pre_commit_config_exists=0 || pre_commit_config_exists=1

# Setup Logging
if [ "$debug" = 1 ]; then
	echo "$dash_separator .pre-commit-config.yaml Setup $dash_separator"
fi

# Install ruamel.yaml if it doesn't exist
ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml)
if [ "$debug" = 1 ]; then
	echo "ruamel_yaml_installed: $ruamel_yaml_installed"
fi

# Create .pre-commit-config.yaml using setup_pre_commit_config.py
python "$script_dir"/setup_prettier.py "$@" --prettierrc_exists="$prettierrc_exists" --pre_commit_config_exists="$pre_commit_config_exists"

# Uninstall ruamel.yaml if it didn't exist prior to running this script
if [ "$ruamel_yaml_installed" = 0 ]; then
	if [ "$debug" = 1 ]; then
		echo "Uninstalling ruamel.yaml since it did not exist in the virtual environment prior to running this script"
	fi
	pip uninstall -y ruamel.yaml
	pip uninstall -y ruamel.yaml.clib
fi

# Attempt to format newly created .pre-commit-config.yaml and .prettierrc using prettier
prettier_format .pre-commit-config.yaml
prettier_format .prettierrc

if [ "$debug" = 1 ]; then
	echo ""
fi
