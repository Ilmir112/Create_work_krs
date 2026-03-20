import data_list
from PyQt5.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
)

from server_response import ApiClient


class EditProfileDialog(QDialog):
    """Редактирование профиля через API (два поля пароля должны совпадать)."""

    def __init__(self, parent, me: dict):
        super().__init__(parent)
        self.setWindowTitle("Профиль пользователя")
        self.setModal(True)
        self._me = me

        layout = QGridLayout(self)
        row = 0
        self._fields = {}

        def add_row(label: str, key: str, value="", secret=False):
            nonlocal row
            layout.addWidget(QLabel(label), row, 0)
            le = QLineEdit(self)
            le.setText(str(value) if value is not None else "")
            if secret:
                le.setEchoMode(QLineEdit.Password)
            layout.addWidget(le, row, 1)
            self._fields[key] = le
            row += 1

        add_row("Логин:", "login_user", me.get("login_user", ""))
        add_row("Имя:", "name_user", me.get("name_user", ""))
        add_row("Фамилия:", "surname_user", me.get("surname_user", ""))
        add_row("Отчество:", "second_name", me.get("second_name", ""))
        add_row("Должность / подразделение:", "position_id", me.get("position_id", ""))
        add_row("Заказчик:", "costumer", me.get("costumer", ""))
        add_row("Организация:", "contractor", me.get("contractor", ""))
        add_row("Цех / экспедиция:", "ctcrs", me.get("ctcrs", ""))
        add_row("Новый пароль (необязательно):", "password", "", secret=True)
        add_row("Повтор пароля:", "password_confirm", "", secret=True)

        btn_save = QPushButton("Сохранить")
        btn_cancel = QPushButton("Отмена")
        btn_save.clicked.connect(self._save)
        btn_cancel.clicked.connect(self.reject)
        layout.addWidget(btn_save, row, 0)
        layout.addWidget(btn_cancel, row, 1)

    def _save(self):
        pwd = self._fields["password"].text()
        pwd2 = self._fields["password_confirm"].text()
        if pwd != pwd2:
            QMessageBox.warning(self, "Пароль", "Пароли не совпадают")
            return
        if (pwd or pwd2) and (not pwd or not pwd2):
            QMessageBox.warning(
                self, "Пароль", "Заполните оба поля пароля или оставьте оба пустыми"
            )
            return

        params = {
            "login_user": self._fields["login_user"].text().strip(),
            "name_user": self._fields["name_user"].text().strip(),
            "surname_user": self._fields["surname_user"].text().strip(),
            "second_name": self._fields["second_name"].text().strip(),
            "position_id": self._fields["position_id"].text().strip(),
            "costumer": self._fields["costumer"].text().strip(),
            "contractor": self._fields["contractor"].text().strip(),
            "ctcrs": self._fields["ctcrs"].text().strip(),
            "password": pwd.strip(),
            "password_confirm": pwd2.strip(),
        }

        result = ApiClient.request_post(ApiClient.update_user_path(), params)
        if isinstance(result, dict) and result.get("status") == "success":
            QMessageBox.information(self, "Профиль", "Данные успешно сохранены")
            data_list.user = (
                params["position_id"] + " " + params["contractor"],
                params["login_user"],
            )
            data_list.contractor = params["contractor"]
            self.accept()
            return
        if result == 409:
            QMessageBox.critical(
                self, "Логин", "Пользователь с таким логином уже существует"
            )
            return
        if result == 422:
            QMessageBox.warning(
                self, "Ошибка", "Проверьте корректность введённых данных"
            )
            return
        QMessageBox.warning(
            self,
            "Ошибка",
            "Не удалось сохранить профиль."
            if result is None
            else f"Код ответа: {result}",
        )
