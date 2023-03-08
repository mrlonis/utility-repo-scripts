#!/bin/bash
dash_separator="--------------------" # 20 dashes

error() {
	# complain to STDERR and exit with error
	echo "$*" >&2
	exit 2
}

# Script Option Defaults
use_pyenv=0
debug=0
package_manager="pip"
rebuild_venv=0
python_version="3.10"
is_package=0
include_jumanji_house=0
include_prettier=0
include_isort=0
isort_profile=""
python_formatter=""
pylint_enabled=0
flake8_enabled=0
pydocstyle_enabled=0
pycodestyle_enabled=0
bandit_enabled=0
mypy_enabled=0
prospector_enabled=0
pylama_enabled=0
pytest_enabled=0
unittest_enabled=0
overwrite_vscode_launch=0
line_length=125
pre_commit_pylint_entry_prefix="utility-repo-scripts/"

# Variables to be set by CLI Options for logging dynamics
remove_parsed_args=0
script_name="process_cli_options.sh"
print_options=0

#region Process CLI Options
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
	v | package_manager)
		package_manager=${OPTARG}
		;;
	r | rebuild_venv)
		rebuild_venv=${OPTARG}
		;;
	python_version)
		python_version=${OPTARG}
		;;
	is_package)
		is_package=1
		;;
	include_jumanji_house)
		include_jumanji_house=1
		;;
	include_prettier)
		include_prettier=1
		;;
	include_isort)
		include_isort=1
		;;
	isort_profile)
		isort_profile=${OPTARG}
		;;
	python_formatter)
		python_formatter=${OPTARG}
		;;
	pylint_enabled)
		pylint_enabled=1
		;;
	flake8_enabled)
		flake8_enabled=1
		;;
	pydocstyle_enabled)
		pydocstyle_enabled=1
		;;
	pycodestyle_enabled)
		pycodestyle_enabled=1
		;;
	bandit_enabled)
		bandit_enabled=1
		;;
	mypy_enabled)
		mypy_enabled=1
		;;
	prospector_enabled)
		prospector_enabled=1
		;;
	pylama_enabled)
		pylama_enabled=1
		;;
	pytest_enabled)
		pytest_enabled=1
		;;
	unittest_enabled)
		unittest_enabled=1
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
	remove_parsed_args)
		remove_parsed_args=1
		;;
	script_name)
		script_name=${OPTARG}
		;;
	print_options)
		print_options=1
		;;
	use_pyenv)
		use_pyenv=${OPTARG}
		;;
	??*)
		echo "Invalid long option provided (--$OPT). Consider removing this from the setup file"
		;;
	?)
		echo "The only valid short flags supported are ['-d', '-v', '-r']"
		;;
	esac
done
#endregion

# Print Values Before Validation for Debugging
if [ "$print_options" = 1 ] && [ "$debug" = 1 ]; then
	echo "$dash_separator $script_name CLI Arguments $dash_separator"
	echo "    -d (--debug): $debug"
	echo "    -v (--package_manager): $package_manager"
	echo "    -r (--rebuild_venv): $rebuild_venv"
	echo "    --python_version: $python_version"
	echo "    --is_package: $is_package"
	echo "    --include_jumanji_house: $include_jumanji_house"
	echo "    --include_prettier: $include_prettier"
	echo "    --include_isort: $include_isort"
	echo "    --isort_profile: $isort_profile"
	echo "    --python_formatter: $python_formatter"
	echo "    --pylint_enabled: $pylint_enabled"
	echo "    --flake8_enabled: $flake8_enabled"
	echo "    --pydocstyle_enabled: $pydocstyle_enabled"
	echo "    --pycodestyle_enabled: $pycodestyle_enabled"
	echo "    --bandit_enabled: $bandit_enabled"
	echo "    --mypy_enabled: $mypy_enabled"
	echo "    --prospector_enabled: $prospector_enabled"
	echo "    --pylama_enabled: $pylama_enabled"
	echo "    --pytest_enabled: $pytest_enabled"
	echo "    --unittest_enabled: $unittest_enabled"
	echo "    --overwrite_vscode_launch: $overwrite_vscode_launch"
	echo "    --line_length: $line_length"
	echo "    --pre_commit_pylint_entry_prefix: $pre_commit_pylint_entry_prefix"
	echo "    --remove_parsed_args: $remove_parsed_args"
	echo "    --script_name: $script_name"
	echo "    --print_options: $print_options"
	echo "    --use_pyenv: $use_pyenv"
	echo ""
fi

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
	[ "$python_formatter" != "black" ] &&
	[ "$python_formatter" != "yapf" ]; then
	error "Invalid python_formatter option: ($python_formatter). Valid values are ['', autopep8, black, yapf]"
fi

if [ "$pylint_enabled" != 0 ] && [ "$pylint_enabled" != 1 ]; then
	error "Invalid pylint_enabled option: ($pylint_enabled). Valid values are [0, 1]"
fi

if [ "$flake8_enabled" != 0 ] && [ "$flake8_enabled" != 1 ]; then
	error "Invalid flake8_enabled option: ($flake8_enabled). Valid values are [0, 1]"
fi

if [ "$pydocstyle_enabled" != 0 ] && [ "$pydocstyle_enabled" != 1 ]; then
	error "Invalid pydocstyle_enabled option: ($pydocstyle_enabled). Valid values are [0, 1]"
fi

if [ "$pycodestyle_enabled" != 0 ] && [ "$pycodestyle_enabled" != 1 ]; then
	error "Invalid pycodestyle_enabled option: ($pycodestyle_enabled). Valid values are [0, 1]"
fi

if [ "$bandit_enabled" != 0 ] && [ "$bandit_enabled" != 1 ]; then
	error "Invalid bandit_enabled option: ($bandit_enabled). Valid values are [0, 1]"
fi

if [ "$mypy_enabled" != 0 ] && [ "$mypy_enabled" != 1 ]; then
	error "Invalid mypy_enabled option: ($mypy_enabled). Valid values are [0, 1]"
fi

if [ "$prospector_enabled" != 0 ] && [ "$prospector_enabled" != 1 ]; then
	error "Invalid prospector_enabled option: ($prospector_enabled). Valid values are [0, 1]"
fi

if [ "$pylama_enabled" != 0 ] && [ "$pylama_enabled" != 1 ]; then
	error "Invalid pylama_enabled option: ($pylama_enabled). Valid values are [0, 1]"
fi

if [ "$pytest_enabled" != 0 ] && [ "$pytest_enabled" != 1 ]; then
	error "Invalid pytest_enabled option: ($pytest_enabled). Valid values are [0, 1]"
fi

if [ "$unittest_enabled" != 0 ] && [ "$unittest_enabled" != 1 ]; then
	error "Invalid unittest_enabled option: ($unittest_enabled). Valid values are [0, 1]"
fi

if [ "$overwrite_vscode_launch" != 0 ] && [ "$overwrite_vscode_launch" != 1 ]; then
	error "Invalid overwrite_vscode_launch option: ($overwrite_vscode_launch). Valid values are [0, 1]"
fi

if [ "$use_pyenv" != 0 ] && [ "$use_pyenv" != 1 ]; then
	error "Invalid use_pyenv option: ($use_pyenv). Valid values are [0, 1]"
fi
#endregion

# Remove Parsed Arguments from $@ List
if [ "$remove_parsed_args" = 1 ]; then
	echo "Removing parsed arguments from \$@ list"
	shift $((OPTIND - 1))
fi
