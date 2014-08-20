#!/usr/bin/env bash
FROM="kortina@gmail.com"
PROJECTID=5402886752916 # my list of things to watch on asana
TO="x+$PROJECTID@mail.asana.com"
SUBJECT=$(cat) # read from STDIN
echo -e "Subject: $SUBJECT\n\n" | sendmail -f "$FROM" "$TO"
echo -e "Added to Watch Queue: $SUBJECT"
