import socket 
import infrastructure.functions as funcs

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
funcs.connect(client)

name = input('Enter name: ')
email = input('Enter email: ')
username = input('Enter username: ')
password = input('Enter password: ')

print(funcs.register(client, name, email, username, password))
