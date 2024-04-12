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

def login(client, uname, password):
    message = 'LOGIN ' + uname + ' ' + password
    client.send(message.encode('utf-8'))

    repCode = client.recv(1024).decode('utf-8')
    return codeHandler(repCode)

def register(client, name, email, username, password):
    message = 'REGISTER ' + name + ' ' + email + ' ' + username + ' ' + password
    client.send(message.encode('utf-8'))

    repCode = client.recv(1024).decode('utf-8')
    return codeHandler(repCode)

def codeHandler(code):
    if(code == '100'):
        return 'Account has been registered.'
    elif(code == '102'):
        return 'The password you entered is incorrect.'
    elif(code == '104'):
        return 'The given user is not found.'
    elif(code == '105'):
        return 'Login Successful.'