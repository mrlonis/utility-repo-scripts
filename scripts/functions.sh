#!/bin/bash
debug=${debug:-0} # Load debug cli option if it already exists

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
		export existed=0
	else
		if [ "$debug" = 1 ]; then
			echo "$pypi_name found"
		fi
		export existed=1
	fi
}
