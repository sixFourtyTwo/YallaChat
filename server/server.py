import socket
import DB
import threading
import queue
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
                continue
            print(message)
            cmnd = message[0]
            if(cmnd == 'LOGIN'): 
                username, password = message[1], message[2]
                reply = Sfunc.authenticate(cursor,username, password)
                conn.send(reply.encode())

                onlineUsers.update({username:username})
                currentUser = username 

            elif(cmnd == "REGISTER"):
                name, email, username, password = message[1], message[2], message[3], message[4]
                reply = Sfunc.register_account(db_conn, cursor, name, email, username, password)
                print('are we sending?')
                print(reply)
                conn.send(reply.encode())

                onlineUsers.update({username:username})
                currentUser = username

            elif(cmnd == 'IOnline'):
                user = message[1]
                if (user not in onlineUsers):
                    return 'OFFLINE'
                else: return 'ONLINE'   

            elif(cmnd == 'DISCONNECT'):
                if(currentUser != None):
                    onlineUsers.pop(currentUser)
                    break
                break
        except (ConnectionResetError, ConnectionAbortedError): 
            if(currentUser != None):
                onlineUsers.pop(currentUser)
                break
    print('mark2')
            

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), port))

    print('Server is now online.')
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()

Server()