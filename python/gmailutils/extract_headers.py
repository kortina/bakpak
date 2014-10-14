import email
import os
import sys
import argparse
from collections import Counter
"""
Works with .eml files you have downloaded with another script such as
https://github.com/abjennings/gmail-backup
"""
usage = """
Run in a direcotry containing eml files to extract headers:

    cd /dir/with/emails && \
    python /path/to/gmailutils/extract_headers.py --task=all --min=0

Params:
--task (required)  "all" or "top"
                   What to do with the emails extracted.
                   "top" - prints summary of most popular emails
                   "all" - print list of all emails encountered
--min (optional)   offset, starting point
--max (optional)   limit, ending point

"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--min')
    parser.add_argument('--max')
    parser.add_argument('--task')
    args = parser.parse_args(sys.argv[1:])


address_headers = ["To", "From", "Cc", "Bcc"]
# other_headers = "Bcc", "Date", "Delivered-To", "Subject"

# Create a dictionary of Counters for each field type
top_addresses = {}
for k in address_headers:
    top_addresses[k] = Counter()

# Create a set to contain distinct people
distinct_addresses = set()


def normalize(address):
    if address:
        address = address.strip()
        address = address.lower()
    return address


def print_top():
    print "-" * 40
    print "-" * 40
    for header in top_addresses:
        print "-" * 20
        print header
        print "-" * 20
        for tup in top_addresses[header].most_common(50):
            print "{0}: {1}".format(*tup)
    print "-" * 40
    print "-" * 40


def print_all():
    for address in distinct_addresses:
        print address


def task_function(task):
    if task == "all":
        return print_all
    if task == "top":
        return print_top


def process_emails_in_dir(directory, min_iter=0, max_iter=0):
    filenames = os.listdir(directory)
    num_files = len(filenames)

    for i, filename in enumerate(filenames):
        print "{0} / {1} : {2}".format(i, num_files, filename)
        if not str.lower(filename[-3:]) == "eml":
            continue

        msg = email.message_from_file(open(filename))
        for header in address_headers:
            v = msg.get(header)
            if v:
                people = v.split(",")
                for p in people:
                    p = normalize(p)
                    distinct_addresses.add(p)
                    # print "{0}: {1}".format(header, p)
                    top_addresses[header][p] += 1

        if max_iter and i >= max_iter:
            break

if __name__ == "__main__":
    min_iter = int(args.min or 0)
    max_iter = int(args.max or 0)
    task = args.task
    task_func = task_function(task)
    if not task_func:
        raise usage
    try:
        process_emails_in_dir("./", min_iter, max_iter)
    except KeyboardInterrupt as kbe:
        raise
    finally:
        task_func()
