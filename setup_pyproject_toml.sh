#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"

# Configure pyproject.toml
[ ! -f "pyproject.toml" ] && pyproject_toml_exists=0 || pyproject_toml_exists=1
if [ "$debug" = 1 ]; then
	echo "$dash_separator pyproject.toml Setup $dash_separator"
	echo "pyproject_toml_exists: $pyproject_toml_exists"
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
			echo "Installing $pypi_name temporarily for pre-commit setup"
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

# Install toml if it doesn't exist
find_site_package tomlkit tomlkit
tomlkit_installed="$existed"
if [ "$debug" = 1 ]; then
	echo "tomlkit_installed: $tomlkit_installed"
fi

# Create .pre-commit-config.yaml using setup_pyproject_toml.py
python "$script_dir"/setup_pyproject_toml.py "$@" --exists="$pyproject_toml_exists"

# Uninstall tomlkit if it didn't exist prior to running this script
if [ "$tomlkit_installed" = 0 ]; then
	echo "Uninstalling tomlkit since it did not exist in the virtual environment prior to running this script"
	pip uninstall -y tomlkit
fi
if [ "$debug" = 1 ]; then
	echo ""
fi
