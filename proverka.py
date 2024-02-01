import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, \
    QHBoxLayout, QWidget


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в приложение")

        self.label_username = QLabel("Имя пользователя:")
        self.edit_username = QLineEdit()
        self.label_password = QLabel("Пароль:")
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.button_login = QPushButton("Вход")
        self.button_login.clicked.connect(self.login)
        self.edit_password.setEchoMode(QLineEdit.Password)


        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.edit_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.edit_password)
        layout.addWidget(self.button_login)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def login(self):
        username = self.edit_username.text()
        password = self.edit_password.text()
        print(username, password)
        # Здесь можно добавить код для проверки имени пользователя и пароля в базе данных


class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация нового пользователя")

        self.label_username = QLabel("Имя пользователя:")
        self.edit_username = QLineEdit()
        self.label_password = QLabel("Пароль:")
        self.edit_password = QLineEdit()
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.button_register = QPushButton("Регистрация")
        self.button_register.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.edit_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.edit_password)
        layout.addWidget(self.button_register)

        self.setLayout(layout)

    def register(self):
        username = self.edit_username.text()
        password = self.edit_password.text()
        # Здесь можно добавить код для регистрации нового пользователя в базе данных


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    register_window = RegisterWindow()

    sys.exit(app.exec_())
