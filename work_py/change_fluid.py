from collections import namedtuple

from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QGridLayout, QTabWidget, QMainWindow, QPushButton, \
    QMessageBox

import well_data
from H2S import calv_h2s
from main import MyMainWindow
from work_py.alone_oreration import need_h2s
from .parent_work import TabPageUnion, WindowUnion, TabWidgetUnion
from .rationingKRS import well_volume_norm


class TabPageSoChange(TabPageUnion):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.validator_int = QIntValidator(0, 600)
        self.validator_float = QDoubleValidator(0.87, 1.65, 2)

        self.need_change_zgs_label = QLabel('Расчет по новому пласту?', self)
        self.need_change_zgs_combo = QComboBox(self)
        self.need_change_zgs_combo.addItems(['Нет', 'Да'])


        self.plast_new_label = QLabel('индекс нового пласта', self)
        aaddf = self.dict_data_well["plast_project"]
        if len(self.dict_data_well["plast_project"]) != 0:
            self.plast_new_combo = QComboBox(self)
            self.plast_new_combo.addItems(self.dict_data_well["plast_project"])
        else:
            self.plast_new_combo = QLineEdit(self)

        self.fluid_new_label = QLabel('удельный вес ЖГС', self)
        self.fluid_new_edit = QLineEdit(self)
        self.fluid_new_edit.setValidator(self.validator_float)

        self.pressuar_new_label = QLabel('Ожидаемое давление', self)
        self.pressuar_new_edit = QLineEdit(self)
        self.pressuar_new_edit.setValidator(self.validator_int)

        self.type_absorbent_label = QLabel('Тип поглотителя')
        self.type_absorbent = QComboBox()
        self.type_absorbent.addItems(['EVASORB марки 121', 'СНПХ-1200', 'ХИМТЕХНО 101 Марка А'])

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.type_absorbent_label, 2, 1)
        self.grid.addWidget(self.type_absorbent, 3, 1)

        self.grid.addWidget(self.need_change_zgs_label, 3, 2)
        self.grid.addWidget(self.need_change_zgs_combo, 4, 2)

        # self.grid.addWidget(self.plast_new_label, 3, 3)
        # self.grid.addWidget(self.plast_new_combo, 4, 3)
        #
        self.grid.addWidget(self.fluid_new_label, 3, 4)
        self.grid.addWidget(self.fluid_new_edit, 4, 4)
        #
        # self.grid.addWidget(self.pressuar_new_label, 3, 5)
        # self.grid.addWidget(self.pressuar_new_edit, 4, 5)
        self.need_change_zgs_combo.currentTextChanged.connect(self.update_change_fluid)

        self.need_change_zgs_combo.setCurrentIndex(1)

    def update_change_fluid(self, index):
        if index == 'Да':
            cat_h2s_list_plan = list(
                map(int, [self.dict_data_well["dict_category"][plast]['по сероводороду'].category for plast in
                          self.dict_data_well["plast_project"] if self.dict_data_well["dict_category"].get(plast) and
                          self.dict_data_well["dict_category"][plast]['отключение'] == 'планируемый']))

            if len(cat_h2s_list_plan) == 0:
                self.category_pressuar_Label = QLabel('По Рпл')
                self.category_pressuar_line_combo = QComboBox(self)
                self.category_pressuar_line_combo.addItems(['1', '2', '3'])
                self.category_h2s_Label = QLabel('По H2S')
                self.category_h2s_edit = QComboBox(self)
                self.category_h2s_edit.addItems(['2', '1', '3'])
                self.h2s_pr_label = QLabel('значение H2s в %')
                self.h2s_pr_edit = QLineEdit(self)
                self.h2s_pr_edit.setValidator(self.validator_float)
                self.h2s_mg_label = QLabel('значение H2s в мг/л')
                self.h2s_mg_edit = QLineEdit(self)
                self.h2s_mg_edit.setValidator(self.validator_float)
                self.category_Label = QLabel('По газовому фактору')
                self.dict_data_well["category_gf"] = QComboBox(self)
                self.dict_data_well["category_gf"].addItems(['2', '1', '3'])
                self.gf_label = QLabel('Газовый фактор')
                self.gf_edit = QLineEdit(self)
                self.gf_edit.setValidator(self.validator_float)
                self.h2s_mg_edit.textChanged.connect(self.update_calculate_h2s)
                self.h2s_pr_edit.textChanged.connect(self.update_calculate_h2s)
                self.gf_edit.textChanged.connect(self.update_calculate_h2s)

                self.calc_h2s_Label = QLabel('расчет поглотителя H2S по вскрываемому пласту')
                self.calc_plast_h2s = QLineEdit(self)

                self.grid.addWidget(self.category_pressuar_Label, 11, 2)
                self.grid.addWidget(self.category_pressuar_line_combo, 12, 2)

                self.grid.addWidget(self.category_h2s_Label, 11, 3)
                self.grid.addWidget(self.category_h2s_edit, 12, 3)

                self.grid.addWidget(self.h2s_pr_label, 13, 3)
                self.grid.addWidget(self.h2s_pr_edit, 14, 3)

                self.grid.addWidget(self.h2s_mg_label, 15, 3)
                self.grid.addWidget(self.h2s_mg_edit, 16, 3)

                self.grid.addWidget(self.category_Label, 11, 4)
                self.grid.addWidget(self.dict_data_well["category_gf"], 12, 4)

                self.grid.addWidget(self.gf_label, 13, 4)
                self.grid.addWidget(self.gf_edit, 14, 4)

                self.grid.addWidget(self.calc_h2s_Label, 11, 5)
                self.grid.addWidget(self.calc_plast_h2s, 12, 5)

            # if len(self.dict_data_well["plast_project"]) != 0:
            #     self.plast_new_combo = QComboBox(self)
            #     self.plast_new_combo.addItems(self.dict_data_well["plast_project"])
            #     plast = self.plast_new_combo.currentText()
            # else:
            #     self.plast_new_combo = QLineEdit(self)
            #     plast = self.plast_new_combo.text()

            # if len(cat_h2s_list_plan) != 0:
            #     self.pressuar_new_edit.setText(f'{self.dict_data_well["dict_category"][plast]["по давлению"].data_pressuar}')

            self.grid.addWidget(self.plast_new_label, 9, 2)
            self.grid.addWidget(self.plast_new_combo, 10, 2)

            self.grid.addWidget(self.pressuar_new_label, 9, 4)
            self.grid.addWidget(self.pressuar_new_edit, 10, 4)
        else:
            try:
                self.category_pressuar_Label.setParent(None)
                self.category_pressuar_line_combo.setParent(None)

                self.category_h2s_Label.setParent(None)
                self.category_h2s_edit.setParent(None)

                self.h2s_pr_label.setParent(None)
                self.h2s_pr_edit.setParent(None)

                self.h2s_mg_label.setParent(None)
                self.h2s_mg_edit.setParent(None)

                self.category_Label.setParent(None)
                self.dict_data_well["category_gf"].setParent(None)
                self.calc_plast_h2s.setParent(None)

                self.gf_label.setParent(None)
                self.gf_edit.setParent(None)

                self.calc_h2s_Label.setParent(None)

                self.plast_new_label.setParent(None)
                self.plast_new_combo.setParent(None)

                self.pressuar_new_label.setParent(None)
                self.pressuar_new_edit.setParent(None)
            except:
                pass

    def update_calculate_h2s(self):
        if self.category_h2s_edit.currentText() in ['3', 3]:
            self.calc_plast_h2s.setText('0')
        else:
            if self.h2s_mg_edit.text() != '' and self.h2s_pr_edit.text() != '':
                self.calc_plast_h2s.setText(str(calv_h2s(self, self.category_h2s_edit.currentText(),
                                                         float(self.h2s_mg_edit.text().replace(',', '.')),
                                                         float(self.h2s_pr_edit.text().replace(',', '.')))))


class TabWidget(TabWidgetUnion):
    def __init__(self, parent=None):
        super().__init__()
        self.addTab(TabPageSoChange(parent), 'Смена объема')


class Change_fluid_Window(WindowUnion):
    def __init__(self, dict_data_well, table_widget, parent=None):
        super().__init__(dict_data_well)

        self.ins_ind = dict_data_well['ins_ind']
        self.tabWidget = TabWidget(self.dict_data_well)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_widget = table_widget

        self.dict_nkt = {}

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        currentWidget = self.tabWidget.currentWidget()
        self.need_change_zgs_combo = currentWidget.need_change_zgs_combo.currentText()
        self.dict_data_well["type_absorbent"] = self.tabWidget.currentWidget().type_absorbent.currentText()
        fluid_new_edit = currentWidget.fluid_new_edit.text().replace(',', '.')
        if fluid_new_edit == '':
            QMessageBox.information(self, 'Ошибка', 'Не введен расчетный уд.вес')
            return
        else:
            fluid_new_edit = round(float(fluid_new_edit), 2)
        if self.need_change_zgs_combo == 'Да':
            if self.dict_data_well["plast_project"]:
                plast_new_combo = currentWidget.plast_new_combo.currentText()
            else:
                plast_new_combo = currentWidget.plast_new_combo.text()

            pressuar_new_edit = float(self.tabWidget.currentWidget().pressuar_new_edit.text())

            if (plast_new_combo == '' or fluid_new_edit == '' or pressuar_new_edit == ''):
                mes = QMessageBox.critical(self, 'Ошибка', 'Введены не все параметры')
                return
            if fluid_new_edit > 1.65 or fluid_new_edit < 0.87:
                mes = QMessageBox.critical(self, 'Ошибка', 'Жидкость не может быть данным удельным весом')
                return
            if pressuar_new_edit < 10 == False:
                mes = QMessageBox.critical(self, 'Ошибка', 'Ожидаемое давление слишком низкое')
                return

            if len(self.dict_data_well["plast_project"]) != 0:
                plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.currentText()
            else:
                plast_new_combo = self.tabWidget.currentWidget().plast_new_combo.text()

                self.dict_data_well["dict_category"].setdefault(plast_new_combo, {}).setdefault('отключение',
                                                                                                False)
                self.dict_data_well["plast_project"].append(plast_new_combo)

            pressuar_new_edit = self.tabWidget.currentWidget().pressuar_new_edit.text()

            if pressuar_new_edit != '':
                pressuar_new_edit = int(float(pressuar_new_edit.replace(',', '.')))

            aassdaad = self.dict_data_well["dict_category"]

            if self.dict_data_well["dict_category"][plast_new_combo]['отключение'] != 'планируемый':
                h2s_pr_edit = self.tabWidget.currentWidget().h2s_pr_edit.text().replace(',', '.')
                h2s_mg_edit = self.tabWidget.currentWidget().h2s_mg_edit.text().replace(',', '.')
                gf_edit = self.tabWidget.currentWidget().gf_edit.text().replace(',', '.')
                calc_plast_h2s = self.tabWidget.currentWidget().calc_plast_h2s.text()
                if h2s_pr_edit != '' and h2s_mg_edit and gf_edit != '' and calc_plast_h2s != '' and pressuar_new_edit != '':

                    asdwd = self.dict_data_well["dict_category"]

                    Pressuar = namedtuple("Pressuar", "category data_pressuar")
                    Data_h2s = namedtuple("Data_h2s", "category data_procent data_mg_l poglot")
                    Data_gaz = namedtuple("Data_gaz", "category data")

                    category_pressuar_line_combo = self.tabWidget.currentWidget().category_pressuar_line_combo.currentText()
                    category_h2s_edit = self.tabWidget.currentWidget().category_h2s_edit.currentText()

                    self.dict_data_well["category_gf"] = self.tabWidget.currentWidget().dict_data_well[
                        "category_gf"].currentText()
                    gf_edit = self.tabWidget.currentWidget().gf_edit.text().replace(',', '.')

                    self.dict_data_well["dict_category"].setdefault(plast_new_combo, {}).setdefault(
                        'по давлению',
                        Pressuar(int(float(category_pressuar_line_combo)),
                                 float(pressuar_new_edit)))

                    self.dict_data_well["dict_category"].setdefault(plast_new_combo, {}).setdefault(
                        'по сероводороду', Data_h2s(
                            int(float(category_h2s_edit)),
                            float(h2s_pr_edit.replace(',', '.')),
                            float(h2s_mg_edit.replace(',', '.')),
                            float(calc_plast_h2s.replace(',', '.'))))

                    self.dict_data_well["dict_category"].setdefault(plast_new_combo, {}).setdefault(
                        'по газовому фактору', Data_gaz(
                            int(self.dict_data_well["category_gf"]),
                            float(gf_edit)))
                    try:
                        self.dict_data_well["dict_category"][plast_new_combo]['отключение'] = 'планируемый'
                    except:
                        self.dict_data_well["dict_category"].setdefault(plast_new_combo, {}).setdefault(
                            'отключение', 'планируемый')
                else:
                    return

        if self.need_change_zgs_combo == 'Да':
            work_list = self.fluid_change(plast_new_combo, fluid_new_edit, pressuar_new_edit)
        else:
            work_list = self.fluid_change_old_plast(fluid_new_edit)
        self.populate_row(self.ins_ind, work_list, self.table_widget)
        well_data.pause = False
        self.close()

    def closeEvent(self, event):
        # Закрываем основное окно при закрытии окна входа
        self.operation_window = None
        event.accept()  # Принимаем событие закрытия

    def fluid_change_old_plast(self, fluid_new_edit):
        from work_py.alone_oreration import well_volume, update_fluid
        fluid_work = str(fluid_new_edit) + self.dict_data_well["fluid_work"][4:]
        self.dict_data_well["fluid_work_short"] = str(fluid_new_edit) + self.dict_data_well["fluid_work_short"][4:]

        fluid_change_list = [
            [
                f'Cмена объема {self.dict_data_well["fluid_work_short"]}- {round(well_volume(self, self.dict_data_well["current_bottom"]), 1)}м3',
                None,
                f'Произвести смену объема обратной промывкой по круговой циркуляции  жидкостью  {fluid_work} '
                f' в объеме не '
                f'менее {round(well_volume(self, self.dict_data_well["current_bottom"]), 1)}м3  в присутствии '
                f'представителя заказчика, Составить акт. '
                f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за '
                f'2 часа до начала работ)',
                None, None, None, None, None, None, None,
                'мастер КРС', well_volume_norm(well_volume(self, self.dict_data_well["current_bottom"]))]]

        update_fluid(self, self.dict_data_well["ins_ind"], fluid_work, self.table_widget)
        self.dict_data_well["fluid_work"] = fluid_work
        return fluid_change_list

    def fluid_change(self, plast_new, fluid_new, pressuar_new):
        from work_py.alone_oreration import well_volume, update_fluid

        fluid_work, self.dict_data_well["fluid_work_short"], plast, expected_pressure = need_h2s(self, fluid_new,
                                                                                                 plast_new,
                                                                                                 pressuar_new)

        fluid_change_list = [
            [
                f'Cмена объема {self.dict_data_well["fluid_work_short"]}-{round(well_volume(self, self.dict_data_well["current_bottom"]), 1)}м3',
                None,
                f'Произвести смену объема обратной промывкой по круговой циркуляции  жидкостью  {fluid_work} '
                f'(по расчету по вскрываемому пласта Рожид- {expected_pressure}атм) в объеме не '
                f'менее {round(well_volume(self, self.dict_data_well["current_bottom"]), 1)}м3  в присутствии '
                f'представителя заказчика, Составить акт. '
                f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за '
                f'2 часа до начала работ)',
                None, None, None, None, None, None, None,
                'мастер КРС', well_volume_norm(well_volume(self, self.dict_data_well["current_bottom"]))]]

        update_fluid(self, self.dict_data_well["ins_ind"], fluid_work, self.table_widget)
        self.dict_data_well["fluid_work"] = fluid_work
        return fluid_change_list
