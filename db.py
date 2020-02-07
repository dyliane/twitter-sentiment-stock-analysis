# -*- coding: utf-8 -*-
from os import path
from glob import glob
import json
import argparse
from contextlib import closing
import mysql.connector as mysql


def use_db(db, db_name):
    with closing(db.cursor()) as cursor:
        cursor.execute(f'use {db_name}')


def create_db(db, db_name):
    with closing(db.cursor()) as cursor:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db_name}')


def create_tables(db):
    with closing(db.cursor()) as cursor:
        cursor.execute('''create table if not exists Tweets(
                        id bigint not null primary key,
                        usernameTweet varchar(30) not null,
                        txt text not null,
                        url text not null,
                        nbr_retweet int not null,
                        nbr_favorite int not null,
                        nbr_reply int not null,
                        datetime datetime not null,
                        has_media boolean not null,
                        is_reply boolean not null,
                        is_retweet boolean not null,
                        user_id bigint not null
                        );''')


def insert(cursor, data):
    query = f"""insert into Tweets values(
                    {data['ID']},
                    '{data['usernameTweet']}',
                    {repr(data['text'])},
                    '{data['url']}',
                    {data['nbr_retweet']},
                    {data['nbr_favorite']},
                    {data['nbr_reply']},
                    str_to_date('{data['datetime']}', "%Y-%m-%d %H:%i:%s"),
                    {1 if data['has_media'] else 0},
                    {1 if data['is_reply'] else 0},
                    {1 if data['is_retweet'] else 0},
                    {data['user_id']}
                    );"""
    
    try:
        cursor.execute(query)
    except mysql.errors.ProgrammingError:
        print(query)
        raise mysql.errors.ProgrammingError


def save_data(db, data_path):
    count = 0
    with closing(db.cursor()) as cursor:
        for f in glob(path.join(data_path, '*')):
            data = read_data(f)
            insert(cursor, data)
            count += 1
            print(count)


def read_data(file_path):
    data = {'ID': 0, 'usernameTweet': '', 'text': '', 'url': '', 'nbr_retweet': 0, 'nbr_favorite': 0,
            'nbr_reply': 0, 'datetime': '', 'has_media': False, 'is_reply': False, 'is_retweet': False, 'user_id': 0}

    with open(file_path, 'r', encoding='utf-8') as file:
        data_json = json.load(file)

        for k in data.keys():
            try:
                data[k] = data_json[k]
            except:
                pass

    return data


def main(data_path, host, user, password, db_name):

    with closing(mysql.connect(host=host, user=user, password=password)) as db:
        create_db(db, db_name)
        use_db(db, db_name)
        create_tables(db)
        save_data(db, data_path)

        db.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path', help='Path with the data', type=str)
    parser.add_argument('--host', help='Host name', type=str)
    parser.add_argument('-u', '--user', help='Username', type=str)
    parser.add_argument('-p', '--password', help='Password', type=str)
    parser.add_argument('-d', '--database', help='Database name', type=str)
    args = parser.parse_args()

    main(data_path=args.data_path, host=args.host, user=args.user,
         password=args.password, db_name=args.database)
