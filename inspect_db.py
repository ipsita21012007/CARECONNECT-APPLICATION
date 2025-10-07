import sqlite3

def main():
    conn = sqlite3.connect('careconnect.db')
    cur = conn.cursor()
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    doctor_info = cur.execute("PRAGMA table_info('Doctor')").fetchall()
    conn.close()
    print('TABLES:', tables)
    print('DOCTOR_SCHEMA:')
    for col in doctor_info:
        print(col)

if __name__ == '__main__':
    main()
