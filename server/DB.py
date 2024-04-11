import sqlite3
import os
conn = sqlite3.connect("accounts.db")
c = conn.cursor()

def create_accounts(c):
    c.execute('''CREATE TABLE IF NOT EXISTS accounts(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             email TEXT,
           username TEXT,
             password TEXT)
           ''')
def create_chats(c):
    pass
    
    
def register_account(name, email, username, password):
    c.execute("SELECT username FROM accounts WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        print("User already exits try logging in ")
        return 409
    else:
        c.execute("INSERT INTO accounts VALUES (NULL, ?, ?, ?, ?);", (name, email,username, password))
        conn.commit()
        print("Accout registered!")
        return 200

def authenticate(username, password):
    c.execute("SELECT username FROM accounts WHERE username=?", (username,))
    result = c.fetchone()
    if not result:
        print("User not found")
        return 401
    else:
         c.execute("SELECT username, password FROM accounts WHERE username=? AND password=?", (username,password))
         result = c.fetchone()
         if not result:
             print("wrong password!")
             return 409
         else:
            print("Login succesful")
            return 200
        
    


conn.close()
