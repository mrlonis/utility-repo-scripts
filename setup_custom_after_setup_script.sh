#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
debug=0
source "$script_dir"/scripts/process_cli_options.sh "$@"

# Custom after setup script
echo "$dash_separator Custom After Setup Script $dash_separator"
custom_script_name=".python_after_setup.sh"
if [ -f "$HOME/$custom_script_name" ]; then
	echo "Running custom after setup script $HOME/$custom_script_name"
	if [ "$debug" = 1 ]; then
		echo "Update this script to customize your virtual environments after creation"
	fi
	"$HOME"/$custom_script_name
else
	echo "No custom after setup script $HOME/$custom_script_name found. The script will be created"
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
echo ""
