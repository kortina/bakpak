#!/bin/bash
# 
# put a list of links you would like to save in a file named
# urls.txt
#
# run bash instapaper-import.sh from directory containing urls.txt


if [[ -z "$INSTAPAPER_EMAIL" ]]; then
    echo "must set \$INSTAPAPER_EMAIL shell var, eg"
    echo "export INSTAPAPER_EMAIL=\"your-secret-email@instapaper.com\""
    exit 1
fi
if [ ! -f urls.txt ]; then
    echo "file urls.txt does not exist in cwd"
    exit 1
fi

echo "Sending email to: $INSTAPAPER_EMAIL"
for url in `cat urls.txt`; do 
    echo "$url" > /tmp/u && mail -s "" $INSTAPAPER_EMAIL < /tmp/u ;
done

echo "emailed urls in urls.txt"
