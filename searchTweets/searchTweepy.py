# -*- coding: utf-8 -*-
from os import path
import argparse
import json
from tweepy import Cursor
from src.TwitterApi import TwitterApi


def search(term, count=15, since='', until='', lang='pt', dest_path=''):
    api = TwitterApi().api
    tweets = []

    # search by pages
    for page in Cursor(api.search,
                       q=term,
                       count=count,
                       lang='pt',
                       tweet_mode='extended',
                       since=since,
                       until=until
                       ).pages():

        for status in page:
            tweets.append(status._json)

    print('Result: ', len(tweets))

    # save in the json file
    with open(path.join(dest_path, 'tweets.json'), 'w', encoding='utf-8') as file:
        json.dump(tweets, file, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Query to be searched', type=str)
    parser.add_argument(
        '-c', '--count', help='Number of tweets per page', type=int, default=15)
    parser.add_argument('--since', help='Start date', type=str, default='')
    parser.add_argument('--until', help='End date', type=str, default='')
    parser.add_argument(
        '-l', '--lang', help='Tweets language', type=str, default='pt')
    parser.add_argument('--dest', help='Destination path',
                        type=str, default='')
    args = parser.parse_args()

    search(args.query, count=args.count, since=args.since,
           until=args.until, lang=args.lang, dest_path=args.dest)
