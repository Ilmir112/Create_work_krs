from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel

class SecondWindow(QDialog):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.setWindowTitle('Second Window')

        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self.save_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Дополнительное окно"))
        layout.addWidget(save_button)
        self.setLayout(layout)

    def save_button_clicked(self):
        self.accept()

app = QApplication()

second_window = SecondWindow()
second_window.setModal(True) # Сделать окно модальным
second_window.show()

sys.exit(app.exec_())