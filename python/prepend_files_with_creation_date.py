#!/usr/bin/env python

# Use this script to prpend photo files with their creation date.
# proceses files in cwd "."

import datetime
import os
import re
import sys


def creation_dt(filepath):
    t = os.stat(filepath).st_mtime
    return datetime.datetime.fromtimestamp(t)


def dt_string_short(dt):
    return dt.strftime("%Y-%m-%d")


def dt_string_long(dt):
    return dt.strftime("%Y-%m-%d %H.%M.%S")


def new_filename(filename):
    dt = creation_dt(filename)
    if filename_starts_with_a_date(filename):
        return None
    else:
        l = dt_string_long(dt)
        return "{0}.{1}".format(l, filename)


def filename_starts_with_a_date(filepath):
    return re.search(r"^\d{4}-\d{2}", filepath)


def file_is_image(filename):
    reg = re.compile(r"(jpg|jpeg|png)$", re.I)
    return re.search(reg, filename)


if __name__ == "__main__":
    filenames = os.walk(".").next()[2]
    dry_run = True
    if "-m" in sys.argv:
        dry_run = False
    else:
        print "### Dry run!"

    for f in filenames:
        if not file_is_image(f):
            continue
        nf = new_filename(f)
        if nf:
            if dry_run:
                print "would rename {0} to {1}".format(f, nf)
            else:
                os.rename(f, nf)
    if dry_run:
        print "### Dry run. Run again with -m flag to perform renames."
