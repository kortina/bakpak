#!/bin/bash
echo "openssl aes-128-cbc -salt -out $1 -in $1.aes"
openssl aes-128-cbc -salt -out $1.aes -in $1
