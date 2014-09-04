import email
import os
import re
import sys
import argparse

username = None
password = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--min')
    parser.add_argument('--max')
    args = parser.parse_args(sys.argv[1:])

min_iter = int(args.min or 0)
max_iter = int(args.max or 0)

email_dir = "./"
filenames = os.listdir(email_dir)
num_files = len(filenames)

# create dir to hold attachments if does not exist
attachments_dir = os.path.join(email_dir, "attachments")
if not os.path.exists(attachments_dir):
    os.makedirs(attachments_dir)


def cleanup_name(name):
    return re.sub(r"\W", "_", name)


for i, filename in enumerate(filenames):
    if i < min_iter:
        continue

    print "{0} / {1} : {2}".format(i, num_files, filename)
    if not str.lower(filename[-3:]) == "eml":
        continue

    email_name = filename[0:-4]  # everything up to the .eml
    msg = email.message_from_file(open(filename))
    attachments = msg.get_payload()
    for j, attachment in enumerate(attachments):
        if type(attachments) is str:
            continue
        attachment_filename = attachment.get_filename()
        if attachment_filename is None:
            continue
        write_filename = email_name + "_" + attachment_filename
        write_filename = cleanup_name(write_filename)
        write_filename = os.path.join(attachments_dir, write_filename)
        f = open(write_filename, 'wb')
        f.write(attachment.get_payload(decode=True,))
        f.close()
    if max_iter and i >= max_iter:
        break
