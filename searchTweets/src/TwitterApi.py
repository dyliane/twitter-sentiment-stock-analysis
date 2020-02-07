# -*- coding:utf-8 -*-
import tweepy

API_KEY = 'mnWgEBTzRi66tERsDCCFBDXDg'
API_SECRET = 'sNyG2xrhgc63roPR3hOMBc85GmuVMMEQ6RH5MMGiNMllmuVIA0'
ACCESS_TOKEN = '1047992355226312706-QC1B4qjVFQjmaAGzCc5145m1gbCQvL'
ACCESS_TOKEN_SECRET = 'xF9KIvFUiYI17Vf93nPigxbg95duNmkrx1mq8BzRkluIA'

# API_KEY = ''
# API_SECRET = ''
# ACCESS_TOKEN = ''
# ACCESS_TOKEN_SECRET = ''


class TwitterApi():
    def __init__(self):
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        self.api = tweepy.API(auth)
