#!/bin/bash
for f in *.ui
	do 
		if [ -f "$f" ]
		then 
			pyuic5 -x "$f" -o "${f%.ui}.py"
			cp "${f%.ui}.py" ..
		fi
	done
# cp *.py ../src/main/python/gui/