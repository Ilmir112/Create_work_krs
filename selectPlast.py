import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QDialog

import data_list


class CheckBoxDialog(QDialog):

    def __init__(self, data_well):
        super().__init__()
        self.data_well = data_well


        layout = QVBoxLayout()
        n = 1
        for plast in self.data_well.plast_work:
            self.plast = QCheckBox(plast)
            layout.addWidget(self.plast)
        if self.data_well.dict_leakiness:
            for nek in list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()):
                self.plast = QCheckBox(f'НЭК {nek}')
                layout.addWidget(self.plast)


        button = QPushButton("OK")
        button.clicked.connect(self.handle_button_click)
        layout.addWidget(button)

        self.setLayout(layout)

    def handle_button_click(self):

        data_list.plast_select = ''
        selected_options = []
        # print(f' рабочие пласты {self.data_well.plast_work}')
        for plast in self.data_well.plast_work:
            if self.plast.isChecked():
                if self.plast.text() not in selected_options:
                    selected_options.append(self.plast.text())

        for plast in self.data_well.plast_project:
            if self.plast.isChecked():
                if self.plast.text() not in selected_options:
                    selected_options.append(self.plast.text())

        print("Selected options:", selected_options)
        plast_select = ', '.join(selected_options)
        self.close()
        return data_list.plast_select

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = CheckBoxDialog()
    dialog.setWindowTitle("Выбор пласта")
    dialog.exec_()