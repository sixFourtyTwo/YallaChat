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
        
def login(server, cursor, username, password):
    dbCheck = DB.authenticate(cursor, username, password)
    if(dbCheck == 'not found'):
        reply = 'User does not exist.'
    else:
        reply = dbCheck
    server.send(reply.encode())

    return dbCheck

def acceptFR(server, c, conn, user, other):
    userID = DB.get_userID(c, user)
    otherID = DB.get_userID(c, other)

    reqID = DB.find_request_id(c, otherID, userID)
    DB.accept_friend_request(conn, c, reqID)

    reply = other + ' is now your friend!'
    server.send(reply.encode('utf-8'))

def rejectFR(server, c, conn, user, other):
    userID = DB.get_userID(c, user)
    otherID = DB.get_userID(c, other)

    reqID = DB.find_request_id(c, otherID, userID)
    DB.reject_friend_request(conn, c, reqID)

    reply = 'Rejected ' + other + '\'s friend request.'
    server.send(reply.encode('utf-8'))

def getFriends(server, c, user):
    userID = DB.get_userID(c, user)
    friends = DB.get_friends(c, userID)

    if(len(friends) == 0):
        reply = 'none'

    else:
        reply = ''

        for i in range(0, len(friends)):
            reply = reply + friends[i][1] + ','
        
        reply = reply.rstrip(reply[-1])

    server.send(reply.encode('utf-8'))

def getPendingFR(server, c, user):
    userID = DB.get_userID(c, user)
    list = DB.get_pending_friend_requests(c, userID)

    if(len(list) == 0):
        reply = 'none'
    
    else:
        reply = ''

        for i in range(0, len(list)):
            reply = reply + str(DB.get_username(c, list[i][1])) + ','
        
        reply = reply.rstrip(reply[-1])

    server.send(reply.encode('utf-8'))

def sendMessage(server, conn, c, user, other, message):
    if(DB.lookup_user(c, other) == False):
        return 'User doesn\'t exist.'

    userID = DB.get_userID(c, user)
    otherID = DB.get_userID(c, other)

    DB.send_message(conn, c, userID, otherID, message)
    server.send('100'.encode('utf-8'))

def startChat(server, conn, cursor, user, other, message):
    if(DB.lookup_user(cursor, other) == False):
        reply = '104'
    else:
        userID = DB.get_userID(cursor, user)
        otherID = DB.get_userID(cursor, other)

        DB.start_chat(conn, cursor, userID, otherID, message)
        DB.send_message(conn, cursor, userID, otherID, message)
        reply = '100'
    server.send(reply.encode('utf-8'))

def checkChats(c, user, other):
    if(DB.lookup_user(c, other) == False):
        return True
    else:
        userID = DB.get_userID(c, user)
        otherID = DB.get_userID(c, other)
        return DB.check_chat_exists(c, userID, otherID)

def getChats(server, c, user):
    chats = DB.get_user_chats(c, user)
    if(chats == []):
            reply = '///'
    else:
        reply = ''
        for chat in chats:
            user1 = DB.get_username(c, chat[1])
            user2 = DB.get_username(c, chat[2])

            if(user1 == user):
                title = user2
            elif(user2 == user):
                title = user1
            reply = reply + title + ': ' + chat[3] + '///'
    print(reply)
    server.send(reply.encode('utf-8'))

def recvOldMessages(server, c, user, other):
    if(DB.lookup_user(c, other) == False):
        reply = 'User doesn\'t exist.'
    else:
        userID = DB.get_userID(c, user)
        otherID = DB.get_userID(c, other)
        messages = DB.get_old_messages(c, userID, otherID)

        if(messages == []):
                reply = '///'
        else:
            reply = ''
            for msg in messages:
                other = DB.get_username(c, msg[1])
                reply = reply + other + ': ' + msg[3] + '///'
                
            reply = reply.rstrip(reply[-1])

    server.send(reply.encode('utf-8'))

def recvMessages(server, conn, c, user, other):
    userID = DB.get_userID(c, user)
    otherID = DB.get_userID(c, other)
    messages = DB.get_new_message(conn, c, otherID, userID)

    if(messages == []):
        reply = '///'
    else:
        reply = ''
        for msg in messages:
            other = DB.get_username(c, msg[1])
            reply = reply + other + ': ' + msg[2] + '///'
            
        reply = reply.rstrip(reply[-1])
    server.send(reply.encode('utf-8'))

def register(server, message, cursor, db_conn):
    name, email, username, password = message[1], message[2], message[3], message[4]
    reply = DB.register_account(db_conn, cursor, name, email, username, password)
    server.send(reply.encode())

    return username