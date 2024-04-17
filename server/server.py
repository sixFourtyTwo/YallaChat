import socket
import DB
import threading
import infrastructure.Sfunctions as Sfunc

port = int(input('Port Number: '))
onlineUsers = {}

def handler(conn, addr):
    db_conn, cursor = DB.connect_to_database()
    DB.create_accounts(cursor)
    print("Database connected successfully.")
    
    currentUser = None
    while True:
        try:
            message = conn.recv(1024).decode('utf-8').split()
            if message == []:
                raise ConnectionResetError
        
            cmnd = message[0]
            if(currentUser == None):

                if(cmnd == 'LOGIN'): 
                    username = Sfunc.login(conn, message, cursor)
                    onlineUsers.update({username:username})
                    currentUser = username

                elif(cmnd == "REGISTER"):
                    username = Sfunc.register(conn, message, cursor, db_conn)
                    onlineUsers.update({username:username})
                    currentUser = username
                
                else:
                    reply = 'Please login or register before using this command.'
                    conn.send(reply.encode('utf-8'))
            else:
                if(cmnd == 'IOnline'):
                    user = message[1]
                    if (user not in onlineUsers):
                        reply = 'OFFLINE'
                    else: reply = 'ONLINE'
                    if(not DB.lookup_user(cursor, user)):
                        reply = 'User does not exist.'
                    else:
                        if (user not in onlineUsers):
                            reply = 'OFFLINE'
                        else: reply = 'ONLINE'
                    
                    conn.send(reply.encode('utf-8'))

                elif(cmnd == 'SMsg'):
                    user = message[1]
                    msg = message[2:]
                    msg = ' '.join(msg)

                    Sfunc.sendMessage(conn, db_conn, cursor, currentUser, user, msg)

                elif(cmnd == 'StChat'):
                    other = message[1]
                    msg = message [2:]
                    msg = ' '.join(msg)

                    Sfunc.startChat(conn, db_conn, cursor, currentUser, other, msg)

                elif(cmnd == 'DispChats'):
                    Sfunc.getChats(conn, cursor, currentUser)

                elif(cmnd == 'RcvMsg'):
                    user = message[1]
                    Sfunc.recvMessages(conn, db_conn, cursor, currentUser, user)

                elif(cmnd == 'GPFR'):
                    Sfunc.getPendingFR(conn, cursor, currentUser)

                elif(cmnd == 'GETF'):
                    Sfunc.getFriends(conn, cursor, currentUser)

                elif(cmnd == 'AcFR'):
                    user = message[1]
                    Sfunc.acceptFR(conn, cursor, db_conn, currentUser, user)

                elif(cmnd == 'RjFR'):
                    user = message[1]
                    Sfunc.rejectFR(conn, cursor, db_conn, currentUser, user)

                elif(cmnd == 'ADDF'):
                    user = message[1]
                    reply = Sfunc.addFriend(cursor, db_conn, currentUser, user)
                    conn.send(reply.encode('utf-8'))

                elif(cmnd == 'DISCONNECT'):
                    if(currentUser != None):
                        onlineUsers.pop(currentUser)
                        break
                    break
        except (ConnectionResetError, ConnectionAbortedError): 
            if(currentUser != None):
                onlineUsers.pop(currentUser)
                break
    print('User ' + currentUser + ' has gracefully disconnected.')


def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), port))

    localIP = socket.gethostbyname(socket.gethostname())
    localPort = str(port)
    print('Server is now online on IP: ' + localIP + ' and port: ' +localPort)
    
    try:
        server.listen()
    except KeyboardInterrupt:
        print('Server shutting down.')
        return
    
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handler, args=(conn, addr))
            thread.start()
        except KeyboardInterrupt: #this does not work, because server.accept() is blocking indefinitely
            print('Server shutting down.')
            break

Server()