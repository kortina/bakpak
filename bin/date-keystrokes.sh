#!/usr/bin/env bash
#
current_date=`date  +"%Y-%m-%d"`
# modified via
# http://www.sixhat.net/applescript-insert-date-and-time-into-your-documents.html
osascript 2>/dev/null <<EOF
tell application "System Events"
    set frontmostApplication to name of the first process whose frontmost is true
end tell
tell application frontmostApplication
    activate
    tell application "System Events"
       repeat with char in the characters of "$current_date" 
            keystroke char
        end repeat
    end tell
end tell
EOF
