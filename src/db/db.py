import sqlite3
from dotenv import load_dotenv
import os

def create_tables(conn):
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        discord_name TEXT NOT NULL,
        display_name TEXT
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        attempt_time INTEGER NOT NULL,
        score INTEGER NOT NULL,
        passed BOOLEAN NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    cur.close()
    conn.commit()


def connect():
    load_dotenv()
    print(os.getenv('DB_PATH'))
    conn = sqlite3.connect(os.getenv('DB_PATH'))

    create_tables(conn)

    return conn


conn = connect()


if __name__ == '__main__':
    create_tables()
