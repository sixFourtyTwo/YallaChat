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
    c.execute('''CREATE TABLE IF NOT EXISTS Chats (
    chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    last_message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES accounts(user_id),
    FOREIGN KEY (receiver_id) REFERENCES accounts(user_id)
);''')
def create_messages(c):
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(user_id),
    FOREIGN KEY (receiver_id) REFERENCES users(user_id)
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
def authenticate(c,username, password):
    c.execute("SELECT username FROM accounts WHERE username=?", (username,))
    result = c.fetchone()
    if not result:
        print("User not found")
        return '104'
    else:
         c.execute("SELECT username, password FROM accounts WHERE username=? AND password=?", (username,password))
         result = c.fetchone()
         if not result:
             print("wrong password!")
             return '102'
         else:
            print("Login succesful")
            return '100'
         
def register_account(conn,c,name, email, username, password):
    c.execute("SELECT username FROM accounts WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        print("User already exits try logging in ")
        return '111'
    else:
        c.execute("INSERT INTO accounts VALUES (NULL, ?, ?, ?, ?);", (name, email,username, password))
        conn.commit()
        print("Accout registered!")
        return '100'
    

def get_user_chats(conn, c, username):
    # Connect to the SQLite database
    # Execute the SQL query to retrieve chats
    c.execute('''SELECT Chats.*, sender.name AS sender_name, receiver.name AS receiver_name
                 FROM Chats
                 JOIN accounts AS sender ON Chats.sender_id = sender.user_id
                 JOIN accounts AS receiver ON Chats.receiver_id = receiver.user_id
                 WHERE sender.username = ? OR receiver.username = ?
                 ORDER BY Chats.timestamp''', (username, username))
    chats = c.fetchall()
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
def get_username(c, user_ID):
    c.execute("SELECT username FROM accounts WHERE user_id=?", (user_ID,))
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
def send_message(conn, c, sender_id, receiver_id, message):
    c.execute('''INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)''', (sender_id, receiver_id, message))
    conn.commit()
def get_messages(conn, c, user_id1, user_id2):
    c.execute('''SELECT * FROM messages WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?) ORDER BY timestamp''', (user_id1, user_id2, user_id2, user_id1))
    messages = c.fetchall()
    conn.close()
    return messages
