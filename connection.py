import os
import psycopg2
from psycopg2.extras import RealDictCursor


def return_db_connection():
    """ Connect to the PostgreSQL database server using the SQLAlchemy for
    user"""

    params = "host=localhost dbname=sports_book user=postgres password=postgres"
    print(params)
    conn = psycopg2.connect(params, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    conn.autocommit = True
    return cur, conn
