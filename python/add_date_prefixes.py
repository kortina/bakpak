import datetime
import email
import os
import re
import sys
import time
import argparse
import unittest

from email.utils import parsedate
"""
This is a very adhoc script I used to extract correct dates I had extracted
from some email attachments but not set properly when I created the actual
attachemnt files.  Should probably combine the setting of the utime with the
email attachment extractor script.
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--min')
    parser.add_argument('--max')
    args = parser.parse_args(sys.argv[1:])


def num_from_attachment(attachment_name):
    m = re.match(r"^(\d+)_", attachment_name)
    if m:
        return m.group(1)
    return None


def path_to_email(emails_directory, email_number):
    filename = email_number + ".eml"
    return os.path.join(emails_directory, filename)


def datestr_from_9_tuple(nine_tuple):
        eight_tuple = nine_tuple[0:7]
        dt = datetime.datetime(*eight_tuple)
        return dt.strftime("%Y-%m-%d")


def new_filename(old_filename, datestr):
    head, tail = os.path.split(old_filename)
    tail = "{0}_{1}".format(datestr, tail)
    return os.path.join(head, tail)


def process_emails_in_dir(directory, emails_directory, min_iter=0, max_iter=0):
    filenames = os.listdir(directory)
    num_files = len(filenames)

    for i, filename in enumerate(filenames):
        print "{0} / {1} : {2}".format(i, num_files, filename)
        num = num_from_attachment(filename)
        if not num:  # we already renamed this file
            continue

        email_file = path_to_email(emails_directory, num)
        msg = email.message_from_file(open(email_file))
        nine_tuple = parsedate(msg.get('Date'))
        ds = datestr_from_9_tuple(nine_tuple)
        new_name = new_filename(filename, ds)
        os.rename(filename, new_name)
        print "renamed {0} to {1}".format(filename, new_name)

        ct = time.mktime(nine_tuple)
        os.utime(new_name, (ct, ct))  # set correct file creation time

        if max_iter and i >= max_iter:
            break


class TestModule(unittest.TestCase):
    def test_num_from_attachement(self):
        num = num_from_attachment("1001515_3E700002012EF.PDF")
        self.assertEqual(num, "1001515")
        num = num_from_attachment("1-001515_3E700002012EF.PDF")
        self.assertEqual(num, None)

    def test_path_to_email(self):
        p = path_to_email("../emails/", "100")
        self.assertEqual(p, "../emails/100.eml")

    def test_from_9_tuple(self):
        ds = datestr_from_9_tuple((2011, 4, 1, 7, 41, 5, 0, 1, -1))
        self.assertEqual(ds, "2011-04-01")

    def test_new_filename(self):
        n = new_filename("test.py", "2011-04-01")
        self.assertEqual(n, "2011-04-01_test.py")

        n = new_filename("./test.py", "2011-04-01")
        self.assertEqual(n, "./2011-04-01_test.py")


if __name__ == "__main__":
    min_iter = int(args.min or 0)
    max_iter = int(args.max or 0)
    process_emails_in_dir("./", "../emails/", min_iter, max_iter)
