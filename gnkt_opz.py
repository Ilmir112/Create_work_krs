from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QMainWindow, QTabWidget, QLabel, QLineEdit, QComboBox, \
    QGridLayout, QWidget, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets

import well_data
from cdng import events_gnvp_frez
from krs import GnoWindow
from main import MyMainWindow
from work_py.acid_paker import CheckableComboBox, AcidPakerWindow
from gnkt_data import gnkt_data
from collections import namedtuple

from work_py.gnkt_grp_work import GnktModel


class TabPage_gnkt(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0, 8000, 1)
        # self.gnkt_number_label = QLabel('Номер ГНКТ')
        # self.gnkt_number_combo = QComboBox(self)
        # self.gnkt_number_combo.addItems(['ГНКТ №2', 'ГНКТ №1'])

        self.roof_label = QLabel("кровля пласта", self)
        self.roof_edit = QLineEdit(self)
        self.roof_edit.setText(f'{well_data.perforation_roof}')
        self.roof_edit.setValidator(self.validator_float)

        self.sole_label = QLabel("подошва пласта", self)
        self.sole_edit = QLineEdit(self)
        self.sole_edit.setText(f'{well_data.perforation_sole}')
        self.sole_edit.setValidator(self.validator_float)
        plast_work = ['']
        plast_work.extend(well_data.plast_work)

        self.plast_label = QLabel("Выбор пласта", self)
        self.plast_combo = CheckableComboBox(self)
        self.plast_combo.combo_box.addItems(plast_work)
        # self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

        self.need_rast_label = QLabel("необходимость растворителя", self)
        self.need_rast_combo = QComboBox(self)
        self.need_rast_combo.addItems(['нужно', 'не нужно'])

        self.volume_rast_label = QLabel("Объем растворителя", self)
        self.volume_rast_edit = QLineEdit(self)
        self.volume_rast_edit.setText('2')
        self.volume_rast_edit.setValidator(self.validator_int)

        self.skv_true_label_type = QLabel("необходимость кислотной ванны", self)
        self.svk_true_combo = QComboBox(self)
        self.svk_true_combo.addItems(['Нужно СКВ', 'без СКВ'])
        self.svk_true_combo.setCurrentIndex(1)
        self.svk_true_combo.setProperty('value', 'без СКВ')

        self.skv_acid_label_type = QLabel("Вид кислоты для СКВ", self)
        self.skv_acid_edit = QComboBox(self)
        self.skv_acid_edit.addItems(['HCl', 'HF'])
        self.skv_acid_edit.setCurrentIndex(0)
        self.skv_acid_edit.setProperty('value', 'HCl')

        self.skv_volume_label = QLabel("Объем СКВ", self)
        self.skv_volume_edit = QLineEdit(self)
        self.skv_volume_edit.setValidator(self.validator_float)
        self.skv_volume_edit.setText('1')
        self.skv_volume_edit.setClearButtonEnabled(True)

        self.skv_proc_label = QLabel("Концентрация СКВ", self)
        self.skv_proc_edit = QLineEdit(self)
        self.skv_proc_edit.setClearButtonEnabled(True)
        self.skv_proc_edit.setText('15')
        self.skv_proc_edit.setValidator(self.validator_int)

        self.acid_label = QLabel("необходимость кислотной обработки", self)
        self.acid_true_edit = QComboBox(self)
        self.acid_true_edit.addItems(['нужно', 'не нужно'])

        self.acid_label_type = QLabel("Вид кислотной обработки", self)
        self.acid_edit = QComboBox(self)
        self.acid_edit.addItems(['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка'])
        self.acid_edit.setCurrentIndex(0)

        self.acid_volume_label = QLabel("Объем кислотной обработки", self)
        self.acid_volume_edit = QLineEdit(self)
        self.acid_volume_edit.setValidator(self.validator_float)
        self.acid_volume_edit.setText("10")
        self.acid_volume_edit.setClearButtonEnabled(True)

        self.acid_proc_label = QLabel("Концентрация кислоты", self)
        self.acid_proc_edit = QLineEdit(self)
        self.acid_proc_edit.setText('15')
        self.acid_proc_edit.setClearButtonEnabled(True)
        self.acid_proc_edit.setValidator(self.validator_int)

        self.pressure_Label = QLabel("Давление закачки", self)
        self.pressure_edit = QLineEdit(self)
        self.pressure_edit.setText(f'{well_data.max_admissible_pressure._value}')
        self.pressure_edit.setValidator(self.validator_int)



        self.grid = QGridLayout(self)
        # grid.addWidget(self.gnkt_number_label, 0, 0)
        # grid.addWidget(self.gnkt_number_combo, 1, 0)
        self.grid.addWidget(self.plast_label, 0, 1)
        self.grid.addWidget(self.plast_combo, 1, 1)
        self.grid.addWidget(self.roof_label, 0, 2)
        self.grid.addWidget(self.roof_edit, 1, 2)
        self.grid.addWidget(self.sole_label, 0, 3)
        self.grid.addWidget(self.sole_edit, 1, 3)

        self.grid.addWidget(self.need_rast_label, 2, 0)
        self.grid.addWidget(self.need_rast_combo, 3, 0)
        self.grid.addWidget(self.volume_rast_label, 2, 1)
        self.grid.addWidget(self.volume_rast_edit, 3, 1)

        self.grid.addWidget(self.skv_true_label_type, 4, 0)
        self.grid.addWidget(self.svk_true_combo, 5, 0)
        self.grid.addWidget(self.skv_acid_label_type, 4, 1)
        self.grid.addWidget(self.skv_acid_edit, 5, 1)
        self.grid.addWidget(self.skv_volume_label, 4, 2)
        self.grid.addWidget(self.skv_volume_edit, 5, 2)
        self.grid.addWidget(self.skv_proc_label, 4, 3)
        self.grid.addWidget(self.skv_proc_edit, 5, 3)

        self.grid.addWidget(self.acid_label, 6, 0)
        self.grid.addWidget(self.acid_true_edit, 7, 0)

        self.grid.addWidget(self.acid_label_type, 6, 1)
        self.grid.addWidget(self.acid_edit, 7, 1)
        self.grid.addWidget(self.acid_volume_label, 6, 2)
        self.grid.addWidget(self.acid_volume_edit, 7, 2)
        self.grid.addWidget(self.acid_proc_label, 6, 3)
        self.grid.addWidget(self.acid_proc_edit, 7, 3)
        # grid.addWidget(self.acidOilProcLabel, 4, 4)
        # grid.addWidget(self.acidOilProcEdit, 5, 4)
        self.grid.addWidget(self.pressure_Label, 6, 5)
        self.grid.addWidget(self.pressure_edit, 7, 5)

        self.grid.addWidget(self.pressure_Label, 6, 5)
        self.grid.addWidget(self.pressure_edit, 7, 5)

        self.svk_true_combo.currentTextChanged.connect(self.update_skv_edit)
        self.svk_true_combo.setCurrentIndex(0)
        self.svk_true_combo.setCurrentIndex(1)
        self.acid_edit.currentTextChanged.connect(self.update_sko_type)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)

    def update_skv_edit(self, index):
        if index == 'Нужно СКВ':
            self.grid.addWidget(self.skv_acid_label_type, 4, 1)
            self.grid.addWidget(self.skv_acid_edit, 5, 1)
            self.grid.addWidget(self.skv_volume_label, 4, 2)
            self.grid.addWidget(self.skv_volume_edit, 5, 2)
            self.grid.addWidget(self.skv_proc_label, 4, 3)
            self.grid.addWidget(self.skv_proc_edit, 5, 3)
        else:
            self.skv_acid_label_type.setParent(None)
            self.skv_acid_edit.setParent(None)
            self.skv_volume_label.setParent(None)
            self.skv_volume_edit.setParent(None)
            self.skv_proc_label.setParent(None)
            self.skv_proc_edit.setParent(None)

    def update_plast_edit(self):

        dict_perforation = well_data.dict_perforation
        plasts = well_data.texts
        # print(f'пласты {plasts, len(well_data.texts), len(plasts), well_data.texts}')
        roof_plast = well_data.current_bottom
        sole_plast = 0
        for plast in well_data.plast_work:
            for plast_sel in plasts:
                if plast_sel == plast:
                    if roof_plast >= dict_perforation[plast]['кровля']:
                        roof_plast = dict_perforation[plast]['кровля']
                    if sole_plast <= dict_perforation[plast]['подошва']:
                        sole_plast = dict_perforation[plast]['подошва']
        self.roof_edit.setText(f'{roof_plast}')
        self.sole_edit.setText(f'{sole_plast}')

    def update_sko_type(self, type_sko):
        self.sko_vt_label = QLabel('Высокотехнологическое СКО', self)
        self.sko_vt_edit = QLineEdit(self)
        if type_sko == 'ВТ':
            self.grid.addWidget(self.sko_vt_label, 6, 6)
            self.grid.addWidget(self.sko_vt_edit, 7, 6)
        else:
            self.sko_vt_label.setParent(None)
            self.sko_vt_edit.setParent(None)


class TabWidget(QTabWidget):
    def __init__(self, tableWidget):
        super().__init__()
        self.addTab(TabPage_gnkt(tableWidget), 'ГНКТ ОПЗ')


class GnktOpz(GnktModel):
    def __init__(self, table_widget, fluid_edit, parent=None):

        super(GnktOpz, self).__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.work_plan = 'gnkt_opz'
        self.paker_select = None

        self.tableWidget = QTableWidget(0, 7)
        self.tabWidget = TabWidget(self.tableWidget)

        self.tableWidget.setHorizontalHeaderLabels(
            ["Пласт",  'кровля', 'Подошва', 'СКВ', "вид кислоты", "процент", "объем"])

        self.buttonAddString = QPushButton('Добавить обработку')
        self.buttonAddString.clicked.connect(self.addString)

        self.fluid_edit = fluid_edit

        self.table_widget = table_widget

        self.dict_nkt = {}

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        self.buttonDel = QPushButton('Удалить записи из таблице')
        self.buttonDel.clicked.connect(self.del_row_table)
        self.buttonAddString = QPushButton('Добавить обработку')
        self.buttonAddString.clicked.connect(self.addString)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAddString, 2, 0)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.tableWidget, 1, 0, 1, 2)

        vbox.addWidget(self.buttonDel, 2, 1)
        vbox.addWidget(self.buttonAdd, 3, 0, 1, 0)


    def del_row_table(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            QMessageBox.information(self, 'Внимание', 'Выберите строку для удаления')
            return
        self.tableWidget.removeRow(row)
    def add_work(self):

        self.current_widget = self.tabWidget.currentWidget()

        try:
            self.need_rast_combo = self.current_widget.need_rast_combo.currentText()
            self.volume_rast_edit = float(self.current_widget.volume_rast_edit.text())
            self.skv_volume_edit = float(self.current_widget.skv_volume_edit.text().replace(',', '.'))
            self.skv_proc_edit = int(self.current_widget.skv_proc_edit.text().replace(',', '.'))
            self.svk_true_combo = str(self.current_widget.svk_true_combo.currentText())
            self.skv_acid_edit = str(self.current_widget.skv_acid_edit.currentText())
            # self.distance_pntzh = self.current_widget.distance_pntzh_edit.text()
            self.acid_true_edit = self.current_widget.acid_true_edit.currentText()
            self.update_opz_data(self.current_widget)


        except Exception as e:
            QMessageBox.warning(self, 'Ошибка', f'ВВедены не корректные данные {type(e).__name__}\n\n{str(e)}')
        if self.roof_plast in ['', None, 0] or self.sole_plast in ['', None, 0]:
            mes = QMessageBox.critical(self, "Ошибка", "Не введены данные по кровле и ли подошве обработки")
            return

        if self.acid_edit == 'ВТ':
            self.vt = self.tabWidget.currentWidget().sko_vt_edit.text()
            if self.vt == '':
                QMessageBox.critical(self, "Ошибка", "Нужно расписать объемы и вид кислоты")
                return



        well_data.pause = False
        self.close()

    def addString(self):

        roof_plast = float(self.tabWidget.currentWidget().roof_edit.text().replace(',', '.'))
        sole_plast = float(self.tabWidget.currentWidget().sole_edit.text().replace(',', '.'))

        plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())


        acid_edit_list = ['HCl', 'HF', 'ВТ', 'лимонная кислота']
        acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()
        acid_edit_combo = QComboBox(self)
        acid_edit_combo.addItems(acid_edit_list)
        acid_edit_combo.setCurrentIndex(acid_edit_list.index(acid_edit))
        self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.')
        acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
        acid_proc_edit = int(float(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.')))
        svk_true_combo_str = self.tabWidget.currentWidget().svk_true_combo.currentText()


        svk_true_combo = QComboBox(self)
        svk_true_list = ['Нужно СКВ', 'без СКВ']
        svk_true_combo.addItems(svk_true_list)
        svk_true_combo.setCurrentIndex(svk_true_list.index(svk_true_combo_str))

        if not plast_combo or not acid_edit or not acid_volume_edit or not acid_proc_edit:
            QMessageBox.information(self, 'Внимание', 'Заполните данные по объему')
            return



        self.tableWidget.setSortingEnabled(False)
        rows = self.tableWidget.rowCount()

        self.tableWidget.insertRow(rows)
        self.tableWidget.setItem(rows, 0, QTableWidgetItem(plast_combo))

        self.tableWidget.setItem(rows, 1, QTableWidgetItem(str(roof_plast)))
        self.tableWidget.setItem(rows, 2, QTableWidgetItem(str(sole_plast)))
        self.tableWidget.setCellWidget(rows, 3, svk_true_combo)
        self.tableWidget.setCellWidget(rows, 4, acid_edit_combo)
        self.tableWidget.setItem(rows, 5, QTableWidgetItem(str(acid_proc_edit)))
        self.tableWidget.setItem(rows, 6, QTableWidgetItem(str(acid_volume_edit)))



    def gnkt_work_opz(self, data_gnkt):

        rows = self.tableWidget.rowCount()

        if rows == 0:
            QMessageBox.warning(self, "ВНИМАНИЕ", 'Нужно добавить интервалы обработки')
            return
        acid_info = []

        interval_sko = ''
        for row in range(rows):

            plast_combo = self.tableWidget.item(row, 0).text()

            roof_plast = self.tableWidget.item(row, 1).text()
            sole_plast = self.tableWidget.item(row, 2).text()
            svk_true_combo = self.tableWidget.cellWidget(row, 3).currentText()
            acid_edit = self.tableWidget.cellWidget(row, 4).currentText()
            acid_proc_edit = int(float(self.tableWidget.item(row, 5).text()))
            acid_volume_edit = round(float(self.tableWidget.item(row, 6).text()), 1)
            acid_info.append([plast_combo, svk_true_combo, roof_plast , sole_plast, acid_edit,acid_proc_edit, acid_volume_edit])
            interval_sko += f'{roof_plast}-{sole_plast}, '



        block_gnvp_list = events_gnvp_frez(data_gnkt.distance_pntzh, float(data_gnkt.fluid_edit))

        if self.acid_true_edit == "нужно":
            acid_true_quest = True
        else:
            acid_true_quest = False

        well_data.fluid_work, well_data.fluid_work_short = GnoWindow.calc_work_fluid(self.fluid_edit)

        if self.need_rast_combo == 'нужно':
            volume_rast_edit = self.volume_rast_edit

        depth_fond_paker_do = sum(map(int, list(well_data.dict_nkt.values())))
        if well_data.depth_fond_paker_do["do"] == 0:
            self.depth_fond_paker_do = sum(list(well_data.dict_nkt.values()))
            # print(depth_fond_paker_do)
            if self.depth_fond_paker_do >= well_data.current_bottom:
                depth_fond_paker_do, ok = QInputDialog.getDouble(self, 'глубина НКТ',
                                                                 'Введите Глубины башмака НКТ', 500,
                                                                 0, well_data.current_bottom)
        else:
            self.depth_fond_paker_do= well_data.depth_fond_paker_do["do"]

        gnkt_opz = [
            [None, 'Порядок работы', None, None, None, None, None, None, None, None, None, None],
            [None, 'п/п', 'Наименование работ', None, None, None, None, None, None, None,
             'Ответственный', 'Нормы'],
            [None, 1,
             'ВНИМАНИЕ: Перед спуском и вовремя проведения СПО бурильщикам и мастеру производить осмотр '
              'ГНКТ на наличие '
              '"меток" на г/трубы, установленных запрещённым способом.\nПри обнаружении - доложить руководству'
              f' {well_data.contractor}'
              'по согласованию произвести отрезание ГНКТ выше "метки" с составлением АКТа и указанием метража '
              'отрезанного участка ГНКТ. '
              'Установку меток на г/трубе производить ТОЛЬКО безопасным способом - (краской, лентой фум, '
              'шкемарём, и тд.) '
              'КАТЕГОРИЧЕСКИ ЗАПРЕЩАЕТСЯ устанавливать "метки" опасным способом - вальцевателем (труборезом) или '
              'другим инструментом - '
              'который причиняет механические повреждения на теле г/трубы и может привести к снижению прочностных '
              'характеристик ГНКТ. '
              'Запросить у Заказчика внутренние диаметры спущенной компоновки для исключения заклинивания низа'
              ' компоновки',
             None, None, None, None, None, None, None,
             'Мастер КРС,бурильщик', None],
            [None, 1, 'Провести приемку скважины в ремонт у Заказчика с составлением акта. Переезд бригады КРС '
                      'на скважину. '
                      'Подготовительные работы к КРС. Расставить технику и оборудование.Составить Акт .',
             None, None, None, None, None, None, None, 'Мастер КРС, представитель Заказчика', 'расчет нормы на '
                                                                                              'переезд '],
            [None, 1, 'Провести инструктаж по предупреждению ГНВП и ОФ при КРС, а также по плану ликвидации '
                      'аварий при '
                      'производстве работ с записью в журнале (инструктаж, в обязательном порядке, проводить '
                      'с обеими вахтами бригады).',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 3,
             'Мастеру бригады - запретить бурильщикам оставлять устье скважины незагерметизированным независимо '
             'от продолжительности перерывов в работе.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 4, 'Проводить замеры газовоздушной среды согласно утвержденного графика',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 7,
             'Все операции при производстве выполнять в соответствии с технологической инструкцией, '
             'федеральных норм и правила в области промышленной безопасности "Правила безопасности в '
             'нефтяной и газовой промышленности" '
             'от 15.12.2020г и РД 153-39-023-97.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 8,
             f'Произвести монтаж колтюбингового оборудования согласно утверждённой схемы №5 '
             f'{well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г '
             f'("Обвязки устья '
             f'при глушении скважин, после проведения гидроразрыва пласта и работы на скважинах ППД с оборудованием'
             f' койлтюбинговых установок на месторождениях ООО "Башнефть-Добыча") превентором ППК 80х35 '
             f'(4-х секционный превентор БП 80-70.00.00.000 (700атм)) №{well_data.pvo_number} и инжектором. '
             f'РАБОТЫ ПО МОНТАЖУ КОЛТЮБИНГОВОЙ УСТАНОВКИ'
             ' В СООТВЕТСТВИИ С ТЕХНОЛОГИЧЕСКОЙ ИНСТРУКЦИЕЙ, ФЕДЕРАЛЬНЫХ НОРМ И ПРАВИЛА В ОБЛАСТИ ПРОМЫШЛЕННОЙ '
             'БЕЗОПАСНОСТИ «ПРАВИЛА БЕЗОПАСНОСТИ В НЕФТЯНОЙ И ГАЗОВОЙ ПРОМЫШЛЕННОСТИ»  РОСТЕХНАДЗОР '
             'ПРИКАЗ №1 ОТ 15.12.2020Г И РД 153-39-023-97.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, бур-к КРС, машинист подъёмника, пред. УСРСиСТ', 3.5],
            [None, 9, 'Пусковой комиссии в составе мастера и членов бригады согласно положения от 2015г.'
                      '"Положение о проведении пусковой комиссии при ТКРС" произвести проверку готовности бригады '
                      'для ремонта скважины с последующим составлением акта.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, бур-к КРС, машинист подъёмника, пред. УСРСиСТ', 0.5],
            [None, 10,
             f'Перед началом опрессовки принять все требуемые меры безопасности. Подготовиться к опрессовке.'
                   f' Удостовериться в том, рабочая зона вокруг линий высокого давления обозначена знаками '
                   f'безопосности.'
                   f' Запустить систему регистрации СОРП. Оповестить всех людей на кустовой площадке о проведении '
                   f'опрессовки.'
                   f' Опрессовать все нагнетательные линии на {min(225, well_data.max_admissible_pressure._value * 1.5)}атм. '
                   f'Опрессовать  выкидную линию '
                   f'от устья скважины до желобной ёмкости на '
                   f'{min(225, round(well_data.max_admissible_pressure._value * 1.5, 1))}атм c выдержкой 30мин'
                   f'(надёжно закрепить, оборудовать дроссельными задвижками)',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, представ.БВО (вызов по телефонограмме при необходимости)', 'факт'],
            [None, 11,
             f'При закрытой центральной задвижке фондовой арматуры. Опрессовать превентор, глухие и трубные  '
               f'плашки на '
               f'устье скважины на Р={well_data.max_admissible_pressure._value}атм с выдержкой 30 мин (опрессовку ПВО '
               f'зафиксировать'
               f' в вахтовом журнале). Оформить соответствующий акт в присутствии представителя Башкирского '
               f'военизированного '
               f'отряда с выдачей разрешения на дальнейшее проведение работ (вызов представителя БВО по '
               f'телефонограмме за 24 '
               f'часа). Провести учебно-тренировочное занятие по сигналу "Выброс" с записью в журнале.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, представ.БВО (вызов по телефонограмме при необходимости)', 0.47],
            [None, 'СПУСК КНК И ОБРАБОТКА РАСТВОРИТЕЛЕМ',
             None, None, None, None, None, None, None, None,
             'Мастер ГНКТ, представитель Заказчика', None],
            [None, 12,
             f'Произвести спуск БДТ + насадка 5 каналов до {well_data.current_bottom}м (забой) с промывкой скважины '
             f'мин.водой уд.веса {well_data.fluid_work} с фиксацией давления промывки, расход жидкости не менее 200л\\мин, объем '
             f'промывки не менее 1 цикла  со скоростью 5м/мин. Убедиться в наличии свободного прохода КНК-2 (при '
             f'прохождении насадкой лубрикаторной задвижки, пакера, воронки скорость спуска минимальная 2м/мин). При '
             f'посадке ГНКТ в колонне НКТ произвести закачку (на циркуляции) растворителя в объёме 0,2 м3 в ГНКТ. '
             f'Произвести продавку (на циркуляции) растворителя АСПО до башмака ГНКТ мин.водой уд.вес {well_data.fluid_work} '
             f'в объёме 2,0м3. Закрыть Кран на тройнике устьевого оборудования. '
             f'{"Стоянка на реакции 2 часа." if well_data.region != "ТГМ" and acid_info[0][3] != "HF" else "без реагирования"}'
             f' Промывка колонны '
             f'НКТ - не менее1 цикла. Составить Акт. Промывка подвески ФНКТ по согласованию ПТО и ЦДНГ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, представитель Заказчика', 2.04],
            [f'Промыть НКТ и скважину с гл.{well_data.current_bottom}м',
             13, f'Промыть НКТ и скважину с гл.{well_data.current_bottom}м мин.водой уд.веса {well_data.fluid_work}  в 1 цикл'
                 f' с добавлением 1т растворителя с составлением соответствующего акта. При появлении затяжек или '
                 f'посадок при спуско-подъемных операциях произвести интенсивную промывку '
                 f'осложненного участка скважины. ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представит. Заказчика', 0.84],
            [f'обработку НКТ {volume_rast_edit}м3 растворителя',
             14, f'Произвести обработку НКТ {volume_rast_edit}м3 растворителя в присутствии'
                 f' представителя Заказчика при открытом'
                 f' малом затрубном пространстве на циркуляции. Произвести продавку растворителя АСПО до '
                 f'башмака ГНКТ '
                 f'мин.водой уд.вес {well_data.fluid_work} в объёме 2,2м3 не превышая давления закачки не более  '
                 f'Р={well_data.max_admissible_pressure._value}атм. ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', 1.92],
            [None, 15,
             f'Приподнять БДТ до {int(depth_fond_paker_do) - 20}м. Произвести круговую циркуляцию растворителя в '
             f'течении 2часов. Составить Акт',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 2.06],
            [None, 'ГИДРОСВАБИРОВАНИЕ И ОПРЕДЕЛЕНИЕ ПРИЕМИСТОСТИ',
             None, None, None, None, None, None, None, None, None,
             'Мастер ГНКТ, представитель Заказчика', None],
            [f'гидросвабирование в инт {interval_sko}м при Рзак={well_data.max_admissible_pressure._value}атм',
             23, f'Произвести гидросвабирование пласта в интервале {interval_sko[:-2]}м (закрыть затруб, произвести '
                 f'задавку в пласт '
                 f'жидкости при не более Рзак={well_data.max_admissible_pressure._value}атм при установленном '
                 f'герметичном пакере. '
                 f'Операции по задавке и изливу произвести 3-4 раза в зависимости от приёмистости). ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', 1],
            [f'Исследовать скважину на приёмистость при Рзак={well_data.expected_P}атм',
             24, f'Исследовать скважину на приёмистость при Рзак={well_data.expected_P}атм с составлением акта в '
                 f' в присутствии представителя ЦДНГ с составлением соответствующего акта (для вызова представителя '
                 f'давать телефонограмму в ЦДНГ). Определение приёмистости производить после насыщения пласта не '
                 f'менее 6м3 или '
                 f'при установившемся давлении закачки, но не более 1 часов. При недостижении запланированной '
                 f'приёмистости '
                 f'{well_data.expected_Q}м3/сут при Р= {well_data.expected_P}атм дальнейшие работы производить '
                 f'по согласованию с Заказчиком. Составить Акт ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика', 1.4],
            [None,
             25, f'Вызвать телефонограммой представителя Заказчика для замера приёмистости  при '
                 f'Рзак={well_data.expected_P}атм прибором "Панаметрикс".Перед запуском скважины '
                 f'произвести сброс жидкости с водовода в объёме 3-5м3 в ЕДК в зависимости от наличия нефтяной '
                 f'эмульсии на '
                 f'выходе в технологическую емкость для предупреждения повторной кольматации ПЗП шламом с водовода и '
                 f'произвести замер приемистости переносным прибором после насыщения скважины в течении 1-2 часа от КНС. '
                 f'При недостижении запланированной приёмистости дальнейшие работы производить по согласованию с '
                 f'Заказчиком. '
                 f'Составить Акт ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представитель Заказчика УСРСиСТ', 1.4],
            [None, 26,
             f'Поднять БДТ до устья с промывкой скважины мин.водой {well_data.fluid_work} . Составить Акт. '
             f'Согласовать с '
             f'Заказчиком утилизацию жидкости в коллектор.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 1.56],
            [None, 27, 'Произвести демонтаж колтюбингового оборудования и линии обвязки желобной системы.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', 2.25],
            [None, 28, 'Запустить скважину под закачку. ',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады', None],
            [None, 29, 'Сдать территорию скважину представителю Заказчика. Составить Акт.',
             None, None, None, None, None, None, None,
             'Мастер ГНКТ, представитель Заказчика', None],
        ]
        paker_opr = [f'Опрессовать пакер на {well_data.max_admissible_pressure._value}атм',
                     5, f'Опрессовать пакер на {well_data.max_admissible_pressure._value}атм с выдержкой 30 мин с '
                        f'оформлением соответствующего акта в присутствии  представителя ЦДНГ',
                     None, None, None, None, None, None, None,
                     'Мастер ГНКТ, предст. Заказчика', 1]

        opz = self.work_opz_gnkt(acid_info)
        n = 17
        if well_data.depth_fond_paker_do['do'] != 0:  # вставка строк при наличии пакера
            gnkt_opz.insert(7, paker_opr)
            n += 1

        if acid_true_quest:  # Вставка строк при необходимости ОПЗ
            for i in opz:
                gnkt_opz.insert(n, i)
                n += 1

        for row in block_gnvp_list[::-1]:
            gnkt_opz.insert(0, row)

        number_punkt = 1
        for i in range(3, len(gnkt_opz)):  # нумерация работ
            if len(str(gnkt_opz[i][1])) <= 3 and gnkt_opz[i][1] not in ['№', 'п/п']:
                gnkt_opz[i][1] = number_punkt
                number_punkt += 1
            else:
                number_punkt = 1

        return gnkt_opz




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    # window = GnktOpz()
    # window.show()
    sys.exit(app.exec_())