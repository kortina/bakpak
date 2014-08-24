import os
import subprocess


def get_md5(filename):
    p = subprocess.Popen(['md5', '-q', filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, err = p.communicate()
    return output.strip()


def remove_files_with_duplicate_contents():
    filenames = os.walk(".").next()[2]
    num_files = len(filenames)
    md5s = {}
    for i, filename in enumerate(filenames):
        print "{0} / {1} : {2}".format(i, num_files, filename)
        checksum = get_md5(filename)
        if checksum in md5s:
            print "deleting {0}, duplicate of {1}".format(filename,
                                                          md5s[checksum])
            os.remove(filename)
        else:
            md5s[checksum] = filename


if __name__ == '__main__':
    remove_files_with_duplicate_contents()
