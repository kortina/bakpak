#!/usr/bin/env bash
#
# modified via
# http://www.macosxtips.co.uk/geeklets/productivity/mountain-lion-reminders-list/
# http://stackoverflow.com/questions/4146516/how-can-i-get-rid-of-this-osascript-output
osascript 2>/dev/null <<EOF
tell application "Reminders"
    if (count of (reminders whose completed is false)) > 0 then
        set todoList to name of reminders whose completed is false
        set output to ""
        repeat with itemNum from 1 to (count of (reminders whose completed is false))
            set output to output & linefeed & "- " & (item itemNum of todoList) 
        end repeat
    else
        set output to "no reminders"
    end if
end tell
EOF
