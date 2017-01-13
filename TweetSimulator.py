#!/usr/bin/env python
# encoding: utf-8

import sys
import time
import random
import tweepy 
import markovify
import TweetSimulatorConfig
import TweetSimulatorTweetRepository
import TweetSimulatorTweet

def get_twitter_api():
    config = TweetSimulatorConfig.TweetSimulatorConfig()
    auth = tweepy.OAuthHandler(config.ConsumerKey(),config.ConsumerSecret())
    auth.set_access_token(config.AccessKey(), config.AccessSecret())
    return tweepy.API(auth)

def get_all_tweets(repo):
    config = TweetSimulatorConfig.TweetSimulatorConfig()
    screen_name = config.TwitterUser()
    api = get_twitter_api()
    count = 0
    # alltweets = []	
    # new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    # alltweets.extend(new_tweets)
    tweets = api.user_timeline(screen_name = screen_name,count=200)
    while tweets != None and len(tweets) > 0:
        oldest = tweets[-1].id - 1
        count = count + len(tweets)
        print "...%s tweets downloaded so far" % (count)
        for tweet in tweets:
                repo.insert(TweetSimulatorTweet.TweetSimulatorTweet(tweet.id_str, tweet.created_at, tweet.text))
        print "getting tweets before %s" % (oldest)
        tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

def get_latest_tweets(repo):
    pass

def update_tweets():
    print 'Updating tweets from Twitter.'
    repo = TweetSimulatorTweetRepository.TweetSimulatorTweetRepository()
    if repo.count() == 0:
        get_all_tweets(repo)
    else:
        get_latest_tweets(repo)

def get_corpus():
    print 'Retrieving corpus from database.'
    repo = TweetSimulatorTweetRepository.TweetSimulatorTweetRepository()
    return repo.select_all()


def create_status():
    print 'Creating status sentence.'
    res = ''
    model = markovify.NewlineText(get_corpus())
    while True:
        portion_done = len(res) / float(327)
        continue_chance = 1.0 - portion_done
        continue_chance = max(0, continue_chance)
        continue_chance += 0.1
        if random.random() > continue_chance:
            break
        s = model.make_sentence(tries = 10000, max_overlap_total = 10, max_overlap_ratio = 0.5)
        res += " " + s
    return res

def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))

def update_status():
    print 'Updating status.'
    sentence = create_status()
    print 'Created status:  %s' % (sentence)
    api = get_twitter_api()
    n = 0
    words = sentence.split()
    while True:
        if n >= len(words):
            break
        ss = ''
        while True:
            if n >= len(words):
                break;
            if len(ss) + len(words[n]) > 135:
                break
            ss += " " + words[n]
            n = n + 1
        if len(ss) > 0:
            if n < len(words):
                ss += '...'
            print 'Posting: %s' % (ss)
            api.update_status(ss)


def main():
    config = TweetSimulatorConfig.TweetSimulatorConfig()
    while True:
        update_tweets()
        update_status()
        time.sleep(int(config.StatusUpdateInterval()) * 60)

if __name__ == '__main__':
    main()


