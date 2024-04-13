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
    
def create_friends(c):
    c.execute('''CREATE TABLE IF NOT EXISTS friend_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    status TEXT DEFAULT 'pending',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES accounts(user_id),
    FOREIGN KEY (receiver_id) REFERENCES accounts(user_id)
);
''')

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
#helper functions for general use
def lookup_user(c, username):
    c.execute("SELECT username FROM accounts WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        return True
    else: 
        return False
def get_userID(c, username):
    c.execute("SELECT user_id FROM accounts WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        return result[0]
def find_request_id(conn, c, sender_id, receiver_id):
    c.execute('''SELECT request_id
                 FROM friend_requests
                 WHERE sender_id = ? AND receiver_id = ?''', (sender_id, receiver_id))
    request_id = c.fetchone()
    conn.close()
    return request_id[0]

def send_friend_request(conn, c, sender_id, receiver_id):
    c.execute('''INSERT INTO friend_requests (sender_id, receiver_id) VALUES (?, ?)''', (sender_id, receiver_id))
    conn.commit()
    conn.close()
    print("friend request sent")

def accept_friend_request(conn, c, request_id):

    c.execute('''UPDATE friend_requests SET status = 'accepted' WHERE request_id = ?''', (request_id,))
    conn.commit()
    conn.close()

def reject_friend_request(conn, c, request_id):
    c.execute('''UPDATE friend_requests SET status = 'rejected' WHERE request_id = ?''', (request_id,))
    conn.commit()
    conn.close()

def get_pending_friend_requests(conn, c, user_id):
    c.execute('''SELECT * FROM friend_requests WHERE receiver_id = ? AND status = 'pending' ''', (user_id,))
    requests = c.fetchall()
    conn.close()
    return requests

conn, c = connect_to_database()
Sfunc.register_account(conn, c, "dani", "dani@edu", "dani123", "123456")
Sfunc.register_account(conn, c, "dani2", "dani2@edu", "dani1223", "1234256")
send_friend_request(conn, c, get_userID(c,'dani123'), get_userID(c,'dani1223'))