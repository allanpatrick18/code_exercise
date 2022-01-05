import psycopg2
import os
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    - Creates and connects to the sport_book
    - Returns the connection and cursor to sport_book
    """

    # connect to default database
    DB_HOST = os.environ['DB_HOST']
    params = "host={} dbname=postgres user=postgres password=postgres".format(DB_HOST)
    conn = psycopg2.connect(params)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    # cur.execute("REVOKE CONNECT ON DATABASE sports_book FROM public")
    cur.execute("DROP DATABASE IF EXISTS sports_book")
    cur.execute("CREATE DATABASE sports_book WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sports_book database
    DB_HOST = os.environ['DB_HOST']
    params = "host={} dbname=sports_book user=postgres password=postgres".format(DB_HOST)
    conn = psycopg2.connect(params)
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        if len(query) < 10:
            print("Empty query, skipping")
            continue
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sports_book database.

    - Establishes connection with the sports_book database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
