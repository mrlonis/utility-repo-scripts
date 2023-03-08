#!/bin/bash
dash_separator="--------------------" # 20 dashes
pylintrc_filename=".pylintrc"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
pylint_enabled=0
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"

# pylintrc Setup
if [ "$pylint_enabled" = 1 ]; then
	# If pylint_enabled setup pylintrc
	if [ "$debug" = 1 ]; then
		echo "$dash_separator Setup $pylintrc_filename $dash_separator"
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
				echo "Installing $pypi_name temporarily for $pylintrc_filename setup"
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

	# Create pylintrc using setup_pylintrc.py
	[ ! -f "$pylintrc_filename" ] && pylintrc_exists=0 || pylintrc_exists=1
	python "$script_dir"/setup_pylintrc.py "$@" --exists="$pylintrc_exists"

	# Remove trailing whitespace from pylintrc
	tmp=$(mktemp)
	sed -e 's/[[:space:]]*$//' <"$pylintrc_filename" >"$tmp"
	mv "$tmp" "$pylintrc_filename"

	# Uninstall configupdater if it didn't exist prior to running this script
	if [ "$configupdater_installed" = 0 ]; then
		echo "Uninstalling configupdater since it did not exist in the virtual environment prior to running this script"
		pip uninstall -y configupdater
	fi
	if [ "$debug" = 1 ]; then
		echo ""
	fi
fi
