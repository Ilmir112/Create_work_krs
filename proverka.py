# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, \
#     QHBoxLayout, QWidget
#
#
# class LoginWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Вход в приложение")
#
#         self.label_username = QLabel("Имя пользователя:")
#         self.edit_username = QLineEdit()
#         self.label_password = QLabel("Пароль:")
#         self.edit_password = QLineEdit()
#         self.edit_password.setEchoMode(QLineEdit.Password)
#         self.button_login = QPushButton("Вход")
#         self.button_login.clicked.connect(self.login)
#         self.edit_password.setEchoMode(QLineEdit.Password)
#
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.label_username)
#         layout.addWidget(self.edit_username)
#         layout.addWidget(self.label_password)
#         layout.addWidget(self.edit_password)
#         layout.addWidget(self.button_login)
#
#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)
#
#     def login(self):
#         username = self.edit_username.text()
#         password = self.edit_password.text()
#         print(username, password)
#         # Здесь можно добавить код для проверки имени пользователя и пароля в базе данных
#
#
# class RegisterWindow(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Регистрация нового пользователя")
#
#         self.label_username = QLabel("Имя пользователя:")
#         self.edit_username = QLineEdit()
#         self.label_password = QLabel("Пароль:")
#         self.edit_password = QLineEdit()
#         self.edit_password.setEchoMode(QLineEdit.Password)
#         self.button_register = QPushButton("Регистрация")
#         self.button_register.clicked.connect(self.register)
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.label_username)
#         layout.addWidget(self.edit_username)
#         layout.addWidget(self.label_password)
#         layout.addWidget(self.edit_password)
#         layout.addWidget(self.button_register)
#
#         self.setLayout(layout)
#
#     def register(self):
#         username = self.edit_username.text()
#         password = self.edit_password.text()
#         # Здесь можно добавить код для регистрации нового пользователя в базе данных
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     login_window = LoginWindow()
#     login_window.show()
#
#     register_window = RegisterWindow()
#
#     sys.exit(app.exec_())
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QMainWindow, QVBoxLayout, QWidget
from openpyxl import Workbook

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save to Excel")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.table1 = QTableWidget()
        layout.addWidget(self.table1)

        self.table2 = QTableWidget()
        layout.addWidget(self.table2)

        self.table3 = QTableWidget()
        layout.addWidget(self.table3)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

        self.load_data()
        self.save_to_excel()

    def load_data(self):
        data1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        data2 = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        data3 = [["apple", "banana", "cherry"], ["durian", "elderberry", "fig"], ["grape", "honeydew", "kiwi"]]

        self.table1.setRowCount(len(data1))
        self.table1.setColumnCount(len(data1[0]))
        for row in range(len(data1)):
            for col in range(len(data1[row])):
                item = QTableWidgetItem(str(data1[row][col]))
                self.table1.setItem(row, col, item)

        self.table2.setRowCount(len(data2))
        self.table2.setColumnCount(len(data2[0]))
        for row in range(len(data2)):
            for col in range(len(data2[row])):
                item = QTableWidgetItem(str(data2[row][col]))
                self.table2.setItem(row, col, item)

        self.table3.setRowCount(len(data3))
        self.table3.setColumnCount(len(data3[0]))
        for row in range(len(data3)):
            for col in range(len(data3[row])):
                item = QTableWidgetItem(str(data3[row][col]))
                self.table3.setItem(row, col, item)

    def save_to_excel(self):
        workbook = Workbook()
        sheets = ["Титульник", 'Схема', 'Sheet3']

        tables = [self.table1, self.table2, self.table3]

        for i, sheet_name in enumerate(sheets):
            worksheet = workbook.create_sheet(sheet_name)
            table = tables[i]

            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item is not None:
                        cell = worksheet.cell(row=row+1, column=col+1)
                        cell.value = item.text()

        workbook.remove(workbook['Sheet'])
        workbook.save('excel_file.xlsx')

        print("Saved to excel_file.xlsx")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
