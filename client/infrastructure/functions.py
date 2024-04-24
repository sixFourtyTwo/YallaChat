import socket
import time
import random

def connect(client):
    IP = input('Enter IP: ')
    for j in range(12):
        try:
            client.connect((IP, 9999))
            print('Connection achieved.')
            return
        except:
            print('No response... ['+ str(j) + '/12]')
            time.sleep(5)
    print('Connection failed.')
    return

def commandHandler(client, command):
    if(command == 'login'):
        collectLogin(client)
    elif(command == 'register'):
        collectRegister(client)
    elif(command == 'onlinecheck'):
        isOnlineCollector(client)
    elif(command == 'help'):
        print('Commands: login, register, onlinecheck, add friend, help')
    elif(command == 'add friend'):
        addFriendsCollector(client)
    elif(command == 'fetch requests'):
        dispFriendReqsCollector(client)
    elif(command == 'fetch friends'):
        dispFriendsCollector(client)
    elif(command == 'accept pending'):
        acceptFRCollector(client)
    elif(command == 'reject pending'):
        rejectFRCollector(client)
    elif(command == 'send message'):
        sendMessageCollector(client)
    elif(command == 'disp messages'):
        getNewMessagesCollector(client)
    elif(command == 'disp old messages'):
        getOldMsgsCollector(client)
    elif(command == 'start chat'):
        startChatCollector(client)
    elif(command == 'disp chats'):
        dispChatsCollector(client)
    elif(command == 'send group message'):
        sendGroupMessageCollector(client)
    elif(command == 'start group'):
        startGroupCollector(client)
    elif(command == 'GOF'):
        GOFColl(client)
    elif(command == 'GAU'):
        GAUColl(client)
    elif(command == 'GRU'):
        getRandomUserColl(client)

def addFriend(client, user):
    message = 'ADDF ' + user
    client.send(message.encode('utf-8'))
    
    return client.recv(1024).decode('utf-8')

def dispFriendRequests(client):
    friendReqs = getPendingFR(client)

    if(friendReqs == 'none'):
        return 'You have no pending friend requests.'

    return friendReqs.split(',')

def dispFriends(client):
    friendsList = getFriends(client)

    if(friendsList == 'none'):
        return 'You have no friends.'
    
    return friendsList.split(',')

def getFriends(client):
    client.send('GETF'.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def getPendingFR(client):
    client.send('GPFR'.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def acceptFR(client, user):
    friendReqs = getPendingFR(client)
    friends = friendReqs.split(',')
    other = None

    for friend in friends:
        if(user == friend):
            other = friend
            break
    if(other == None):
        return '\'' + user + '\' does not exist in your pending friend requests.'
    
    message = 'AcFR ' + other
    client.send(message.encode('utf-8'))

    return client.recv(1024).decode('utf-8')

def rejectFR(client, user):
    friendReqs = getPendingFR(client)
    friends = friendReqs.split(',')
    other = None

    for friend in friends:
        if(user == friend):
            other = friend
            break
    if(other == None):
        return '\'' + user + '\' does not exist in your pending friend requests.'
    
    message = 'RjFR ' + other
    client.send(message.encode('utf-8'))

    return client.recv(1024).decode('utf-8')

def login(client, uname, password):
    message = 'LOGIN ' + uname + ' ' + password
    client.send(message.encode('utf-8'))

    repCode = client.recv(1024).decode('utf-8')
    return repCode

def register(client, name, email, username, password):
    message = 'REGISTER ' + name + ' ' + email + ' ' + username + ' ' + password
    client.send(message.encode('utf-8'))

    repCode = client.recv(1024).decode('utf-8')
    return repCode

def isOnline(client, user):
    message = 'IOnline ' + user
    client.send(message.encode('utf-8'))

    return client.recv(1024).decode('utf-8')

def getNewMsgs(client, other):
    toSend = 'RcvMsg ' + other

    client.send(toSend.encode('utf-8'))
    messages = client.recv(1024).decode()

    return messages

def getGroupID(client, name):
    msg = 'GetGID ' + name
    client.send(msg.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def sendGroupMessage(client, message, groupName):
    groupId = getGroupID(client, groupName)
    
    if(groupId == 'Doesn\'t exist.'):
        return 'Group does not exist.'
    else:
        msg = 'SGM ' + groupId + ' ' + message
        client.send(msg.encode('utf-8'))
        return client.recv(1024).decode('utf-8')

def startGroup(client, name, members):
    message = 'SGroup ' + name + ' ' + members

    client.send(message.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def getOldMsgs(client, other):
    toSend = 'RcvOldMsg ' + other

    client.send(toSend.encode('utf-8'))
    messages = client.recv(1024).decode()

    return messages

def sendMessage(client, user, uInput):
    message = 'SMsg ' + user + ' ' + uInput

    client.send(message.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def startChat(client, user, uInput):
    message = 'StChat ' + user + ' ' + uInput

    client.send(message.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def dispChats(client):
    client.send('DispChats'.encode('utf-8'))
    chats = client.recv(1024).decode('utf-8')

    if(chats == '///'):
        chatList = []
    else:
        chatList = chats.split('///')
        chatList.pop()

    return chatList

def getOnlineFriends(client):
    friends = getFriends(client)

    msg = 'GOFriends ' + friends
    client.send(msg.encode('utf-8'))
    reply = client.recv(1024).decode('utf-8')

    if(reply == 'None'):
        reply = 'None of your friends are online.'
    else:
        reply = reply.split(',')

    return reply

def getRandomUser(client):
    users = getAllUsers(client)
    users = users.split(',')

    rndmNbr = random.randint(0, len(users)-1)

    return users[rndmNbr]

def getAllUsers(client):
    msg = 'GAU'
    client.send(msg.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def codeHandler(code):
    if(code == '100'):
        return 'Success'
    elif(code == '102'):
        return 'The password you entered is incorrect.'
    elif(code == '104'):
        return 'The given user is not found.'
    elif(code == '105'):
        return 'Login Successful.'
    elif(code == '111'):
        return 'User already exits, try loggin in.'
    elif(code == '120'):
        return 'Please login first.'
    elif(code == '444'):
        return 'Something went wrong.'    



##COLLECTOR FUNCTIONS, USELESS WHEN GUI IS IMPLEMENTED:
def isOnlineCollector(client):
    user = input('Who do you wish to check?: ')
    print(isOnline(client, user))

def addFriendsCollector(client):
    user = input('Username: ')
    print(addFriend(client, user))

def collectRegister(client):
    name = input('Enter your name: ')

    while True:
        email = input('Enter email: ')
        try:
            if(email.split('@')[1] != 'gmail.com'):
                raise Exception
            else: break
        except Exception:
            print('Email is invalid.')

    uname = input('Enter username: ')
    password = input('Enter password: ')

    print(register(client, name, email, uname, password))

def collectLogin(client):
    uname = input('Username: ')
    password = input('Password: ')
    
    print(login(client, uname, password))

def dispFriendsCollector(client):
    friends = dispFriends(client)

    if(friends == 'You have no friends.'):
        print(friends)
    else:
        for friend in friends:
            print('-' + friend)

def dispFriendReqsCollector(client):
    friends = dispFriendRequests(client)

    if(friends == 'You have no pending friend requests.'):
        print(friends)
    else:
        for friend in friends:
            print('-' + friend)

def acceptFRCollector(client):
    user = input('Username: ')
    print(acceptFR(client, user))

def rejectFRCollector(client):
    user = input('Username: ')
    print(rejectFR(client, user))

def getMessageInput():
    message = input('Enter your message: ')
    return message

def sendMessageCollector(client):
    user = input('Enter user: ')
    uInput = getMessageInput()

    print(sendMessage(client, user, uInput))

def getNewMessagesCollector(client):    
    other = input('Enter user: ')
    messages = getNewMsgs(client, other)

    if(messages == '///'):
        print('You have no new messages.')
    else:
        msgList = messages.split('///')
        for msg in msgList:
            print(msg)

def getOldMsgsCollector(client):
    other = input('User: ')
    messages = getOldMsgs(client, other)

    if(messages == '///'):
        print('You have no messages with ' + other + '.')
    else:
        print('Chat: ' + other)
        msgList = messages.split('///')
        for msg in msgList:
            print(msg)

def startChatCollector(client):  
    user = input('User: ')
    uInput = getMessageInput()
    print(startChat(client, user, uInput))

def dispChatsCollector(client):
    print(dispChats(client))

def sendGroupMessageCollector(client):
    name = input('Enter group name: ')
    uInput = input('Enter message: ')
    print(sendGroupMessage(client, uInput, name))

def startGroupCollector(client):
    name = input('Enter Group Name: ')
    members = input('Enter members [seperated by commas]: ')

    print(startGroup(client, name, members))

def extract_first_part(string):
    # Find the index of the colon ":"
    colon_index = string.find(":")
    # If colon is found, return the substring before it, otherwise return the original string
    if colon_index != -1:
        return string[:colon_index]
    else:
        return string
    
def GOFColl(client):
    print(getOnlineFriends(client))

def GAUColl(client):
    print(getAllUsers(client))

def getRandomUserColl(client):
    print(getRandomUser(client))