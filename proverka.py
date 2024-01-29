from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QFileDialog
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Example")

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()

        self.button_load = QPushButton("Загрузить JSON")
        self.button_load.clicked.connect(self.load_json)

        self.button_save = QPushButton("Сохранить JSON")
        self.button_save.clicked.connect(self.save_json)

        layout.addWidget(self.text_edit)
        layout.addWidget(self.button_load)
        layout.addWidget(self.button_save)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def load_json(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("JSON files (*.json)")
        file_dialog.selectNameFilter("JSON files (*.json)")

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]

            with open(file_path, 'r',  encoding='utf-8') as json_file:
                json_data = json.load(json_file)

            self.text_edit.setPlainText(json.dumps(json_data, indent=4))

    def save_json(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("JSON files (*.json)")
        file_dialog.selectNameFilter("JSON files (*.json)")

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]

            json_data = json.loads(self.text_edit.toPlainText())

            with open(file_path, 'w',  encoding='utf-8') as json_file:
                json.dump(json_data, json_file, indent=4)

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
