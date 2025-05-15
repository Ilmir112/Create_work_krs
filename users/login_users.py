import psutil
from PyQt5.QtCore import QSettings

import data_list

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QGridLayout, QDialog
from PyQt5.QtCore import Qt

from data_base.config_base import UserService, connection_to_database, \
    RegistrationService
from data_base.work_with_base import ApiClient
from decrypt import decrypt


class LoginWindow(QDialog):
    def __init__(self, ):
        super().__init__()
        self.user_dict = None
        self.register_window = None
        self.setWindowTitle('окно входа')

        self.label_username = QLabel("Пользователь:", self)
        self.username = QComboBox(self)
        users_list = self.get_list_users()

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
        self.db = connection_to_database(decrypt("DB_NAME_USER"))

        self.user_service = UserService(self.db)

    def update_users(self):
        self.users_list = list(map(lambda x: x[1], self.get_list_users()))
        self.username.clear()
        self.username.addItems(self.users_list)

    def closeEvent(self, event):
        if self.sender() is None:  # Проверяем вызывающий объект
            # Закрываем основное окно при закрытии окна входа
            for proc in psutil.process_iter():
                if proc.name() == 'ZIMA.exe':
                    proc.terminate()  # Принудительное завершение
            event.accept()  # Принимаем событие закрытия

    def login(self):

        username = self.username.currentText()
        password = self.password.text()

        if data_list.connect_in_base:
            params = {
                  "login_user": username,
                  "password": password
                }

            user_access = ApiClient.get_info_data(params, ApiClient.login_path())
            if user_access:
                ApiClient.SETTINGS_TOKEN = QSettings('Zima', 'ZimaApp')

                ApiClient.SETTINGS_TOKEN.setValue('auth_token', user_access["access_token"])

                # aswadw = ApiClient.SETTINGS_TOKEN
                # anshwer = ApiClient.request_params_get(ApiClient.me_info(), params)
                self.user_dict = user_access


                data_list.user = ( self.user_dict["position_id"] + ' ' + self.user_dict["contractor"],  self.user_dict["login_user"])
                data_list.contractor = self.user_dict["contractor"]

                data_list.pause = False
                self.close()

        else:

            last_name, first_name, second_name, _ = username.split(' ')
            if self.user_dict is None:
                self.user_dict = self.user_service.get_user(last_name, first_name, second_name)

            if self.user_dict["last_name"] == last_name and self.user_dict["first_name"] == first_name \
                    and self.user_dict["second_name"] and self.user_dict["password"] == str(password):
                # mes = QMessageBox.information(self, 'Пароль', 'вход произведен')

                data_list.user = (self.user_dict["pozition_id"] + ' ' + self.user_dict["organization"],
                                  f'{self.user_dict["last_name"]} '
                                  f'{self.user_dict["first_name"][0]}.{self.user_dict["second_name"][0]}.')

                data_list.contractor = self.user_dict["organization"]

                data_list.pause = False
                self.close()

            else:
                QMessageBox.critical(self, 'Пароль', 'логин и пароль не совпадает')
                data_list.pause = True
                self.user_dict = None

        # if 'РН' in data_list.contractor:
        #     data_list.connect_in_base = False

    @staticmethod
    def get_list_users():
        if data_list.connect_in_base is False:
            db = connection_to_database(decrypt("DB_NAME_USER"))
            user_service = UserService(db)
            users_list = user_service.get_users_list()
        else:
            users_list = ApiClient.request_get_all(ApiClient.get_all_users())

            users_list = list(map(lambda x: x["login_user"], users_list))
        return users_list

    def show_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.setWindowModality(Qt.ApplicationModal)
        self.register_window.show()


class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Окно регистрация')
        self.api_client = ApiClient

        self.label_last_name = QLabel("Фамилия:", self)
        self.last_name = QLineEdit(self)

        self.label_first_name = QLabel("Имя:", self)
        self.first_name = QLineEdit(self)

        self.label_second_name = QLabel("Отчество:", self)
        self.second_name = QLineEdit(self)

        self.label_position = QLabel("Должность:", self)
        self.position = QComboBox(self)
        self.position.addItems(['Ведущий геолог ', 'Главный геолог', 'Геолог', 'Ведущий технолог', 'Нормировщик',
                                'Заместитель начальника ПТО'])

        self.label_organization = QLabel("Организация:", self)
        self.organization = QComboBox(self)
        self.organization.addItems(['', 'ООО Ойл-сервис', 'ООО РН-Сервис'])

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
            ['ЦТКРС №1', 'ЦТКРС №2', 'ЦТКРС №3', 'ЦТКРС №4', 'ЦТКРС №5', 'ЦТКРС №6', 'ЦТКРС №7'])

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

        if index == "ООО Ойл-сервис":
            self.label_region.setText("ЦЕХ:")
            self.region.clear()
            self.region.addItems(['ЦТКРС №1', 'ЦТКРС №2', 'ЦТКРС №3', 'ЦТКРС №4',
                                  'ЦТКРС №5', 'ЦТКРС №6', 'ЦТКРС №7'])

        elif index == 'ООО РН-Сервис':
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
        if password == password2:
            if data_list.connect_in_base is False:

                db = connection_to_database(decrypt("DB_NAME_USER"))

                registration = RegistrationService(db)

                existing_user = registration.check_user_in_database(last_name, first_name, second_name)

                if existing_user:  # Если пользователь уже существует
                    QMessageBox.critical(self, 'Данный пользовать существует', 'Данный пользовать существует')
                else:  # Если пользователя с таким именем еще нет
                    position_in = position_in + " " + region
                    if password == password2:
                        registration.registration_user(last_name, first_name, second_name, position_in,
                                                       organization, password, region)

                        QMessageBox.information(self, 'Регистрация', 'пользователь успешно создан')
                        self.close()

            else:

                params = {
                        "login_user": f"{last_name} {first_name[0]}.{second_name[0]}.",
                        "name_user": first_name,
                        "surname_user": last_name,
                        "second_name": second_name,
                        "position_id": position_in,
                        "costumer": data_list.costumer,
                        "contractor": organization,
                        "ctcrs": region,
                        "password": password,
                        "access_level": "user"
                    }
                user = ApiClient.add_new_user(params, self.api_client.register_auth())

                if user == 409:
                    QMessageBox.critical(self, 'Данный пользовать существует', 'Данный пользовать существует')
                elif user == 200:
                    QMessageBox.information(self, 'Регистрация', 'пользователь успешно создан')
                    self.close()
                else:
                    QMessageBox.critical(self, 'Не известная ошибка', 'Не известная ошибка')
        else:
            QMessageBox.information(self, 'пароль', 'Пароли не совпадают')

