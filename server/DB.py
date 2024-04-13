import sqlite3
import os

def connect_to_database():
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    create_chats(c)
    return conn, c
def create_accounts(c):
    c.execute('''CREATE TABLE IF NOT EXISTS accounts(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             email TEXT,
           username TEXT,
             password TEXT);
           ''')
def create_chats(c):
    c.execute('''CREATE TABLE IF NOT EXISTs Chats (
    chat_id INTEGER PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    last_message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES Users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES Users(user_id)
);''')
def create_messages(c):
    c.execute('''CREATE IF NOT EXIST TABLE message (
	id INT NOT NULL PRIMARY KEY AUTOINCREMENT,
	sender_id INT NOT NULL,
	receiver_id INT NOT NULL,
	message TEXT,
	send_date DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (sender_id) REFERENCES users(id),
	FOREIGN KEY (receiver_id) REFERENCES users(id)
);''')

def fetch_chats(cursor):
        cursor.execute('''SELECT id, participant1, participant2 FROM chats''')
        chats = cursor.fetchall()
        return chats
def fetch_messages(cursor, chat_id):
        messages = cursor.execute("SELECT sender, content, timestamp FROM messages WHERE chat_id = ? ORDER BY timestamp", (chat_id,))
        messages = cursor.fetchall()
        return messages


    
    


