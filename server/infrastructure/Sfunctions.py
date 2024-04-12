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
        
def login(server, message, cursor):
    username, password = message[1], message[2]
    reply = authenticate(cursor,username, password)
    server.send(reply.encode())

    return username

def register(server, message, cursor, db_conn):
    name, email, username, password = message[1], message[2], message[3], message[4]
    reply = register_account(db_conn, cursor, name, email, username, password)
    server.send(reply.encode())

    return username