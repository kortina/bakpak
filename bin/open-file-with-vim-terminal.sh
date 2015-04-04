#!/usr/bin/env bash
# Given 1 argument, the path to a file, either:
# a. open that file in vim in a new Terminal tab
# b. bring to focus/front the Terminal where that file is already open in vim
#
# Useful for use with Alfred.

file_to_open="$1"

file_name=${file_to_open##*/}
file_dir=$(dirname "$file_to_open")
swp_file="$file_dir/.$file_name.swp"

if [ -e "$swp_file" ]; then

osascript 2>/dev/null <<EOF
tell application "Terminal"
	repeat with w_i from 1 to (number of windows)
		set window_i to window w_i
		repeat with t_j from 1 to (number of tabs in window_i)
			set tab_j to tab t_j of window_i
			set t_title to custom title of tab_j
			if "$file_name" is in t_title and "vim" is in t_title then
				--log "found " & t_title
				set frontmost of window_i to true
				set selected of tab_j to true
			end if
		end repeat
	end repeat
end tell
EOF

else

osascript 2>/dev/null <<EOF
tell application "Terminal"
    activate
    tell application "System Events" to keystroke "t" using command down
    repeat while contents of selected tab of window 1 starts with linefeed
        delay 0.01
    end repeat
    do script "vim \"$file_to_open\"" in window 1
end tell
EOF

fi
