import socket 
import infrastructure.functions as funcs

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
funcs.connect(client)

while True:
    try:
        command = input('Enter command [help]: ')
        funcs.commandHandler(client, command)
    except KeyboardInterrupt:
        break