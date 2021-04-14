import os
import argparse
import pyodbc
import psycopg2
import sqlite3
from psycopg2.extras import execute_values
from lib.dotenv import parse_args_env
from lib.Logger import Logger

def migrate(pgcurs, sqcurs):

    print('not implemented')




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

    try:
        migrate(pgcon.cursor, sqcon.cursor)
        pgcon.commit()
    except Exception as ex:
        log.error(str(ex))
        pgcon.rollback()


if __name__ == '__main__':
    main()
