import sqlite3

"""Ensure the Doctor table exists and optionally insert a sample row if empty.

This script is safe to run multiple times.
"""

conn = sqlite3.connect('careconnect.db')
cursor = conn.cursor()
# Create table if it doesn't exist. Use a simple schema: doctorID, name, specialty.
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Doctor (
        doctorID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT
    )
    """
)

# If table is empty, insert a sample doctor to help testing
cursor.execute("SELECT COUNT(*) FROM Doctor")
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute(
        "INSERT INTO Doctor (name, specialty) VALUES (?, ?)",
        ("Dr. Smith", "Cardiology")
    )

conn.commit()
conn.close()
