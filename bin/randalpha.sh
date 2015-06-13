#!/usr/bin/env bash
NUMCHARS=16
LC_CTYPE=C tr -dc A-Za-z0-9 < /dev/urandom | head -c $NUMCHARS
