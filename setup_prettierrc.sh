#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"
source "$script_dir"/scripts/functions.sh "$@"

[ ! -f ".prettierrc" ] && prettierrc_exists=0 || prettierrc_exists=1

if [ "$debug" = 1 ]; then
	echo "$dash_separator .prettierrc Setup $dash_separator"
fi

ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml)
python "$script_dir"/setup_prettierrc.py "$@" --prettierrc_exists="$prettierrc_exists"
uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_installed"
prettier_format .prettierrc

if [ "$debug" = 1 ]; then
	echo ""
fi
