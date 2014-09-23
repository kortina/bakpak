#!/usr/bin/env bash
# eg:
# curl -O http://www.ribbonfarm.com/sitemap.xml
# cat sitemap.xml | ./urls-from-sitemap.sh
#
# NB: you may still have to remove some non-posts, eg, things that are category or archive list pages
# eg:
# cat sitemap.xml| ./urls-from-sitemap.sh | ack -v "\d{4}\/\d{2}\/$" | ack -v category

# read from STDIN
cat /dev/stdin | grep "<loc>" | grep -o "http.*" | sed -E 's/\<\/.*$//'
