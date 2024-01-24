import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit


class MyWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.labels = {}
        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout()

        for key, value in self.data.items():
            label = QLabel(key)
            line_edit = QLineEdit(value)

            layout.addWidget(label)
            layout.addWidget(line_edit)

            # Переименование атрибута
            setattr(self, f"{key}_label", label)

            self.labels[key] = (label, line_edit)

        self.setLayout(layout)


if __name__ == '__main__':
    data = {
        "name": "John",
        "age": "25",
        "city": "New York"
    }

    app = QApplication(sys.argv)
    window = MyWindow(data)
    window.show()
    sys.exit(app.exec_())
