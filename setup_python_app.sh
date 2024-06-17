#!/bin/bash
#region Variables, Script Dir Validation & Load Functions
current_dir=$PWD
project_name=$(basename "$current_dir")
python_exe="python$python_version"
python_exe="${python_exe:-python3}" # If the specified python version is not installed, default to python3
pylintrc_filename=".pylintrc"
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# script_dir workaround for when a project using this submodule tries to source the 'setup' script file
if [ ! -f "$script_dir"/scripts/functions.sh ]; then
	echo "Failed to find functions.sh in $script_dir/scripts"
	backup_script_path=$(dirname -- "$0")
	echo "Attempting to find functions.sh in $script_dir/$backup_script_path/scripts"
	script_dir="$script_dir/$backup_script_path"
fi

if [ ! -f "$script_dir"/scripts/functions.sh ]; then
	echo "Failed to find functions.sh in $script_dir/scripts"
	echo "Something went teribbly wrong"
	exit 1
fi
source "$script_dir"/scripts/functions.sh "$@"
#endregion

#region Process CLI Options
debug=0
rebuild_venv=0
python_version="3.10"
package_manager="poetry"
is_package=0
isort_profile="black"
python_formatter="black"
overwrite_vscode_launch=0
line_length=120
pre_commit_pylint_entry_prefix="utility-repo-scripts/"

while getopts d:v:r:-: OPT; do
	# support long options: https://stackoverflow.com/a/28466267/519360
	if [ "$OPT" = "-" ]; then  # long option: reformulate OPT and OPTARG
		OPT="${OPTARG%%=*}"       # extract long option name
		OPTARG="${OPTARG#"$OPT"}" # extract long option argument (may be empty)
		OPTARG="${OPTARG#=}"      # if long option argument, remove assigning `=`
	fi
	case "${OPT}" in
	d | debug)
		debug=1
		;;
	r | rebuild_venv)
		rebuild_venv=${OPTARG}
		;;
	python_version)
		python_version=${OPTARG}
		;;
	package_manager)
		package_manager=${OPTARG}
		;;
	is_package)
		is_package=1
		;;
	isort_profile)
		isort_profile=${OPTARG}
		;;
	python_formatter)
		python_formatter=${OPTARG}
		;;
	overwrite_vscode_launch)
		overwrite_vscode_launch=1
		;;
	line_length)
		line_length=${OPTARG}
		;;
	pre_commit_pylint_entry_prefix)
		pre_commit_pylint_entry_prefix=${OPTARG}
		;;
	??*)
		echo "Invalid long option provided (--$OPT). Consider removing this from the setup file"
		;;
	?)
		echo "The only valid short flags supported are ['-d', '-r']"
		;;
	esac
done
#endregion

#region Print Values Before Validation for Debugging
if [ "$debug" = 1 ]; then
	echo "$dash_separator setup_python_app.sh CLI Arguments $dash_separator"
	echo "    -d (--debug): $debug"
	echo "    -r (--rebuild_venv): $rebuild_venv"
	echo "    --python_version: $python_version"
	echo "    --package_manager: $package_manager"
	echo "    --is_package: $is_package"
	echo "    --isort_profile: $isort_profile"
	echo "    --python_formatter: $python_formatter"
	echo "    --overwrite_vscode_launch: $overwrite_vscode_launch"
	echo "    --line_length: $line_length"
	echo "    --pre_commit_pylint_entry_prefix: $pre_commit_pylint_entry_prefix"
	echo ""
fi
#endregion

#region Validate CLI Arguments
if [ "$debug" != 0 ] && [ "$debug" != 1 ]; then
	error "Invalid debug option: ($debug). Valid values are [0, 1]"
fi

if [ "$package_manager" != "pip" ] &&
	[ "$package_manager" != "pip-tools" ] &&
	[ "$package_manager" != "poetry" ]; then
	error "Invalid package_manager option: ($package_manager). Valid values are ['pip', 'pip-tools', 'poetry']"
else
	if [ "$rebuild_venv" != 0 ] && [ "$rebuild_venv" != 1 ]; then
		error "Invalid rebuild_venv option: ($rebuild_venv). Valid values are [0, 1]"
	fi

	if [ "$is_package" != 0 ] && [ "$is_package" != 1 ]; then
		error "Invalid is_package option: ($is_package). Valid values are [0, 1]"
	fi
fi

if [ "$python_version" != "3.8" ] &&
	[ "$python_version" != "3.9" ] &&
	[ "$python_version" != "3.10" ] &&
	[ "$python_version" != "3.11" ]; then
	error "Invalid python_version option: ($python_version). Valid values are ['3.8', '3.9', '3.10', '3.11']"
fi

if [ "$isort_profile" != "" ] &&
	[ "$isort_profile" != "black" ] &&
	[ "$isort_profile" != "django" ] &&
	[ "$isort_profile" != "pycharm" ] &&
	[ "$isort_profile" != "google" ] &&
	[ "$isort_profile" != "open_stack" ] &&
	[ "$isort_profile" != "plone" ] &&
	[ "$isort_profile" != "attrs" ] &&
	[ "$isort_profile" != "hug" ] &&
	[ "$isort_profile" != "wemake" ] &&
	[ "$isort_profile" != "appnexus" ]; then
	error "Invalid isort_profile option: ($isort_profile). Valid values are ['', 'black', 'django', 'pycharm', 'google', 'open_stack', 'plone', 'attrs', 'hug', 'wemake', 'appnexus']"
fi

if [ "$python_formatter" != "" ] &&
	[ "$python_formatter" != "autopep8" ] &&
	[ "$python_formatter" != "black" ]; then
	error "Invalid python_formatter option: ($python_formatter). Valid values are ['', autopep8, black]"
fi

if [ "$overwrite_vscode_launch" != 0 ] && [ "$overwrite_vscode_launch" != 1 ]; then
	error "Invalid overwrite_vscode_launch option: ($overwrite_vscode_launch). Valid values are [0, 1]"
fi
#endregion

#region Virtual Environment Setup
if [ "$debug" = 1 ]; then
	echo "$dash_separator Virtual Environment Setup $dash_separator"
fi

pyenv_installed=0
if command -v pyenv >/dev/null; then
	pyenv_installed=1
fi

if [ "$pyenv_installed" = 1 ]; then
	pyenv install -s "$python_version"

	if [ "$package_manager" = "poetry" ]; then
		# If using this setup script, remove the auto-generated poetry virtual environments
		poetry env remove --all
	fi

	if [ "$package_manager" = "pip" ] || [ "$rebuild_venv" = 1 ]; then
		# We have to always delete the environment if using pip as package manager since it doesn't
		# provide a way to synchronize the dependencies within the virtual environment like pip-tools or poetry
		# We provide an option flag rebuild_venv to force delete the environment if using poetry or pip-tools
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
		echo "    - You might not have pyenv-virtualenv installed. Run 'brew install pyenv-virtualenv' to install it."
		echo "Please try the setup script again."
		exit 1
	fi
else
	echo "pyenv not installed! Please installl pyenv to use this setup script."
	echo "To Install run the following command using brew:"
	echo ""
	echo "brew install pyenv pyenv-virtualenv"
	echo ""
	echo "Exiting..."
	exit 1
fi
echo ""
#endregion

#region Setup Prettier .prettierrc
[ ! -f ".prettierrc" ] && prettierrc_exists=0 || prettierrc_exists=1

if [ "$debug" = 1 ]; then
	echo "$dash_separator .prettierrc Setup $dash_separator"
fi

ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml)
python "$script_dir"/setup_prettierrc.py "$@" --exists="$prettierrc_exists"
uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_installed"
prettier_format .prettierrc

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region pre-commit Setup
[ ! -f ".pre-commit-config.yaml" ] && pre_commit_config_exists=0 || pre_commit_config_exists=1

if [ "$debug" = 1 ]; then
	echo "$dash_separator .pre-commit-config.yaml Setup $dash_separator"
fi

ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml)
python "$script_dir"/setup_pre_commit_config.py "$@" --exists="$pre_commit_config_exists"
uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_installed"
prettier_format .pre-commit-config.yaml

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region pyproject.toml Setup
[ ! -f "pyproject.toml" ] && pyproject_toml_exists=0 || pyproject_toml_exists=1

tomlkit_installed=$(find_site_package tomlkit tomlkit)
python "$script_dir"/setup_pyproject_toml.py "$@" --exists="$pyproject_toml_exists"
uninstall_site_package tomlkit "$tomlkit_installed"

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region pylintrc Setup
if [ "$debug" = 1 ]; then
	echo "$dash_separator Setup $pylintrc_filename $dash_separator"
fi

configupdater_installed=$(find_site_package configupdater configupdater)
[ ! -f "$pylintrc_filename" ] && pylintrc_exists=0 || pylintrc_exists=1
python "$script_dir"/setup_pylintrc.py "$@" --exists="$pylintrc_exists"
uninstall_site_package configupdater "$configupdater_installed"
remove_trailing_whitespace "$pylintrc_filename"

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region .flake8 Setup
if [ "$debug" = 1 ]; then
	echo "$dash_separator Setup .flake8 $dash_separator"
fi

configupdater_installed=$(find_site_package configupdater configupdater)
[ ! -f ".flake8" ] && flake8_exists=0 || flake8_exists=1
python "$script_dir"/setup_flake8.py "$@" --exists="$flake8_exists"
uninstall_site_package configupdater "$configupdater_installed"
remove_trailing_whitespace .flake8

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

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

	# if no test or dev files, check for regular requirements
	if [ "$req_installed" = "0" ] && [ -f "requirements.txt" ]; then
		pip install -r requirements.txt
		req_installed=1
	fi
elif [ "$package_manager" = "pip-tools" ]; then
	pip install --upgrade pip-tools

	[ -f "requirements-dev.txt" ] && dev_requirements=1 || dev_requirements=0
	[ -f "requirements-test.txt" ] && test_requirements=1 || test_requirements=0
	[ -f "requirements.txt" ] && requirements=1 || requirements=0

	if [ "$dev_requirements" = 1 ] && [ "$test_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		pip-sync requirements-dev.txt requirements-test.txt requirements.txt
		req_installed=1
	elif [ "$dev_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		pip-sync requirements-dev.txt requirements.txt
		req_installed=1

	elif [ "$test_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		pip-sync requirements-test.txt requirements.txt
		req_installed=1
	elif [ "$requirements" = 1 ]; then
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
# No need for an else statement since we validate inputs above

# if no requirements files, check for setup.py
if [ "$req_installed" = "0" ] && [ -f "setup.py" ]; then
	if [ "$package_manager" = "poetry" ]; then
		# Poetry does not support setup.py files since it has it's own build system
		error "Poetry does not support setup.py files. Please use a pyproject.toml file instead for Poetry support"
	fi

	pip install -e .
	req_installed=1
fi

if [ "$req_installed" = "0" ]; then
	error "ERROR: Unable to install any dependencies! Consider adding a requirements-dev.txt, requirements-test.txt, and/or requirements.txt. setup.py works as well but is experimental."
fi

echo ""
#endregion

#region Install pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
	if [ "$debug" = 1 ]; then
		echo "$dash_separator pre-commit install & pre-commit autoupdate $dash_separator"
	fi
	pre-commit install
	pre-commit autoupdate
	if [ "$debug" = 1 ]; then
		echo ""
	fi
fi
#endregion

#region Fix Prettier pre-commit hook
if [ "$debug" = 1 ]; then
	echo "$dash_separator .pre-commit-config.yaml Setup $dash_separator"
fi

[ ! -f ".pre-commit-config.yaml" ] && pre_commit_config_exists=0 || pre_commit_config_exists=1

ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml)
python "$script_dir"/setup_fix_prettier_pre_commit.py "$@" --pre_commit_config_exists="$pre_commit_config_exists"
uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_installed"
prettier_format .pre-commit-config.yaml

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region VS Code Settings
if [ "$debug" = 1 ]; then
	echo "$dash_separator VS Code settings.json $dash_separator"
fi

[ ! -f ".vscode/settings.json" ] && vscode_settings_exist=0 || vscode_settings_exist=1
mkdir -p .vscode
python "$script_dir"/setup_vscode_settings.py "$@" --exists="$vscode_settings_exist"
json_sort .vscode/settings.json
prettier_format .vscode/settings.json

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region VS Code Launch
if [ "$debug" = 1 ]; then
	echo "$dash_separator VS Code launch.json $dash_separator"
fi

if [ ! -e .vscode/launch.json ] && [ -e .vscode/launch.sample.json ]; then
	if [ "$overwrite_vscode_launch" = 1 ]; then
		if [ "$debug" = 1 ]; then
			echo "Creating .vscode/launch.json file from .vscode/launch.sample.json template"
		fi
		cp .vscode/launch.sample.json .vscode/launch.json
	else
		if [ "$debug" = 1 ]; then
			echo "Skipping .vscode/launch.json creation. File already exists."
			echo "To overwrite, run this script with the --overwrite_vscode_launch flag"
			echo "Please make a backup of your existing file before performing this action."
		fi
	fi
else
	if [ "$debug" = 1 ]; then
		echo "Skipping .vscode/launch.json creation. No .vscode/launch.sample.json file found."
	fi
fi

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region VS Code Extensions
if [ "$debug" = 1 ]; then
	echo "$dash_separator VS Code Extensions $dash_separator"
fi

if command -v code >/dev/null; then
	if [ "$debug" = 1 ]; then
		echo "Installing VSCode Extensions"
	fi

	installed_extensions=$(code --list-extensions)

	install_vscode_Extension_if_not_installed Boto3typed.boto3-ide "$installed_extensions"
	install_vscode_Extension_if_not_installed bungcip.better-toml "$installed_extensions"
	install_vscode_Extension_if_not_installed ms-python.python "$installed_extensions"
	install_vscode_Extension_if_not_installed ms-python.vscode-pylance "$installed_extensions"
	install_vscode_Extension_if_not_installed editorconfig.editorconfig "$installed_extensions"
	install_vscode_Extension_if_not_installed streetsidesoftware.code-spell-checker "$installed_extensions"
	install_vscode_Extension_if_not_installed visualstudioexptteam.vscodeintellicode "$installed_extensions"
	install_vscode_Extension_if_not_installed esbenp.prettier-vscode "$installed_extensions"
	install_vscode_Extension_if_not_installed ms-python.isort "$installed_extensions"
	install_vscode_Extension_if_not_installed ms-python.pylint "$installed_extensions"
	install_vscode_Extension_if_not_installed ms-python.flake8 "$installed_extensions"

	if [ "$python_formatter" = "black" ]; then
		install_vscode_Extension_if_not_installed ms-python.black-formatter "$installed_extensions"
	elif [ "$python_formatter" = "autopep8" ]; then
		install_vscode_Extension_if_not_installed ms-python.autopep8 "$installed_extensions"
	fi
else
	# VS Code Not Found
	if [ "$debug" = 1 ]; then
		echo "The code command was not found, skipping VSCode settings..."
		echo "To install VSCode, see https://code.visualstudio.com/download"
		echo "If you have VSCode installed, make sure it is in your Applications folder, if on Mac, or in your PATH on Windows/Linux/Mac"
		echo "To add the code command to your path, see https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line"
	fi
fi

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region Custom after setup script
if [ "$debug" = 1 ]; then
	echo "$dash_separator Custom After Setup Script $dash_separator"
fi

custom_script_name=".python_after_setup.sh"
if [ -f "$HOME/$custom_script_name" ]; then
	echo "Running custom after setup script: $HOME/$custom_script_name"
	echo "Update this script to customize your virtual environments after creation"
	"$HOME"/$custom_script_name
else
	echo "No custom after setup script was found at $HOME/$custom_script_name found. The script will be created..."
	echo "Update this script to customize your virtual environments after creation"
	{
		echo "#!$SHELL"
		echo "# This script will run after the setup script in your python repos"
		echo "# Update this script to add extra python packages that you may need for your environment"
		echo "# such as common editor packages"
		echo ""
		echo "# pip install package1 package2"
	} >>"$HOME"/$custom_script_name
	chmod u+x "$HOME"/$custom_script_name
fi

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region Print out the final message
echo "$dash_separator Project setup complete $dash_separator"
echo "Either re-launch $SHELL or run 'pyenv shell $project_name' to activate your virtual environment."
#endregion
