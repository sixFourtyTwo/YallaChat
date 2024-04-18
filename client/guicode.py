import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from PyQt5 import uic
import infrastructure.functions as funcs
import socket 


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.56.1', 9999))


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("YallaChat")
        self.setWindowFlags(
            qtc.Qt.Window | qtc.Qt.WindowMinimizeButtonHint | qtc.Qt.WindowMaximizeButtonHint | qtc.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: #ADD8E6;")

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addStretch()

        self.label = qtw.QLabel("YallaChat")
        self.label.setFont(qtg.QFont('Arial', 36, qtg.QFont.Bold))
        self.label.setStyleSheet("color: white;")
        self.layout.addWidget(self.label, alignment=qtc.Qt.AlignCenter)

        button_layout = qtw.QVBoxLayout()
        button_layout.setAlignment(qtc.Qt.AlignCenter)

        self.sign_in_button = qtw.QPushButton("Sign In")
        self.sign_in_button.setStyleSheet(
            "background-color: #FFA500; color: white; border: 2px solid #FFA500; padding: 10px 20px; font-size: 20px;")
        self.sign_in_button.clicked.connect(self.show_sign_in)
        button_layout.addWidget(self.sign_in_button)

        self.register_button = qtw.QPushButton("Register")
        self.register_button.setStyleSheet(
            "background-color: #FFA500; color: white; border: 2px solid #FFA500; padding: 10px 20px; font-size: 20px;")
        self.register_button.clicked.connect(self.show_registration)
        button_layout.addWidget(self.register_button)

        self.layout.addLayout(button_layout)

        self.layout.addStretch()

    def show_registration(self):
        registration_window = RegistrationWindow()
        if registration_window.exec_() == qtw.QDialog.Accepted:
            self.show_friends_button.setEnabled(True)

    def show_sign_in(self):
        sign_in_window = SignInWindow()
        if sign_in_window.exec_() == qtw.QDialog.Accepted:
            self.show_friends_button.setEnabled(True)

    def show_friends(self):
        friends_window = FriendsWindow()
        friends_window.exec_()



class RegistrationWindow(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Registration")
        self.setWindowFlags(
            qtc.Qt.Window | qtc.Qt.WindowMinimizeButtonHint | qtc.Qt.WindowMaximizeButtonHint | qtc.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: #ADD8E6;")

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addStretch()

        self.name_input = qtw.QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.layout.addWidget(self.name_input)

        self.email_input = qtw.QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.layout.addWidget(self.email_input)

        self.username_input = qtw.QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input)

        self.password_input = qtw.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(qtw.QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.register_button = qtw.QPushButton("Register")
        self.register_button.setStyleSheet(
            "background-color: #FFA500; color: white; border: 2px solid #FFA500; padding: 10px 20px; font-size: 20px;")
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button, alignment=qtc.Qt.AlignCenter)

        self.layout.addStretch()

    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

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


class SignInWindow(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sign In")
        self.setWindowFlags(
            qtc.Qt.Window | qtc.Qt.WindowMinimizeButtonHint | qtc.Qt.WindowMaximizeButtonHint | qtc.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: #ADD8E6;")

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addStretch()

        self.username_input = qtw.QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input)

        self.password_input = qtw.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(qtw.QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.sign_in_button = qtw.QPushButton("Sign In")
        self.sign_in_button.setStyleSheet(
            "background-color: #FFA500; color: white; border: 2px solid #FFA500; padding: 10px 20px; font-size: 20px;")
        self.sign_in_button.clicked.connect(self.sign_in)
        self.layout.addWidget(self.sign_in_button, alignment=qtc.Qt.AlignCenter)

        self.layout.addStretch()

    def sign_in(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Call login function from infrastructure.functions
        result = funcs.login(client, username, password)
        if result == 'Success':
            # Fetch chat list upon successful login
            chat_list = funcs.dispChats(client)
            self.show_chat_list(chat_list)

    def show_chat_list(self, chat_list):
        chat_main_window = ChatMainWindow(chat_list)
        chat_main_window.exec_()

        self.accept()


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
            self.chat_list_widget.addItem(chat)

        self.layout.addStretch()

        self.friends_button = qtw.QPushButton("View Friends")
        self.friends_button.setStyleSheet(
            "background-color: #FFA500; color: white; border: 2px solid #FFA500; padding: 10px 20px; font-size: 20px;")
        self.friends_button.clicked.connect(self.view_friends)
        self.layout.addWidget(self.friends_button, alignment=qtc.Qt.AlignCenter)

        self.users_button = qtw.QPushButton("View Users")
        self.users_button.setStyleSheet(
            "background-color: #FFA500; color: white; border: 2px solid #FFA500; padding: 10px 20px; font-size: 20px;")
        self.users_button.clicked.connect(self.view_users)
        self.layout.addWidget(self.users_button, alignment=qtc.Qt.AlignCenter)

        self.layout.addStretch()

    def view_friends(self):
        friends_window = FriendsWindow()
        friends_window.exec_()

    def view_users(self):
        users_window = UsersWindow()
        users_window.exec_()

class UsersWindow(qtw.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Users")
        self.setWindowFlags(
            qtc.Qt.Window | qtc.Qt.WindowMinimizeButtonHint | qtc.Qt.WindowMaximizeButtonHint | qtc.Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: #ADD8E6;")

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.layout.addStretch()

        self.users_list = qtw.QListWidget()
        self.layout.addWidget(self.users_list)

        self.update_button = qtw.QPushButton("Update Users")
        self.update_button.setStyleSheet(
            "background-color: #FFA500; color: white; border: 2px solid #FFA500; padding: 10px 20px; font-size: 20px;")
        self.update_button.clicked.connect(self.update_users)
        self.layout.addWidget(self.update_button, alignment=qtc.Qt.AlignCenter)

        self.layout.addStretch()

    def update_users(self):
        # Retrieve and display the list of users
        users = funcs.get_users()  # Implement this function in your infrastructure.functions
        self.users_list.clear()
        for user in users:
            self.users_list.addItem(user)

if __name__ == "__main__":
    import sys
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())