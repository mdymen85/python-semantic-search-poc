import psycopg2
import sys

# --- Your Database Connection Details ---
# Replace with your actual credentials from your Docker setup
db_params = {
    "host": "localhost",
    "port": "5432",
    "database": "mydb",
    "user": "user",
    "password": "password"  # The password you set in your docker-compose.yml
}

def test_pg_connection():
    """Connects to a PostgreSQL database and tests the connection."""
    conn = None
    try:
        # Establish the connection
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**db_params)

        # A "cursor" is an object used to interact with the database
        with conn.cursor() as cur:
            # Execute a simple query to get the version
            print("Executing 'SELECT version()' query...")
            cur.execute("SELECT version();")

            # Fetch the result of the query
            db_version = cur.fetchone()

            # Print the successful connection message and the version
            print("\n✅ Connection successful!")
            print("PostgreSQL database version:")
            print(db_version[0])

    except psycopg2.OperationalError as e:
        # Handle connection errors (e.g., wrong password, DB not running)
        print(f"❌ Could not connect to the database: {e}", file=sys.stderr)

    except Exception as e:
        # Handle other potential errors
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

    finally:
        # Make sure to close the connection, whether it succeeded or failed
        if conn is not None:
            conn.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    test_pg_connection()