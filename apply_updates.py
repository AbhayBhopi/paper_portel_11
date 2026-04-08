from termcolor import colored
import sqlite3

conn = sqlite3.connect('portal.db')
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE users ADD COLUMN department VARCHAR(50)")
    conn.commit()
    print(colored("Successfully added department column to users table.", "green"))
except Exception as e:
    print(colored(f"Column might already exist or error: {e}", "yellow"))
finally:
    conn.close()
