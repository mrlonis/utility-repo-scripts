#!/bin/bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
script_dir_parent="$(dirname "$script_dir")"

# Root
shfmt -l -w "$script_dir_parent"/ensure_venv.sh
shfmt -l -w "$script_dir_parent"/setup

# Scripts
shfmt -l -w "$script_dir"/format.sh
shfmt -l -w "$script_dir"/functions.sh
