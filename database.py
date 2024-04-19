# database.py
import mysql.connector

def get_connection():
    """Create and return a database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="Stillwater!1009",  # Replace with your MySQL password
        database="MOVIE_THEATRE"
    )

def close_connection(conn):
    """Close the given database connection."""
    conn.close()
