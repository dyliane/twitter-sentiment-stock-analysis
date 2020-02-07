# -*- coding: utf-8 -*-
import json
import argparse
from contextlib import closing
import mysql.connector as mysql
from google.cloud import translate_v2 as translate

translator = translate.Client.from_service_account_json('credential.json')

def use_db(db, db_name):
    with closing(db.cursor()) as cursor:
        cursor.execute(f'use {db_name}')

def create_table(db):
    with closing(db.cursor()) as cursor:
        cursor.execute('''create table if not exists Translations(
                        id bigint not null primary key,
                        txt text not null
                        );''')
    
def get_tweets(cursor):
    return cursor.execute("SELECT t.id, t.txt FROM tweets AS t INNER JOIN filteredtweets AS f ON t.id = f.id;")

def check_if_exists(cursor, id):
    cursor.execute(f"SELECT 1 from translations WHERE id = {id}")
    data = cursor.fetchone()

    return True if data else False

def insert(cursor, id, text):
    query = f"""insert into Translations values({id}, {repr(str(text))});"""
    
    try:
        cursor.execute(query)
    except mysql.errors.ProgrammingError:
        print(query)
        raise mysql.errors.ProgrammingError


def translate(text):
    return translator.translate(text, target_language="en")['translatedText']

def main(host, user, password, db_name):

    with closing(mysql.connect(host=host, user=user, password=password)) as db:
        use_db(db, db_name)
        create_table(db)
        cursor = db.cursor()
        get_tweets(cursor)

        result = cursor.fetchall()
        count = 0

        for x in result:
            if not check_if_exists(cursor, x[0]):
                insert(cursor, x[0], translate(x[1]))
            count += 1
            print(count)
            db.commit()
            
            
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host name', type=str)
    parser.add_argument('-u', '--user', help='Username', type=str)
    parser.add_argument('-p', '--password', help='Password', type=str)
    parser.add_argument('-d', '--database', help='Database name', type=str)
    args = parser.parse_args()

    main(host=args.host, user=args.user,
         password=args.password, db_name=args.database)
