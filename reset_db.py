import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='m_2009_2011_n',
        host='localhost',
        port='2009'
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'online_library_db'
          AND pid <> pg_backend_pid();
    """)
    cursor.execute("DROP DATABASE IF EXISTS online_library_db;")
    cursor.execute("CREATE DATABASE online_library_db;")
    cursor.close()
    conn.close()
    print("Database reset successfully.")
except Exception as e:
    print(f"Failed to reset DB: {e}")
