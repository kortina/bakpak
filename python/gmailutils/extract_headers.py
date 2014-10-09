import email
import os
import sys
import argparse
from collections import Counter
"""
Works with .eml files you have downloaded with another script such as
https://github.com/abjennings/gmail-backup
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--min')
    parser.add_argument('--max')
    args = parser.parse_args(sys.argv[1:])


people_headers = {"To": Counter(), "From": Counter(),
                  "Cc": Counter()}
# other_headers = "Bcc", "Date", "Delivered-To", "Subject"


def print_top_people():
    print "-" * 40
    print "-" * 40
    for header in people_headers:
        print "-" * 20
        print header
        print "-" * 20
        for tup in people_headers[header].most_common(50):
            print "{0}: {1}".format(*tup)
    print "-" * 40
    print "-" * 40


def process_emails_in_dir(directory, min_iter=0, max_iter=0):
    filenames = os.listdir(directory)
    num_files = len(filenames)

    for i, filename in enumerate(filenames):
        print "{0} / {1} : {2}".format(i, num_files, filename)
        if not str.lower(filename[-3:]) == "eml":
            continue

        msg = email.message_from_file(open(filename))
        for header in people_headers:
            v = msg.get(header)
            if v:
                people = v.split(",")
                for p in people:
                    p = p.strip()
                    # print "{0}: {1}".format(header, p)
                    people_headers[header][p] += 1

        if max_iter and i >= max_iter:
            break

if __name__ == "__main__":
    min_iter = int(args.min or 0)
    max_iter = int(args.max or 0)
    try:
        process_emails_in_dir("./", min_iter, max_iter)
    except KeyboardInterrupt as kbe:
        raise
    finally:
        print_top_people()
