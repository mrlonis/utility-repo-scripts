#!/bin/bash
debug=${debug:-0} # Load debug cli option if it already exists

find_site_package() {
	package_name="$1"
	pypi_name="$2"
	package_location=$(python -c "import $package_name; print($package_name.__file__)")
	if [ "$debug" = 1 ]; then
		echo "find_site_package(): $package_location"
	fi

	if [ "$package_location" = "" ]; then
		if [ "$debug" = 1 ]; then
			echo "find_site_package(): $pypi_name not found"
			echo "find_site_package(): Installing $pypi_name temporarily for pre-commit setup"
		fi
		pip install "$pypi_name"
		exists=0
	else
		if [ "$debug" = 1 ]; then
			echo "find_site_package(): $pypi_name found"
		fi
		exists=1
	fi
	if [ "$debug" = 1 ]; then
		echo "find_site_package(): $package_name exists = $exists"
	fi
	return $exists
}

uninstall_site_package() {
	package_name="$1"
	package_installed="$2"
	if [ "$package_installed" = 0 ]; then
		echo "Uninstalling $package_name since it did not exist in the virtual environment prior to running this script. Consider adding $package_name as a dev dependency to stop seeing message."
		pip uninstall -y "$package_name"
	fi
}

prettier_format() {
	file_name="$1"
	if command -v prettier >/dev/null; then
		if [ "$debug" = 1 ]; then
			echo "prettier_format(): prettier found"
			echo "prettier_format(): Formatting $file_name"
		fi
		prettier --write "$file_name"
		return 0
	else
		if [ "$debug" = 1 ]; then
			echo "prettier_format(): prettier not found"
		fi

		if command -v npm >/dev/null; then
			if [ "$debug" = 1 ]; then
				echo "prettier_format(): npm found"
				echo "prettier_format(): Installing prettier globally to format $file_name"
			fi
			npm install -g prettier
			prettier --write "$file_name"
			return 0
		else
			if [ "$debug" = 1 ]; then
				echo "prettier_format(): npm not found"
				echo "prettier_format(): Skipping formatting of $file_name"
			fi
		fi
	fi
	return 1
}

json_sort() {
	file_path="$1"
	if command -v sort-json >/dev/null; then
		if [ "$debug" = 1 ]; then
			echo "sort-json found"
			echo "Sorting $file_path"
		fi
		sort-json "$file_path"
		return 0
	else
		if [ "$debug" = 1 ]; then
			echo "sort-json not found"
		fi

		if command -v npm >/dev/null; then
			if [ "$debug" = 1 ]; then
				echo "npm found"
				echo "Installing sort-json globally to format $file_path"
			fi
			npm install -g sort-json
			sort-json "$file_path"
			return 0
		else
			if [ "$debug" = 1 ]; then
				echo "npm not found"
				echo "Skipping sorting of $file_path"
			fi
		fi
	fi
	return 1
}
