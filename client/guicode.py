import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from PyQt5 import uic
import infrastructure.functions as funcs
import socket 
import sys
import threading
import re
import os
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QFileDialog, QVBoxLayout


class ClientSocketManager:
    def __init__(self):
        self.client = None

    def connect_to_server(self, ip, port):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip, port))
            return True
        except Exception as e:
            print("Error connecting to server:", e)
            return False

    def is_connected(self):
        return self.client is not None

    def get_client(self):
        return self.client


class ChatMainWindow(qtw.QDialog):
    def __init__(self, chat_list, client_manager):
        super().__init__()
        self.chat_list = chat_list
        self.client_manager = client_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YALLA CHAT")
        self.setWindowFlags(
            qtc.Qt.Window | qtc.Qt.WindowMinimizeButtonHint | qtc.Qt.WindowMaximizeButtonHint | qtc.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 255);")

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        # Display recent chats
        self.recent_chats_label = qtw.QLabel("Recent Chats:")
        self.recent_chats_label.setStyleSheet("font-size: 18px; color: rgba(0, 0, 0, 200);")
        self.layout.addWidget(self.recent_chats_label, alignment=qtc.Qt.AlignCenter)
        self.recent_chats_list = qtw.QListWidget()
        self.recent_chats_list.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
        for chat in self.chat_list:
            chat_button = qtw.QPushButton(chat)
            chat_button.clicked.connect(lambda checked, button=chat_button: self.open_chat_window(button))
            item = qtw.QListWidgetItem()
            item.setSizeHint(chat_button.sizeHint())
            self.recent_chats_list.addItem(item)
            self.recent_chats_list.setItemWidget(item, chat_button)
        self.layout.addWidget(self.recent_chats_list)

        # Add a search input field and button to search for online users
        self.search_layout = qtw.QHBoxLayout()
        self.layout.addLayout(self.search_layout)
        self.search_input = qtw.QLineEdit(placeholderText="Online User Check")
        self.search_input.setStyleSheet("background-color: rgba(255, 255, 255, 255); border: 1px solid rgba(0, 0, 0, 100);")
        self.search_layout.addWidget(self.search_input)
        self.search_button = qtw.QPushButton("Search")
        self.search_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.search_button.clicked.connect(self.search_online_users)
        self.search_layout.addWidget(self.search_button)

        # Display all server registered users
        self.online_users_label = qtw.QLabel("Registered Users:")
        self.online_users_label.setStyleSheet("font-size: 18px; color: rgba(0, 0, 0, 200);")
        self.layout.addWidget(self.online_users_label, alignment=qtc.Qt.AlignCenter)
        self.online_users_list = qtw.QTextEdit()
        self.online_users_list.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
        self.layout.addWidget(self.online_users_list)
        userlist=funcs.getAllUsers(self.client_manager.get_client())
        userlist = userlist.replace(',', '\n')
        self.online_users_list.setPlainText( userlist)

        # Add a "View Friends" button
        self.view_friends_button = qtw.QPushButton("View Friends")
        self.view_friends_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.view_friends_button.clicked.connect(self.view_friends)
        self.layout.addWidget(self.view_friends_button)

        # Add a "New Chat" button to open a window for starting a new chat with a friend
        self.new_chat_button = qtw.QPushButton("New Chat")
        self.new_chat_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.new_chat_button.clicked.connect(self.new_chat)
        self.layout.addWidget(self.new_chat_button)
        
        self.refresh_button = qtw.QPushButton("Refresh")
        self.refresh_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.refresh_button.clicked.connect(self.refreshChats)
        self.layout.addWidget(self.refresh_button)
        self.layout.addStretch()

        self.layout.addStretch()
        
    def refreshChats(self):
        try:
            # Clear existing chat list
            self.recent_chats_list.clear()
            # Fetch updated chat list
            chat_list = funcs.dispChats(self.client_manager.get_client())
            # Populate the chat list widget with updated chats
            for chat in chat_list:
                chat_button = qtw.QPushButton(chat)
                chat_button.clicked.connect(lambda checked, button=chat_button: self.open_chat_window(button))
                item = qtw.QListWidgetItem()
                item.setSizeHint(chat_button.sizeHint())
                self.recent_chats_list.addItem(item)
                self.recent_chats_list.setItemWidget(item, chat_button)
                userlist=funcs.getAllUsers(self.client_manager.get_client())
                userlist = userlist.replace(',', '\n')
                self.online_users_list.setPlainText( userlist)
        except Exception as e:
            print("Error refreshing chats:", e)

    def search_online_users(self):
        if self.search_input.text()!="":
            search_window = SearchWindow(self.client_manager.get_client(), self.search_input)
            search_window.exec_()
        else:
            pass
            #qtw.QMessageBox.warning(self, "Attention", funcs.isOnline(self.client_manager.get_client(), search_input.text()))

    def view_friends(self):
        friends_window = FriendsWindow(self.client_manager.get_client())
        friends_window.exec_() 

    def new_chat(self):
        new_chat_window = NewChatWindow(self.client_manager.get_client())
        new_chat_window.exec_()
        #if (new_chat_window.exec_()==0):
        #   chat_list = funcs.dispChats(self.client_manager.get_client())
        #   self.show_chat_list(chat_list)

    def open_chat_window(self, button):
        chat_title = button.text()
        client = self.client_manager.get_client()
        if client is None:
            print("Client socket is not connected.")
            return
        chatting_window = ChattingWindow(chat_title, client)
        chatting_window.exec_()

    def show_chat_list(self, chat_list):
        chat_main_window = ChatMainWindow(chat_list, self.client_manager.get_client())
        chat_main_window.exec_()


class ChattingWindow(qtw.QDialog):
    message_received = qtc.pyqtSignal(str)

    def __init__(self, chat_title, client):
        super().__init__()
        self.chat_title = chat_title
        self.client = client
        self.running = True
        self.initUI()
        self.fetch_messages()  # Fetch both old and new messages when window is initialized

    def initUI(self):
        self.setWindowTitle(self.chat_title)
        self.layout = qtw.QVBoxLayout(self)

        self.message_area = qtw.QTextEdit()
        self.layout.addWidget(self.message_area)

        self.input_field = qtw.QLineEdit()
        self.layout.addWidget(self.input_field)

        self.send_button = qtw.QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)
        
        self.multi_button = qtw.QPushButton("Multimedia")
        self.multi_button.clicked.connect(self.send_multimedia)
        self.layout.addWidget(self.multi_button)

        # Back button
        self.back_button = qtw.QPushButton("Back")
        self.back_button.clicked.connect(self.close_window_and_go_back)
        self.layout.addWidget(self.back_button)

        # Start a separate thread to continuously fetch messages
        self.fetch_thread = threading.Thread(target=self.continuous_fetch)
        self.fetch_thread.start()

        self.message_received.connect(self.update_message_area)

    def continuous_fetch(self):
        while self.running:
            try:
                messages = funcs.getNewMsgs(self.client, funcs.extract_first_part(self.chat_title))
                if messages:
                    self.message_received.emit(messages)
            except Exception as e:
                print("Error fetching messages:", e)
            qtc.QThread.msleep(2000)  # Fetch messages every 2 seconds

    def fetch_messages(self):
        try:
            old_messages = funcs.getOldMsgs(self.client, funcs.extract_first_part(self.chat_title))
            new_messages = funcs.getNewMsgs(self.client, funcs.extract_first_part(self.chat_title))
            messages = old_messages + "///" + new_messages
            self.update_message_area(messages)  # Update message area directly
        except Exception as e:
            print("Error fetching messages:", e)

    def update_message_area(self, messages):
        message_list = messages.split("///")
        messages_to_display = []  # Use a list to store messages to maintain the order
        for message in message_list:
            if message.strip():  # Check if the message is not empty after stripping whitespace
                messages_to_display.append(message)
        for message in messages_to_display:
            self.message_area.append(message)

    def send_message(self):
        message = self.input_field.text()
        try:
            funcs.sendMessage(self.client, funcs.extract_first_part(self.chat_title), message)
            self.input_field.clear()  # Clear input field after sending the message
            self.update_message_area(message)  # Update message area with the sent message immediately
        except Exception as e:
            print("Error sending message:", e)

    def close_window_and_go_back(self):
        self.running = False  # Stop the fetch thread when the window is closed
        self.close()  # Close the current window

    def closeEvent(self, event):
        self.running = False  # Stop the fetch thread when the window is closed
        event.accept()
        
    def send_multimedia(self):
        myApp = MyApp()
        myApp.exec_()


class SearchWindow(qtw.QDialog):
    def __init__(self, client, user):
        super().__init__()
        self.user = user
        self.client = client
        self.initUI()

    def initUI(self):
        self.setWindowTitle("User Search")
        self.layout = qtw.QVBoxLayout(self)
        reply=funcs.isOnline(self.client, self.user.text())
        reply2= self.user.text()+" is "+reply
        self.search_label = qtw.QLabel(reply2)
        self.search_label.setStyleSheet("font-size: 18px; color: rgba(0, 0, 0, 200);")
        self.layout.addWidget(self.search_label, alignment=qtc.Qt.AlignCenter)
        self.start_chat2_button = qtw.QPushButton("Start Chat")
        self.start_chat2_button.clicked.connect(lambda: funcs.startChat(self.client, self.user.text(), "New Chat"))
        self.layout.addWidget(self.start_chat2_button)
        self.accept()

class NewChatWindow(qtw.QDialog):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.initUI()

    def initUI(self):
        self.setWindowTitle("New Chat")
        self.layout = qtw.QVBoxLayout(self)
        self.input_field = qtw.QLineEdit()
        self.layout.addWidget(self.input_field)
        self.start_chat_button = qtw.QPushButton("Start Chat")
        self.start_chat_button.clicked.connect(lambda: funcs.startChat(self.client, self.input_field.text(), "New Chat"))
        self.layout.addWidget(self.start_chat_button)
        self.random_chat_button = qtw.QPushButton("Random Chat")
        self.random_chat_button.clicked.connect(lambda: funcs.startChat(self.client, funcs.getRandomUser(self.client), "New Chat"))
        self.layout.addWidget(self.random_chat_button)
        self.accept()

class SignInWindow(qtw.QDialog):
    def __init__(self, client_manager):
        super().__init__()
        self.client_manager = client_manager
        self.initUI()

    def initUI(self):
        uic.loadUi('loginUi1.1.ui', self)
        self.pushButton.clicked.connect(self.sign_in)
        self.pushButton_2.clicked.connect(self.show_registration)

    def sign_in(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        ip = '192.168.56.1'
        port = 9999

        if not self.client_manager.connect_to_server(ip, port):
            print("Failed to connect to server")
            return

        result = funcs.login(self.client_manager.get_client(), username, password)
        if result == 'Login successful!':
            print(result)
            chat_list = funcs.dispChats(self.client_manager.get_client())
            self.show_chat_list(chat_list)

    def show_chat_list(self, chat_list):
        chat_main_window = ChatMainWindow(chat_list, self.client_manager)
        chat_main_window.exec_()


    def show_registration(self):
        registration_window = RegistrationWindow(self.client_manager)
        if registration_window.exec_() == qtw.QDialog.Accepted:
            self.show_chat_list([])

class RegistrationWindow(qtw.QDialog):
    def __init__(self, client_manager):
        super().__init__()
        self.client_manager = client_manager
        self.initUI()

    def initUI(self):
        uic.loadUi('registerUi.ui', self)
        self.pushButton.clicked.connect(self.register)
        self.pushButton_2.clicked.connect(self.show_login_window)

    def register(self):
        name = self.lineEdit_4.text()
        email = self.lineEdit_3.text()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        ip = "192.168.56.1"
        port = 9999

        if not self.client_manager.connect_to_server(ip, port):
            print("Failed to connect to server")
            return
        result = funcs.register(self.client_manager.get_client(), name, email, username, password)
        print(result)
        if result == '100':
            chat_list = funcs.dispChats(self.client_manager.get_client())
            self.show_chat_list(chat_list)

        self.accept()

    def show_chat_list(self, chat_list):
        chat_main_window = ChatMainWindow(chat_list, self.client_manager)
        chat_main_window.exec_()

    def show_login_window(self):
        login_window = SignInWindow(self.client_manager)
        login_window.exec_()


class PendingRequestsWindow(qtw.QDialog):
    request_accepted = qtc.pyqtSignal()

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pending Friend Requests")
        self.layout = qtw.QVBoxLayout(self)

        # Display pending friend requests
        self.requests_label = qtw.QLabel("Pending Friend Requests:")
        self.requests_label.setStyleSheet("font-size: 18px; color: rgba(0, 0, 0, 200);")
        self.layout.addWidget(self.requests_label, alignment=qtc.Qt.AlignCenter)
        self.requests_list = qtw.QListWidget()
        self.requests_list.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
        self.layout.addWidget(self.requests_list)

        # Add a button to accept the selected request
        self.accept_button = qtw.QPushButton("Accept Request")
        self.accept_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.accept_button.clicked.connect(self.accept_request)
        self.layout.addWidget(self.accept_button)

        # Add a button to reject the selected request
        self.reject_button = qtw.QPushButton("Reject Request")
        self.reject_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.reject_button.clicked.connect(self.reject_request)
        self.layout.addWidget(self.reject_button)

        self.refresh_requests_list()  # Populate the list initially

    def accept_request(self):
        selected_item = self.requests_list.currentItem()
        if selected_item is not None:
            username = selected_item.text()
            result = funcs.acceptFR(self.client, username)
            qtw.QMessageBox.information(self, "Accept Request", result)
            self.request_accepted.emit()
            self.refresh_requests_list()

    def reject_request(self):
        selected_item = self.requests_list.currentItem()
        if selected_item is not None:
            username = selected_item.text()
            result = funcs.rejectFR(self.client, username)
            qtw.QMessageBox.information(self, "Reject Request", result)
            self.refresh_requests_list()

    def refresh_requests_list(self):
        self.requests_list.clear()
        pending_requests = funcs.dispFriendRequests(self.client)
        if isinstance(pending_requests, list):
            self.requests_list.addItems(pending_requests)
        else:
            qtw.QMessageBox.warning(self, "Error", pending_requests)


class FriendsWindow(qtw.QDialog):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.initUI()
        self.refresh_friends_list()

    def initUI(self):
        self.setWindowTitle("Friends")
        self.layout = qtw.QVBoxLayout(self)

        # Display friends list
        self.friends_label = qtw.QLabel("Your Friends:")
        self.friends_label.setStyleSheet("font-size: 18px; color: rgba(0, 0, 0, 200);")
        self.layout.addWidget(self.friends_label, alignment=qtc.Qt.AlignCenter)
        self.friends_list = qtw.QListWidget()
        self.friends_list.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
        self.layout.addWidget(self.friends_list)

        # Add a button to check pending friend requests
        self.pending_requests_button = qtw.QPushButton("Check Pending Requests")
        self.pending_requests_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.pending_requests_button.clicked.connect(self.check_pending_requests)
        self.layout.addWidget(self.pending_requests_button)

        # Add a button to add friends
        self.add_friend_button = qtw.QPushButton("Add Friend")
        self.add_friend_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.add_friend_button.clicked.connect(self.add_friend)
        self.layout.addWidget(self.add_friend_button)

        self.layout.addStretch()
        
        # Display friends and their online status
        friends = funcs.dispFriends(self.client)
        self.friends_list.addItem(friends)

    def check_pending_requests(self):
        pending_requests_window = PendingRequestsWindow(self.client)
        pending_requests_window.request_accepted.connect(self.refresh_friends_list)
        pending_requests_window.exec_()

    def refresh_friends_list(self):
        self.friends_list.clear()
        friends = funcs.dispFriends(self.client)
        if isinstance(friends, list):
            self.friends_list.addItems(friends)
        else:
            qtw.QMessageBox.warning(self, "Error", friends)

    def add_friend(self):
        dialog = qtw.QInputDialog(self)
        dialog.setWindowTitle("Add Friend")
        dialog.setLabelText("Enter username of the friend you want to add:")
        dialog.setInputMode(qtw.QInputDialog.TextInput)
        dialog.setOkButtonText("Add")
        dialog.setCancelButtonText("Cancel")
        if dialog.exec_():
            username = dialog.textValue().strip()
            if username:
                result = funcs.addFriend(self.client, username)
                qtw.QMessageBox.information(self, "Add Friend", result)
                self.refresh_friends_list()

class MyApp(qtw.QDialog):
    def __init__(self):
       super().__init__()
       self.window_width, self.window_height =  100,50
       self.setMinimumSize(self.window_width, self.window_height)
       
       layout = QVBoxLayout()
       self.setLayout(layout)
       
       self.options = ('Upload Image', 'Uplaod Video', 'Upload Text', 'Upload Audio')
       
       self.combo = QComboBox()
       self.combo.addItems(self.options)
       layout.addWidget(self.combo)
       
       btn = QPushButton('Open')
       btn.clicked.connect(self.launchDialog)
       layout.addWidget(btn)
       
       
    def launchDialog(self):
       option = self.options.index(self.combo.currentText())
       
       if option == 0:
           response = self.getImageName()
       elif option == 1:
           response = self.getVideoName()
       elif option == 2:
           response = self.getTextName()
       elif option == 3:
           response = self.getAudioName()
           
       if response:
           print("Selected file:", response)
           
    def getImageName(self):
       file_filter = 'Image File (*.jpg *.png);; Video File(*.mp4 *.mov);; Text File(*.txt *.docx *.pdf);; Audio File(*.mp3)'
       response= QFileDialog.getOpenFileName(
               parent=self,
               caption= 'Select an image file',
               directory= os.getcwd(),
               filter=file_filter,
               initialFilter= 'Image File (*.jpg *.png)'
               )
       return response[0]
   
    def getVideoName(self):
       file_filter = 'Image File (*.jpg *.png);; Video File(*.mp4 *.mov);; Text File(*.txt *.docx *.pdf);; Audio File(*.mp3)'
       response= QFileDialog.getOpenFileName(
               parent=self,
               caption= 'Select a video file',
               directory= os.getcwd(),
               filter=file_filter,
               initialFilter= 'Video File(*.mp4 *.mov)'
               )
       return response[0]
   
    def getTextName(self):
       file_filter = 'Image File (*.jpg *.png);; Video File(*.mp4 *.mov);; Text File(*.txt *.docx *.pdf);; Audio File(*.mp3)'
       response= QFileDialog.getOpenFileName(
               parent=self,
               caption= 'Select a text file',
               directory= os.getcwd(),
               filter=file_filter,
               initialFilter= 'Text File(*.txt *.docx *.pdf)'
               )
       return response[0]
   
    def getAudioName(self):
       file_filter = 'Image File (*.jpg *.png);; Video File(*.mp4 *.mov);; Text File(*.txt *.docx *.pdf);; Audio File(*.mp3)'
       response= QFileDialog.getOpenFileName(
               parent=self,
               caption= 'Select an audio file',
               directory= os.getcwd(),
               filter=file_filter,
               initialFilter= 'Audio File(*.mp3)'
               )
       return response[0]



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    client_manager = ClientSocketManager()
    window = SignInWindow(client_manager)
    window.show()
    sys.exit(app.exec_())