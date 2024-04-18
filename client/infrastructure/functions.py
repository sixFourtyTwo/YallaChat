import socket
import time

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
        print('Commands: login, register, onlinecheck, add friend, help :D')
    elif(command == 'add friend'):
        addFriend(client)
    elif(command == 'fetch requests'):
        dispFriendRequests(client)
    elif(command == 'fetch friends'):
        dispFriends(client)
    elif(command == 'accept pending'):
        acceptFR(client)
    elif(command == 'reject pending'):
        rejectFR(client)
    elif(command == 'send message'):
        sendMessage(client)
    elif(command == 'disp messages'):
        getNewMsgs(client)
    elif(command == 'disp old messages'):
        getOldMsgs(client)
    elif(command == 'start chat'):
        startChat(client)
    elif(command == 'disp chats'):
        dispChats(client)

def addFriend(client):
    username = input('Username: ')
    message = 'ADDF ' + username
    client.send(message.encode('utf-8'))
    
    print(client.recv(1024).decode('utf-8'))
    return

def dispFriendRequests(client):
    friendReqs = getPendingFR(client)

    if(friendReqs == 'none'):
        print('You have no pending friend requests.')
        return

    print('Incoming Friend Requests: ')
    friends = friendReqs.split(',')

    for friend in friends:
        print('-' + friend)

def dispFriends(client):
    friendsList = getFriends(client)

    if(friendsList == 'none'):
        print('You have no friends. ')
        return
    
    print('Friends: ')
    friends = friendsList.split(',')

    for friend in friends:
        print('-' + friend)

def getFriends(client):
    client.send('GETF'.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def getPendingFR(client):
    client.send('GPFR'.encode('utf-8'))
    return client.recv(1024).decode('utf-8')

def acceptFR(client):
    friendReqs = getPendingFR(client)
    friends = friendReqs.split(',')
    other = None

    user = input('Username: ')

    for friend in friends:
        if(user == friend):
            other = friend
            break
    if(other == None):
        print('\'' + user + '\' does not exist in your pending friend requests.')
        return
    message = 'AcFR ' + other
    client.send(message.encode('utf-8'))

    print(client.recv(1024).decode('utf-8'))

def rejectFR(client):
    friendReqs = getPendingFR(client)
    friends = friendReqs.split(',')
    other = None

    user = input('Username: ')

    for friend in friends:
        if(user == friend):
            other = friend
            break
    if(other == None):
        print('\'' + user + '\' does not exist in your pending friend requests.')
        return
    message = 'RjFR ' + other
    client.send(message.encode('utf-8'))

    print(client.recv(1024).decode('utf-8'))

def collectLogin(client):
    uname = input('Username: ')
    password = input('Password: ')
    
    return login(client, uname, password)

def login(client, uname, password):
    message = 'LOGIN ' + uname + ' ' + password
    client.send(message.encode('utf-8'))

    repCode = client.recv(1024).decode('utf-8')
    return codeHandler(repCode)

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

    return register(client, name, email, uname, password)

def register(client, name, email, username, password):
    message = 'REGISTER ' + name + ' ' + email + ' ' + username + ' ' + password
    client.send(message.encode('utf-8'))

    repCode = client.recv(1024).decode('utf-8')
    return codeHandler(repCode)

def isOnlineCollector(client):
    user = input('Who do you wish to check?: ')
    print(isOnline(client, user))

def isOnline(client, user):
    message = 'IOnline ' + user
    client.send(message.encode('utf-8'))

    return client.recv(1024).decode('utf-8')

def getNewMsgs(client):
    other = input('Enter user: ')
    toSend = 'RcvMsg ' + other

    client.send(toSend.encode('utf-8'))
    messages = client.recv(1024).decode()

    if(messages == '///'):
        print('You have no new messages.')
    else:
        msgList = messages.split('///')
        for msg in msgList:
            print(msg)

def getOldMsgs(client):
    other = input('User: ')
    toSend = 'RcvOldMsg ' + other

    client.send(toSend.encode('utf-8'))
    messages = client.recv(1024).decode()

    if(messages == '///'):
        print('You have no messages with ' + other + '.')
    else:
        print('Chat: ' + other)
        msgList = messages.split('///')
        for msg in msgList:
            print(msg)

def getMessageInput():
    message = input('Enter your message: ')
    return message

def sendMessage(client):
    user = input('Enter user: ')
    uInput = getMessageInput()
    message = 'SMsg ' + user + ' ' + uInput

    client.send(message.encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

def startChat(client):
    user = input('Enter user: ')
    uInput = getMessageInput()
    message = 'StChat ' + user + ' ' + uInput

    client.send(message.encode('utf-8'))
    print(codeHandler(client.recv(1024).decode('utf-8')))

def dispChats(client):
    client.send('DispChats'.encode('utf-8'))
    chats = client.recv(1024).decode('utf-8')
    chatList = chats.split('///')

    for chat in chatList:
        print(chat)

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