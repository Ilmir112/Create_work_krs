import json

from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QMainWindow, QPushButton, QMessageBox

import data_list

from PyQt5 import QtCore, QtWidgets

from work_py.parent_work import TabWidgetUnion, WindowUnion


class TabPageSO(QWidget):
    selected_region = None
    podpis_dict = None

    def __init__(self, parent=None):
        super().__init__()

        # Открытие JSON файла и чтение данных
        with open(f'{data_list.path_image}podpisant.json', 'r', encoding='utf-8') as file:
            self.podpis_dict = json.load(file)

        self.productLavelLabel = QLabel("Подрядчик", self)
        self.productLavelType = QComboBox(self)
        self.productLavelType.addItems([data_list.contractor])

        self.regionLabel = QLabel("Экспедиция", self)
        self.region_combo_box = QComboBox(self)
        # self.region_combo_box.addItems([list(data_list.DICT_CONTRACTOR.keys())])

        if 'РН' in data_list.contractor:
            asw = self.podpis_dict[self.productLavelType.currentText()]["Экспедиция"]
            self.region_list = list(self.podpis_dict[self.productLavelType.currentText()]["Экспедиция"].keys())
            self.region_combo_box.addItems(self.region_list)

        elif 'Ойл' in data_list.contractor:
            self.region_list = list(self.podpis_dict[self.productLavelType.currentText()]["Экспедиция"].keys())
            self.region_combo_box.addItems(self.region_list)

        grid = QGridLayout(self)

        self.title_job_Label = QLabel("Должность", self)
        self.surname_Label = QLabel("Фамилия И.О.", self)

        self.сhief_engineer_edit = QLineEdit(self)
        self.сhief_engineer_name_edit = QLineEdit(self)
        self.сhief_engineer_edit.setReadOnly(True)

        self.chief_geologist_edit_type = QLineEdit(self)
        self.chief_geologist_edit_type.setReadOnly(True)
        self.chief_geologist_name_edit_type = QLineEdit(self)
        self.сhief_engineer_expedition_edit = QLineEdit(self)
        self.сhief_engineer_expedition_name_edit = QLineEdit(self)
        self.сhief_engineer_expedition_edit.setReadOnly(True)
        grid.addWidget(self.сhief_engineer_expedition_edit, 14, 0, 1, 2)
        grid.addWidget(self.сhief_engineer_expedition_name_edit, 14, 2, 1, 2)

        if 'РН' in data_list.contractor:
            self.chief_geologist_expedition_edit_type = QLineEdit(self)
            self.chief_geologist_expedition_edit_type.setReadOnly(True)
            self.chief_geologist_expedition_name_edit_type = QLineEdit(self)

            grid.addWidget(self.chief_geologist_expedition_edit_type, 16, 0, 1, 2)
            grid.addWidget(self.chief_geologist_expedition_name_edit_type, 16, 2, 1, 2)

        self.region_combo_box.currentTextChanged.connect(self.update_line)
        # self.region_combo_box.setCurrentIndex(1)

        grid.addWidget(self.productLavelLabel, 0, 0)
        grid.addWidget(self.productLavelType, 0, 1)

        grid.addWidget(self.regionLabel, 1, 0)
        grid.addWidget(self.region_combo_box, 1, 1)

        grid.addWidget(self.title_job_Label, 3, 0)
        grid.addWidget(self.surname_Label, 3, 2)
        grid.addWidget(self.сhief_engineer_edit, 4, 0, 1, 2)
        grid.addWidget(self.сhief_engineer_name_edit, 4, 2, 1, 2)
        grid.addWidget(self.chief_geologist_edit_type, 6, 0, 1, 2)
        grid.addWidget(self.chief_geologist_name_edit_type, 6, 2, 1, 2)

        # grid.addWidget(self.geolog_edit_type, 9, 0)
        # grid.addWidget(self.geolog_name_edit_type, 9, 2)

    def update_line(self, index):
        self.сhief_engineer_edit.setText(
            self.podpis_dict[data_list.contractor]['Руководство']['сhief_engineer']['post'])
        self.сhief_engineer_name_edit.setText(
            self.podpis_dict[data_list.contractor]['Руководство']['сhief_engineer']["surname"])
        self.chief_geologist_edit_type.setText(
            self.podpis_dict[data_list.contractor]['Руководство']['chief_geologist']['post'])
        self.chief_geologist_name_edit_type.setText(
            self.podpis_dict[data_list.contractor]['Руководство']['chief_geologist']["surname"])
        self.сhief_engineer_expedition_edit.setText(
            self.podpis_dict[data_list.contractor]['Экспедиция'][index]['сhief_engineer']['post'])
        self.сhief_engineer_expedition_name_edit.setText(
            self.podpis_dict[data_list.contractor]['Экспедиция'][index]['сhief_engineer']["surname"])
        if 'РН' in data_list.contractor:
            awdwadw = self.podpis_dict[data_list.contractor]['Экспедиция'][index]['chief_geologist']['post']

            self.chief_geologist_expedition_edit_type.setText(
                self.podpis_dict[data_list.contractor]['Экспедиция'][index]['chief_geologist']['post'])
            self.chief_geologist_expedition_name_edit_type.setText(
                self.podpis_dict[data_list.contractor]['Экспедиция'][index]['chief_geologist']["surname"])

            # self.geolog_edit_type.setText(
            #     self.podpis_dict[data_list.contractor][self.region_combo_box.currentText()]['ЦДНГ'][index][
            #         'Ведущий геолог']['post'])
            # self.geolog_name_edit_type.setText(
            #     self.podpis_dict[data_list.contractor][self.region_combo_box.currentText()]['ЦДНГ'][index][
            #         # 'Ведущий геолог']['surname'])


class TabWidget(TabWidgetUnion):
    def __init__(self):
        super().__init__()
        self.addTab(TabPageSO(self), 'Изменение данных')


class CorrectSignaturesContractor(QMainWindow):

    def __init__(self):
        super(CorrectSignaturesContractor, self).__init__()

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
        self.current_widget = self.tab_widget.currentWidget()

        сhief_engineer_edit = self.current_widget.сhief_engineer_edit.text()
        сhief_engineer_name_edit = self.current_widget.сhief_engineer_name_edit.text().title()
        chief_geologist_edit_type = self.current_widget.chief_geologist_edit_type.text()
        chief_geologist_name_edit_type = self.current_widget.chief_geologist_name_edit_type.text().title()
        сhief_engineer_expedition_edit = self.current_widget.сhief_engineer_expedition_edit.text()
        сhief_engineer_expedition_name_edit = self.current_widget.сhief_engineer_expedition_name_edit.text()
        if "РН" in data_list.contractor:
            chief_geologist_expedition_edit_type = self.current_widget.chief_geologist_expedition_edit_type.text()
            chief_geologist_expedition_name_edit_type = self.current_widget.chief_geologist_expedition_name_edit_type.text()
        # geolog_edit_type = self.current_widget.geolog_edit_type.text()
        # geolog_name_edit_type = self.current_widget.geolog_name_edit_type.text().title()

        name_list = [сhief_engineer_name_edit, chief_geologist_name_edit_type,  сhief_engineer_expedition_name_edit]

        if selected_region is None:
            QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
            return
        aded = [string.count('.') == 2 for string in name_list]
        if all([string.count('.') == 2 for string in name_list]) is False:
            # print([string.count('.') == 2 for string in name_list])
            QMessageBox.information(self, 'Внимание', 'Не корректны сокращения в фамилиях')
            return

        else:
            self.podpis_dict = self.current_widget.podpis_dict

            self.podpis_dict[data_list.contractor]['Руководство']['сhief_engineer'][
                'post'] = сhief_engineer_edit
            self.podpis_dict[data_list.contractor]['Руководство']['сhief_engineer'][
                "surname"] = сhief_engineer_name_edit

            self.podpis_dict[data_list.contractor]['Руководство']["chief_geologist"][
                'post'] = chief_geologist_edit_type
            self.podpis_dict[data_list.contractor]['Руководство']["chief_geologist"][
                'surname'] = chief_geologist_name_edit_type

            self.podpis_dict[data_list.contractor]['Экспедиция'][selected_region]['сhief_engineer'][
                'post'] = сhief_engineer_expedition_edit

            self.podpis_dict[data_list.contractor]['Экспедиция'][selected_region][
                'сhief_engineer']['surname'] = сhief_engineer_expedition_name_edit
            if 'РН' in data_list.contractor:
                self.podpis_dict[data_list.contractor]['Экспедиция'][selected_region]["chief_geologist"][
                    'surname'] = chief_geologist_expedition_name_edit_type

                self.podpis_dict[data_list.contractor]['Экспедиция'][selected_region][
                    "chief_geologist"]['post'] = chief_geologist_expedition_edit_type

            with open(f'{data_list.path_image}podpisant.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.podpis_dict, json_file, indent=4, ensure_ascii=False)

            self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = CorrectSignaturesContractor()
    window.show()
    app.exec_()
