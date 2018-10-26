#!/usr/bin/env python

from dateutil.parser import parse
import argparse
import pytz
import sys


def utc_to_pacific(date_str: str):
    t = parse(date_str)
    p = pytz.utc.localize(t).astimezone(pytz.timezone('US/Pacific'))
    s = "UTC:        {0}\nUS/Pacific: {1}".format(t, p)
    return s


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('stdin', default=sys.stdin,
                        type=argparse.FileType('r'), nargs='?')
    args = parser.parse_args()
    data = args.stdin.read()
    if data in ['', None]:
        print("Usage echo '2018-10-26 02:57:57.52' | ./utc_to_pacific.py")
    else:
        print(utc_to_pacific(data))
