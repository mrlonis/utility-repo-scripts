#!/bin/bash
#region Variables, Script Dir Validation & Load Functions
current_dir=$PWD
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
	echo "Something went terribly wrong"
	exit 1
fi
source "$script_dir"/scripts/functions.sh "$@"
#endregion

#region Process CLI Options
debug=0
rebuild_venv=0
python_version="3.14.3"
package_manager="poetry"
is_package=0
include_jumanji_house=1
include_prettier=1
include_isort=1
isort_profile="black"
python_formatter="black"
pylint_enabled=1
flake8_enabled=1
mypy_enabled=1
pytest_enabled=1
unittest_enabled=0
pre_commit_autoupdate=0
overwrite_vscode_launch=0
line_length=120
pre_commit_pylint_entry_prefix="utility-repo-scripts/"

while getopts dr:-: OPT; do
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
	include_jumanji_house)
		include_jumanji_house=${OPTARG:-1}
		;;
	include_prettier)
		include_prettier=${OPTARG:-1}
		;;
	include_isort)
		include_isort=${OPTARG:-1}
		;;
	isort_profile)
		isort_profile=${OPTARG}
		;;
	python_formatter)
		python_formatter=${OPTARG}
		;;
	pylint_enabled)
		pylint_enabled=${OPTARG:-1}
		;;
	flake8_enabled)
		flake8_enabled=${OPTARG:-1}
		;;
	mypy_enabled)
		mypy_enabled=${OPTARG:-1}
		;;
	pytest_enabled)
		pytest_enabled=${OPTARG:-1}
		;;
	unittest_enabled)
		unittest_enabled=${OPTARG:-1}
		;;
	pre_commit_autoupdate)
		pre_commit_autoupdate=${OPTARG:-1}
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
	echo "    --include_jumanji_house: $include_jumanji_house"
	echo "    --include_prettier: $include_prettier"
	echo "    --include_isort: $include_isort"
	echo "    --isort_profile: $isort_profile"
	echo "    --python_formatter: $python_formatter"
	echo "    --pylint_enabled: $pylint_enabled"
	echo "    --flake8_enabled: $flake8_enabled"
	echo "    --mypy_enabled: $mypy_enabled"
	echo "    --pytest_enabled: $pytest_enabled"
	echo "    --unittest_enabled: $unittest_enabled"
	echo "    --pre_commit_autoupdate: $pre_commit_autoupdate"
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
	[ "$package_manager" != "poetry" ] &&
	[ "$package_manager" != "uv-pip" ] &&
	[ "$package_manager" != "uv" ]; then
	error "Invalid package_manager option: ($package_manager). Valid values are ['pip', 'pip-tools', 'poetry', 'uv-pip', 'uv']"
else
	if [ "$rebuild_venv" != 0 ] && [ "$rebuild_venv" != 1 ]; then
		error "Invalid rebuild_venv option: ($rebuild_venv). Valid values are [0, 1]"
	fi

	if [ "$is_package" != 0 ] && [ "$is_package" != 1 ]; then
		error "Invalid is_package option: ($is_package). Valid values are [0, 1]"
	fi
fi

if [ -z "$python_version" ] || [[ "$python_version" == -* ]]; then
	error "Invalid python_version option: ($python_version). Valid values are any non-empty pyenv install version string"
fi

if [ "$include_jumanji_house" != 0 ] && [ "$include_jumanji_house" != 1 ]; then
	error "Invalid include_jumanji_house option: ($include_jumanji_house). Valid values are [0, 1]"
fi

if [ "$include_prettier" != 0 ] && [ "$include_prettier" != 1 ]; then
	error "Invalid include_prettier option: ($include_prettier). Valid values are [0, 1]"
fi

if [ "$include_isort" != 0 ] && [ "$include_isort" != 1 ]; then
	error "Invalid include_isort option: ($include_isort). Valid values are [0, 1]"
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

if [ "$pylint_enabled" != 0 ] && [ "$pylint_enabled" != 1 ]; then
	error "Invalid pylint_enabled option: ($pylint_enabled). Valid values are [0, 1]"
fi

if [ "$flake8_enabled" != 0 ] && [ "$flake8_enabled" != 1 ]; then
	error "Invalid flake8_enabled option: ($flake8_enabled). Valid values are [0, 1]"
fi

if [ "$mypy_enabled" != 0 ] && [ "$mypy_enabled" != 1 ]; then
	error "Invalid mypy_enabled option: ($mypy_enabled). Valid values are [0, 1]"
fi

if [ "$pytest_enabled" != 0 ] && [ "$pytest_enabled" != 1 ]; then
	error "Invalid pytest_enabled option: ($pytest_enabled). Valid values are [0, 1]"
fi

if [ "$unittest_enabled" != 0 ] && [ "$unittest_enabled" != 1 ]; then
	error "Invalid unittest_enabled option: ($unittest_enabled). Valid values are [0, 1]"
fi

if [ "$pre_commit_autoupdate" != 0 ] && [ "$pre_commit_autoupdate" != 1 ]; then
	error "Invalid pre_commit_autoupdate option: ($pre_commit_autoupdate). Valid values are [0, 1]"
fi

if [ "$overwrite_vscode_launch" != 0 ] && [ "$overwrite_vscode_launch" != 1 ]; then
	error "Invalid overwrite_vscode_launch option: ($overwrite_vscode_launch). Valid values are [0, 1]"
fi

if [ "$package_manager" = "uv" ] || [ "$package_manager" = "uv-pip" ]; then
	uv_installed=0
	if command -v uv >/dev/null; then
		uv_installed=1
	fi

	if [ "$uv_installed" != 1 ]; then
		echo "uv not installed! Please install uv to use this setup script."
		echo "To Install run one of the following commands:"
		echo ""
		echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
		echo "brew install uv"
		echo ""
		echo "Exiting..."
		exit 1
	fi
fi
#endregion

#region Virtual Environment Setup
if [ "$debug" = 1 ]; then
	echo "$dash_separator Virtual Environment Setup $dash_separator"
fi

venv_dir="$current_dir/.venv"
venv_activate_path="$venv_dir/bin/activate"
venv_python_path="$venv_dir/bin/python"
pyenv_installed=0
if command -v pyenv >/dev/null; then
	pyenv_installed=1
fi

if [ "$pyenv_installed" = 1 ]; then
	eval "$(pyenv init - bash)"

	pyenv install -s "$python_version"
	pyenv local "$python_version"

	rebuild_reason=""
	if [ "$package_manager" = "pip" ]; then
		# We have to always delete the environment if using pip as package manager since it doesn't
		# provide a way to synchronize the dependencies within the virtual environment like pip-tools or poetry
		# We provide an option flag rebuild_venv to force delete the environment if using poetry or pip-tools
		rebuild_reason="pip package manager requires a clean virtual environment"
	elif [ "$rebuild_venv" = 1 ]; then
		rebuild_reason="--rebuild_venv is enabled"
	elif [ ! -x "$venv_python_path" ] || [ ! -f "$venv_activate_path" ]; then
		rebuild_reason="virtual environment is missing or incomplete"
	fi

	if [ "$rebuild_reason" != "" ]; then
		if [ "$debug" = 1 ]; then
			echo "Preparing virtual environment at $venv_dir"
			echo "Reason: $rebuild_reason"
		fi
		rm -rf "$venv_dir"
	fi

	if [ ! -x "$venv_python_path" ] || [ ! -f "$venv_activate_path" ]; then
		pyenv_python=$(PYENV_VERSION="$python_version" pyenv which python)
		echo "pyenv_python: $pyenv_python"
		if [ "$pyenv_python" = "" ] || [ ! -x "$pyenv_python" ]; then
			echo "pyenv failed to resolve the requested python version ($python_version)."
			echo "Please verify the version is installed and try the setup script again."
			exit 1
		fi

		"$pyenv_python" -m venv "$venv_dir"
	elif [ "$debug" = 1 ]; then
		echo "Reusing existing virtual environment at $venv_dir"
	fi

	if [ ! -f "$venv_activate_path" ]; then
		echo "python -m venv failed to create a virtual environment for this project."
		echo "Expected activation script was not found at $venv_activate_path."
		echo "Please try the setup script again."
		exit 1
	fi

	# shellcheck disable=SC1090
	source "$venv_activate_path"

	venv_python=$(command -v python)
	echo "venv_python: $venv_python"
	if [ "$venv_python" = "" ] || [ "$venv_python" != "$venv_python_path" ]; then
		echo "The project virtual environment failed to activate from $venv_dir."
		echo ""
		echo "Possible reasons include:"
		echo "    - The activation script did not update your shell PATH as expected."
		echo "    - The virtual environment already exists and is linked to a different python version."
		echo "        - In this case run ./setup 1 to force a rebuild of the virtual environment."
		echo "    - The requested python version could not create virtual environments on this system."
		echo "Please try the setup script again."
		exit 1
	fi

	if [ "$package_manager" = "poetry" ]; then
		export POETRY_VIRTUALENVS_IN_PROJECT=true
	fi
else
	echo "pyenv not installed! Please install pyenv to use this setup script."
	echo "To Install run the following command using brew:"
	echo ""
	echo "brew install pyenv"
	echo ""
	echo "Exiting..."
	exit 1
fi
echo ""
#endregion

#region Install Dependencies
if [ "$debug" = 1 ]; then
	echo "$dash_separator Installing Dependencies $dash_separator"
fi

# Install Common Dependencies
if [ "$package_manager" != "uv" ] && [ "$package_manager" != "uv-pip" ]; then
	python -m pip install --upgrade pip
	pip install --upgrade setuptools
	pip install wheel

	if [ -f "tox.ini" ]; then
		pip install tox
	fi
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
elif [ "$package_manager" = "uv-pip" ]; then
	[ -f "requirements-dev.txt" ] && dev_requirements=1 || dev_requirements=0
	[ -f "requirements-test.txt" ] && test_requirements=1 || test_requirements=0
	[ -f "requirements.txt" ] && requirements=1 || requirements=0

	if [ "$dev_requirements" = 1 ] && [ "$test_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		uv pip sync requirements-dev.txt requirements-test.txt requirements.txt
		req_installed=1
	elif [ "$dev_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		uv pip sync requirements-dev.txt requirements.txt
		req_installed=1
	elif [ "$test_requirements" = 1 ] && [ "$requirements" = 1 ]; then
		uv pip sync requirements-test.txt requirements.txt
		req_installed=1
	elif [ "$requirements" = 1 ]; then
		uv pip sync requirements.txt
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

	poetry sync
	echo "Calling poetry show -o to list outdated packages"
	poetry show -o
	echo "Consider running poetry update and using poetry show -o to update your packages."
	req_installed=1
elif [ "$package_manager" = "uv" ]; then
	[ -f "pyproject.toml" ] && py_project_toml=1 || py_project_toml=0

	if [ "$py_project_toml" = 0 ]; then
		error "pyproject.toml not found. Cannot install requirements via uv"
	fi

	if [ "$debug" = 1 ]; then
		echo "Found pyproject.toml. Installing requirements via uv"
	fi

	uv sync
	req_installed=1
fi
# No need for an else statement since we validate inputs above

# if no requirements files, check for setup.py
if [ "$req_installed" = "0" ] && [ -f "setup.py" ]; then
	if [ "$package_manager" = "poetry" ] || [ "$package_manager" = "uv" ]; then
		# Poetry and uv native project support both depend on pyproject.toml
		error "$package_manager does not support setup.py files. Please use a pyproject.toml file instead for $package_manager support"
	fi

	if [ "$package_manager" = "uv-pip" ]; then
		uv pip install -e .
	else
		pip install -e .
	fi
	req_installed=1
fi

if [ "$req_installed" = "0" ]; then
	error "ERROR: Unable to install any dependencies! Consider adding a requirements-dev.txt, requirements-test.txt, requirements.txt, and/or pyproject.toml. setup.py works as well but is experimental."
fi

echo ""
#endregion

#region Setup Prettier .prettierrc
[ ! -f ".prettierrc" ] && prettierrc_exists=0 || prettierrc_exists=1

if [ "$debug" = 1 ]; then
	echo "$dash_separator .prettierrc Setup $dash_separator"
fi

if ! ruamel_yaml_clib_installed=$(find_site_distribution ruamel.yaml.clib); then
	error "Failed to determine whether ruamel.yaml.clib is installed"
fi
if ! ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml); then
	error "Failed to locate or temporarily install ruamel.yaml"
fi
python "$script_dir"/setup_prettierrc.py "$@" --exists="$prettierrc_exists"
uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_clib_installed"
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

if ! ruamel_yaml_clib_installed=$(find_site_distribution ruamel.yaml.clib); then
	error "Failed to determine whether ruamel.yaml.clib is installed"
fi
if ! ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml); then
	error "Failed to locate or temporarily install ruamel.yaml"
fi
python "$script_dir"/setup_pre_commit_config.py "$@" --exists="$pre_commit_config_exists"
uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_clib_installed"
prettier_format .pre-commit-config.yaml

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region pyproject.toml Setup
[ ! -f "pyproject.toml" ] && pyproject_toml_exists=0 || pyproject_toml_exists=1

if ! tomlkit_installed=$(find_site_package tomlkit tomlkit); then
	error "Failed to locate or temporarily install tomlkit"
fi
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

if ! configupdater_installed=$(find_site_package configupdater configupdater); then
	error "Failed to locate or temporarily install configupdater"
fi
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

if ! configupdater_installed=$(find_site_package configupdater configupdater); then
	error "Failed to locate or temporarily install configupdater"
fi
[ ! -f ".flake8" ] && flake8_exists=0 || flake8_exists=1
python "$script_dir"/setup_flake8.py "$@" --exists="$flake8_exists"
uninstall_site_package configupdater "$configupdater_installed"
remove_trailing_whitespace .flake8

if [ "$debug" = 1 ]; then
	echo ""
fi
#endregion

#region Install pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
	if [ "$debug" = 1 ]; then
		echo "$dash_separator pre-commit install $dash_separator"
	fi
	pre-commit install
	if [ "$debug" = 1 ]; then
		echo ""
	fi
fi
#endregion

#region pre-commit autoupdate
if [ -f ".pre-commit-config.yaml" ] && [ "$pre_commit_autoupdate" = 1 ]; then
	if [ "$debug" = 1 ]; then
		echo "$dash_separator pre-commit autoupdate $dash_separator"
	fi
	pre-commit autoupdate
	if [ "$debug" = 1 ]; then
		echo ""
	fi
elif [ -f ".pre-commit-config.yaml" ] && [ "$debug" = 1 ]; then
	echo "Skipping pre-commit autoupdate because --pre_commit_autoupdate is disabled"
	echo ""
fi
#endregion

#region Fix Prettier pre-commit hook
if [ "$include_prettier" = 1 ]; then
	if [ "$debug" = 1 ]; then
		echo "$dash_separator .pre-commit-config.yaml Setup $dash_separator"
	fi

	[ ! -f ".pre-commit-config.yaml" ] && pre_commit_config_exists=0 || pre_commit_config_exists=1

	if ! ruamel_yaml_clib_installed=$(find_site_distribution ruamel.yaml.clib); then
		error "Failed to determine whether ruamel.yaml.clib is installed"
	fi
	if ! ruamel_yaml_installed=$(find_site_package ruamel.yaml ruamel.yaml); then
		error "Failed to locate or temporarily install ruamel.yaml"
	fi
	python "$script_dir"/setup_fix_prettier_pre_commit.py "$@" --pre_commit_config_exists="$pre_commit_config_exists"
	uninstall_site_package ruamel.yaml "$ruamel_yaml_installed"
	uninstall_site_package ruamel.yaml.clib "$ruamel_yaml_clib_installed"
	prettier_format .pre-commit-config.yaml

	if [ "$debug" = 1 ]; then
		echo ""
	fi
elif [ "$debug" = 1 ]; then
	echo "Skipping Prettier pre-commit hook fix because --include_prettier is disabled"
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

ensure_vscode_launch_file ".vscode/launch.sample.json" ".vscode/launch.json" "$overwrite_vscode_launch" "$debug"

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

	install_vscode_Extension_if_not_installed ms-python.python "$installed_extensions"
	install_vscode_Extension_if_not_installed ms-python.vscode-pylance "$installed_extensions"
	install_vscode_Extension_if_not_installed editorconfig.editorconfig "$installed_extensions"
	install_vscode_Extension_if_not_installed streetsidesoftware.code-spell-checker "$installed_extensions"
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
echo "Run 'source .venv/bin/activate' to activate your virtual environment."
#endregion
