
import sqlite3

conn  =  sqlite3.connect('users.sqlite3')

cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS users(
uid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
username TEXT,
user_email TEXT,
user_oauth_id TEXT,
user_oauth_platform TEXT,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
)
               
conn.commit()
conn.close()
print('database created')
