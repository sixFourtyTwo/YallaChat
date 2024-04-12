import sqlite3
import os

def connect_to_database():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    return conn, c
def create_accounts(c):
    c.execute('''CREATE TABLE IF NOT EXISTS accounts(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             email TEXT,
           username TEXT,
             password TEXT);
           ''')
def create_chats(c):
    c.execute('''CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    participant1 TEXT,
    participant2 TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Timestamp column
    UNIQUE(participant1, participant2)
);''')
def create_messages(c):
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    recipient TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    chat_id INTEGER,
    FOREIGN KEY (chat_id) REFERENCES chats(id)
);''')

def fetch_chats(cursor):
        cursor.execute("SELECT id, participant1, participant2 FROM chats")
        chats = cursor.fetchall()
        return chats
def fetch_messages(cursor, chat_id):
        messages = cursor.execute("SELECT sender, content, timestamp FROM messages WHERE chat_id = ? ORDER BY timestamp", (chat_id,))
        messages = cursor.fetchall()
        return messages
    
    


