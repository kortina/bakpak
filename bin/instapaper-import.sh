#!/bin/bash
# 
# USAGE
# ./instapaper-import.sh http://www.multivax.com/last_question.html
# 
# BULK
# put a list of urls in a file named `urls.txt`
# and run 
# cat urls.txt | xargs -I {} ./instapaper-import.sh "{}"


if [[ -z "$INSTAPAPER_EMAIL" ]]; then
    echo "You must set \$INSTAPAPER_EMAIL shell var, eg"
    echo "export INSTAPAPER_EMAIL=\"your-secret-email@instapaper.com\""
    echo -e "\nGet your secret import email here: \nhttps://www.instapaper.com/save/email"
    exit 1
fi
if [[ -z "$1" ]]; then
    echo "Supply a url as first and only arg"
    echo "eg, ./instapaper-import.sh \"http://blog.instapaper.com/\""
    exit 1
fi

echo "Sending $1 via email to: $INSTAPAPER_EMAIL"
echo "$1" > /tmp/u && mail -s "" $INSTAPAPER_EMAIL < /tmp/u ;
