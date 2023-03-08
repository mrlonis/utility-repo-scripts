#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
flake8_enabled=0
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"
source "$script_dir"/scripts/functions.sh "$@" # Loads find_site_package function

# .flake8 Setup
if [ "$flake8_enabled" = 1 ]; then
	# If flake8_enabled setup .flake8
	if [ "$debug" = 1 ]; then
		echo "$dash_separator Setup .flake8 $dash_separator"
	fi

	source "$script_dir"/scripts/functions.sh "$@" # Loads find_site_package function

	# Install configupdater if it doesn't exist
	find_site_package configupdater configupdater
	configupdater_installed="$existed"
	if [ "$debug" = 1 ]; then
		echo "configupdater_installed: $configupdater_installed"
	fi

	# Create .flake8 using setup_flake8.py
	[ ! -f ".flake8" ] && flake8_exists=0 || flake8_exists=1
	python "$script_dir"/setup_flake8.py "$@" --exists="$flake8_exists"

	# Remove trailing whitespace from .flake8
	tmp=$(mktemp)
	sed -e "s/[[:space:]]*$//" <".flake8" >"$tmp"
	mv "$tmp" ".flake8"

	# Uninstall configupdater if it didn't exist prior to running this script
	if [ "$configupdater_installed" = 0 ]; then
		echo "Uninstalling configupdater since it did not exist in the virtual environment prior to running this script"
		pip uninstall -y configupdater
	fi
	if [ "$debug" = 1 ]; then
		echo ""
	fi
fi
