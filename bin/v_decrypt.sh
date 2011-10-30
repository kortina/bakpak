#!/bin/bash
encfile=$1
destfile=${encfile%.*}
echo "openssl aes-128-cbc -d -salt -in $encfile > $destfile"
openssl aes-128-cbc -d -salt -in $encfile > $destfile
