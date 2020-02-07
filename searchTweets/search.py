# -*- coding:utf-8 -*-
import os
import argparse


def search(query, since='', until='', lang='pt'):
    since_str = 'since:' + since if since else ''
    until_str = 'until:' + until if until else ''
    query_str = f'{query} {since_str} {until_str}'

    os.system(
        f'scrapy crawl TweetScraper -a query="{query_str}" -a lang="{lang}"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query', help='Query to be searched', type=str)
    parser.add_argument('--since', help='Start date', type=str, default='')
    parser.add_argument('--until', help='End date', type=str, default='')
    parser.add_argument(
        '-l', '--lang', help='Tweets language', type=str, default='pt')
    args = parser.parse_args()

    search(args.query, count=args.count, since=args.since,
           until=args.until, lang=args.lang, dest_path=args.dest)
