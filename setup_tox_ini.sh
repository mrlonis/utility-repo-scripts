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

	find_site_package() {
		package_name="$1"
		pypi_name="$2"
		package_location=$(python -c "import $package_name; print($package_name.__file__)")
		if [ "$debug" = 1 ]; then
			echo "$package_location"
		fi

		if [ "$package_location" = "" ]; then
			if [ "$debug" = 1 ]; then
				echo "$pypi_name not found"
				echo "Installing $pypi_name temporarily for $tox_ini_filename setup"
			fi
			pip install "$pypi_name"
			existed=0
		else
			if [ "$debug" = 1 ]; then
				echo "$pypi_name found"
			fi
			existed=1
		fi
	}

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
