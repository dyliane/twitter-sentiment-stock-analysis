from contextlib import closing
import mysql.connector as mysql
import re
from datetime import datetime
import argparse
import csv

def use_db(db, db_name):
    with closing(db.cursor()) as cursor:
        cursor.execute(f'use {db_name}')

def get_dates(cursor):
    query = "select distinct date_format(datetime, '%Y-%m-%d') from tweetstime where year(datetime) = 2017 or year(datetime) = 2018 order by datetime;"
    cursor.execute(query)

    return [d[0] for d in cursor.fetchall()]

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def volume_to_dates(cursor, d1, d2=None):
    start_date = d1 + " 18:00:00"
    end_date = (d2 if d2 else d1) + " " + ("17:59:59" if d2 else "11:59:59")

    query = f"""select count(s.txt) as total, count(case when s.txt > 0 then 1 end) as positivos, count(case when s.txt < 0 then 1 end) as negativos, avg(s.txt) as media
                from tweetstime as t 
                inner join sentiments as s 
                on t.id = s.id 
                where t.datetime >= '{start_date}' and t.datetime <= '{end_date}';"""
    
    cursor.execute(query)
    data = cursor.fetchone()
    row = [f'{start_date} - {end_date}'] + [d for d in data]
    
    return row

def main(host, user, password, db_name, terms_file):

    with closing(mysql.connect(host=host, user=user, password=password)) as db:
        use_db(db, db_name)
        cursor = db.cursor()
        dates = get_dates(cursor)

        with open("sentimentos-periodo.csv", 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["periodo", "total", "positivos", "negativos", "media"])

            for i, date in enumerate(dates):
                next_date = dates[i+1] if i < len(dates) - 1 else None
                print(date)
                writer.writerow(volume_to_dates(cursor, date, next_date))
        
        

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