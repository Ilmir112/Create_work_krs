import psycopg2
from PyQt5.QtWidgets import  QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox



import well_data


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('окно входа')
        self.setGeometry(100, 100, 400, 300)

        self.label_username = QLabel("Пользователь:", self)
        self.label_username.move(50, 30)
        self.username = QComboBox(self)
        users_list = list(map(lambda x:x[1], self.get_list_users()))

        self.username.addItems(users_list)
        self.username.move(120, 30)

        self.label_password = QLabel("Пароль:", self)
        self.label_password.move(50, 70)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля
        self.password.setPlaceholderText('введите пароль')
        self.password.setEchoMode(QLineEdit.Password)
        self.password.move(120, 70)

        self.button_login = QPushButton("вход", self)
        self.button_login.move(50, 120)
        self.button_login.clicked.connect(self.login)

        self.button_register = QPushButton("Регистрация", self)
        self.button_register.move(150, 120)
        self.button_register.clicked.connect(self.show_register_window)

    def login(self):
        username = self.username.currentText()
        password = self.password.text()
        last_name, first_name, second_name, _ = username.split(' ')
        conn = psycopg2.connect(dbname='users', user='postgres', password='1953')
        cursor = conn.cursor()
        cursor.execute("SELECT last_name, first_name, second_name, password, position_in, organization FROM users "
                       "WHERE last_name=(%s) AND first_name=(%s) AND second_name=(%s)",
                       (last_name, first_name, second_name))
        password_base = cursor.fetchone()

        password_base_short = f'{password_base[0]} {password_base[1]} {password_base[2]} '
        if password_base_short == username and password_base[3] == str(password):
            # mes = QMessageBox.information(self, 'Пароль', 'вход произведен')
            self.close()
            well_data.user = (password_base[4] + ' ' + password_base[5], password_base_short)

            well_data.pause = False
        else:
             mes = QMessageBox.critical(self, 'Пароль', 'логин и пароль не совпадает')


    def get_list_users(self):
        # Создаем подключение к базе данных

        conn = psycopg2.connect(dbname='users', user='postgres', password='1953')
        cursor = conn.cursor()
        cursor.execute("SELECT last_name, first_name, second_name, position_in, organization  FROM users")
        users = cursor.fetchall()
        users_list = []

        for user in users:
            position = user[3] + " " + user[4]
            user_name = user[0] + " " + user[1] + ' ' + user[2] + ' '
            users_list.append((position, user_name))
        conn.close()

        return users_list


    def show_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Окно регистрация')
        self.setGeometry(100, 100, 400, 500)

        self.label_last_name = QLabel("Фамилия:", self)
        self.label_last_name.move(50, 30)
        self.last_name = QLineEdit(self)
        # self.last_name.setText('Зуфаров')
        self.last_name.move(150, 30)

        self.label_first_name = QLabel("Имя:", self)
        self.label_first_name.move(50, 80)
        self.first_name = QLineEdit(self)
        # self.first_name.setText('Ильмир')
        self.first_name.move(150, 80)

        self.label_second_name = QLabel("Отчество:", self)
        self.label_second_name.move(50, 130)
        self.second_name = QLineEdit(self)
        # self.second_name.setText('Мияссарович')
        self.second_name.move(150, 130)

        self.label_position = QLabel("Должность:", self)
        self.label_position.move(50, 180)
        self.position = QLineEdit(self)
        # self.position.setText('Зам. главного геолога')
        self.position.move(150, 180)

        self.label_organization = QLabel("Организация:", self)
        self.label_organization.move(50, 230)
        self.organization = QLineEdit(self)
        self.organization.setText('ООО "Ойл-сервис"')
        self.organization.move(150, 230)

        self.label_password = QLabel("Пароль", self)
        self.label_password .move(50, 280)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля
        self.password .move(150, 280)

        self.label_password2 = QLabel("Повторить Пароль", self)
        self.label_password2.move(50, 350)
        self.password2 = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля
        self.password2.move(150, 350)

        self.button_register_user = QPushButton("Регистрация", self)
        self.button_register_user.move(150, 380)
        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля
        self.button_register_user.clicked.connect(self.register_user)

    def register_user(self):
        last_name = self.last_name.text().title()
        first_name = self.first_name.text().title()
        second_name = self.second_name.text().title()
        position_in = self.position.text()
        organization = self.organization.text()
        password = self.password.text()
        password2 = self.password2.text()

        conn = psycopg2.connect(dbname='users', user='postgres', password='1953')
        cursor = conn.cursor()

        # Проверяем, существует ли пользователь с таким именем
        cursor.execute("SELECT last_name, first_name, second_name  FROM users "
                       "WHERE last_name(%s) AND first_name(%s) AND second_name(%s)",
                       (last_name, first_name, second_name))
        existing_user = cursor.fetchone()

        if existing_user:  # Если пользователь уже существует
            QMessageBox.critical(self, 'Данный пользовать существует', 'Данный пользовать существует')
        else:  # Если пользователя с таким именем еще нет

            if password == password2:
                cursor.execute(
                    "INSERT INTO users ("
                    "last_name, first_name, second_name, position_in, organization, password) VALUES (%s, %s, %s, %s, %s, %s)",
                    (last_name, first_name, second_name, position_in, organization, password))
                conn.commit()
                conn.close()

                mes = QMessageBox.information(self, 'Регистрация', 'пользователь успешно создан')
                self.close()
            else:
                mes = QMessageBox.information(self, 'пароль', 'Пароли не совпадают')
# app = QApplication(sys.argv)
# login_window = LoginWindow()
# login_window.show()
# sys.exit(app.exec_())
