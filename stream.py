'''
Stream tweets about 2016 US presidential candidates

Inspiration from:
Adil Moujahid
Reference: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
'''

import os
import re
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from secrets import API_KEY, API_SECRET, ACCESS_TOKEN, TOKEN_SECRET
from constants import CANDIDATES, PROJECT_ROOT


class StdOutListener(StreamListener):
    '''
    Tweet listener that does some very basic data cleaning
    '''

    def write(self, tweet):
        # file_name = 'tweets.json'
        path = os.getcwd()
        file_loc = '{0}/data/tweets.json'.format(path) 
        print file_loc
        output = json.dumps(tweet) + ',\n'
        mode = 'w'
        if os.path.isfile(file_loc):
            mode = 'a'
        
        with open(file_loc, mode) as json_file:
            json_file.write(output)

    def get_candidate(self, tweet):
        text = tweet.get('text')
        # assume the first matched candidate is the ONLY candidate
        # discussed in the tweet for simplicity
        for key, value in CANDIDATES.iteritems():
            candidate = CANDIDATES[key]
            if re.search(candidate, text, re.IGNORECASE):
                return key
        return None

    def clean(self, data):
        parsed = json.loads(data)
        tweet = dict((k, parsed[k]) for k in ('id', 'text', 'user', 'created_at'))
        return tweet

    def on_data(self, data):
        tweet = self.clean(data)
        candidate = self.get_candidate(tweet)
        if candidate:
            tweet['candidate'] = candidate
            print "Write tweet for candidate: {0}".format(CANDIDATES[candidate])
            self.write(tweet)
        else:
            print 'notta'

        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    listener = StdOutListener()
    auth = OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, TOKEN_SECRET)
    stream = Stream(auth, listener)
    stream.filter(track=CANDIDATES.values())

