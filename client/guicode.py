import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from PyQt5 import uic
import infrastructure.functions as funcs
import socket 
import sys
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.56.1', 9999))

class RegistrationWindow(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Load the UI file
        uic.loadUi('client/registerUi.ui', self)
        

        # Connect button click signal to slot
        self.pushButton.clicked.connect(self.register)
        self.pushButton_2.clicked.connect(self.show_login_window)
    def register(self):
        name = self.lineEdit_4.text()
        email = self.lineEdit_3.text()
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # Call register function from infrastructure.functions
        result = funcs.register(client, name, email, username, password)
        if result == 'Success':
            # Fetch chat list upon successful registration
            chat_list = funcs.dispChats(client)
            self.show_chat_list(chat_list)

        self.accept()

    def show_chat_list(self, chat_list):
        chat_main_window = ChatMainWindow(chat_list)
        chat_main_window.exec_()
    def show_login_window(self):
        login_window = SignInWindow()
        login_window.exec_()

class SignInWindow(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Load the UI file
        uic.loadUi('client/loginUi1.1.ui', self)

        # Connect button click signals to slots
        self.pushButton.clicked.connect(self.sign_in)
        self.pushButton_2.clicked.connect(self.show_registration)

    def sign_in(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        # Call login function from infrastructure.functions
        result = funcs.login(client, username, password)
        if result == 'Login successful!':
            print(result)
            # Fetch chat list upon successful login
            chat_list = funcs.dispChats(client)
            print(chat_list)
            self.show_chat_list(chat_list)

    def show_chat_list(self, chat_list):
        chat_main_window = ChatMainWindow(chat_list)
        chat_main_window.exec_()

    def show_registration(self):
        registration_window = RegistrationWindow()
        if registration_window.exec_() == qtw.QDialog.Accepted:
            self.show_chat_list([])



class FriendsWindow(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Friends")
        self.setWindowFlags(
            qtc.Qt.Window | qtc.Qt.WindowMinimizeButtonHint | qtc.Qt.WindowMaximizeButtonHint | qtc.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: #ADD8E6;")

        self.layout = qtw.QVBoxLayout()
        self.setLayout


class ChatMainWindow(qtw.QDialog):
    def __init__(self, chat_list):
        super().__init__()
        self.chat_list = chat_list
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Chat Main Window")
        self.setWindowFlags(
            qtc.Qt.Window | qtc.Qt.WindowMinimizeButtonHint | qtc.Qt.WindowMaximizeButtonHint | qtc.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: #ADD8E6;")

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addStretch()

        self.chat_list_widget = qtw.QListWidget()
        self.layout.addWidget(self.chat_list_widget)

        for chat in self.chat_list:
            item = qtw.QListWidgetItem(chat)
            item.setTextAlignment(qtc.Qt.AlignCenter)
            item.setFlags(item.flags() | qtc.Qt.ItemIsSelectable | qtc.Qt.ItemIsUserCheckable | qtc.Qt.ItemIsEnabled)
            item.setCheckState(qtc.Qt.Unchecked)
            self.chat_list_widget.addItem(item)

        self.layout.addStretch()

        self.chat_list_widget.itemClicked.connect(self.open_chat_window)

    def open_chat_window(self, item):
        chat_title = item.text()
        chatting_window = ChattingWindow(chat_title)
        chatting_window.exec_()


class ChattingWindow(qtw.QDialog):
    def __init__(self, chat_title):
        super().__init__()
        self.chat_title = chat_title
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.chat_title)
        self.setWindowFlags(
            qtc.Qt.Window | qtc.Qt.WindowMinimizeButtonHint | qtc.Qt.WindowMaximizeButtonHint | qtc.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: #ADD8E6;")

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.message_field = qtw.QTextEdit()
        self.layout.addWidget(self.message_field)

        self.send_button = qtw.QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        self.back_button = qtw.QPushButton("Back")
        self.back_button.clicked.connect(self.close)
        self.layout.addWidget(self.back_button)

    def send_message(self):
        message = self.message_field.toPlainText()
        # Code to send the message to the selected chat

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = SignInWindow()
    window.show()
    sys.exit(app.exec_())
