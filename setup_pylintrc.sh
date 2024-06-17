#!/bin/bash
dash_separator="--------------------" # 20 dashes
pylintrc_filename=".pylintrc"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
pylint_enabled=0
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"
source "$script_dir"/scripts/functions.sh "$@"

# pylintrc Setup
if [ "$pylint_enabled" = 1 ]; then
	# If pylint_enabled setup pylintrc
	if [ "$debug" = 1 ]; then
		echo "$dash_separator Setup $pylintrc_filename $dash_separator"
	fi

	source "$script_dir"/scripts/functions.sh "$@" # Loads find_site_package function

	# Install configupdater if it doesn't exist
	configupdater_installed=$(find_site_package configupdater configupdater)

	# Create pylintrc using setup_pylintrc.py
	[ ! -f "$pylintrc_filename" ] && pylintrc_exists=0 || pylintrc_exists=1
	python "$script_dir"/setup_pylintrc.py "$@" --exists="$pylintrc_exists"

	# Remove trailing whitespace from pylintrc
	tmp=$(mktemp)
	sed -e 's/[[:space:]]*$//' <"$pylintrc_filename" >"$tmp"
	mv "$tmp" "$pylintrc_filename"

	# Uninstall configupdater if it didn't exist prior to running this script
	uninstall_site_package configupdater "$configupdater_installed"
	if [ "$debug" = 1 ]; then
		echo ""
	fi
fi
