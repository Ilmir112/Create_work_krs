import well_data

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QGridLayout
from PyQt5.QtCore import Qt

from data_base.config_base import UserService, connection_to_database, \
    RegistrationService


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('окно входа')



        self.label_username = QLabel("Пользователь:", self)
        self.username = QComboBox(self)
        users_list = list(map(lambda x: x[1], self.get_list_users()))

        self.username.addItems(users_list)
        self.label_password = QLabel("Пароль:", self)

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля
        self.password.setPlaceholderText('введите пароль')
        self.password.setEchoMode(QLineEdit.Password)

        self.button = QPushButton("обновить")
        self.button.clicked.connect(self.update_users)

        self.button_login = QPushButton("вход", self)
        self.button_login.move(50, 120)
        self.button_login.clicked.connect(self.login)

        self.button_register = QPushButton("Регистрация", self)
        self.button_register.clicked.connect(self.show_register_window)

        self.box_layout = QGridLayout(self)

        self.box_layout.addWidget(self.label_username, 0, 1)
        self.box_layout.addWidget(self.username, 0, 2)
        self.box_layout.addWidget(self.button, 0, 3)

        self.box_layout.addWidget(self.label_password, 1, 1)
        self.box_layout.addWidget(self.password, 1, 2)
        self.box_layout.addWidget(self.button_login, 2, 1)
        self.box_layout.addWidget(self.button_register, 2, 2)

    def update_users(self):

        users_list = list(map(lambda x: x[1], self.get_list_users()))
        self.username.clear()
        self.username.addItems(users_list)

    def closeEvent(self, event):
        if self.sender() == None:  # Проверяем вызывающий объект
            # Закрываем основное окно при закрытии окна входа
            # self.main_window.close()
            event.accept()  # Принимаем событие закрытия
    def login(self):

        username = self.username.currentText()
        password = self.password.text()
        last_name, first_name, second_name, _ = username.split(' ')

        db = connection_to_database(well_data.DB_NAME_USER)

        user_service = UserService(db, db.path_index)

        user_dict = user_service.get_user(last_name, first_name, second_name)
        if user_dict['last_name'] == last_name and user_dict['first_name'] == first_name \
                and user_dict['second_name'] and user_dict['password'] == str(password):
            # mes = QMessageBox.information(self, 'Пароль', 'вход произведен')
            self.close()
            well_data.user = (user_dict["pozition"] + ' ' + user_dict["organization"],
                              f'{user_dict["last_name"]} '
                              f'{user_dict["first_name"][0]}.{user_dict["second_name"][0]}.')

            well_data.contractor = user_dict["organization"]

            well_data.pause = True
        else:
            QMessageBox.critical(self, 'Пароль', 'логин и пароль не совпадает')


        well_data.pause = False


        if 'РН' in well_data.contractor:
            well_data.connect_in_base = False

    def get_list_users(self):
        db = connection_to_database(well_data.DB_NAME_USER)
        user_service = UserService(db, db.path_index)
        users_list = user_service.get_users_list()
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
        self.position = QComboBox(self)
        self.position.addItems(['Ведущий геолог ', 'Главный геолог', 'геолог'])

        self.label_organization = QLabel("Организация:", self)
        self.organization = QComboBox(self)
        self.organization.addItems(['', 'ООО "Ойл-cервис"', 'ООО "РН-Сервис"'])

        self.label_password = QLabel("Пароль", self)
        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля

        self.label_password2 = QLabel("Повторить Пароль", self)
        self.password2 = QLineEdit(self)
        self.password2.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля

        self.button_register_user = QPushButton("Регистрация", self)

        self.password.setEchoMode(QLineEdit.Password)  # Устанавливаем режим скрытия пароля
        self.button_register_user.clicked.connect(self.register_user)

        self.label_region = QLabel("ЦЕХ:", self)
        self.region = QComboBox(self)
        self.region.addItems(
            ['ЦТКРС № 1', 'ЦТКРС № 2', 'ЦТКРС № 3', 'ЦТКРС № 4', 'ЦТКРС № 5', 'ЦТКРС № 6', 'ЦТКРС № 7'])

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
        self.grid.addWidget(self.label_region, 5, 1)
        self.grid.addWidget(self.region, 5, 2)
        self.grid.addWidget(self.label_password, 6, 1)
        self.grid.addWidget(self.password, 6, 2)
        self.grid.addWidget(self.label_password2, 7, 1)
        self.grid.addWidget(self.password2, 7, 2)
        self.grid.addWidget(self.button_register_user, 8, 1, 2, 2)
        self.organization.currentTextChanged.connect(self.update_organization)

    def update_organization(self, index):

        if index == 'ООО "Ойл-cервис"':

            self.label_region.setText("ЦЕХ:")
            self.region.clear()
            self.region.addItems(['ЦТКРС № 1', 'ЦТКРС № 2', 'ЦТКРС № 3', 'ЦТКРС № 4',
                                  'ЦТКРС № 5', 'ЦТКРС № 6', 'ЦТКРС № 7'])

        elif index == 'ООО "РН-Сервис"':
            self.label_region.setText("Экспедиция:")
            self.region.clear()
            self.region.addItems(['экспедиции №1', 'экспедиции №2', 'экспедиции №3', 'экспедиции №4',
                                  'экспедиции №5', 'экспедиции №6',
                                  'экспедиции №7'])
        self.grid.addWidget(self.label_region, 5, 1)
        self.grid.addWidget(self.region, 5, 2)

    def register_user(self):

        last_name = self.last_name.text().title().strip()
        first_name = self.first_name.text().title().strip()
        second_name = self.second_name.text().title().strip()
        position_in = self.position.currentText().strip()
        organization = self.organization.currentText().strip()
        region = self.region.currentText().strip()
        password = self.password.text().strip()
        password2 = self.password2.text().strip()

        db = connection_to_database(well_data.DB_NAME_USER)

        registration = RegistrationService(db, db.path_index)

        existing_user = registration.check_user_in_database(last_name, first_name, second_name)

        if existing_user:  # Если пользователь уже существует
            QMessageBox.critical(self, 'Данный пользовать существует', 'Данный пользовать существует')
        else:  # Если пользователя с таким именем еще нет
            position_in = position_in + " " + region
            if password == password2:
                registration.registration_user(last_name, first_name, second_name, position_in, organization, password)

                QMessageBox.information(self, 'Регистрация', 'пользователь успешно создан')
                self.close()
            else:
                QMessageBox.information(self, 'пароль', 'Пароли не совпадают')

