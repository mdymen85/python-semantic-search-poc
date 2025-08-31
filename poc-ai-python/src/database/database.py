# database.py

import os
import psycopg2.pool
from . import config
from contextlib import contextmanager

# --- Initialize Connection Pool ---
# This code runs only once when the module is imported.
try:
    print("Initializing database connection pool...")
    pool = psycopg2.pool.SimpleConnectionPool(
        minconn=config.MINCONN,
        maxconn=config.MAXCONN,
        host=config.HOST,
        port=config.PORT,
        database=config.DATABASE,
        user=config.USER,
        password=config.PASSWORD
    )
    print("✅ Connection pool created successfully.")
except psycopg2.OperationalError as e:
    print(f"❌ Could not connect to the database: {e}")
    pool = None

@contextmanager
def get_db_connection():
    """
    A context manager to get a connection from the pool.
    It automatically returns the connection to the pool.
    """
    if pool is None:
        raise ConnectionError("Database connection pool is not available.")

    conn = None
    try:
        conn = pool.getconn()
        yield conn
    finally:
        if conn:
            pool.putconn(conn)