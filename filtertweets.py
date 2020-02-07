from os import path
from glob import glob
import json
import argparse
from contextlib import closing
import mysql.connector as mysql
import re

def use_db(db, db_name):
    with closing(db.cursor()) as cursor:
        cursor.execute(f'use {db_name}')

def create_tables(db):
    with closing(db.cursor()) as cursor:
        cursor.execute('''create table if not exists FilteredTweets(
                        id bigint not null primary key
                        );''')

def insert(cursor, id):
    query = f"""insert into FilteredTweets values({id});"""
    
    try:
        cursor.execute(query)
    except mysql.errors.ProgrammingError:
        print(query)
        raise mysql.errors.ProgrammingError

def is_valid_tweet(text, terms_regex):
    return True if terms_regex.search(text) else False

def read_terms(terms_file):
    terms = []

    with open(terms_file, 'r', encoding='utf-8') as file:
        for line in file:
            for term in re.findall(r'(\"[^"]+\")|(\S+)', line.replace('\n', '')):
                t = term[1]

                if term[0]:
                    t = term[0].replace('"', '')
                else:
                    t  = term[1].replace('$', '\$')
                
                terms.append(f'({t})')
    
    return re.compile('|'.join(terms), re.IGNORECASE)

def main(host, user, password, db_name, terms_file):

    with closing(mysql.connect(host=host, user=user, password=password)) as db:
        use_db(db, db_name)
        create_tables(db)
        cursor = db.cursor()
        cursor.execute("SELECT id, txt from tweets")
        terms = read_terms(terms_file)

        count = 0
        for t in cursor.fetchall():
            try:
                if is_valid_tweet(t[1], terms):
                    insert(cursor, t[0])
                    count += 1
                    print(count)
            except:
                pass
            
        db.commit()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host name', type=str)
    parser.add_argument('-u', '--user', help='Username', type=str)
    parser.add_argument('-p', '--password', help='Password', type=str)
    parser.add_argument('-d', '--database', help='Database name', type=str)
    parser.add_argument('-t', '--terms', help='Terms file path', type=str)
    args = parser.parse_args()

    main(host=args.host, user=args.user,
         password=args.password, db_name=args.database,
         terms_file=args.terms)