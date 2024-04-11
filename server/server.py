import socket
import DB
import threading


port = input('Port Number: ')


def handler(conn, addr):
    cmnd = conn.recv(1024).decode('utf-8')

    if(cmnd == 'foo'): #implement commands like this
        pass #do something

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostbyname(socket.gethostname()), 50))

    print('Server is now online.')

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()

Server()