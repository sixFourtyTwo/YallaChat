import socket
import DB
import threading
import queue
import infrastructure.Sfunctions as Sfunc

port = int(input('Port Number: '))


def handler(conn, addr):
    while True:
        db_conn, cursor = DB.connect_to_database()
        DB.create_accounts(cursor)
        print("Database connected successfully.")
        message = conn.recv(1024).decode('utf-8').split()
        cmnd = message[0]
        if(cmnd == 'LOGIN'): 
            username, password = message[1], message[2]
            reply = Sfunc.authenticate(cursor,username, password)
            conn.send(reply.encode())
        if(cmnd == "REGISTER"):
            name, email, username, password = message[1], message[2], message[3], message[4]
            reply = Sfunc.register_account(db_conn, cursor, name, email, username, password)
            conn.send(reply.encode())

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