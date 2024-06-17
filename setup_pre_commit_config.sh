#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"
source "$script_dir"/scripts/functions.sh "$@" # Loads find_site_package function

# Check if .pre-commit-config.yaml exists
[ ! -f ".pre-commit-config.yaml" ] && pre_commit_config_exists=0 || pre_commit_config_exists=1

# Setup Logging
if [ "$debug" = 1 ]; then
	echo "$dash_separator .pre-commit-config.yaml Setup $dash_separator"
fi

# Install ruamel.yaml if it doesn't exist
ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml)

# Create .pre-commit-config.yaml using setup_pre_commit_config.py
python "$script_dir"/setup_pre_commit_config.py "$@" --exists="$pre_commit_config_exists"

# Uninstall ruamel.yaml if it didn't exist prior to running this script
uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_installed"

# Attempt to format newly created .pre-commit-config.yaml using prettier
prettier_format .pre-commit-config.yaml
echo ""
