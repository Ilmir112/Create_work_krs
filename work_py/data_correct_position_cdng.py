import json
import data_list

from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import *

from main import MyMainWindow
from work_py.parent_work import TabWidgetUnion, WindowUnion


class TabPageSO(QWidget):
    selected_region = None
    podpis_dict = None

    def __init__(self, parent=None):
        super().__init__()

        # Открытие JSON файла и чтение данных
        with open(f'{data_list.path_image}podpisant.json', 'r', encoding='utf-8') as file:
            self.podpis_dict = json.load(file)
        TabPageSO.podpis_dict = self.podpis_dict

        self.productLavelLabel = QLabel("Заказчик", self)
        self.productLavelType = QComboBox(self)
        self.productLavelType.addItems([data_list.costumer])

        self.regionLabel = QLabel("Регион", self)
        self.region_combo_box = QComboBox(self)
        self.region_list = list(self.podpis_dict[data_list.costumer].keys())
        self.region_combo_box.addItems(self.region_list)

        self.cdngLabel = QLabel("ЦДНГ", self)
        self.cdng_combo_box = QComboBox(self)

        self.region_select = self.region_combo_box.currentText()

        self.title_job_Label = QLabel("Должность", self)
        self.surname_Label = QLabel("Фамилия И.О.", self)

        self.nach_chng_edit_type = QLineEdit(self)
        self.nach_chng_name_edit_type = QLineEdit(self)

        self.tehnolog_edit_type = QLineEdit(self)
        self.tehnolog_name_edit_type = QLineEdit(self)

        self.geolog_edit_type = QLineEdit(self)
        self.geolog_name_edit_type = QLineEdit(self)

        self.region_combo_box.currentIndexChanged.connect(self.update_line_edit)
        self.region_combo_box.setCurrentIndex(1)
        grid = QGridLayout(self)

        grid.addWidget(self.productLavelLabel, 0, 0)
        grid.addWidget(self.productLavelType, 0, 1)

        grid.addWidget(self.regionLabel, 1, 0)
        grid.addWidget(self.region_combo_box, 1, 1)

        grid.addWidget(self.cdngLabel, 1, 2)
        grid.addWidget(self.cdng_combo_box, 1, 3)

        grid.addWidget(self.title_job_Label, 3, 0)
        grid.addWidget(self.surname_Label, 3, 2)
        grid.addWidget(self.nach_chng_edit_type, 4, 0)
        grid.addWidget(self.nach_chng_name_edit_type, 4, 2)
        grid.addWidget(self.tehnolog_edit_type, 6, 0)
        grid.addWidget(self.tehnolog_name_edit_type, 6, 2)

        grid.addWidget(self.geolog_edit_type, 9, 0)
        grid.addWidget(self.geolog_name_edit_type, 9, 2)

    def update_line_edit(self):
        self.cdng_list = list(self.podpis_dict[data_list.costumer][self.region_combo_box.currentText()]['ЦДНГ'].keys())
        self.cdng_combo_box.clear()
        self.cdng_combo_box.addItems(self.cdng_list)
        self.cdng_combo_box.currentTextChanged.connect(self.update_line_cdng)
        self.cdng_combo_box.setCurrentIndex(1)

    def update_line_cdng(self, index):
        if index in self.cdng_list:
            self.nach_chng_edit_type.setText(
                self.podpis_dict[data_list.costumer][self.region_combo_box.currentText()]['ЦДНГ'][index]['Начальник'][
                    'post'])
            self.nach_chng_name_edit_type.setText(
                self.podpis_dict[data_list.costumer][self.region_combo_box.currentText()]['ЦДНГ'][index]['Начальник'][
                    "surname"])
            self.tehnolog_edit_type.setText(
                self.podpis_dict[data_list.costumer][self.region_combo_box.currentText()]['ЦДНГ'][index][
                    'Ведущий инженер-технолог']['post'])
            self.tehnolog_name_edit_type.setText(
                self.podpis_dict[data_list.costumer][self.region_combo_box.currentText()]['ЦДНГ'][index][
                    'Ведущий инженер-технолог']['surname'])
            self.geolog_edit_type.setText(
                self.podpis_dict[data_list.costumer][self.region_combo_box.currentText()]['ЦДНГ'][index][
                    'Ведущий геолог']['post'])
            self.geolog_name_edit_type.setText(
                self.podpis_dict[data_list.costumer][self.region_combo_box.currentText()]['ЦДНГ'][index][
                    'Ведущий геолог']['surname'])


class TabWidget(TabWidgetUnion):
    def __init__(self):
        super().__init__()
        self.addTab(TabPageSO(self), 'Изменение данных')


class CorrectSignaturesCdng(QMainWindow):

    def __init__(self):
        super(CorrectSignaturesCdng, self).__init__()

        # self.selected_region = instance.selected_region
        self.podpis_dict = TabPageSO.podpis_dict

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна

        # self.selected_region = selected_region
        self.tab_widget = TabWidget()
        # self.tableWidget = QTableWidget(0, 4)
        # self.labels_nkt = labels_nkt

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.add_row_table)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)

    def add_row_table(self):
        self.current_widget = self.tab_widget.currentWidget()

        selected_region = self.current_widget.region_combo_box.currentText()
        cdng_combo = self.current_widget.cdng_combo_box.currentText()
        self.current_widget = self.tab_widget.currentWidget()

        nach_chng_edit_type = self.current_widget.nach_chng_edit_type.text()
        nach_chng_name_edit_type = self.current_widget.nach_chng_name_edit_type.text().title()
        tehnolog_edit_type = self.current_widget.tehnolog_edit_type.text()
        tehnolog_name_edit_type = self.current_widget.tehnolog_name_edit_type.text().title()
        geolog_edit_type = self.current_widget.geolog_edit_type.text()
        geolog_name_edit_type = self.current_widget.geolog_name_edit_type.text().title()

        name_list = [nach_chng_name_edit_type, tehnolog_name_edit_type, geolog_name_edit_type]

        if selected_region is None:
            QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
            return
        aded = [len(string.split(' ')) == 3 for string in name_list]
        if all([len(string.split(' ')) == 3 for string in name_list]) is False:
            # print([string.count('.') == 2 for string in name_list])
            QMessageBox.information(self, 'Внимание', 'Не корректны сокращения в фамилиях')
            return

        else:
            self.podpis_dict = TabPageSO.podpis_dict

            self.podpis_dict[data_list.costumer][selected_region]["ЦДНГ"][cdng_combo]['Начальник'][
                'post'] = nach_chng_edit_type
            self.podpis_dict[data_list.costumer][selected_region]["ЦДНГ"][cdng_combo]['Начальник'][
                "surname"] = nach_chng_name_edit_type

            self.podpis_dict[data_list.costumer][selected_region]["ЦДНГ"][cdng_combo]['Ведущий инженер-технолог'][
                'post'] = tehnolog_edit_type
            self.podpis_dict[data_list.costumer][selected_region]["ЦДНГ"][cdng_combo]['Ведущий инженер-технолог'][
                'surname'] = tehnolog_name_edit_type

            self.podpis_dict[data_list.costumer][selected_region]["ЦДНГ"][cdng_combo]['Ведущий геолог'][
                'post'] = geolog_edit_type
            self.podpis_dict[data_list.costumer][selected_region]["ЦДНГ"][cdng_combo]['Ведущий геолог'][
                'surname'] = geolog_name_edit_type

            with open(f'{data_list.path_image}podpisant.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.podpis_dict, json_file, indent=4, ensure_ascii=False)

            self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = CorrectSignaturesCdng()
    # window.show()
    app.exec_()
