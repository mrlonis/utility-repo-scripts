#!/bin/bash
dash_separator="--------------------" # 20 dashes
tox_ini_filename="tox.ini"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
pycodestyle_enabled=0
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"

# tox.ini Setup
if [ "$pycodestyle_enabled" = 1 ]; then
	# If pycodestyle_enabled setup tox.ini
	if [ "$debug" = 1 ]; then
		echo "$dash_separator Setup $tox_ini_filename $dash_separator"
	fi

	source "$script_dir"/scripts/functions.sh "$@" # Loads find_site_package function

	# Install configupdater if it doesn't exist
	find_site_package configupdater configupdater
	configupdater_installed="$existed"
	if [ "$debug" = 1 ]; then
		echo "configupdater_installed: $configupdater_installed"
	fi

	# Create tox.ini using setup_tox_ini.py
	[ ! -f "$tox_ini_filename" ] && tox_ini_exists=0 || tox_ini_exists=1
	python "$script_dir"/setup_tox_ini.py "$@" --exists="$tox_ini_exists"

	# Remove trailing whitespace from tox.ini
	tmp=$(mktemp)
	sed -e 's/[[:space:]]*$//' <"$tox_ini_filename" >"$tmp"
	mv "$tmp" "$tox_ini_filename"

	# Uninstall configupdater if it didn't exist prior to running this script
	if [ "$configupdater_installed" = 0 ]; then
		echo "Uninstalling configupdater since it did not exist in the virtual environment prior to running this script"
		pip uninstall -y configupdater
	fi
	if [ "$debug" = 1 ]; then
		echo ""
	fi
fi
