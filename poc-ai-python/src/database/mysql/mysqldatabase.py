

import mysql.connector.pooling
from . import mysqlconfig
from contextlib import contextmanager

# --- Initialize Connection Pool ---
# This code runs only once when the module is imported.
try:
    print("Initializing MySQL database connection pool...")
    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mysql_pool",
        pool_size=mysqlconfig.MAXCONN,  # Controls the max number of connections
        host=mysqlconfig.HOST,
        port=mysqlconfig.PORT,
        database=mysqlconfig.DATABASE,
        user=mysqlconfig.USER,
        password=mysqlconfig.PASSWORD
    )
    print("✅ Connection pool created successfully.")
except mysql.connector.OperationalError as e:
    print(f"❌ Could not connect to the database: {e}")
    pool = None

@contextmanager
def get_mysql_db_connection():
    """
    A context manager to get a MySQL connection from the pool.
    It automatically returns the connection to the pool upon closing.
    """
    if pool is None:
        raise ConnectionError("MySQL database connection pool is not available.")

    conn = None
    try:
        # Correct method name is get_connection()
        conn = pool.get_connection()
        yield conn
    finally:
        if conn:
            # For mysql-connector-python, you close the connection
            # to return it to the pool.
            conn.close()