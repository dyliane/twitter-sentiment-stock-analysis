# -*- coding: utf-8 -*-
import os
import argparse
import re
from search import search


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def search_terms(terms_file, count=15, since='', until='', lang='pt', dest_path=''):
    terms_re = re.compile(r'(("[^"]+")|([#$]?\w+))')

    # create_dir(dest_path)

    with open(terms_file, 'r', encoding='utf-8') as file:
        os.chdir('TweetScraper')

        for line in file:
            terms = []

            for t in terms_re.finditer(line):
                terms.append(t.group(1))

            terms_query = ' OR '.join(terms).replace('"', '\\"')
            print('Query: ' + terms_query)
            search(terms_query, since=since, until=until, lang=lang)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_terms', help='File with the terms', type=str)
    parser.add_argument(
        '-c', '--count', help='Number of tweets per page', type=int, default=15)
    parser.add_argument('--since', help='Start date', type=str, default='')
    parser.add_argument('--until', help='End date', type=str, default='')
    parser.add_argument(
        '-l', '--lang', help='Tweets language', type=str, default='pt')
    parser.add_argument('--dest', help='Destination path',
                        type=str, default='')
    args = parser.parse_args()

    search_terms(args.file_terms, count=args.count, since=args.since,
                 until=args.until, lang=args.lang, dest_path=args.dest)
