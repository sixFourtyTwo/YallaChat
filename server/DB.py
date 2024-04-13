import sqlite3
import os
import infrastructure.Sfunctions as Sfunc

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
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    last_message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES accounts(user_id),
    FOREIGN KEY (receiver_id) REFERENCES accounts(user_id)
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

def get_user_chats(username):
    # Connect to the SQLite database
    conn, c = connect_to_database()
    # Execute the SQL query to retrieve chats
    c.execute('''SELECT Chats.*, sender.name AS sender_name, receiver.name AS receiver_name
                 FROM Chats
                 JOIN accounts AS sender ON Chats.sender_id = sender.user_id
                 JOIN accounts AS receiver ON Chats.receiver_id = receiver.user_id
                 WHERE sender.username = ? OR receiver.username = ?
                 ORDER BY Chats.timestamp''', (username, username))


    # Fetch all rows
    chats = c.fetchall()

    # Close the cursor and connection
    c.close()
    conn.close()

    return chats
def lookup_user(c, username):
    c.execute("SELECT username FROM accounts WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        return True
    else: False

conn, c = connect_to_database()
create_accounts(c)
create_chats(c)

chats = get_user_chats('sfefefe')
print(chats)

conn.close()   

