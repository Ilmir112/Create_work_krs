import json

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtGui import QRegExpValidator, QColor, QPalette

import re



class TabPage_SO(QWidget):
    selected_region = None
    podpis_dict = None

    def __init__(self, parent=None):
        super().__init__(parent)



        # Открытие JSON файла и чтение данных
        with open(f'{well_data.path_image}podpisant.json', 'r', encoding='utf-8') as file:
            self.podpis_dict = json.load(file)
        TabPage_SO.podpis_dict = self.podpis_dict
        self.region_list = [' ', 'АГМ', 'ИГМ', 'ТГМ', 'ЧГМ', 'КГМ']

        self.productLavelLabel = QLabel("Заказчик", self)
        self.productLavelType = QLineEdit(self)
        self.productLavelType.setText(f"ООО Башнефть_добыча")

        self.regionLabel = QLabel("Регион", self)
        self.regioncomboBox = QComboBox(self)
        self.regioncomboBox.addItems(self.region_list)
        self.regioncomboBox.currentIndexChanged.connect(self.update_line_edit)

        self.region_select = self.regioncomboBox.currentText()

        self.title_job_Label = QLabel("Должность", self)
        self.surname_Label = QLabel("Фамилия и.о.", self)

        self.chief_Label = QLabel("Руководители региона", self)
        self.head_of_ORM_Label = QLabel("Сектор разработки", self)
        self.head_of_GTM_Label = QLabel("Сектор Анализа ГТМ", self)
        self.head_of_GO_Label = QLabel("Сектор геологический и ВНС", self)
        self.head_of_GRR_Label = QLabel("Сектор геолого-разведки", self)
        self.head_of_USRSIST_Label = QLabel("Сектор супервайзерской службы", self)

        self.chiefEngineerEditType = QLineEdit(self)
        self.chiefEngineer_nameEditType = QLineEdit(self)

        self.chiefGeologistEditType = QLineEdit(self)
        self.chiefGeologist_nameEditType = QLineEdit(self)

        self.head_of_ORM_editType = QLineEdit(self)
        self.head_of_ORM_name_editType = QLineEdit(self)

        self.representative_of_ORM_editType = QLineEdit(self)
        self.representative_of_ORM_name_editType = QLineEdit(self)

        self.head_of_GTM_editType = QLineEdit(self)
        self.head_of_GTM_name_editType = QLineEdit(self)

        self.representative_of_GTM_editType = QLineEdit(self)
        self.representative_of_GTM_name_editType = QLineEdit(self)

        self.representative_of_GO_editType = QLineEdit(self)
        self.representative_of_GO_name_editType = QLineEdit(self)

        self.head_of_USRSIST_editType = QLineEdit(self)
        self.head_of_USRSIST_name_editType = QLineEdit(self)

        self.representative_of_GRR_editType = QLineEdit(self)
        self.representative_of_GRR_name_editType = QLineEdit(self)

        grid = QGridLayout(self)

        grid.addWidget(self.productLavelLabel, 0, 0)
        grid.addWidget(self.productLavelType, 0, 1)

        grid.addWidget(self.regionLabel, 1, 0)
        grid.addWidget(self.regioncomboBox, 1, 1)

        grid.addWidget(self.chief_Label, 2, 1)
        grid.addWidget(self.title_job_Label, 3, 0)
        grid.addWidget(self.surname_Label, 3, 2)
        grid.addWidget(self.chiefEngineerEditType, 4, 0)
        grid.addWidget(self.chiefEngineer_nameEditType, 4, 2)
        grid.addWidget(self.chiefGeologistEditType, 6, 0)
        grid.addWidget(self.chiefGeologist_nameEditType, 6, 2)

        grid.addWidget(self.head_of_ORM_Label, 7, 1)

        grid.addWidget(self.head_of_ORM_editType, 9, 0)
        grid.addWidget(self.head_of_ORM_name_editType, 9, 2)
        grid.addWidget(self.representative_of_ORM_editType, 10, 0)
        grid.addWidget(self.representative_of_ORM_name_editType, 10, 2)

        grid.addWidget(self.head_of_GTM_Label, 11, 1)

        grid.addWidget(self.head_of_GTM_editType, 13, 0)
        grid.addWidget(self.head_of_GTM_name_editType, 13, 2)
        grid.addWidget(self.representative_of_GTM_editType, 14, 0)
        grid.addWidget(self.representative_of_GTM_name_editType, 14, 2)

        grid.addWidget(self.head_of_GO_Label, 15, 1)

        grid.addWidget(self.representative_of_GO_editType, 17, 0)
        grid.addWidget(self.representative_of_GO_name_editType, 17, 2)

        grid.addWidget(self.head_of_GRR_Label, 18, 1)

        grid.addWidget(self.representative_of_GRR_editType, 20, 0)
        grid.addWidget(self.representative_of_GRR_name_editType, 20, 2)

        grid.addWidget(self.head_of_USRSIST_Label, 21, 1)

        grid.addWidget(self.head_of_USRSIST_editType, 23, 0)
        grid.addWidget(self.head_of_USRSIST_name_editType, 23, 2)

    def update_line_edit(self):
        selected_region = self.regioncomboBox.currentText()
        TabPage_SO.selected_region = selected_region

        self.chiefEngineerEditType.setText(self.podpis_dict[selected_region]['gi']['post'])
        self.chiefEngineer_nameEditType.setText(self.podpis_dict[selected_region]['gi']["surname"])

        self.chiefGeologistEditType.setText(self.podpis_dict[selected_region]['gg']['post'])
        self.chiefGeologist_nameEditType.setText(self.podpis_dict[selected_region]['gg']['surname'])

        self.head_of_ORM_editType.setText(self.podpis_dict[selected_region]["ruk_orm"]['post'])
        self.head_of_ORM_name_editType.setText(self.podpis_dict[selected_region]["ruk_orm"]['surname'])

        self.representative_of_ORM_editType.setText(self.podpis_dict[selected_region]["ved_orm"]['post'])
        self.representative_of_ORM_name_editType.setText(self.podpis_dict[selected_region]["ved_orm"]['surname'])

        self.head_of_GTM_editType.setText(self.podpis_dict[selected_region]["ruk_gtm"]['post'])
        self.head_of_GTM_name_editType.setText(self.podpis_dict[selected_region]["ruk_gtm"]['surname'])

        self.representative_of_GTM_editType.setText(self.podpis_dict[selected_region]["ved_gtm"]['post'])
        self.representative_of_GTM_name_editType.setText(self.podpis_dict[selected_region]["ved_gtm"]['surname'])

        self.representative_of_GO_editType.setText(self.podpis_dict[selected_region]["go"]['post'])
        self.representative_of_GO_name_editType.setText(self.podpis_dict[selected_region]["go"]['surname'])

        self.head_of_USRSIST_editType.setText(self.podpis_dict[selected_region]["usrs"]['post'])
        self.head_of_USRSIST_name_editType.setText(self.podpis_dict[selected_region]["usrs"]['surname'])

        self.representative_of_GRR_editType.setText(self.podpis_dict[selected_region]["grr"]['post'])
        self.representative_of_GRR_name_editType.setText(self.podpis_dict[selected_region]["grr"]['surname'])


class TabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_SO(self), 'Изменение данных')


class CorrectSignaturesWindow(QMainWindow):

    def __init__(self, parent=None):
        super(CorrectSignaturesWindow, self).__init__()

        # self.selected_region = instance.selected_region

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна

        # self.selected_region = selected_region
        self.tabWidget = TabWidget()
        # self.tableWidget = QTableWidget(0, 4)
        # self.labels_nkt = labels_nkt

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.addRowTable)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)



    def addRowTable(self):
        selected_region = TabPage_SO.selected_region
        self.podpis_dict = TabPage_SO.podpis_dict

        chiefEngineerEditType = self.tabWidget.currentWidget().chiefEngineerEditType.text()
        chiefEngineer_nameEditType = self.tabWidget.currentWidget().chiefEngineer_nameEditType.text().title()
        chiefGeologistEditType = self.tabWidget.currentWidget().chiefGeologistEditType.text()
        chiefGeologist_nameEditType = self.tabWidget.currentWidget().chiefGeologist_nameEditType.text().title()
        head_of_ORM_editType = self.tabWidget.currentWidget().head_of_ORM_editType.text()
        head_of_ORM_name_editType = self.tabWidget.currentWidget().head_of_ORM_name_editType.text().title()
        representative_of_ORM_editType = self.tabWidget.currentWidget().representative_of_ORM_editType.text()
        representative_of_ORM_name_editType = self.tabWidget.currentWidget().representative_of_ORM_name_editType.text().title()
        head_of_GTM_editType = self.tabWidget.currentWidget().head_of_GTM_editType.text()
        head_of_GTM_name_editType = self.tabWidget.currentWidget().head_of_GTM_name_editType.text().title()
        representative_of_GTM_editType = self.tabWidget.currentWidget().representative_of_GTM_editType.text()
        representative_of_GTM_name_editType = self.tabWidget.currentWidget().representative_of_GTM_name_editType.text().title()
        representative_of_GO_editType = self.tabWidget.currentWidget().representative_of_GO_editType.text()
        representative_of_GO_name_editType = self.tabWidget.currentWidget().representative_of_GO_name_editType.text().title()
        head_of_USRSIST_editType = self.tabWidget.currentWidget().head_of_USRSIST_editType.text()
        head_of_USRSIST_name_editType = self.tabWidget.currentWidget().head_of_USRSIST_name_editType.text().title()
        representative_of_GRR_editType = self.tabWidget.currentWidget().representative_of_GRR_editType.text()

        representative_of_GRR_name_editType = self.tabWidget.currentWidget().representative_of_GRR_name_editType.text().title()

        name_list = [chiefEngineer_nameEditType, chiefGeologist_nameEditType,
                    head_of_USRSIST_name_editType, head_of_GTM_name_editType, head_of_ORM_name_editType,
                    representative_of_GRR_name_editType, representative_of_GTM_name_editType,
                         representative_of_ORM_name_editType]
        if  TabPage_SO.selected_region == None:
            msg = QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
            return

        elif all([string.count('.') == 2 for string in name_list]) is False:
            # print([string.count('.') == 2 for string in name_list])
            msg = QMessageBox.information(self, 'Внимание', 'Не корректны сокращения в фамилиях')
            return

        else:

            self.podpis_dict[selected_region]['gi']['post'] = chiefEngineerEditType
            self.podpis_dict[selected_region]['gi']["surname"] = chiefEngineer_nameEditType

            self.podpis_dict[selected_region]['gg']['post'] = chiefGeologistEditType
            self.podpis_dict[selected_region]['gg']['surname'] = chiefGeologist_nameEditType

            self.podpis_dict[selected_region]["ruk_orm"]['post'] = head_of_ORM_editType
            self.podpis_dict[selected_region]["ruk_orm"]['surname'] = head_of_ORM_name_editType

            self.podpis_dict[selected_region]["ved_orm"]['post'] = representative_of_ORM_editType
            self.podpis_dict[selected_region]["ved_orm"]['surname'] = representative_of_ORM_name_editType

            self.podpis_dict[selected_region]["ruk_gtm"]['post'] = head_of_GTM_editType
            self.podpis_dict[selected_region]["ruk_gtm"]['surname'] = head_of_GTM_name_editType

            self.podpis_dict[selected_region]["ved_gtm"]['post'] = representative_of_GTM_editType
            self.podpis_dict[selected_region]["ved_gtm"]['surname'] = representative_of_GTM_name_editType

            self.podpis_dict[selected_region]["go"]['post'] = representative_of_GO_editType
            self.podpis_dict[selected_region]["go"]['surname'] = representative_of_GO_name_editType

            self.podpis_dict[selected_region]["usrs"]['post'] = head_of_USRSIST_editType
            self.podpis_dict[selected_region]["usrs"]['surname'] = head_of_USRSIST_name_editType

            self.podpis_dict[selected_region]["grr"]['post'] = representative_of_GRR_editType
            self.podpis_dict[selected_region]["grr"]['surname'] = representative_of_GRR_name_editType


            with open(f'{well_data.path_image}podpisant.json', 'w', encoding = 'utf-8') as json_file:
                json.dump(self.podpis_dict, json_file, indent=4, ensure_ascii=False)

            self.close()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = CorrectSignaturesWindow()
    # window.show()
    app.exec_()
