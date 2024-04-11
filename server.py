import socket
import DB.py
import threading

def Server():
    serverSocket = socket.socket()








while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handler, args=(conn, addr))
    thread.start()