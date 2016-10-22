import datetime
import os
import logging
import re
import sqlite3
import sys
import argparse
from collections import Counter
from email import message_from_file
from email.utils import getaddresses
try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock


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
    parser.add_argument('-v', action='store_true', dest="verbose",
                        help="Verbose output.")
    parser.add_argument('-vv', action='store_true', dest="vverbose",
                        help="Very verbose output.")
    parser.add_argument('-vvv', action='store_true', dest="vvverbose",
                        help="Very verbose output.")
    args = parser.parse_args(sys.argv[1:])


address_headers = ["To", "From", "Cc", "Bcc"]
# other_headers = "Bcc", "Date", "Delivered-To", "Subject"

# Create a dictionary of Counters for each field type
top_addresses = {}
for k in address_headers:
    top_addresses[k] = Counter()

# Create a set to contain distinct people
distinct_addresses = set()


def pair(name, email):
    return "\"{0}\"\t{1}".format(name, email)


def pair_lower(name, email):
    return pair(name, email).lower()


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


def db_finish():
    DB.all()
    DB.commit_and_close()
    print "Created sqlite database: {0}".format(DB.dbfile())


def task_function(task):
    if task == "all":
        return print_all
    if task == "top":
        return print_top
    if task == "insert":
        return db_finish


class Person:
    def __init__(self, name, email):
        self.name = self.normalize_name(name)
        self.email = self.normalize_email(email)

    @classmethod
    def clean_header(klass, s):
        """remove linebreaks and tabs"""
        return re.sub(r"[\n\r\t]+", " ", s).strip()

    @classmethod
    def from_eml(klass, eml, header):
        """ Extract all the people from an eml contained in the header.
        eml: email.message.Message
        header: string, eg "From"

        @see:
        https://docs.python.org/2/library/email.message.html#email.message.Message.get_all
        """
        tuples = getaddresses(map(klass.clean_header,
                                  eml.get_all(header, [])))
        return [klass(t[0], t[1]) for t in tuples]

    @classmethod
    def normalize_string(klass, string):
        """strip:
        " | \t \r \n
        and replace multi space with single spaces.

        strip leading and trailing single and double quotes

        used for names and emails."""
        if string:
            string = re.sub(r"[\"\n\r\t\s\|]+", " ", string)
            string = string.strip()
            string = string.strip("'")
            string = string.strip('"')
        return string

    @classmethod
    def normalize_email(klass, address):
        if address:
            address = re.sub(r"['\<\>]", "", address)
            address = klass.normalize_string(address)
            address = address.lower()
        return address

    @classmethod
    def normalize_name(klass, name):
        if name:
            name = klass.normalize_string(name)
            # if no capitals or @'s , then titlecase
            if not re.search(r"[A-Z@]", name):
                name = name.title()
            name = klass.flip_last_first(name)
        return name

    @classmethod
    def flip_last_first(klass, name):
        """Attempt to recognize name in
        Last, First
        form and flip to
        First Last.

        Try to be smart enough to correctly handle things like
        Ken Griffey, Jr.
        """
        if not name:
            return name
        parts = name.split(",")
        if len(parts) != 2:
            return name
        bef = parts[0].strip()
        aft = parts[1].strip()
        flipped = "{0} {1}".format(aft, bef)
        if re.search(r"[\(\)\<\>\&]", aft):
            return name
        if re.search(r"^and ", aft) or re.search(r" and ", aft):
            return name
        # 2-4 non-vowels, probably a suffix
        if re.search(r"^[^aeiouyAEIOUY]{2,4}$", aft):
            return name
        # 2-4 roman numerals, probably a suffix
        if re.search(r"^[ixvIXV]{2,4}$", aft):
            return name
        known_suffixes = ['cpa', 'do', 'edd', 'esq', 'inc', 'mba', 'od',
                          'osb', 'ret', 'usa', 'usaf']
        # known suffixes with vowels
        if aft.lower().replace(".", "") in known_suffixes:
            return name
        # 2-3 letters followed by period, probably a suffix
        if re.search(r"^\w{2,3}\.$", aft):
            return name
        return flipped


def process_emails_in_dir(directory, min_iter=0, max_iter=0, task=None):
    filenames = os.listdir(directory)
    num_files = len(filenames)

    for i, filename in enumerate(filenames):
        progress = "{0} / {1} : {2}".format(i, num_files, filename)
        logging.info(progress)
        if not str.lower(filename[-3:]) == "eml":
            continue

        eml = message_from_file(open(filename))
        # sender = Person.from_eml(eml, "From")[0]

        for header in address_headers:
            for p in Person.from_eml(eml, header):
                if "," in p.email:
                    emsg = "DISCARDING BAD EMAIL. name: {1} email: {2}"
                    emsg = emsg.format(p.name, p.email)
                    logging.warning(emsg)
                combined = pair(p.name, p.email)
                distinct_addresses.add(combined)
                top_addresses[header][combined] += 1
                if task == "insert":
                    DB.insert_or_increment(p.name, p.email)

        if max_iter and i >= max_iter:
            break


class PersonTests(TestCase):
    def test_init(self):
        p = Person("Andrew", "kortina@gmail.com")
        self.assertEqual(p.name, "Andrew")
        self.assertEqual(p.email, "kortina@gmail.com")

    def test_normalize_header(self):
        self.assertEqual(Person.clean_header("\t\"a\r b\" <a@b.c>,\r\n"),
                         "\"a  b\" <a@b.c>,")

    def test_from_eml(self):
        eml = MagicMock()
        header = """"Sandy [Test]" <sandy@test.com>, suzi@test.com"""
        eml.get_all.return_value = [header]
        people = Person.from_eml(eml, "From")
        self.assertEqual(people[0].name, "Sandy [Test]")
        self.assertEqual(people[0].email, "sandy@test.com")
        self.assertEqual(people[1].name, "")
        self.assertEqual(people[1].email, "suzi@test.com")

    def test_normalize_string(self):
        self.assertEqual(Person.normalize_string("\ta\r\n b "), "a b")

    def test_normalize_email(self):
        self.assertEqual(Person.normalize_email("\t\nB@TEST.com "),
                         "b@test.com")

    def test_normalize_name(self):
        self.assertEqual(Person.normalize_name("\t\nAdam Smith "),
                         "Adam Smith")

    def test_domain(self):
        self.assertEqual(email_domain("joe@test.net"), "test.net")
        self.assertEqual(email_domain("joe,test.net"), None)

    def test_last_first(self):
        self.assertEqual(Person.flip_last_first("Ken Griffey, Jr."),
                         "Ken Griffey, Jr.")
        self.assertEqual(Person.flip_last_first("ken griffey, jr"),
                         "ken griffey, jr")
        self.assertEqual(Person.flip_last_first("Smith, Mary Jo"),
                         "Mary Jo Smith")
        self.assertEqual(Person.flip_last_first("Mary Smith, Esq."),
                         "Mary Smith, Esq.")
        self.assertEqual(Person.flip_last_first("mary smith, esq"),
                         "mary smith, esq")
        self.assertEqual(Person.flip_last_first("Anderson, Paul T"),
                         "Paul T Anderson")
        self.assertEqual(Person.flip_last_first("Anderson, Paul T."),
                         "Paul T. Anderson")
        self.assertEqual(Person.flip_last_first("Multiple, Commas, Noop"),
                         "Multiple, Commas, Noop")
        self.assertEqual(Person.flip_last_first("Smith, Alex (US - New York)"),
                         "Smith, Alex (US - New York)")
        self.assertEqual(Person.flip_last_first("Crosby, Stills, & Nash"),
                         "Crosby, Stills, & Nash")
        self.assertEqual(Person.flip_last_first("Crosby, Stills, and Nash"),
                         "Crosby, Stills, and Nash")
        self.assertEqual(Person.flip_last_first("Crosby, Stills and Nash"),
                         "Crosby, Stills and Nash")
        self.assertEqual(Person.flip_last_first("Smith, Amy"),
                         "Amy Smith")
        self.assertEqual(Person.flip_last_first("John Davis, II"),
                         "John Davis, II")
        self.assertEqual(Person.flip_last_first("John Davis, III"),
                         "John Davis, III")
        self.assertEqual(Person.flip_last_first("John Davis, iv"),
                         "John Davis, iv")
        self.assertEqual(Person.flip_last_first("John Davis, MBA"),
                         "John Davis, MBA")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def email_domain(email):
    """Assumes email has already been run through normalize_email to strip bad
    chars"""
    parts = email.split("@")
    if len(parts) == 2:
        return parts[1]
    else:
        return None


class DB(object):
    _FILTERS = ["@.*@",
                "@bounce",
                "@list",
                "@mail\.asana",
                "@googlegroups",
                "@\w+\.google\.com",
                "@letter\.ly",
                "@txt\.voice\.google",
                "accounts*@",
                "alerts*@",
                "^api@",
                "bounce.*@",
                "customer.*@",
                "daemon",
                "developers*@",
                "digests*@",
                "disqus"
                "hello@",
                "help",
                "info@",
                "^info",
                "information@",
                "invitations*@",
                "members*@",
                "munin",
                "nagios",
                "news@",
                "no.*reply",
                "notifications*@",
                "notifier@",
                "notify@",
                "orders*@",
                "postmaster",
                "reply",
                "reports*@",
                "support"]
    FILTERS = [re.compile(p, re.I) for p in _FILTERS]

    _NAME_FILTERS = ["\?",
                     "\<",
                     "\<External\>",
                     "Google Docs",
                     "Google Drive"]
    NAME_FILTERS = [re.compile(p, re.I) for p in _NAME_FILTERS]

    @classmethod
    def dbfile(klass):
        return datetime.datetime.now().strftime("contacts-%Y-%m-%d.sql")

    @classmethod
    def conn(klass):
        if not hasattr(klass, '_conn'):
            db = klass.dbfile()
            klass._conn = sqlite3.connect(db)
            klass._conn.row_factory = dict_factory
            klass.setupdb()
        return klass._conn

    @classmethod
    def commit_and_close(klass):
        klass._conn.commit()
        klass._conn.close()

    @classmethod
    def ex(klass, sql, args=None):
        if not args:
            args = []
        return klass.conn().execute(sql, args)

    @classmethod
    def query(klass, sql, args=None):
        if not args:
            args = []
        cursor = klass.ex(sql, args)
        return cursor

    @classmethod
    def setupdb(klass):
        klass.query("""CREATE TABLE IF NOT EXISTS contacts (
                                pair VARCHAR(255) UNIQUE,
                                name VARCHAR(255),
                                email VARCHAR(255),
                                domain VARCHAR(255),
                                occurs INT,
                                from_me INT,
                                from_them INT,
                                from_other INT
                                );""")
        klass.query("""CREATE INDEX IF NOT EXISTS
                                name_ix ON contacts(name);""")
        klass.query("""CREATE INDEX IF NOT EXISTS
                                email_ix ON contacts(email);""")
        klass.query("""CREATE INDEX IF NOT EXISTS
                                domain_ix ON contacts(domain);""")

    @classmethod
    def exclude(klass, email):
        for f in klass.FILTERS:
            if re.search(f, email):
                return True
        return False

    @classmethod
    def exclude_on_name(klass, name):
        for f in klass.NAME_FILTERS:
            if re.search(f, name):
                return True
        return False

    @classmethod
    def exists(klass, name, email):
        p = pair_lower(name, email)
        sql = """SELECT COUNT(*) AS c FROM contacts WHERE pair = ?;"""
        cursor = klass.query(sql, [p])
        row = cursor.fetchone()
        if not row:
            return False
        else:
            return row.get('c', 0) > 0

    @classmethod
    def insert(klass, name, email):
        if DB.exclude(email) or DB.exclude_on_name(name):
            logging.warning("EXCLUDING: {0} {1}".format(name, email))
            return
        p = pair_lower(name, email)
        domain = email_domain(email)
        if not domain:
            emsg = "EXCLUDING, no domain: {0} {1}"
            logging.warning(emsg.format(name, email))
            return

        sql = """INSERT INTO contacts (pair, name, email, domain, occurs) \
                 VALUES (?, ?, ?, ?, 1);"""
        return klass.query(sql, [p, name, email, domain])

    @classmethod
    def increment(klass, name, email):
        p = pair_lower(name, email)
        sql = """UPDATE contacts SET occurs = occurs + 1 WHERE pair = ?;"""
        return klass.query(sql, [p])

    @classmethod
    def insert_or_increment(klass, name, email):
        if DB.exists(name, email):
            logging.info("increment {0} {1}".format(name, email))
            return DB.increment(name, email)
        else:
            logging.info("insert {0} {1}".format(name, email))
            return DB.insert(name, email)

    @classmethod
    def get(klass, name, email):
        p = pair_lower(name, email)
        sql = """SELECT * FROM contacts WHERE pair = ?;"""
        return klass.query(sql, [p]).fetchone()

    @classmethod
    def all(klass):
        sql = """SELECT * FROM contacts;"""
        cursor = klass.query(sql)
        for row in cursor:
            print row

    @classmethod
    def delete(klass, name, email):
        p = pair_lower(name, email)
        sql = """DELETE FROM contacts WHERE pair = ?;"""
        return klass.query(sql, [p])


class DBTests(TestCase):
    def test_setup(self):
        DB.setupdb()

    def test_exclude(self):
        self.assertTrue(DB.exclude("help@test.com"))
        self.assertTrue(DB.exclude("no-reply@test.com"))
        self.assertTrue(DB.exclude("support@test.com"))
        self.assertTrue(DB.exclude("accounts@test.com"))
        self.assertTrue(DB.exclude("notification@test.com"))
        self.assertFalse(DB.exclude("joe@test.com"))

        self.assertTrue(DB.exclude_on_name("?Andrew"))
        self.assertFalse(DB.exclude_on_name("Andrew"))

    def test_exists(self):
        name = "testname"
        email = "test@email.com"
        DB.delete(name, email)
        ex = DB.exists(name, email)
        self.assertFalse(ex)

        DB.insert(name, email)
        ex = DB.exists(name, email)
        self.assertTrue(ex)

        DB.delete(name, email)

    def test_increment(self):
        name = "testname"
        email = "test@email.com"
        DB.delete(name, email)

        DB.insert(name, email)
        row = DB.get(name, email)
        self.assertEqual(row['occurs'], 1)

        DB.increment(name, email)

        row = DB.get(name, email)
        self.assertEqual(row['occurs'], 2)

        DB.delete(name, email)

    def test_insert_or_increment(self):
        name = "testname"
        email = "test@email.com"
        DB.delete(name, email)

        DB.insert_or_increment(name, email)
        row = DB.get(name, email)
        self.assertEqual(row['occurs'], 1)

        DB.insert_or_increment(name, email)

        row = DB.get(name, email)
        self.assertEqual(row['occurs'], 2)

        DB.delete(name, email)

USEFUL_QUERIES = """
popular domains:
SELECT domain, COUNT(*) as c FROM contacts GROUP BY domain ORDER BY c;

popular contacts
SELECT * FROM contacts ORDER BY occurs DESC LIMIT 500;

alpha contacts
SELECT name, email, domain, occurs FROM contacts
WHERE name <> '' AND name NOT LIKE '%@%'
ORDER BY name, occurs DESC;
"""

if __name__ == "__main__":
    min_iter = int(args.min or 0)
    max_iter = int(args.max or 0)
    task = args.task
    task_func = task_function(task)
    if args.vvverbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("logging set to DEBUG")
    elif args.vverbose:
        logging.basicConfig(level=logging.INFO)
        logging.info("logging set to INFO")
    elif args.verbose:
        logging.basicConfig(level=logging.WARNING)
        logging.warning("logging set to WARNING")

    if not task_func:
        raise usage
    try:
        process_emails_in_dir("./", min_iter, max_iter, task)
    except KeyboardInterrupt as kbe:
        raise
    finally:
        task_func()
