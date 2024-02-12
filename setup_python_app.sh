#!/bin/bash
debug=0
dash_separator="--------------------" # 20 dashes

if [ "$debug" = 1 ]; then
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
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# script_dir workaround for when a project using this submodule tries to source the 'setup' script file
if [ ! -f "$script_dir"/scripts/process_cli_options.sh ]; then
	echo "Failed to find process_cli_options.sh in $script_dir/scripts"
	backup_script_path=$(dirname -- "$0")
	echo "Attempting to find process_cli_options.sh in $script_dir/$backup_script_path/scripts"
	script_dir="$script_dir/$backup_script_path"
fi

if [ ! -f "$script_dir"/scripts/process_cli_options.sh ]; then
	echo "Failed to find process_cli_options.sh in $script_dir/scripts"
	echo "Something went teribbly wrong"
	exit 1
fi

# Process CLI Arguments
python_version="3.10"
package_manager="pip"
rebuild_venv=0
source "$script_dir"/scripts/process_cli_options.sh "$@" --script_name="setup_python_app.sh" --print_options=1

# Variables
venv_folder_location="${WORKON_HOME:-"$HOME/.venvs"}"
current_dir=$PWD
project_name=$(basename "$current_dir")
python_exe="python$python_version"
python_exe="${python_exe:-python3}" # If the specified python version is not installed, default to python3
venv_location="$venv_folder_location/$project_name"
venv_activate_location="$venv_location/bin/activate"

#region Virtual Environment Setup
echo "$dash_separator Virtual Environment Setup $dash_separator"

pyenv_installed=0
if command -v pyenv >/dev/null; then
	pyenv_installed=1
fi

use_pyenv=0
if [ "$pyenv_installed" = 1 ]; then
	echo "pyenv Installed! Using pyenv to setup project..."
	use_pyenv=1
	pyenv install -s "$python_version"

	if [ "$package_manager" = "poetry" ]; then
		# If using this setup script, remove the auto-generated poetry virtual environments
		poetry env remove --all
	fi

	if [ "$package_manager" = "pip" ] || [ "$rebuild_venv" = 1 ]; then
		# We have to always delete the environment if using pip as package manager since it doesn't
		# provide a way to synchronize the dependencies within the virtual environment like pip-tools or poetry
		# We provide an option plag rebuild_venv to force delete the environment if using poetry or pip-tools
		if [ "$debug" = 1 ]; then
			echo "Rebuilding virtual environment"
		fi
		pyenv virtualenv-delete -f "$project_name"
	fi

	pyenv virtualenv -f "$python_version" "$project_name"
	pyenv local "$project_name"
	export PYENV_VERSION="$project_name"
	eval "$(pyenv init -)"
	PYENV_VIRTUALENV_DISABLE_PROMPT=1 pyenv shell "$project_name"

	pyenv_python=$(pyenv which python)
	echo "pyenv_python: $pyenv_python"
	if [ "$pyenv_python" = "" ] || [[ ! "$pyenv_python" == *"$project_name"* ]]; then
		echo "pyenv virtualenv failed to create a virtual environment for this project."
		echo ""
		echo "Possible reasons include:"
		echo "    - The python executable from pyenv is mapped to a different virtual environment than the one we created."
		echo "        - This can happen if you haven't set a global pyenv version. Try running 'pyenv global <version>' to set a global version and then re-launch your SHELL."
		echo "    - The virtual environment already exists and is mapped to a different python version. In this case run ./setup 1 to force a rebuild of the virtual environment. If this doesn't work consider reading the README.md for the utility-repo-scripts repository."
		echo "Please try the setup script again."
		exit 1
	fi
else
	echo "Using python from brew or system to setup project..."

	if [ "$package_manager" = "pip" ] || [ "$rebuild_venv" = 1 ]; then
		if [ "$debug" = 1 ]; then
			echo "Rebuilding virtual environment"
		fi
		deactivate 2>/dev/null || true # deactivate the current virtual environment if it exists
		rm -rf "$venv_location"
	fi

	set -e # make sure we exit if this fails, otherwise we may corrupt the main environment
	if [ -d "$venv_location" ]; then
		if [ "$debug" = 1 ]; then
			echo "Found $venv_location folder"
		fi
	else
		if [ "$debug" = 1 ]; then
			echo "Did not find $venv_location folder. Creating virtual environment"
		fi
		$python_exe -m venv "$venv_location"
	fi
	if [ "$debug" = 1 ]; then
		echo "Activating virtual environment"
	fi
	# shellcheck disable=SC1090
	source "$venv_activate_location"
	set +e
fi
echo ""
#endregion

# pre-commit Setup
"$script_dir"/setup_pre_commit_config.sh "$@"

# pyproject.toml Setup
"$script_dir"/setup_pyproject_toml.sh "$@"

# pylintrc Setup
"$script_dir"/setup_pylintrc.sh "$@"

# .flake8 Setup
"$script_dir"/setup_flake8.sh "$@"

# Install Dependencies
"$script_dir"/setup_install_dependencies.sh "$@"

# Install pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
	echo "$dash_separator pre-commit install & pre-commit autoupdate $dash_separator"
	pre-commit install
	pre-commit autoupdate
	echo ""
fi

# Setup VS Code
"$script_dir"/setup_vscode.sh "$@" --use_pyenv="$use_pyenv"

# Custom after setup script
"$script_dir"/setup_custom_after_setup_script.sh "$@"

# Print out the final message
echo "$dash_separator Project setup complete $dash_separator"
if [ "$use_pyenv" = 1 ]; then
	echo "Either re-launch $SHELL or run 'pyenv shell $project_name' to activate your virtual environment"
	echo ""
	echo "You can also have the setup script activate the virtual environment for you on exit."
	echo "To do this run 'source setup' instead of './setup'."
else
	echo "Run 'source $venv_activate_location' to activate your virtual environment"
	echo "If using virtualenvwrapper, run 'workon $project_name' to activate your virtual environment"
	if [ "$debug" = 1 ]; then
		echo "To learn about virtualenvwrapper, go to https://virtualenvwrapper.readthedocs.io/en/latest/"
	fi
fi
