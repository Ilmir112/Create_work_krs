import psycopg2
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QBoxLayout, QGridLayout
from PyQt5.QtCore import Qt

import well_data


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('окно входа')

        # Установка флага `Qt.WindowModal`
        self.setWindowModality(Qt.WindowModal)


        self.label_username = QLabel("Пользователь:", self)
        self.username = QComboBox(self)
        users_list = list(map(lambda x: x[1], self.get_list_users()))

        self.username.addItems(users_list)
        self.label_password = QLabel("Пароль:", self)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля
        self.password.setPlaceholderText('введите пароль')
        self.password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("вход", self)
        self.button_login.move(50, 120)
        self.button_login.clicked.connect(self.login)

        self.button_register = QPushButton("Регистрация", self)
        self.button_register.clicked.connect(self.show_register_window)
        self.username.currentTextChanged.connect(self.update_users)

        self.box_layout = QGridLayout(self)

        self.box_layout.addWidget(self.label_username, 0, 1)
        self.box_layout.addWidget(self.username, 0, 2)
        self.box_layout.addWidget(self.label_password, 1, 1)
        self.box_layout.addWidget(self.password, 1, 2)
        self.box_layout.addWidget(self.button_login, 2, 1)
        self.box_layout.addWidget(self.button_register, 2, 2)

    def update_users(self):
        self.username.clear()

        users_list = list(map(lambda x: x[1], self.get_list_users()))
        self.username.addItems(users_list)

    def login(self):
        try:
            conn = psycopg2.connect(**well_data.postgres_conn_user)
            cursor = conn.cursor()
            cursor.execute("SELECT last_name, first_name, middle_name, position, organization FROM plan_krs_employee;")

            password_base = cursor.fetchone()

            well_data.user = (f'{password_base[0]} {password_base[1][0]}.{password_base[2][0]}.',
                              f'{password_base[3]} {password_base[4]}')



        except psycopg2.Error as e:
            # well_data.user = ('Зуфаров Ильмир Мияссарович', 'Зам главного геолога ООО "Ойл-сервис"')
            # Выведите сообщение об ошибке
            mes = QMessageBox.warning(None, 'Ошибка', 'Ошибка подключения к базе данных django_users, '
                                                      'проверьте наличие интернета')


        finally:

            # Закройте курсор и соединение
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    def login(self):
        username = self.username.currentText()
        password = self.password.text()
        last_name, first_name, second_name, _ = username.split(' ')
        try:
            conn = psycopg2.connect(**well_data.postgres_conn_user)
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
        except psycopg2.Error as e:
            self.pause_app()
            well_data.pause = False
            # Выведите сообщение об ошибке
            mes = QMessageBox.warning(None, 'Ошибка', 'Ошибка подключения к базе данных, проверьте наличие интернета')
        finally:
            # Закройте курсор и соединение
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_list_users(self):
        # Создаем подключение к базе данных

        conn = psycopg2.connect(**well_data.postgres_conn_user)
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

        self.label_last_name = QLabel("Фамилия:", self)
        self.last_name = QLineEdit(self)

        self.label_first_name = QLabel("Имя:", self)
        self.first_name = QLineEdit(self)

        self.label_second_name = QLabel("Отчество:", self)
        self.second_name = QLineEdit(self)

        self.label_position = QLabel("Должность:", self)
        self.position = QLineEdit(self)

        self.label_organization = QLabel("Организация:", self)
        self.organization = QLineEdit(self)

        self.label_password = QLabel("Пароль", self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля

        self.label_password2 = QLabel("Повторить Пароль", self)
        self.password2 = QLineEdit(self)
        self.password2.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля

        self.button_register_user = QPushButton("Регистрация", self)

        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля
        self.button_register_user.clicked.connect(self.register_user)

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.label_last_name, 0, 1)
        self.grid.addWidget(self.last_name, 0, 2)
        self.grid.addWidget(self.label_first_name, 1, 1)
        self.grid.addWidget(self.first_name, 1, 2)
        self.grid.addWidget(self.label_second_name, 2, 1)
        self.grid.addWidget(self.second_name, 2, 2)
        self.grid.addWidget(self.label_position, 3, 1)
        self.grid.addWidget(self.position, 3, 2)
        self.grid.addWidget(self.label_organization, 4, 1)
        self.grid.addWidget(self.organization, 4, 2)
        self.grid.addWidget(self.label_password, 5, 1)
        self.grid.addWidget(self.password, 5, 2)
        self.grid.addWidget(self.label_password2, 6, 1)
        self.grid.addWidget(self.password2, 6, 2)
        self.grid.addWidget(self.button_register_user, 7, 1, 2, 2)

    def register_user(self):
        last_name = self.last_name.text().title().strip()
        first_name = self.first_name.text().title().strip()
        second_name = self.second_name.text().title().strip()
        position_in = self.position.text().strip()
        organization = self.organization.text().strip()
        password = self.password.text().strip()
        password2 = self.password2.text().strip()

        conn = psycopg2.connect(**well_data.postgres_conn_user)
        cursor = conn.cursor()

        # Проверяем, существует ли пользователь с таким именем
        cursor.execute("SELECT last_name, first_name, second_name  FROM users "
                       "WHERE last_name=(%s) AND first_name=(%s) AND second_name=(%s)",
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
