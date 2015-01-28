#!/bin/bash
# convert HTML from OS X clipboard to markdown
#
# Dependencies:
# pip install html2text
osascript -e 'the clipboard as "HTML"'|perl -ne 'print chr foreach unpack("C*",pack("H*",substr($_,11,-3)))' | html2text
