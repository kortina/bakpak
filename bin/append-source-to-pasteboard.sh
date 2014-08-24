#!/usr/bin/env bash
URL=`osascript -e "tell application \"Google Chrome\" to return URL of active tab of front window"`
TITLE=`osascript -e "tell application \"Google Chrome\" to return title of active tab of front window"`
PBP=`pbpaste`
echo -e "$PBP\n\n-- via: [$TITLE]($URL)" | pbcopy
