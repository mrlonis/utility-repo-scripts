#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"
source "$script_dir"/scripts/functions.sh "$@"

[ ! -f ".pre-commit-config.yaml" ] && pre_commit_config_exists=0 || pre_commit_config_exists=1

if [ "$debug" = 1 ]; then
	echo "$dash_separator .pre-commit-config.yaml Setup $dash_separator"
fi

ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml)
python "$script_dir"/setup_fix_prettier_pre_commit.py "$@" --pre_commit_config_exists="$pre_commit_config_exists"
uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_installed"
prettier_format .pre-commit-config.yaml

if [ "$debug" = 1 ]; then
	echo ""
fi
