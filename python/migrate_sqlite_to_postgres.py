import os
import json
import argparse
import psycopg2
import sqlite3
from psycopg2.extras import execute_values
from lib.dotenv import parse_args_env
from lib.logger import Logger

tables = [
    'citation',
    'data_credit',
    'sample_category',
    'sample',
    'tracer_fallout_radionuclide',
    'tracer_inorganic',
    'tracer_isotope',
    'tracer_organic',
    'tracer_other'
]

def migrate(pgcurs, sqcurs):

    for table in tables:
        print('Processing table {}'.format(table))
        sqcurs.execute('SELECT * FROM {}'.format(table))
        rows = sqcurs.fetchall()
        cols = list(rows[0].keys())

        # Skip empty tables
        if len(rows) < 1:
            continue

        # skip the sample locations
        if table == 'sample':
            cols.remove('Location_Longitude')
            cols.remove('Location_Latitude')

        data = [[None if isinstance(row[col], str) and len(row[col]) < 1 else row[col] for col in cols] for row in rows]

        insert_many_rows(pgcurs, table, cols, data)

        # Now update the sample locations
        if table == 'sample':
            for row in rows:
                if isinstance(row['Location_Longitude'], float) and isinstance(row['Location_Latitude'], float):
                    pgcurs.execute('UPDATE sample SET location = ST_SetSRID(ST_MakePoint(%s, %s), 4326) WHERE sample_id = %s', [row['Location_Longitude'], row['Location_Latitude'], row['Sample_ID']])


def insert_many_rows(pgcurs, table, columns, data, sql=None):

    # Convert dictionaries to JSON
    values = []
    for item in data:
        values.append([json.dumps(value) if isinstance(value, dict) else value for value in item])

    if not sql:
        cols_quoted = ['\"{}\"'.format(col.lower()) if col[0].isnumeric() else col for col in columns]

        sql = 'INSERT INTO {} ({}) VALUES ({});'.format(
            table,
            ','.join(cols_quoted),
            ','.join('s' * len(columns)).replace('s', '%s'))


    pgcurs.executemany(sql, values)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pghost', help='Postgres password', type=str)
    parser.add_argument('pgport', help='Postgres password', type=str)
    parser.add_argument('pgdb', help='Postgres password', type=str)
    parser.add_argument('pguser_name', help='Postgres user name', type=str)
    parser.add_argument('pgpassword', help='Postgres password', type=str)
    parser.add_argument('sqlite_path', help='Path to SQLite database', type=str)
    parser.add_argument('--verbose', help='verbose logging', default=False)

    args = parse_args_env(parser, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../docker/.env.database'))

    log = Logger('DB Migration')
    log.setup(logPath=os.path.join(os.path.dirname(__file__), "bugdb_migration.log"), verbose=args.verbose)

    # Postgres connection
    pgcon = psycopg2.connect(user=args.pguser_name, password=args.pgpassword, host=args.pghost, port=args.pgport, database=args.pgdb)

    # SQLite connection
    sqcon = sqlite3.connect(args.sqlite_path)
    sqcon.row_factory = dict_factory

    try:
        migrate(pgcon.cursor(), sqcon.cursor())
        pgcon.commit()

        log.info('database migration complete')
    except Exception as ex:
        log.error(str(ex))
        pgcon.rollback()


if __name__ == '__main__':
    main()
