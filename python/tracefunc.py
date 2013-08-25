import time
from collections import defaultdict

print_after_every_X_func_calls = 10000
minimum_time_spent_to_print = 0.01

class CallCount:
    call_count = 0

func_call_records = defaultdict(lambda:{"num_calls": 0, "time_of_last_call": time.time(), "total_time_spent_in_func": 0})

def record_func_call(func_key):
    now = time.time()
    func_call_records[func_key]["num_calls"] += 1
    func_call_records[func_key]["time_of_last_call"] = now
    print_func_call_records_periodically()

def record_func_return(func_key):
    now = time.time()
    time_of_last_call = func_call_records[func_key]["time_of_last_call"]
    func_call_records[func_key]["total_time_spent_in_func"] += now - time_of_last_call

def print_func_call_records_periodically():
    CallCount.call_count += 1
    if CallCount.call_count >= print_after_every_X_func_calls:
        CallCount.call_count = 0
        print_func_call_records()

def print_func_call_records():
    items = func_call_records.items()
    items.sort(key=lambda x: x[1]['total_time_spent_in_func'], reverse=True)
    print "#" * 40
    print "total_time_spent_in_func\tnum_calls\tfunc"
    print "#" * 40
    for item in items:
        if 'lib/python' not in item[0] \
                and item[1]['total_time_spent_in_func'] < minimum_time_spent_to_print:
        #     break
            print "%s\t%s\t%s" % (round(item[1]['total_time_spent_in_func'], 3), item[1]['num_calls'], item[0])
    print "#" * 40
    print "\n"


def tracefunc(frame, event, arg, indent=[0]):
    filename =  frame.f_code.co_filename
    lineno = frame.f_lineno
    funcname = frame.f_code.co_name
    func_key = "%s:%s:%s" % (filename, lineno, funcname)
# print "%s:%s:%s, event: %s, arg: %s" % (filename, lineno, funcname, event, arg)
    if event == "call":
      record_func_call(func_key)
    elif event == "return":
      record_func_return(func_key)
# if event == "call":
#     indent[0] += 2
#     print "-" * indent[0] + "> call function", frame.f_code.co_name
# elif event == "return":
#     print "<" + "-" * indent[0], "exit function", frame.f_code.co_name
#     indent[0] -= 2
    return tracefunc

def enable_tracefunc():
    import sys
    sys.settrace(tracefunc)
