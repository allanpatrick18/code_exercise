import os
import psycopg2
from psycopg2.extras import RealDictCursor


def return_db_connection():
    """ Connect to the PostgreSQL database server using the SQLAlchemy for
    user"""
    try:
        params = "host={} dbname=sports_book user=postgres password=postgres".format(str(os.environ['DB_HOST']))
        print(params)
        conn = psycopg2.connect(params,
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        return cur, conn
    except Exception as e:
        print(e)