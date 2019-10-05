'''
Stream tweets about 2020 Democratic presidential candidates

Inspiration from:
Adil Moujahid
Reference: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
'''

import os
import re
import json
import analytics

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from secrets import API_KEY, API_SECRET, ACCESS_TOKEN, TOKEN_SECRET, SEGMENT_WRITE_KEY
from constants import CANDIDATES, PROJECT_ROOT, RETWEET

analytics.write_key = SEGMENT_WRITE_KEY


class StdOutListener(StreamListener):
    '''
    Tweet listener that does some very basic data cleaning
    '''

    def _write_tweet(self, tweet):
        path = os.getcwd()
        file_loc = '{0}/data/tweets.json'.format(path) 
        output = json.dumps(tweet) + ',\n'
        mode = 'w'
        if os.path.isfile(file_loc):
            mode = 'a'
        
        with open(file_loc, mode) as json_file:
            json_file.write(output)

        analytics.track('1', tweet['candidate'], tweet)

    def _get_candidate(self, tweet):
        text = tweet.get('text')
        # assume the first matched candidate is the ONLY candidate
        # discussed in the tweet for simplicity
        for key, value in CANDIDATES.items():
            candidate = re.compile(CANDIDATES[key], flags=re.IGNORECASE)
            if re.search(candidate, text):
                return key
        return None

    def _clean(self, data):
        parsed = json.loads(data)
        tweet = dict((k, parsed[k]) for k in ('id', 'text', 'user', 'created_at'))
        return tweet

    def _is_retweet(self, tweet):
        return tweet['text'].startswith(RETWEET)

    def on_data(self, data):
        tweet = self._clean(data)
        candidate = self._get_candidate(tweet)
        is_retweet = self._is_retweet(tweet)
        if candidate and not is_retweet:
            tweet['candidate'] = candidate
            print("Write tweet for candidate: {0}".format(candidate))
            self._write_tweet(tweet)

    def on_error(self, status):
        print('StreamListener error: ', status)

def _get_track_list():
    track_strings = []
    for value in CANDIDATES.values():
        matches = re.sub('[()]', '', value)
        matches = matches.split('|')
        track_strings += matches
    return track_strings

if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, TOKEN_SECRET)
    stream = Stream(auth, listener)
    stream.filter(track=_get_track_list())

