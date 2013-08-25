"""
Simple example of using the argparse module.
"""
import argparse
parser = argparse.ArgumentParser("python argparse_example.py")
# required argument, allow 2 different keyword names
parser.add_argument('-f','--file', required=True, dest="file", type=str,
                    help="Path to file to process.")
# optional T/F argument with a default
parser.add_argument('-d', action='store_true', dest="dry_run", 
                    help="Do a dry run.")
# just the basics
parser.add_argument('--username')
args = parser.parse_args()
print "username: %s" % args.username
print "file: %s" % args.file
print "dry_run: %s" % args.dry_run
