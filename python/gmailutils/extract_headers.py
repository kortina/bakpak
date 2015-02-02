import os
import re
import sys
import argparse
from collections import Counter
from email import message_from_file
from email.utils import getaddresses
try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase


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


def normalize_string(string):
    """strip, remove tabs and newlines. replace multi space with single spaces.
    used for names and emails"""
    if string:
        string = re.sub(r"[\n\r\t\s]+", " ", string)
        string = string.strip()
    return string


def normalize_email(address):
    if address:
        address = normalize_string(address)
        address = address.lower()
    return address


def normalize_name(name):
    if name:
        name = normalize_string(name)
    return name


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

        msg = message_from_file(open(filename))
        for header in address_headers:
            v = msg.get_all(header)
            if v:
                for person in tuples_for_address_list(v):
                    name = normalize_name(person[0])
                    email = normalize_email(person[1])
                    combined = "\"{0}\"\t{1}".format(name, email)
                    distinct_addresses.add(combined)
                    top_addresses[header][combined] += 1

        if max_iter and i >= max_iter:
            break


def tuples_for_address_list(value_list):
    """Parse list returned by email.message.Message.get_all
    https://docs.python.org/2/library/email.message.html#email.message.Message.get_all

    eg, a list of the form
    ['kortina@venmo.com, magdon@venmo.com, shreyans@venmo.com']
    for an email with the 'to' header
    'kortina@venmo.com, magdon@venmo.com, shreyans@venmo.com'

    returns
    [('', 'kortina@venmo.com'), ('', 'magdon@venmo.com'),
     ('', 'shreyans@venmo.com')]
    """
    return getaddresses(value_list) or []


class ParseEmailTests(TestCase):
    def test_tuples(self):
        header = """"Sandy [Test]" <sandy@test.com>, suzi@test.com"""
        value_list = [header]
        tuples = tuples_for_address_list(value_list)
        expected_name = "Sandy [Test]"
        expected_email = "sandy@test.com"
        tup = tuples[0]
        self.assertEqual(expected_name, tup[0])
        self.assertEqual(expected_email, tup[1])
        expected_name = ""
        expected_email = "suzi@test.com"
        tup = tuples[1]
        self.assertEqual(expected_name, tup[0])
        self.assertEqual(expected_email, tup[1])

    def test_normalize_string(self):
        self.assertEqual(normalize_string("\ta\r\n b "), "a b")

    def test_normalize_email(self):
        self.assertEqual(normalize_email("\t\nB@TEST.com "), "b@test.com")

    def test_normalize_name(self):
        self.assertEqual(normalize_name("\t\nAdam Smith "), "Adam Smith")


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
