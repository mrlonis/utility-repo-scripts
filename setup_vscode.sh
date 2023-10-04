#!/bin/bash
dash_separator="--------------------" # 20 dashes
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

# Process CLI Arguments
debug=0
include_prettier=0
include_isort=0
python_formatter=""
overwrite_vscode_launch=0
pylint_enabled=0
flake8_enabled=0
source "$script_dir"/scripts/process_cli_options.sh "$@"

# VS Code Settings
echo "$dash_separator VS Code settings.json $dash_separator"
[ ! -f ".vscode/settings.json" ] && vscode_settings_exist=0 || vscode_settings_exist=1

mkdir -p .vscode

# Create settings.json using setup_vscode.py
python "$script_dir"/setup_vscode.py "$@" --exists="$vscode_settings_exist"

# Attempt to sort newly created .vscode/settings.json using prettier
if command -v sort-json >/dev/null; then
	if [ "$debug" = 1 ]; then
		echo "sort-json found"
		echo "Sorting .vscode/settings.json"
	fi
	sort-json .vscode/settings.json
else
	if [ "$debug" = 1 ]; then
		echo "sort-json not found"
	fi

	if command -v npm >/dev/null; then
		if [ "$debug" = 1 ]; then
			echo "npm found"
			echo "Installing sort-json globally to format .vscode/settings.json"
		fi
		npm install -g sort-json
		sort-json .vscode/settings.json
	else
		if [ "$debug" = 1 ]; then
			echo "npm not found"
			echo "Skipping sorting of .vscode/settings.json"
		fi
	fi
fi

# Attempt to format newly created .vscode/settings.json using prettier
if command -v prettier >/dev/null; then
	if [ "$debug" = 1 ]; then
		echo "prettier found"
		echo "Formatting .vscode/settings.json"
	fi
	prettier .vscode/settings.json --write --config .prettierrc --ignore-path .prettierignore
else
	if [ "$debug" = 1 ]; then
		echo "prettier not found"
	fi

	if command -v npm >/dev/null; then
		if [ "$debug" = 1 ]; then
			echo "npm found"
			echo "Installing prettier globally to format .vscode/settings.json"
		fi
		npm install -g prettier
		prettier .vscode/settings.json --write --config .prettierrc --ignore-path .prettierignore
	else
		if [ "$debug" = 1 ]; then
			echo "npm not found"
			echo "Skipping formatting of .vscode/settings.json"
		fi
	fi
fi
echo ""

#region VS Code Launch
echo "$dash_separator VS Code launch.json $dash_separator"
if [ ! -e .vscode/launch.json ] && [ -e .vscode/launch.sample.json ]; then
	# copy launch json template file
	if [ "$overwrite_vscode_launch" = 1 ]; then
		if [ "$debug" = 1 ]; then
			echo "Creating .vscode/launch.json file from .vscode/launch.sample.json template"
		fi
		cp .vscode/launch.sample.json .vscode/launch.json
	else
		echo "Skipping .vscode/launch.json creation. File already exists."
		echo "To overwrite, run this script with the --overwrite_vscode_launch=1 flag"
	fi
else
	echo "Skipping .vscode/launch.json creation. No .vscode/launch.sample.json file found."
fi
echo ""
#endregion

#region VS Code Extensions
if [ "$debug" = 1 ]; then
	echo "$dash_separator VS Code Extensions $dash_separator"
fi
if command -v code >/dev/null; then
	# VS Code Extensions
	if [ "$debug" = 1 ]; then
		echo "Installing VSCode Extensions"
	fi

	function in_list() {
		LIST=$1
		DELIMITER=$2
		VALUE=$3
		[[ "$LIST" =~ ($DELIMITER|^)$VALUE($DELIMITER|$) ]]
	}

	installed_extensions=$(code --list-extensions)

	# Vue
	# code --install-extension dbaeumer.vscode-eslint --force >/dev/null

	if [ "$include_prettier" = 1 ]; then
		in_list "$installed_extensions" " " "esbenp.prettier-vscode" && prettier_extension_installed=0 || prettier_extension_installed=1
		if [ "$prettier_extension_installed" = 0 ]; then
			echo "Installing Prettier VSCode Extension"
			code --install-extension esbenp.prettier-vscode --force >/dev/null
		fi
	fi

	# code --install-extension Vue.volar --force >/dev/null
	# code --install-extension Vue.vscode-typescript-vue-plugin --force >/dev/null

	# Python
	in_list "$installed_extensions" " " "Boto3typed.boto3-ide" && boto3_extension_installed=0 || boto3_extension_installed=1
	if [ "$boto3_extension_installed" = 0 ]; then
		echo "Installing AWS boto3 VSCode Extension"
		code --install-extension Boto3typed.boto3-ide --force >/dev/null
	fi
	in_list "$installed_extensions" " " "bungcip.better-toml" && toml_extension_installed=0 || toml_extension_installed=1
	if [ "$toml_extension_installed" = 0 ]; then
		echo "Installing Better TOML VSCode Extension"
		code --install-extension bungcip.better-toml --force >/dev/null
	fi

	if [ "$include_isort" = 1 ]; then
		in_list "$installed_extensions" " " "ms-python.isort" && isort_extension_installed=0 || isort_extension_installed=1
		if [ "$isort_extension_installed" = 0 ]; then
			echo "Installing isort VSCode Extension"
			code --install-extension ms-python.isort --force >/dev/null
		fi
	fi

	in_list "$installed_extensions" " " "ms-python.python" && python_extension_installed=0 || python_extension_installed=1
	if [ "$python_extension_installed" = 0 ]; then
		echo "Installing Python VSCode Extension"
		code --install-extension ms-python.python --force >/dev/null
	fi

	in_list "$installed_extensions" " " "ms-python.vscode-pylance" && pylance_extension_installed=0 || pylance_extension_installed=1
	if [ "$pylance_extension_installed" = 0 ]; then
		echo "Installing Pylance VSCode Extension"
		code --install-extension ms-python.vscode-pylance --force >/dev/null
	fi

	if [ "$python_formatter" = "black" ]; then
		in_list "$installed_extensions" " " "ms-python.black-formatter" && black_extension_installed=0 || black_extension_installed=1
		if [ "$black_extension_installed" = 0 ]; then
			echo "Installing Black VSCode Extension"
			code --install-extension ms-python.black-formatter --force >/dev/null
		fi
	elif [ "$python_formatter" = "autopep8" ]; then
		in_list "$installed_extensions" " " "ms-python.autopep8" && autopep8_extension_installed=0 || autopep8_extension_installed=1
		if [ "$autopep8_extension_installed" = 0 ]; then
			echo "Installing autopep8 VSCode Extension"
			code --install-extension ms-python.autopep8 --force >/dev/null
		fi
	fi

	if [ "$pylint_enabled" = 1 ]; then
		in_list "$installed_extensions" " " "ms-python.pylint" && pylint_extension_installed=0 || pylint_extension_installed=1
		if [ "$pylint_extension_installed" = 0 ]; then
			echo "Installing pylint VSCode Extension"
			code --install-extension ms-python.pylint --force >/dev/null
		fi
	fi
	if [ "$flake8_enabled" = 1 ]; then
		in_list "$installed_extensions" " " "ms-python.flake8" && flake8_extension_installed=0 || flake8_extension_installed=1
		if [ "$flake8_extension_installed" = 0 ]; then
			echo "Installing flake8 VSCode Extension"
			code --install-extension ms-python.flake8 --force >/dev/null
		fi
	fi

	# Tools
	in_list "$installed_extensions" " " "editorconfig.editorconfig" && editorconfig_extension_installed=0 || editorconfig_extension_installed=1
	if [ "$editorconfig_extension_installed" = 0 ]; then
		echo "Installing EditorConfig VSCode Extension"
		code --install-extension editorconfig.editorconfig --force >/dev/null
	fi

	in_list "$installed_extensions" " " "streetsidesoftware.code-spell-checker" && spellcheck_extension_installed=0 || spellcheck_extension_installed=1
	if [ "$spellcheck_extension_installed" = 0 ]; then
		echo "Installing Spell Checker VSCode Extension"
		code --install-extension streetsidesoftware.code-spell-checker --force >/dev/null
	fi

	in_list "$installed_extensions" " " "visualstudioexptteam.vscodeintellicode" && intellicode_extension_installed=0 || intellicode_extension_installed=1
	if [ "$intellicode_extension_installed" = 0 ]; then
		echo "Installing IntelliCode VSCode Extension"
		code --install-extension visualstudioexptteam.vscodeintellicode --force >/dev/null
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
