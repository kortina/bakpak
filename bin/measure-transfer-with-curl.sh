#!/bin/bash
# via
# http://unixbhaskar.wordpress.com/2010/11/12/measure-website-response-time-through-curl/
CURL="/usr/bin/curl"
GAWK="/usr/bin/awk"
URL="$1"
result=`$CURL -o /dev/null -s -w %{time_connect}:%{time_starttransfer}:%{time_total} $URL`
echo "TimeConnect TimeStartTransfer TimeTotal"
echo $result | $GAWK -F: '{ print $1" "$2" "$3}'
