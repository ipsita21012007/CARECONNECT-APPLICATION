import sqlite3

DB = 'careconnect.db'


def get_connection():
    return sqlite3.connect(DB)


def ensure_users_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
    conn.commit()
    conn.close()


def add_user(name, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email) VALUES (?,?)', (name, email))
    conn.commit()
    conn.close()


def get_users():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    rows = c.fetchall()
    conn.close()
    return rows


# Ensure the users table exists on import
ensure_users_table()
