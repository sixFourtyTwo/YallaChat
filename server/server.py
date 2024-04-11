import socket
import DB
import threading


port = input('Port Number: ')


def handler(conn, addr):
    message = conn.recv(1024).decode('utf-8').split()
    cmnd = message[0]
    if(cmnd == 'LOGIN'): 
        username, password = message[1], message[2]
        reply = DB.authenticate(username, password)
        conn.send(reply.encode())
        

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), 50))

    print('Server is now online.')
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()

Server()