import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
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
    import sys
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
