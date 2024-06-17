#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
debug=0
package_manager="pip"
source "$script_dir"/scripts/process_cli_options.sh "$@"

#region Install Dependencies
if [ "$debug" = 1 ]; then
	echo "$dash_separator Installing Dependencies $dash_separator"
fi

# Install Common Dependencies
python -m pip install --upgrade pip
pip install --upgrade setuptools
pip install wheel

if [ -f "tox.ini" ]; then
	pip install tox
fi

# Install requirements
req_installed=0
if [ "$package_manager" = "pip" ]; then
	if [ -f "requirements-dev.txt" ]; then
		pip install -r requirements-dev.txt
		req_installed=1
	elif [ -f "requirements-test.txt" ]; then
		pip install -r requirements-test.txt
		req_installed=1
	fi

	### if no test or dev files, check for regular requirements
	if [ "$req_installed" = "0" ] && [ -f "requirements.txt" ]; then
		pip install -r requirements.txt
		req_installed=1
	fi
elif [ "$package_manager" = "pip-tools" ]; then
	pip install --upgrade pip-tools

	[ -f "requirements-dev.txt" ] && dev_requirements=1 || dev_requirements=0
	[ -f "requirements-test.txt" ] && test_requirements=1 || test_requirements=0
	[ -f "requirements.txt" ] && requirements=1 || requirements=0

	if [ "$debug" = 1 ]; then
		echo "dev_requirements: $dev_requirements"
		echo "test_requirements: $test_requirements"
		echo "requirements: $requirements"
	fi

	if [ "$dev_requirements" = 1 ] && [ "$test_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		if [ "$debug" = 1 ]; then
			echo "Found all requirements files. Installing dev, test and prod requirements"
		fi
		pip-sync requirements-dev.txt requirements-test.txt requirements.txt
		req_installed=1
	elif [ "$dev_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		if [ "$debug" = 1 ]; then
			echo "Found dev and prod requirements files. Installing dev and prod requirements"
		fi
		pip-sync requirements-dev.txt requirements.txt
		req_installed=1

	elif [ "$test_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		if [ "$debug" = 1 ]; then
			echo "Found test and prod requirements files. Installing test and prod requirements"
		fi
		pip-sync requirements-test.txt requirements.txt
		req_installed=1
	elif [ "$requirements" = 1 ]; then
		if [ "$debug" = 1 ]; then
			echo "Found prod requirements file. Installing prod requirements"
		fi
		pip-sync requirements.txt
		req_installed=1
	fi
elif [ "$package_manager" = "poetry" ]; then
	[ -f "pyproject.toml" ] && py_project_toml=1 || py_project_toml=0

	if [ "$py_project_toml" = 0 ]; then
		error "pyproject.toml not found. Cannot install requirements via Poetry"
	fi

	if [ "$debug" = 1 ]; then
		echo "Found pyproject.toml. Installing requirements via Poetry"
	fi

	poetry install --sync
	echo "Calling poetry show -o to list outdated packages"
	poetry show -o
	echo "Consider running poetry update and using poetry show -o to update your packages."
	req_installed=1
fi
### No need for an else statement since we validate inputs above

### if no requirements files, check for setup.py
if [ "$req_installed" = "0" ] && [ -f "setup.py" ]; then
	if [ "$package_manager" = "poetry" ]; then
		# Poetry does not support setup.py files since it has it's own build system
		error "Poetry does not support setup.py files. Please use a pyproject.toml file instead for Poetry support"
	fi

	pip install -e .
	req_installed=1
fi
echo ""
#endregion
