#!/bin/bash
# 
# jtoday is a journaling tool that is basically a shortcut to open a file of
# the format YYYY-mm-dd-journal.txt with vim
# 
# Default directory for journal files is 
# ~/Dropbox/todaytxt
# But can be set with environment variable, $TODAYTXT_DIR

# check for direcotry setting or use default
if [ -z "$TODAYTXT_DIR" ]; then
    export TODAYTXT_DIR="$HOME/Dropbox/todaytxt";
fi

# create directory if it does not exist
test -d $TODAYTXT_DIR || mkdir -p $TODAYTXT_DIR 

TODAY_DATE=`date '+%Y-%m-%d'`
TODAY_FILE="$TODAYTXT_DIR/$TODAY_DATE-journal.txt"

# if journal file does not exist, create one with heading at the top
test -e $TODAY_FILE || echo -e "$TODAY_DATE\n===========\n" > $TODAY_FILE

# open the file in vim. +99999 makes file open at last line
vim +99999 $TODAY_FILE
