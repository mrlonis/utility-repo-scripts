#!/bin/bash

VAR="3.8.16"
DOTS=${VAR//[^.]/}
DOTS=${#DOTS}
if [ "$DOTS" = 1 ]; then
	echo "ONE DOT"
else
	echo "IDK HOW MANY DOTS"
	VAR=${VAR%.*}
	echo "Modified: $VAR"
fi
