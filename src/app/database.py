"""PostgreSQL connection with graceful fallback to mock data."""

import os

import psycopg2

DB_URL = os.getenv("DATABASE_URL", "")


def get_db_connection():
    """Try to connect to PostgreSQL. Return None if unavailable."""
    if not DB_URL:
        return None
    try:
        return psycopg2.connect(DB_URL)
    except Exception:
        return None


def is_db_available() -> bool:
    """Check if the database is reachable."""
    conn = get_db_connection()
    if conn:
        conn.close()
        return True
    return False
