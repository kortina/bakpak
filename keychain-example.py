#!/usr/bin/python
"""
via
http://blog.macromates.com/2006/keychain-access-from-shell/
"""
import sys
import os
import re

def decode_hex(s):
    s = eval('"' + re.sub(r"(..)", r"\x\1", s) + '"')
    if "" in s: s = s[:s.index("")]
    return s

def main(svce, acct):
    cmd = ' '.join([
        "/usr/bin/security",
        " find-internet-password",
        "-g -s '%s' -a '%s'" % (svce, acct),
        "2>&1 >/dev/null"
    ])
    p = os.popen(cmd)
    s = p.read()
    p.close()
    m = re.match(r"password: (?:0x([0-9A-F]+)\s*)?\"(.*)\"$", s)
    if m:
        hexform, stringform = m.groups()
        if hexform: print decode_hex(hexform)
        else: print stringform

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
