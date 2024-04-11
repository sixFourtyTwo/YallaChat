import socket
import DB.py
import threading

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("Yalla Chat", 5050))

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()

def handler():
    pass