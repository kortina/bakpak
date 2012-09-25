"""
NB:

From a comment:
Your test incorrectly makes it look like frozen sets are faster than normal sets, by giving the frozen set the advantage of being created second. If you will try using a second normal set where you have "frozenset()", you will find that the second set still wins, and by exactly the same amount! The test would be more fair if you created both the set and the frozenset in the competition from a third, untested set that gets created from the list. That way neither the set nor frozenset would have any advantage; they would have been initialized the same way. (Or maybe you could initialize both of them right from the list?)


"""


import os
import random
import re
import string
import time

def n_random_words(num_words=3000):
    
    stat = os.stat('/usr/share/dict/words')
    # the filesize if the 7th element of the array
    flen = stat[6]
    f = open('/usr/share/dict/words')
    
    min_word_len = 3
    max_word_len = 30
    word_regexp = re.compile(r'^[a-z]{%s,%s}$' % (min_word_len, max_word_len)) # only allow lower case
    
    words = []
    while len(words) < num_words:
        word = None
        # seek to a random offset in the file
        f.seek(int(random.random() * flen))
        # do a single read with sufficient characters
        chars = f.read(50)
        # split it on white space
        wrds = string.split(chars)
        # the first element may be only a partial word so use the second
        # you can also make other tests on the word here
        if len(wrds) > 1 and re.search(word_regexp, wrds[1]):
            word = wrds[1]
        if word and not word in words:
            words.append(word)
    
    return words


def test_performance(num_words_in_universe=5000, num_rand_words_to_search=2000, num_tests=10):
    times = {"list": [], "set": [], "frozenset": [], "dict": []}

    for i in range(0, num_tests):
        words = n_random_words(num_rand_words_to_search)
        search_words = n_random_words(num_rand_words_to_search)

        words_list = list(words) #copy the list
        words_set = set(words)
        words_frozenset = frozenset(words_set)
        words_dict = {}
        for w in words:
            words_dict[w] = 1

        s = time.time()
        for w in search_words:
            if w in words_list:
                pass
        e = time.time()
        times['list'].append(e - s)

        s = time.time()
        for w in search_words:
            if w in words_set:
                pass
        e = time.time()
        times['set'].append(e - s)

        s = time.time()
        for w in search_words:
            if w in words_frozenset:
                pass
        e = time.time()
        times['frozenset'].append(e - s)

        s = time.time()
        for w in search_words:
            if words_dict.get(w):
                pass
        e = time.time()
        times['dict'].append(e - s)
    
    avg_times = []
    for label,results in times.iteritems():
        avg_times.append([label, sum(results)/len(results)])
    
    avg_times.sort(key=lambda x: x[1])
    for a in avg_times:
        print a

