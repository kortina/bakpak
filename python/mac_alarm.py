import argparse
import subprocess
import time
parser = argparse.ArgumentParser("python mac_alarm.py --minutes=20")
parser.add_argument('--seconds', type=int, default=0)
parser.add_argument('--minutes', type=int, default=0)


def alarm(seconds=0, minutes=0):
    print "Alarm will sound in {0} min {1} sec".format(minutes, seconds)
    print "End by pressing Ctrl+C"
    seconds += minutes * 60
    while seconds > 0:
        print "Wake in {0} sec".format(seconds)
        time.sleep(1)
        seconds -= 1

    while 1:
        subprocess.call(["say", "a"])
        time.sleep(1)

if __name__ == "__main__":
    args = parser.parse_args()
    alarm(seconds=args.seconds, minutes=args.minutes)
