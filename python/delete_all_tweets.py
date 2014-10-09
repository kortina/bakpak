# -*- coding: utf-8 -*-
"""
This script will delete all of the tweets in the specified account.
You may need to hit the "more" button on the bottom of your twitter profile
page every now and then as the script runs, this is due to a bug in twitter.

You will need to get a consumer key and consumer secret token to use this
script, you can do so by registering a twitter application at https://dev.twitter.com/apps

Get your ACCESS_TOKEN and ACCESS_TOKEN_SECRET from:
https://apps.twitter.com/app/[your app id]/keys

Define in twitter_settings.py:
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

@requirements: Python 2.5+, Tweepy (http://pypi.python.org/pypi/tweepy/1.7.1)

Forked from gist by Dave Jeffery
"""

import tweepy
from twitter_settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

def batch_delete(api):
    print "You are about to Delete all tweets from the account @%s." % api.verify_credentials().screen_name
    print "Does this sound ok? There is no undo! Type yes to carry out this action."
    do_delete = raw_input("> ")
    if do_delete.lower() == 'yes':
        for status in tweepy.Cursor(api.user_timeline).items():
            try:
                api.destroy_status(status.id)
                print "Deleted:", status.id
            except:
                print "Failed to delete:", status.id

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    batch_delete(api)
