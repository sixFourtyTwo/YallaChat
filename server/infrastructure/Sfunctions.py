import sqlite3
import DB


def addFriend(c, conn, user, other):
    if(DB.lookup_user(c, other) == False):
        reply =  'User does not exist.'
    else:
        userID1 = DB.get_userID(c, user)
        userID2 = DB.get_userID(c, other)

        DB.send_friend_request(conn, c, userID1, userID2)
        reply = 'Friend request sent to ' + other + '.'

    return reply
        
def login(server, message, cursor):
    username, password = message[1], message[2]
    reply = DB.authenticate(cursor,username, password)
    server.send(reply.encode())

    return username

def getPendingFR(server, c, conn, user):
    userID = DB.get_userID(c, user)
    reply = DB.get_pending_friend_requests(conn, c, userID)
    server.send(str(reply).encode('utf-8'))
    print(str(reply))

def register(server, message, cursor, db_conn):
    name, email, username, password = message[1], message[2], message[3], message[4]
    reply = DB.register_account(db_conn, cursor, name, email, username, password)
    server.send(reply.encode())

    return username