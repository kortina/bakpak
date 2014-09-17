#!/usr/bin/env bash
FROM="kortina@gmail.com"
TO="kortina+notes@gmail.com"
SUBJECT=$(cat) # read from STDIN
echo -e "Subject: $SUBJECT\n\n" | sendmail -f "$FROM" "$TO"
echo -e "Emailed self: $SUBJECT"
