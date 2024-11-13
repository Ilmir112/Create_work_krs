import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QDialog

import well_data


class CheckBoxDialog(QDialog):

    def __init__(self, dict_data_well):
        super().__init__()
        self.dict_data_well = dict_data_well


        layout = QVBoxLayout()
        n = 1
        for plast in self.dict_data_well['plast_work']:
            self.plast = QCheckBox(plast)
            layout.addWidget(self.plast)
        if self.dict_data_well["dict_leakiness"]:
            for nek in list(self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()):
                self.plast = QCheckBox(f'НЭК {nek}')
                layout.addWidget(self.plast)


        button = QPushButton("OK")
        button.clicked.connect(self.handle_button_click)
        layout.addWidget(button)

        self.setLayout(layout)

    def handle_button_click(self):

        well_data.plast_select = ''
        selected_options = []
        # print(f' рабочие пласты {self.dict_data_well['plast_work']}')
        for plast in self.dict_data_well['plast_work']:
            if self.plast.isChecked():
                if self.plast.text() not in selected_options:
                    selected_options.append(self.plast.text())

        for plast in self.dict_data_well["plast_project"]:
            if self.plast.isChecked():
                if self.plast.text() not in selected_options:
                    selected_options.append(self.plast.text())

        print("Selected options:", selected_options)
        plast_select = ', '.join(selected_options)
        self.close()
        return well_data.plast_select

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = CheckBoxDialog()
    dialog.setWindowTitle("Выбор пласта")
    dialog.exec_()