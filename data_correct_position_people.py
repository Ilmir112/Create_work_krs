import json
import data_list
from typing import cast

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (  # type: ignore[import-untyped]
    QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QMainWindow, QPushButton, QMessageBox,
)
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
        self.REGION_LIST = data_list.REGION_LIST
        self.region_combo_box.addItems(self.REGION_LIST)
        self.region_combo_box.currentIndexChanged.connect(self.update_line_edit)

        self.region_select = self.region_combo_box.currentText()

        self.title_job_label = QLabel("Должность", self)
        self.surname_label = QLabel("Фамилия И.О.", self)

        self.chief_label = QLabel("Руководители региона", self)
        self.head_of_orm_label = QLabel("Сектор разработки", self)
        self.head_of_gtm_label = QLabel("Сектор Анализа ГТМ", self)
        self.head_of_go_label = QLabel("Сектор геологический и ВНС", self)
        self.head_of_grr_label = QLabel("Сектор геолого-разведки", self)
        self.head_of_usrsist_label = QLabel("Сектор супервайзерской службы", self)

        self.chief_engineer_edit_type = QLineEdit(self)
        self.chief_engineer_edit_type.setReadOnly(True)
        self.chief_engineer_name_edit_type = QLineEdit(self)

        self.chief_geologist_edit_type = QLineEdit(self)
        self.chief_geologist_edit_type.setReadOnly(True)
        self.chief_geologist_name_edit_type = QLineEdit(self)

        self.head_of_orm_edit_type = QLineEdit(self)
        self.head_of_orm_edit_type.setReadOnly(True)
        self.head_of_orm_name_edit_type = QLineEdit(self)

        self.representative_of_orm_edit_type = QLineEdit(self)
        self.representative_of_orm_name_edit_type = QLineEdit(self)

        self.head_of_gtm_edit_type = QLineEdit(self)
        self.head_of_gtm_edit_type.setReadOnly(True)
        self.head_of_gtm_name_edit_type = QLineEdit(self)

        self.representative_of_gtm_edit_type = QLineEdit(self)
        self.representative_of_gtm_name_edit_type = QLineEdit(self)

        self.representative_of_go_edit_type = QLineEdit(self)
        self.representative_of_go_name_edit_type = QLineEdit(self)

        self.head_of_usrsist_edit_type = QLineEdit(self)
        self.head_of_usrsist_name_edit_type = QLineEdit(self)

        self.representative_of_grr_edit_type = QLineEdit(self)
        self.representative_of_grr_name_edit_type = QLineEdit(self)

        grid = QGridLayout(self)

        grid.addWidget(self.productLavelLabel, 0, 0)
        grid.addWidget(self.productLavelType, 0, 1)

        grid.addWidget(self.regionLabel, 1, 0)
        grid.addWidget(self.region_combo_box, 1, 1)

        grid.addWidget(self.chief_label, 2, 1)
        grid.addWidget(self.title_job_label, 3, 0)
        grid.addWidget(self.surname_label, 3, 2)
        grid.addWidget(self.chief_engineer_edit_type, 4, 0)
        grid.addWidget(self.chief_engineer_name_edit_type, 4, 2)
        grid.addWidget(self.chief_geologist_edit_type, 6, 0)
        grid.addWidget(self.chief_geologist_name_edit_type, 6, 2)

        grid.addWidget(self.head_of_orm_label, 7, 1)

        grid.addWidget(self.head_of_orm_edit_type, 9, 0)
        grid.addWidget(self.head_of_orm_name_edit_type, 9, 2)
        grid.addWidget(self.representative_of_orm_edit_type, 10, 0)
        grid.addWidget(self.representative_of_orm_name_edit_type, 10, 2)

        grid.addWidget(self.head_of_gtm_label, 11, 1)

        grid.addWidget(self.head_of_gtm_edit_type, 13, 0)
        grid.addWidget(self.head_of_gtm_name_edit_type, 13, 2)
        grid.addWidget(self.representative_of_gtm_edit_type, 14, 0)
        grid.addWidget(self.representative_of_gtm_name_edit_type, 14, 2)

        grid.addWidget(self.head_of_go_label, 15, 1)

        grid.addWidget(self.representative_of_go_edit_type, 17, 0)
        grid.addWidget(self.representative_of_go_name_edit_type, 17, 2)

        grid.addWidget(self.head_of_grr_label, 18, 1)

        grid.addWidget(self.representative_of_grr_edit_type, 20, 0)
        grid.addWidget(self.representative_of_grr_name_edit_type, 20, 2)

        grid.addWidget(self.head_of_usrsist_label, 21, 1)

        grid.addWidget(self.head_of_usrsist_edit_type, 23, 0)
        grid.addWidget(self.head_of_usrsist_name_edit_type, 23, 2)

    def _safe_get(self, region_data: dict, role: str, field: str) -> str:
        """Get nested value; avoid 'None is not subscriptable' when dict/role is missing or None."""
        role_data = region_data.get(role) if region_data else None
        if not isinstance(role_data, dict):
            return ''
        return role_data.get(field, '')

    def update_line_edit(self):
        selected_region = self.region_combo_box.currentText()
        TabPageSO.selected_region = selected_region
        if not selected_region or not self.podpis_dict:
            return
        costumer_data = self.podpis_dict.get(data_list.costumer) if isinstance(self.podpis_dict, dict) else None
        region_data = (costumer_data.get(selected_region) if isinstance(costumer_data, dict) else None) or {}

        self.chief_engineer_edit_type.setText(self._safe_get(region_data, 'gi', 'post'))
        self.chief_engineer_name_edit_type.setText(self._safe_get(region_data, 'gi', 'surname'))

        self.chief_geologist_edit_type.setText(self._safe_get(region_data, 'gg', 'post'))
        self.chief_geologist_name_edit_type.setText(self._safe_get(region_data, 'gg', 'surname'))

        self.head_of_orm_edit_type.setText(self._safe_get(region_data, 'ruk_orm', 'post'))
        self.head_of_orm_name_edit_type.setText(self._safe_get(region_data, 'ruk_orm', 'surname'))

        self.representative_of_orm_edit_type.setText(self._safe_get(region_data, 'ved_orm', 'post'))
        self.representative_of_orm_name_edit_type.setText(self._safe_get(region_data, 'ved_orm', 'surname'))

        self.head_of_gtm_edit_type.setText(self._safe_get(region_data, 'ruk_gtm', 'post'))
        self.head_of_gtm_name_edit_type.setText(self._safe_get(region_data, 'ruk_gtm', 'surname'))

        self.representative_of_gtm_edit_type.setText(self._safe_get(region_data, 'ved_gtm', 'post'))
        self.representative_of_gtm_name_edit_type.setText(self._safe_get(region_data, 'ved_gtm', 'surname'))

        self.representative_of_go_edit_type.setText(self._safe_get(region_data, 'go', 'post'))
        self.representative_of_go_name_edit_type.setText(self._safe_get(region_data, 'go', 'surname'))

        self.head_of_usrsist_edit_type.setText(self._safe_get(region_data, 'usrs', 'post'))
        self.head_of_usrsist_name_edit_type.setText(self._safe_get(region_data, 'usrs', 'surname'))

        self.representative_of_grr_edit_type.setText(self._safe_get(region_data, 'grr', 'post'))
        self.representative_of_grr_name_edit_type.setText(self._safe_get(region_data, 'grr', 'surname'))


class TabWidget(TabWidgetUnion):
    def __init__(self):
        super().__init__()
        self.addTab(TabPageSO(self), 'Изменение данных')


class CorrectSignaturesWindow(QMainWindow):

    def __init__(self):
        super(CorrectSignaturesWindow, self).__init__()

        # self.selected_region = instance.selected_region
        self.podpis_dict = TabPageSO.podpis_dict

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна

        # self.selected_region = selected_region
        self.tab_widget = TabWidget()
        # self.tableWidget = QTableWidget(0, 4)
        # self.labels_nkt = labels_nkt

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.add_row_table)

        vbox = QGridLayout(central_widget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)

    def close_modal_forcefully(self) -> None:
        self.close()

    def add_row_table(self):
        selected_region = TabPageSO.selected_region
        self.current_widget = self.tab_widget.currentWidget()
        tab = cast(TabPageSO, self.current_widget)

        chief_engineer_edit_type = tab.chief_engineer_edit_type.text()
        chief_engineer_name_edit_type = tab.chief_engineer_name_edit_type.text().title()
        chief_geologist_edit_type = tab.chief_geologist_edit_type.text()
        chief_geologist_name_edit_type = tab.chief_geologist_name_edit_type.text().title()
        head_of_orm_edit_type = tab.head_of_orm_edit_type.text()
        head_of_orm_name_edit_type = tab.head_of_orm_name_edit_type.text().title()
        representative_of_orm_edit_type = tab.representative_of_orm_edit_type.text()
        representative_of_orm_name_edit_type = tab.representative_of_orm_name_edit_type.text().title()
        head_of_gtm_edit_type = tab.head_of_gtm_edit_type.text()
        head_of_gtm_name_edit_type = tab.head_of_gtm_name_edit_type.text().title()
        representative_of_gtm_edit_type = tab.representative_of_gtm_edit_type.text()
        representative_of_gtm_name_edit_type = tab.representative_of_gtm_name_edit_type.text().title()
        representative_of_go_edit_type = tab.representative_of_go_edit_type.text()
        representative_of_go_name_edit_type = tab.representative_of_go_name_edit_type.text().title()
        head_of_usrsist_edit_type = tab.head_of_usrsist_edit_type.text()
        head_of_usrsist_name_edit_type = tab.head_of_usrsist_name_edit_type.text().title()
        representative_of_grr_edit_type = tab.representative_of_grr_edit_type.text()
        representative_of_grr_name_edit_type = tab.representative_of_grr_name_edit_type.text().title()

        name_list = [chief_engineer_name_edit_type, chief_geologist_name_edit_type,
                     head_of_usrsist_name_edit_type, head_of_gtm_name_edit_type, head_of_orm_name_edit_type,
                     representative_of_grr_name_edit_type, representative_of_gtm_name_edit_type,
                     representative_of_orm_name_edit_type]
        if TabPageSO.selected_region is None:
            QMessageBox.information(self, 'Внимание', 'Не все поля соответствуют значениям')
            return

        elif all([string.count('.') == 2 for string in name_list]) is False:
            # print([string.count('.') == 2 for string in name_list])
            QMessageBox.information(self, 'Внимание', 'Не корректны сокращения в фамилиях')
            return

        else:
            self.podpis_dict = TabPageSO.podpis_dict
            if not isinstance(self.podpis_dict, dict):
                QMessageBox.information(self, 'Внимание', 'Данные подписей не загружены')
                self.close_modal_forcefully()
                return
            costumer_data = self.podpis_dict.setdefault(data_list.costumer, {})
            region_data = costumer_data.setdefault(selected_region, {})
            for role, default in (
                ('gi', {}), ('gg', {}), ('ruk_orm', {}), ('ved_orm', {}),
                ('ruk_gtm', {}), ('ved_gtm', {}), ('go', {}), ('usrs', {}), ('grr', {}),
            ):
                if region_data.get(role) is None:
                    region_data[role] = {'post': '', 'surname': ''}

            region_data['gi']['post'] = chief_engineer_edit_type
            region_data['gi']['surname'] = chief_engineer_name_edit_type

            region_data['gg']['post'] = chief_geologist_edit_type
            region_data['gg']['surname'] = chief_geologist_name_edit_type

            region_data['ruk_orm']['post'] = head_of_orm_edit_type
            region_data['ruk_orm']['surname'] = head_of_orm_name_edit_type

            region_data['ved_orm']['post'] = representative_of_orm_edit_type
            region_data['ved_orm']['surname'] = representative_of_orm_name_edit_type

            region_data['ruk_gtm']['post'] = head_of_gtm_edit_type
            region_data['ruk_gtm']['surname'] = head_of_gtm_name_edit_type

            region_data['ved_gtm']['post'] = representative_of_gtm_edit_type
            region_data['ved_gtm']['surname'] = representative_of_gtm_name_edit_type

            region_data['go']['post'] = representative_of_go_edit_type
            region_data['go']['surname'] = representative_of_go_name_edit_type

            region_data['usrs']['post'] = head_of_usrsist_edit_type
            region_data['usrs']['surname'] = head_of_usrsist_name_edit_type

            region_data['grr']['post'] = representative_of_grr_edit_type
            region_data['grr']['surname'] = representative_of_grr_name_edit_type

            with open(f'{data_list.path_image}podpisant.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.podpis_dict, json_file, indent=4, ensure_ascii=False)

            self.close()
        self.close_modal_forcefully()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = CorrectSignaturesWindow()
    # window.show()
    app.exec_()