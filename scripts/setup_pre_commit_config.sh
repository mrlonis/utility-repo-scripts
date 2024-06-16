#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
debug=0
source "$script_dir"/utils/process_cli_options.sh "$@"
source "$script_dir"/utils/functions.sh "$@" # Loads find_site_package function

# Check if .pre-commit-config.yaml exists
[ ! -f ".pre-commit-config.yaml" ] && pre_commit_config_exists=0 || pre_commit_config_exists=1

# Setup Logging
echo "$dash_separator .pre-commit-config.yaml Setup $dash_separator"

# Install ruamel.yaml if it doesn't exist
ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml)
if [ "$debug" = 1 ]; then
	echo "ruamel_yaml_installed: $ruamel_yaml_installed"
fi

# Create .pre-commit-config.yaml using setup_pre_commit_config.py
poetry run setup_pre_commit_config "$@" --exists="$pre_commit_config_exists"

# Uninstall ruamel.yaml if it didn't exist prior to running this script
if [ "$ruamel_yaml_installed" = 0 ]; then
	echo "Uninstalling ruamel.yaml since it did not exist in the virtual environment prior to running this script"
	pip uninstall -y ruamel.yaml
	pip uninstall -y ruamel.yaml.clib
fi

# Attempt to format newly created .pre-commit-config.yaml using prettier
if command -v prettier >/dev/null; then
	if [ "$debug" = 1 ]; then
		echo "prettier found"
		echo "Formatting .pre-commit-config.yaml"
	fi
	prettier --write .pre-commit-config.yaml
else
	if [ "$debug" = 1 ]; then
		echo "prettier not found"
	fi

	if command -v npm >/dev/null; then
		if [ "$debug" = 1 ]; then
			echo "npm found"
			echo "Installing prettier globally to format .pre-commit-config.json"
		fi
		npm install -g prettier
		prettier --write .pre-commit-config.yaml
	else
		if [ "$debug" = 1 ]; then
			echo "npm not found"
			echo "Skipping formatting of .pre-commit-config.yaml"
		fi
	fi
fi
echo ""
