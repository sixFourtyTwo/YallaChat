import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from PyQt5 import uic
import infrastructure.functions as funcs
import socket 
import sys
import threading


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
        self.search_input = qtw.QLineEdit(placeholderText=" Search")
        self.search_input.setStyleSheet("background-color: rgba(255, 255, 255, 255); border: 1px solid rgba(0, 0, 0, 100);")
        self.search_layout.addWidget(self.search_input)
        self.search_button = qtw.QPushButton("Search")
        self.search_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.search_layout.addWidget(self.search_button)

        # Display online users with an "Add Friend" button next to each
        self.online_users_label = qtw.QLabel("Online Users:")
        self.online_users_label.setStyleSheet("font-size: 18px; color: rgba(0, 0, 0, 200);")
        self.layout.addWidget(self.online_users_label, alignment=qtc.Qt.AlignCenter)
        self.online_users_list = qtw.QListWidget()
        self.online_users_list.setStyleSheet("background-color: rgba(255, 255, 255, 255);")
        self.layout.addWidget(self.online_users_list)

        # Add a "View Friends" button
        self.view_friends_button = qtw.QPushButton("View Friends")
        self.view_friends_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.layout.addWidget(self.view_friends_button)

        # Add a "New Chat" button to open a window for starting a new chat with a friend
        self.new_chat_button = qtw.QPushButton("New Chat")
        self.new_chat_button.setStyleSheet("background-color: rgba(85, 98, 112, 255); color: rgba(255, 255, 255, 200); border-radius: 5px;")
        self.layout.addWidget(self.new_chat_button)

        self.layout.addStretch()

    def search_online_users(self):
        pass

    def view_friends(self):
        pass

    def new_chat(self):
        pass

    def open_chat_window(self, button):
        chat_title = button.text()
        client = self.client_manager.get_client()
        if client is None:
            print("Client socket is not connected.")
            return
        chatting_window = ChattingWindow(chat_title, client)
        chatting_window.exec_()




class ChattingWindow(qtw.QDialog):
    message_received = qtc.pyqtSignal(str)

    def __init__(self, chat_title, client):
        super().__init__()
        self.chat_title = chat_title
        self.client = client
        self.initUI()

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

        self.fetch_button = qtw.QPushButton("Fetch Messages")
        self.fetch_button.clicked.connect(self.fetch_messages)
        self.layout.addWidget(self.fetch_button)

        self.message_received.connect(self.update_message_area)

    def fetch_messages(self):
        try:
            messages = funcs.getNewMsgs(self.client, self.chat_title)
            self.update_message_area(messages)  # Update message area directly
        except Exception as e:
            print("Error fetching messages:", e)

    def update_message_area(self, messages):
        self.message_area.setPlainText(messages)

    def send_message(self):
        message = self.input_field.text()
        try:
            funcs.sendMessage(self.client, self.chat_title, message)
            self.input_field.clear()
            self.fetch_messages()  # Fetch messages immediately after sending the message
        except Exception as e:
            print("Error sending message:", e)

class SignInWindow(qtw.QDialog):
    def __init__(self, client_manager):
        super().__init__()
        self.client_manager = client_manager
        self.initUI()

    def initUI(self):
        uic.loadUi('client/loginUi1.1.ui', self)
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
        uic.loadUi('client/registerUi.ui', self)
        self.pushButton.clicked.connect(self.register)
        self.pushButton_2.clicked.connect(self.show_login_window)

    def register(self):
        name = self.lineEdit_4.text()
        email = self.lineEdit_3.text()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        result = funcs.register(self.client_manager.get_client(), name, email, username, password)
        if result == 'Success':
            chat_list = funcs.dispChats(self.client_manager.get_client())
            self.show_chat_list(chat_list)

        self.accept()

    def show_chat_list(self, chat_list):
        chat_main_window = ChatMainWindow(chat_list, self.client_manager)
        chat_main_window.exec_()

    def show_login_window(self):
        login_window = SignInWindow(self.client_manager)
        login_window.exec_()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    client_manager = ClientSocketManager()
    window = SignInWindow(client_manager)
    window.show()
    sys.exit(app.exec_())
