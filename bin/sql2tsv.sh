#!/usr/bin/env bash
SQLOUT=$(cat) # read from STDIN
echo -e "$SQLOUT" | grep "|" | awk  '{gsub("\\|","\t",$0); print;}' 
