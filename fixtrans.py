# -*- coding: utf-8 -*-
import json
import argparse
from contextlib import closing
import mysql.connector as mysql
from textblob import TextBlob
import time
from google.cloud import translate_v2 as translate
import random

translator = translate.Client.from_service_account_json('credential.json')

def use_db(db, db_name):
    with closing(db.cursor()) as cursor:
        cursor.execute(f'use {db_name}')
    
def get_translations(cursor):
    return cursor.execute("SELECT id FROM translations where txt REGEXP '^Translated';")

def get_tweet(cursor, id):
    cursor.execute(f"SELECT txt from tweets WHERE id = {id}")
    return cursor.fetchone()

def update_tranlation(cursor, id, text):
    cursor.execute(f"update translations set txt = {repr(str(text))} where id = {id}")

def translate(text):
    return translator.translate(text, target_language="en")['translatedText']

def main(host, user, password, db_name):

    with closing(mysql.connect(host=host, user=user, password=password)) as db:
        use_db(db, db_name)
        cursor = db.cursor()
        get_translations(cursor)

        result = cursor.fetchall()
        count = 0

        for x in result:
            txt = get_tweet(cursor, x[0])[0]
            update_tranlation(cursor, x[0], translate(txt))
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
