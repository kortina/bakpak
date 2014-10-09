import imaplib     
import getpass
import sys
import argparse
from email.parser import HeaderParser
import simplejson
"""
Find all people you've interacted with on email threads and print their email
addresses.
"""

username = None
password = None

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--min')
    parser.add_argument('--max')
    args = parser.parse_args(sys.argv[1:])

username = args.username or raw_input("Enter your gmail username: ")
password = args.password or getpass.getpass("Enter your password: ")
min_iter = args.min or 1
max_iter = args.max or 0
min_iter = int(min_iter)
max_iter = int(max_iter)

connection = imaplib.IMAP4_SSL('imap.gmail.com', 993)    
connection.login(username, password) 

status, counts = connection.select("[Gmail]/All Mail", readonly=True)
count = int(counts[0])
print "Count: count"
for i in range(min_iter, count):
    print "iter: %s" % i
    typ, header_data = connection.fetch(str(i), '(BODY.PEEK[HEADER] FLAGS)')
    parser = HeaderParser()
    headers = parser.parsestr(header_data[0][1]) # extract header string from nested tuple/list returned by fetch
    d = {}
    d['To'] = headers.get('To')
    d['From'] = headers.get('From')
    d['Cc'] = headers.get('Cc')
    d['Bcc'] = headers.get('Bcc')
    d['Date'] = headers.get('Date')
    d['Delivered-To'] = headers.get('Delivered-To')
    print simplejson.dumps(d)
    if max_iter and i >= max_iter:
         break
