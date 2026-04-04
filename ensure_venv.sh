#!/bin/bash

# make sure we're in a virtual environment (useful for running pre-commit hooks from vscode git integration (pylint, etc))
# If there is no active virtual environment, tries to activate one using the following precedence:
# 1. $PWD/.venv
# 2. $WORKON_HOME/<project_folder_name>
# 3. ${PYENV_ROOT:-$HOME/.pyenv}/versions/<project_folder_name>
#
# setup_python_app.sh creates project environments in the local .venv folder above, so the first option works out of the box.
# Set WORKON_HOME if your environments live somewhere else.
#
# Example
# cd my/python/package
# ./ensure_venv.sh pylint src

try_activate_venv() {
	local venv_path="$1"
	local activate_path="$venv_path/bin/activate"

	if [ ! -f "$activate_path" ]; then
		return 1
	fi

	# shellcheck disable=SC1090
	if source "$activate_path" && [ -n "$VIRTUAL_ENV" ]; then
		return 0
	fi

	return 1
}

if [ -z "$VIRTUAL_ENV" ]; then
	venv_name=$(basename "$PWD")
	pyenv_root="${PYENV_ROOT:-$HOME/.pyenv}"
	candidate_venv_paths=("$PWD/.venv")

	if [ -n "$WORKON_HOME" ]; then
		candidate_venv_paths+=("$WORKON_HOME/$venv_name")
	fi
	candidate_venv_paths+=("$pyenv_root/versions/$venv_name")

	activated=0
	for candidate_venv_path in "${candidate_venv_paths[@]}"; do
		if try_activate_venv "$candidate_venv_path"; then
			activated=1
			break
		fi
	done

	if [ "$activated" -ne 1 ]; then
		echo "Command is run without a virtual environment in place and none of the candidate virtual environments exist or can be activated: ${candidate_venv_paths[*]}. This may cause the command to fail" >&2
	fi
fi
"$@"
