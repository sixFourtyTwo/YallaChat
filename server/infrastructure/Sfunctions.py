
import sqlite3


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
        
    

