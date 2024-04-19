import sqlite3

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
    seen INTEGER DEFAULT 0,
    FOREIGN KEY (sender_id) REFERENCES accounts(user_id),
    FOREIGN KEY (receiver_id) REFERENCES accounts(user_id)
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
def create_groups(c):
    c.execute('''CREATE TABLE IF NOT EXISTS Groups (
        group_id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT NOT NULL
    );''')

def create_user_groups(c):
    c.execute('''CREATE TABLE IF NOT EXISTS UserGroups (
        user_id INTEGER,
        group_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES accounts(user_id),
        FOREIGN KEY (group_id) REFERENCES Groups(group_id),
        PRIMARY KEY (user_id, group_id)
    );''')
#register and login
def authenticate(c,username, password):
    c.execute("SELECT username FROM accounts WHERE username=?", (username,))
    result = c.fetchone()
    if not result:
        return 'not found'
    else:
         c.execute("SELECT username, password FROM accounts WHERE username=? AND password=?", (username,password))
         result = c.fetchone()
         if not result:
            return 'Wrong password.'
         else:
            return 'Login successful!'
         
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
#chatting functions
def check_chat_exists(c, sender_id, receiver_id):
        c.execute('''SELECT * FROM Chats 
                          WHERE (sender_id = ? AND receiver_id = ?) 
                          OR (sender_id = ? AND receiver_id = ?)''', 
                       (sender_id, receiver_id, receiver_id, sender_id))
        result = c.fetchone()
        if result:
            return True
        else: 
            return False
def get_user_chats(c, username):
    c.execute('''SELECT Chats.*, sender.username AS sender_name, receiver.username AS receiver_name
                 FROM Chats
                 JOIN accounts AS sender ON Chats.sender_id = sender.user_id
                 JOIN accounts AS receiver ON Chats.receiver_id = receiver.user_id
                 WHERE sender.username = ? OR receiver.username = ?
                 ORDER BY Chats.timestamp''', (username, username))
    chats = c.fetchall()
    return chats

def start_chat(conn, c, sender_id, receiver_id, initial_message):
    c.execute('''INSERT INTO Chats (sender_id, receiver_id, last_message) 
                          VALUES (?, ?, ?)''', (sender_id, receiver_id, initial_message))
    conn.commit()

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
    
def get_users(c):
    c.execute("SELECT username FROM accounts")
    result = c.fetchall()
    return result


def find_request_id(c, sender_id, receiver_id):
    c.execute('''SELECT request_id
                 FROM friend_requests
                 WHERE sender_id = ? AND receiver_id = ?''', (sender_id, receiver_id))
    request_id = c.fetchone()
    return request_id[0]

#friends functions
def send_friend_request(conn, c, sender_id, receiver_id):
    c.execute('''INSERT INTO friend_requests (sender_id, receiver_id) VALUES (?, ?)''', (sender_id, receiver_id))
    conn.commit()
    print("friend request sent")


def accept_friend_request(conn, c, request_id):
    c.execute('''UPDATE friend_requests SET status = 'accepted' WHERE request_id = ?''', (request_id,))
    conn.commit()


def reject_friend_request(conn, c, request_id):
    c.execute('''UPDATE friend_requests SET status = 'rejected' WHERE request_id = ?''', (request_id,))
    conn.commit()


def get_pending_friend_requests(c, user_id):
    c.execute('''SELECT * FROM friend_requests WHERE receiver_id = ? AND status = 'pending' ''', (user_id,))
    requests = c.fetchall()
    return requests


def get_friends(c, user_id):
    c.execute('''SELECT accounts.user_id, accounts.username
                 FROM friend_requests
                 JOIN accounts ON (friend_requests.sender_id = accounts.user_id OR friend_requests.receiver_id = accounts.user_id)
                 WHERE (friend_requests.sender_id = ? OR friend_requests.receiver_id = ?)
                 AND friend_requests.status = 'accepted' AND accounts.user_id != ?''',
              (user_id, user_id, user_id))
    friends = c.fetchall()
    return friends
#messaging functions
def send_message(conn, c, sender_id, receiver_id, message):
    c.execute('''INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)''', (sender_id, receiver_id, message))
    conn.commit()
    c.execute('''UPDATE Chats SET last_message=? WHERE ((sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)) ''', (message, sender_id, receiver_id, receiver_id, sender_id))
    conn.commit()
def get_old_messages(c, user_id1, user_id2):
    c.execute('''SELECT * FROM messages 
                 WHERE ((sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?))
                 AND seen = 1 
                 ORDER BY timestamp''', (user_id1, user_id2, user_id2, user_id1))
    messages = c.fetchall()
    return messages
def get_new_message(conn, c, sender_id, receiver_id):
    c.execute('''SELECT message_id, sender_id, message 
              FROM messages 
              WHERE ((sender_id = ? AND receiver_id = ?) 
              OR (sender_id = ? AND receiver_id = ?))
              AND seen = 0''', (sender_id, receiver_id, receiver_id, sender_id))

     
    new_messages = c.fetchall()
    
    # Mark the fetched messages as seen
    for msg in new_messages:
        message_id = msg[0]
        c.execute('''UPDATE messages SET seen = 1 WHERE message_id = ? AND receiver_id = ?''', (message_id, receiver_id ))
        conn.commit()
    
    return new_messages

#groups functions
def send_group_message(conn, c, sender_id, group_id, message):
    c.execute('''INSERT INTO messages (sender_id, receiver_id, message) 
                  SELECT ?, user_id, ? FROM UserGroups WHERE group_id = ?''', 
              (sender_id, message, group_id))
    conn.commit()

def get_group_messages(c, group_id):
    c.execute('''SELECT * FROM messages 
                  WHERE receiver_id IN 
                  (SELECT user_id FROM UserGroups WHERE group_id = ?)''', (group_id,))
    messages = c.fetchall()
    return messages
def start_group(conn, c, creator_id, group_name, members):
    # Create a new group
    c.execute('''INSERT INTO Groups (group_name) VALUES (?)''', (group_name,))
    conn.commit()
    group_id = c.lastrowid
    
    # Add creator to the group
    c.execute('''INSERT INTO UserGroups (user_id, group_id) VALUES (?, ?)''', (creator_id, group_id))
    
    # Add other members to the group
    for member_id in members:
        c.execute('''INSERT INTO UserGroups (user_id, group_id) VALUES (?, ?)''', (member_id, group_id))
    
    conn.commit()
    print("Group '{}' created successfully!".format(group_name))
    return group_id
def get_group_id(c, group_name):
    c.execute('''SELECT group_id FROM Groups WHERE group_name = ?''', (group_name,))
    group_id = c.fetchone()
    if group_id:
        return group_id[0]
    else:
        print("Group '{}' not found.".format(group_name))
        return None
    
def display_groups(c, user_id):
    c.execute('''SELECT group_id, group_name FROM Groups
                 WHERE group_id IN (SELECT group_id FROM UserGroups WHERE user_id = ?)''', (user_id,))
    groups = c.fetchall()
    return groups
def add_to_group(conn, c, group_id, user_ids):
    for user_id in user_ids:
        # Check if the user is already a member of the group
        c.execute('''SELECT * FROM UserGroups WHERE user_id = ? AND group_id = ?''', (user_id, group_id))
        if not c.fetchone():
            # If the user is not already a member, add them to the group
            c.execute('''INSERT INTO UserGroups (user_id, group_id) VALUES (?, ?)''', (user_id, group_id))
            conn.commit()
            print("User with ID {} added to group ID {}".format(user_id, group_id))
        else:
            print("User with ID {} is already a member of group ID {}".format(user_id, group_id))



