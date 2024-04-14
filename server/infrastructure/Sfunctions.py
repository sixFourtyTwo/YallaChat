import sqlite3
import DB


    
def addFriend(c, conn, user, other):
    userID1 = DB.get_userID(user)
    userID2 = DB.get_userID(other)

    DB.send_friend_request(conn, c, userID1, userID2)
    return


        
def login(server, message, cursor):
    username, password = message[1], message[2]
    reply = DB.authenticate(cursor,username, password)
    server.send(reply.encode())

    return username

def register(server, message, cursor, db_conn):
    name, email, username, password = message[1], message[2], message[3], message[4]
    reply = DB.register_account(db_conn, cursor, name, email, username, password)
    server.send(reply.encode())

    return username