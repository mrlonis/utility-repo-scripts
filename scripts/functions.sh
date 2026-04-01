#!/bin/bash
debug=${debug:-0} # Load debug cli option if it already exists

function find_site_package() {
	local package_name="$1"
	local pypi_name="$2"
	local package_location
	local package_previously_installed
	local package_probe_result
	package_probe_result=$(python -c '
import importlib.util
import sys
import traceback

package_name = sys.argv[1]

try:
    package_spec = importlib.util.find_spec(package_name)
except (ImportError, ModuleNotFoundError):
    print("missing")
except Exception:
    traceback.print_exc()
    raise
else:
    if package_spec is None:
        print("missing")
    else:
        package_location = package_spec.origin or ""
        print(f"present:{package_location}")
' "$package_name")
	local package_probe_status=$?
	if [ "$package_probe_status" -ne 0 ]; then
		return 1
	fi

	case "$package_probe_result" in
	"missing")
		package_location=""
		;;
	"present:"*)
		package_location="${package_probe_result#present:}"
		;;
	*)
		echo "find_site_package(): Unexpected probe result for $package_name: $package_probe_result" >&2
		return 1
		;;
	esac

	if [ "$debug" = 1 ]; then
		echo "find_site_package(): $package_location" >&2
	fi

	if [ "$package_location" = "" ]; then
		if [ "$debug" = 1 ]; then
			echo "find_site_package(): $pypi_name not found" >&2
			echo "find_site_package(): Installing $pypi_name temporarily for this setup step" >&2
		fi
		if ! pip install "$pypi_name"; then
			return 1
		fi
		package_previously_installed=0
	else
		if [ "$debug" = 1 ]; then
			echo "find_site_package(): $pypi_name found" >&2
		fi
		package_previously_installed=1
	fi
	if [ "$debug" = 1 ]; then
		echo "find_site_package(): $package_name exists = $package_previously_installed" >&2
	fi
	printf '%s' "$package_previously_installed"
}

function find_site_distribution() {
	local distribution_name="$1"
	local distribution_previously_installed
	local distribution_probe_result
	distribution_probe_result=$(python -c '
from importlib import metadata
import sys
import traceback

distribution_name = sys.argv[1]

try:
    metadata.distribution(distribution_name)
except metadata.PackageNotFoundError:
    print("missing")
except Exception:
    traceback.print_exc()
    raise
else:
    print("present")
' "$distribution_name")
	local distribution_probe_status=$?
	if [ "$distribution_probe_status" -ne 0 ]; then
		return 1
	fi

	case "$distribution_probe_result" in
	"missing")
		distribution_previously_installed=0
		;;
	"present")
		distribution_previously_installed=1
		;;
	*)
		echo "find_site_distribution(): Unexpected probe result for $distribution_name: $distribution_probe_result" >&2
		return 1
		;;
	esac

	if [ "$debug" = 1 ]; then
		echo "find_site_distribution(): $distribution_name exists = $distribution_previously_installed" >&2
	fi

	printf '%s' "$distribution_previously_installed"
}

function uninstall_site_package() {
	local package_name="$1"
	local package_installed="$2"
	if [ "$package_installed" = 0 ]; then
		echo "Uninstalling $package_name since it did not exist in the virtual environment prior to running this script. Consider adding $package_name as a dev dependency to stop seeing message."
		pip uninstall -y "$package_name"
	fi
}

function prettier_format() {
	file_name="$1"
	if command -v prettier >/dev/null; then
		if [ "$debug" = 1 ]; then
			echo "prettier_format(): prettier found"
			echo "prettier_format(): Formatting $file_name"
		fi
		prettier "$file_name" --write --ignore-path .prettierignore
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
			prettier "$file_name" --write --ignore-path .prettierignore
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

function json_sort() {
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

function print_bash_source_information() {
	echo "Printing BASH_SOURCE array ${BASH_SOURCE[*]}"
	bash_source_dir_name=$(dirname "${BASH_SOURCE[0]}")
	echo "bash_source_dir_name = $bash_source_dir_name"
	bash_source_length=${#BASH_SOURCE[@]}
	echo "bash_source_length = $bash_source_length"

	echo "pwd: $(pwd)"
	echo "\$0: $0"
	echo "basename: $(basename -- "$0")"
	echo "dirname: $(dirname -- "$0")"
	echo "dirname/readlink: $(dirname -- "$(readlink -f -- "$0")")"
	echo ""
}

function remove_trailing_whitespace() {
	filename="$1"
	tmp=$(mktemp)
	sed -e 's/[[:space:]]*$//' <"$filename" >"$tmp"
	mv "$tmp" "$filename"
}

function in_list() {
	LIST=$1
	DELIMITER=$2
	VALUE=$3
	[[ "$LIST" =~ ($DELIMITER|^)$VALUE($DELIMITER|$) ]]
}

function install_vscode_Extension_if_not_installed() {
	extension_name="$1"
	installed_extensions="$2"

	if ! printf '%s\n' "$installed_extensions" | grep -Fxq -- "$extension_name"; then
		code --install-extension "$extension_name" --force >/dev/null
	fi
}

function ensure_vscode_launch_file() {
	local sample_launch_path="$1"
	local launch_path="$2"
	local overwrite_launch="$3"
	local debug_enabled="$4"

	if [ ! -e "$sample_launch_path" ]; then
		if [ "$debug_enabled" = 1 ]; then
			echo "Skipping $launch_path creation. No $sample_launch_path file found."
		fi
		return 0
	fi

	if [ ! -e "$launch_path" ]; then
		if [ "$debug_enabled" = 1 ]; then
			echo "Creating $launch_path file from $sample_launch_path template"
		fi
		cp "$sample_launch_path" "$launch_path"
		return $?
	fi

	if [ "$overwrite_launch" = 1 ]; then
		if [ "$debug_enabled" = 1 ]; then
			echo "Overwriting $launch_path file from $sample_launch_path template"
		fi
		cp "$sample_launch_path" "$launch_path"
	elif [ "$debug_enabled" = 1 ]; then
		echo "Skipping $launch_path creation. File already exists."
		echo "To overwrite, run this script with the --overwrite_vscode_launch flag"
		echo "Please make a backup of your existing file before performing this action."
	fi
}

function error() {
	# complain to STDERR and exit with error
	echo "$*" >&2
	exit 2
}
