import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QDialog

class CheckBoxDialog(QDialog):

    def __init__(self):
        super().__init__()
        from open_pz import CreatePZ

        layout = QVBoxLayout()
        n = 1
        for plast in CreatePZ.plast_work:
            self.plast = QCheckBox(plast)
            layout.addWidget(self.plast)
        if CreatePZ.leakiness:
            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                self.plast = QCheckBox(f'НЭК {nek}')
                layout.addWidget(self.plast)


        button = QPushButton("OK")
        button.clicked.connect(self.handle_button_click)
        layout.addWidget(button)

        self.setLayout(layout)

    def handle_button_click(self):
        from open_pz import CreatePZ
        CreatePZ.plast_select = ''
        selected_options = []
        print(f' рабочие пласты {CreatePZ.plast_work}')
        for plast in CreatePZ.plast_work:
            if self.plast.isChecked():
                if self.plast.text() not in selected_options:
                    selected_options.append(self.plast.text())


        print("Selected options:", selected_options)
        CreatePZ.plast_select = ', '.join(selected_options)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = CheckBoxDialog()
    dialog.setWindowTitle("Выбор пласта")
    dialog.exec_()