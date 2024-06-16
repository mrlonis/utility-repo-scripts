#!/bin/bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
script_dir_parent="$(dirname "$script_dir")"

# Root
shfmt -l -w "$script_dir_parent"/ensure_venv.sh
shfmt -l -w "$script_dir_parent"/setup
shfmt -l -w "$script_dir_parent"/setup_custom_after_setup_script.sh
shfmt -l -w "$script_dir_parent"/setup_flake8.sh
shfmt -l -w "$script_dir_parent"/setup_install_dependencies.sh
shfmt -l -w "$script_dir_parent"/setup_pre_commit_config.sh
shfmt -l -w "$script_dir_parent"/setup_pylintrc.sh
shfmt -l -w "$script_dir_parent"/setup_pyproject_toml.sh
shfmt -l -w "$script_dir_parent"/setup_python_app.sh
shfmt -l -w "$script_dir_parent"/setup_vscode.sh

# Scripts
shfmt -l -w "$script_dir"/format.sh
shfmt -l -w "$script_dir"/pip_compile.sh
shfmt -l -w "$script_dir"/process_cli_options.sh
shfmt -l -w "$script_dir"/testing.sh
