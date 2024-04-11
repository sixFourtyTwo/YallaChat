import socket
import time

def connect(client):
    for j in range(12):
        try:
            client.connect((socket.gethostbyname(socket.gethostname()), 9999))
            print('Connection achieved.')
            return
        except:
            print('No response... ['+ str(j) + '/12]')
            time.sleep(5)
    print('Connection failed.')
    return
