import data_list

from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtGui import QRegExpValidator, QColor, QPalette

from find import FindIndexPZ
from work_py.advanted_file import definition_plast_work
from work_py.parent_work import TabWidgetUnion, WindowUnion


class FloatLineEdit(QLineEdit):
    def __init__(self):
        super(FloatLineEdit, self).__init__()

        # Устанавливаем валидатор для проверки на float

        reg = QRegExp("[0-9.]*")
        p_validator = QRegExpValidator(self)
        p_validator.setRegExp(reg)
        self.setValidator(p_validator)

    def focusOutEvent(self, event):
        # При потере фокуса проверяем, является ли текст float
        if self.validator().validate(self.text(), 0)[0] != QValidator.Acceptable:
            # Если текст не является числом, меняем цвет фона на красный
            palette = self.palette()
            palette.setColor(QPalette.Base, QColor(Qt.red))
            self.setPalette(palette)
        else:
            # Если текст является числом, возвращаем цвет фона по умолчанию
            self.setPalette(self.parentWidget().palette())


class TabPageSo(QWidget):
    def __init__(self, parent: FindIndexPZ):
        super().__init__()
        self.data_well = parent
        self.labels_plast = {}
        self.dict_perforation = parent.dict_perforation
        self.dict_perforation_project = parent.dict_perforation_project

        self.plast_label = QLabel("пласта")
        self.roof_label = QLabel("Кровля")
        self.sole_label = QLabel("Подошва")
        self.plast_status_label = QLabel("Статус пласта")
        self.template_status_label = QLabel("Прошаблонировано")
        self.raiding_status_label = QLabel("Отрайбировано")

        grid = QGridLayout(self)
        grid.addWidget(self.plast_label, 0, 0)
        grid.addWidget(self.roof_label, 0, 1)
        grid.addWidget(self.sole_label, 0, 2)
        grid.addWidget(self.plast_status_label, 0, 3)
        grid.addWidget(self.template_status_label, 0, 4)
        grid.addWidget(self.raiding_status_label, 0, 5)

        plast_all = list(self.dict_perforation.keys())
        plast_projects = list(self.dict_perforation_project.keys())

        index_interval = 1
        for plast in plast_all:
            for index, (roof, sole) in enumerate(list(sorted(self.dict_perforation[plast]["интервал"],
                                                             key=lambda x: x[0]))):
                plast_edit = QLineEdit(self)
                plast_edit.setText(plast)

                roof_edit = QLineEdit(self)
                roof_edit.setText(str(roof))

                sole_edit = QLineEdit(self)
                sole_edit.setText(str(sole))

                plast_status_combo = QComboBox(self)
                plast_status_combo.addItems(['отключен', 'вскрыт', 'проект', 'отсутствует'])
                plast_status_combo.setCurrentIndex(self.check_plast_status(plast))

                template_status_combo = QComboBox(self)
                template_status_combo.addItems(['Прошаблонировано', 'Не прошаблонировано'])
                # template_status_combo.setText('Прошаблонировано')
                template_status_combo.setCurrentIndex(self.check_template_status(plast))

                raiding_status_combo = QComboBox(self)
                raiding_status_combo.addItems(['отрайбировано', 'Не отрайбировано'])
                # raiding_status_combo.setText('отрайбировано')
                raiding_status_combo.setCurrentIndex(self.check_raiding_status(plast))

                grid.addWidget(plast_edit, index_interval, 0)
                grid.addWidget(roof_edit, index_interval, 1)
                grid.addWidget(sole_edit, index_interval, 2)
                grid.addWidget(plast_status_combo, index_interval, 3)
                grid.addWidget(template_status_combo, index_interval, 4)
                grid.addWidget(raiding_status_combo, index_interval, 5)

                # Переименование атрибута
                setattr(self, f"plast_{index_interval}_edit", plast_edit)
                setattr(self, f"roof_{index_interval}_edit", roof_edit)
                setattr(self, f"sole_{index_interval}_edit", sole_edit)
                setattr(self, f"plast_status_{index_interval}_edit", plast_status_combo)
                setattr(self, f"template_status_{index_interval}_edit", template_status_combo)
                setattr(self, f"raiding_status_{index_interval}_edit", raiding_status_combo)

                self.labels_plast[index_interval] = (plast_edit, roof_edit, sole_edit, plast_status_combo,
                                                     template_status_combo, raiding_status_combo)
                index_interval += 1
        if len(self.data_well.dict_perforation) != 0:
            for plast in plast_projects:
                for index, (roof, sole) in enumerate(list(sorted(self.dict_perforation_project[plast]["интервал"],
                                                                 key=lambda x: x[0]))):
                    plast_edit = QLineEdit(self)
                    plast_edit.setText(plast)

                    roof_edit = QLineEdit(self)
                    roof_edit.setText(str(roof))

                    sole_edit = QLineEdit(self)
                    sole_edit.setText(str(sole))

                    plast_status_combo = QComboBox(self)
                    plast_status_combo.addItems(['отключен', 'вскрыт', 'проект', 'отсутствует'])
                    plast_status_combo.setCurrentIndex(2)

                    template_status_combo = QComboBox(self)
                    template_status_combo.addItems(['Прошаблонировано', 'Не прошаблонировано'])
                    # template_status_combo.setText('Прошаблонировано')
                    template_status_combo.setCurrentIndex(1)

                    raiding_status_combo = QComboBox(self)
                    raiding_status_combo.addItems(['отрайбировано', 'Не отрайбировано'])
                    # raiding_status_combo.setText('отрайбировано')
                    raiding_status_combo.setCurrentIndex(1)

                    grid.addWidget(plast_edit, index_interval, 0)
                    grid.addWidget(roof_edit, index_interval, 1)
                    grid.addWidget(sole_edit, index_interval, 2)
                    grid.addWidget(plast_status_combo, index_interval, 3)
                    grid.addWidget(template_status_combo, index_interval, 4)
                    grid.addWidget(raiding_status_combo, index_interval, 5)

                    # Переименование атрибута
                    setattr(self, f"plast_{index_interval}_edit", plast_edit)
                    setattr(self, f"roof_{index_interval}_edit", roof_edit)
                    setattr(self, f"sole_{index_interval}_edit", sole_edit)
                    setattr(self, f"plast_status_{index_interval}_edit", plast_status_combo)
                    setattr(self, f"template_status_{index_interval}_edit", template_status_combo)
                    setattr(self, f"raiding_status_{index_interval}_edit", raiding_status_combo)

                    self.labels_plast[index_interval] = (plast_edit, roof_edit, sole_edit, plast_status_combo,
                                                         template_status_combo, raiding_status_combo)
                    index_interval += 1

    def check_plast_status(self, plast):
        return 0 if self.dict_perforation[plast]['отключение'] else 1

    def check_template_status(self, plast):
        # print(self.dict_perforation[plast].keys())
        return 0 if self.dict_perforation[plast]['Прошаблонировано'] else 1

    def check_raiding_status(self, plast):
        if self.data_well.paker_before["before"] == 0:
            return 0 if self.dict_perforation[plast]['отрайбировано'] else 1
        else:
            max_sole = max(list(map(lambda x: x[1], self.dict_perforation[plast]['интервал'])))
            if (self.data_well.depth_fond_paker_before["before"] >= max_sole or \
                self.data_well.depth_fond_paker_second_before["before"] >= max_sole) and \
                    self.data_well.current_bottom > max_sole:
                return 0
            else:
                return 1


class TabWidget(TabWidgetUnion):
    def __init__(self, data_well):
        super().__init__()
        self.addTab(TabPageSo(data_well), 'Проверка корректности данных перфорации')


class PerforationCorrect(WindowUnion):

    def __init__(self, parent=None):
        super(PerforationCorrect, self).__init__(parent)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowModality(QtCore.Qt.ApplicationModal)  # Устанавливаем модальность окна

        self.tab_widget = TabWidget(self.data_well)
        self.dict_perforation_project = {}
        self.dict_perforation = self.data_well.dict_perforation

        self.buttonAdd = QPushButton('сохранить данные')
        self.buttonAdd.clicked.connect(self.add_row_table)

        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tab_widget, 0, 0, 1, 2)
        # vbox.addWidget(self.tableWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 3, 0)

    def add_row_table(self):

        plast_all = self.tab_widget.currentWidget().labels_plast

        plast_list = []
        plast_oktl = []
        plast_templ = []
        plast_raid = []
        plast_project = []
        plast_del = []
        dict_perforation_project = {}
        dict_perforation_short = {}
        dict_perforation = {}
        for index, plast_dict in plast_all.items():
            plast = plast_dict[0].text()
            roof = plast_dict[1].text()
            sole = plast_dict[2].text()
            plast_status = plast_dict[3].currentText()
            template = plast_dict[4].currentText()
            raid = plast_dict[5].currentText()
            if plast not in plast_list:
                plast_oktl = []
                plast_templ = []
                plast_raid = []
                plast_project = []

            if plast_status == 'отключен':
                plast_oktl.append(True)
            elif plast_status == 'вскрыт':
                plast_oktl.append(False)
            elif plast_status == 'проект':
                plast_project.append(plast)
            elif plast_status == 'отсутствует':
                plast_del.append(plast)

            if template == 'Прошаблонировано':
                plast_templ.append(True)
            else:
                plast_templ.append(False)

            if raid == 'отрайбировано':
                plast_raid.append(True)
            else:
                plast_raid.append(False)

            if len(plast_project) > 0:
                if plast in self.dict_perforation_project:
                    self.dict_perforation_project.setdefault(
                        plast, {}).setdefault('интервал', []).append([float(roof), float(sole)])
            else:
                if plast in self.data_well.dict_perforation:

                    if all([oktl is True for oktl in plast_oktl]):
                        dict_perforation_short.setdefault(plast, {}).setdefault('отключение', True)
                        dict_perforation.setdefault(plast, {}).setdefault('отключение', True)
                    else:
                        dict_perforation_short.setdefault(plast, {}).setdefault('отключение', False)
                        dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
                    if all([oktl is True for oktl in plast_templ]):
                        dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', True)
                        dict_perforation_short.setdefault(plast, {}).setdefault('Прошаблонировано', True)
                    else:
                        dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                        dict_perforation_short.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                    if all([oktl is True for oktl in plast_raid]):
                        dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', True)
                    else:
                        dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)

                    dict_perforation.setdefault(
                        plast, {}).setdefault('интервал', []).append([float(roof), float(sole)])
                    dict_perforation_short.setdefault(
                        plast, {}).setdefault('интервал', []).append([float(roof), float(sole)])

        for plast in list(self.data_well.dict_perforation.keys()):
            self.data_well.dict_perforation[plast]['отключение'] = dict_perforation[plast]["отключение"]
            self.data_well.dict_perforation_short[plast]['отключение'] = dict_perforation_short[plast]["отключение"]
            self.data_well.dict_perforation[plast]['интервал'] = dict_perforation[plast]["интервал"]
            self.data_well.dict_perforation_short[plast]['интервал'] = dict_perforation_short[plast]["интервал"]
            self.data_well.dict_perforation[plast]['Прошаблонировано'] = dict_perforation[plast]["Прошаблонировано"]
            self.data_well.dict_perforation_short[plast]['Прошаблонировано'] = dict_perforation_short[plast][
                "Прошаблонировано"]
            self.data_well.dict_perforation[plast]['отрайбировано'] = dict_perforation[plast]["отрайбировано"]
            # self.data_well.dict_perforation_short[plast]['отрайбировано'] = dict_perforation_short[plast]["отрайбировано"]

        if len(plast_del) > 0:
            for plast in list(self.data_well.dict_perforation.keys()):
                if plast in plast_del:
                    self.data_well.dict_perforation.pop(plast)

        definition_plast_work(self)
        self.data_well.plast_work_short = self.data_well.plast_work

        if len(self.data_well.plast_work) == 0:
            perf_true_quest = QMessageBox.question(self, 'Программа',
                                                   'Программа определили,что в скважине интервалов '
                                                   'перфорации нет, верно ли?')
            if perf_true_quest == QMessageBox.StandardButton.Yes:

                data_list.pause = False
                self.close()
                self.close_modal_forcefully()
                return
            else:

                return

        if self.data_well.paker_before["after"] not in [None, 0, '0', '-'] and \
                'отсут' not in str(self.data_well.paker_before["after"]).lower():
            check_true = self.check_depth_paker_in_perforation(self.data_well.depth_fond_paker_before["after"])
            if check_true is False:
                self.data_well.check_data_in_pz.append(f'Проверка посадки показала фондовый пакер на спуск сажается '
                                                       f'в интервал перфорации, необходимо изменить глубину посадки!!!')

        if self.data_well.paker_before["after"] not in [None, 0, '0', '-'] and \
                'отсут' not in str(self.data_well.paker_before["after"]).lower():
            check_true = self.check_depth_paker_in_perforation(self.data_well.depth_fond_paker_second_before["after"])
            if check_true is False:
                self.data_well.check_data_in_pz.append(f'Проверка посадки показала фондовый пакер на спуск сажается '
                                                       f'в интервал перфорации, необходимо изменить глубину посадки!!!')

        self.data_well.fluid = [max(data['рабочая жидкость']) for plast, data in self.dict_perforation.items()
                                if 'рабочая жидкость' in list(data.keys())]

        if self.data_well.fluid:
            self.data_well.fluid = max(self.data_well.fluid)

        data_list.pause = False
        self.close()
        self.close_modal_forcefully()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = PerforationCorrect()
    QTimer.singleShot(2000, PerforationCorrect.updateLabel)
    # window.show()
    app.exec_()
