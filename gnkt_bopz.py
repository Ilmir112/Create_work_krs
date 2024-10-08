from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QMainWindow, QTabWidget, QLabel, QLineEdit, QComboBox, \
    QGridLayout, QWidget, QPushButton
from PyQt5 import QtWidgets

import well_data
from cdng import events_gnvp_frez
from krs import GnoWindow
from main import MyMainWindow
from work_py.acid_paker import CheckableComboBox, AcidPakerWindow
from gnkt_data import gnkt_data
from collections import namedtuple


class TabPage_gnkt(QWidget):

    def __init__(self, parent=None):
        from krs import volume_jamming_well
        super().__init__()

        self.validator_int = QIntValidator(0, 8000)
        self.validator_float = QDoubleValidator(0, 8000, 2)

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

        self.need_drilling_mud_label = QLabel("вымыв бурового раствора", self)
        self.need_drilling_mud_combo = QComboBox(self)
        self.need_drilling_mud_combo.addItems(['', 'Нужно', 'Не нужно'])

        self.volume_drilling_mud_label = QLabel("Объем бурового раствора", self)
        self.volume_drilling_mud_edit = QLineEdit(self)
        self.volume_drilling_mud_edit.setText(f'{volume_jamming_well(self, well_data.current_bottom)}')
        self.volume_drilling_mud_edit.setValidator(self.validator_int)

        self.drilling_contractor_label = QLabel("Подрядчик по бурению", self)
        self.drilling_contractor_combo = QComboBox(self)
        self.drilling_contractor_combo.addItems(['', 'ООО "АзГОР"', 'РН-Бурение'])

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

        self.fluid_project_label = QLabel('Рассчетная ЖГС', self)
        self.fluid_project_edit = QLineEdit(self)

        self.fluid_project_edit.setValidator(self.validator_float)

        self.distance_pntzh_label = QLabel('Расстояние  до ПНТЖ', self)
        self.distance_pntzh_edit = QLineEdit(self)
        self.distance_pntzh_edit.setValidator(self.validator_int)

        self.grid = QGridLayout(self)

        self.grid.addWidget(self.plast_label, 0, 1)
        self.grid.addWidget(self.plast_combo, 1, 1)
        self.grid.addWidget(self.roof_label, 0, 2)
        self.grid.addWidget(self.roof_edit, 1, 2)
        self.grid.addWidget(self.sole_label, 0, 3)
        self.grid.addWidget(self.sole_edit, 1, 3)

        self.grid.addWidget(self.need_drilling_mud_label, 2, 0)
        self.grid.addWidget(self.need_drilling_mud_combo, 3, 0)
        self.grid.addWidget(self.volume_drilling_mud_label, 2, 1)
        self.grid.addWidget(self.volume_drilling_mud_edit, 3, 1)
        self.grid.addWidget(self.drilling_contractor_label, 2, 2)
        self.grid.addWidget(self.drilling_contractor_combo, 3, 2)

        self.grid.addWidget(self.acid_label, 6, 0)
        self.grid.addWidget(self.acid_true_edit, 7, 0)

        self.grid.addWidget(self.acid_label_type, 6, 1)
        self.grid.addWidget(self.acid_edit, 7, 1)
        self.grid.addWidget(self.acid_volume_label, 6, 2)
        self.grid.addWidget(self.acid_volume_edit, 7, 2)
        self.grid.addWidget(self.acid_proc_label, 6, 3)
        self.grid.addWidget(self.acid_proc_edit, 7, 3)

        self.grid.addWidget(self.pressure_Label, 6, 5)
        self.grid.addWidget(self.pressure_edit, 7, 5)

        self.grid.addWidget(self.pressure_Label, 6, 5)
        self.grid.addWidget(self.pressure_edit, 7, 5)

        self.grid.addWidget(self.fluid_project_label, 8, 1)
        self.grid.addWidget(self.fluid_project_edit, 9, 1)

        self.grid.addWidget(self.distance_pntzh_label, 10, 1, 1, 3)
        self.grid.addWidget(self.distance_pntzh_edit, 11, 1, 1, 3)

        self.acid_edit.currentTextChanged.connect(self.update_sko_type)
        self.plast_combo.combo_box.currentTextChanged.connect(self.update_plast_edit)
        self.need_drilling_mud_combo.currentTextChanged.connect(self.update_drilling_mud_combo)

    def update_drilling_mud_combo(self, index):
        if index == 'Нужно':
            self.mud_label = QLabel("Текст бурового растовра", self)
            self.mud_edit = QLineEdit(self)
            self.mud_edit.setText(well_data.bur_rastvor)
            self.grid.addWidget(self.mud_label, 12, 1, 1, 3)
            self.grid.addWidget(self.mud_edit, 13, 1, 1, 3)
        else:
            try:
                self.mud_label.setParent(None)
                self.mud_edit.setParent(None)
            except:
                pass


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
    def __init__(self):
        super().__init__()
        self.addTab(TabPage_gnkt(self), 'ГНКТ БОПЗ')


class GnktBopz(MyMainWindow):

    def __init__(self, table_widget, gnkt_number_combo, fluid_edit, parent=None): #
        super(GnktBopz, self).__init__()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.work_plan = 'gnkt_bopz'
        self.paker_select = None
        self.gnkt_number_combo = gnkt_number_combo
        self.fluid_edit = fluid_edit

        self.table_widget = table_widget
        self.tabWidget = TabWidget()
        self.dict_nkt = {}

        self.buttonAdd = QPushButton('Добавить данные в план работ')
        self.buttonAdd.clicked.connect(self.add_work)
        vbox = QGridLayout(self.centralWidget)
        vbox.addWidget(self.tabWidget, 0, 0, 1, 2)
        vbox.addWidget(self.buttonAdd, 2, 0)

    def add_work(self):
        try:
            roof_plast = float(self.tabWidget.currentWidget().roof_edit.text())
            sole_plast = float(self.tabWidget.currentWidget().sole_edit.text())
            drilling_contractor_combo = self.tabWidget.currentWidget().drilling_contractor_combo.currentText()
            need_drilling_mud_combo = str(self.tabWidget.currentWidget().need_drilling_mud_combo.currentText())
            if need_drilling_mud_combo == '':
                return
            elif need_drilling_mud_combo == 'Нужно':
                well_data.bur_rastvor = self.tabWidget.currentWidget().acid_proc_edit.text()

            volume_drilling_mud_edit = float(self.tabWidget.currentWidget().volume_drilling_mud_edit.text())
            acid_true_edit = str(self.tabWidget.currentWidget().acid_true_edit.currentText())
            acid_edit = self.tabWidget.currentWidget().acid_edit.currentText()

            acid_volume_edit = float(self.tabWidget.currentWidget().acid_volume_edit.text().replace(',', '.'))
            acid_proc_edit = int(self.tabWidget.currentWidget().acid_proc_edit.text().replace(',', '.'))
            pressure_edit = int(self.tabWidget.currentWidget().pressure_edit.text())
            plast_combo = str(self.tabWidget.currentWidget().plast_combo.combo_box.currentText())
            self.distance = self.tabWidget.currentWidget().distance_pntzh_edit.text()
            fluid_project = self.tabWidget.currentWidget().fluid_project_edit.text().replace(',', '.')
            if fluid_project == "":
                mes = QMessageBox.critical(self, "Ошибка", "Нужно указать расчетный ЖГС")
                return
            if 1.01 > float(fluid_project) > 1.64:
                mes = QMessageBox.critical(self, "Ошибка", "расчетный ЖГС не корректен")
                return
            if drilling_contractor_combo == '':
                mes = QMessageBox.critical(self, "Ошибка", "Нужно указать подрядчика по бурению")
                return
            if self.distance == '':
                mes = QMessageBox.critical(self, "Ошибка", "Нужно указать расстояние до ПНТЖ")
                return
        except:
            QMessageBox.information(self, 'Ошибка', 'Введите корректные данные')

        if acid_edit == 'ВТ':
            self.vt = self.tabWidget.currentWidget().sko_vt_edit.text()
            if self.vt == '':
                mes = QMessageBox.critical(self, "Ошибка", "Нужно расписать объемы и вид кислоты")
                return

        work_list = self.gnkt_work(
            roof_plast, sole_plast, need_drilling_mud_combo, volume_drilling_mud_edit, acid_true_edit,
           acid_edit, acid_volume_edit, acid_proc_edit, pressure_edit,
           plast_combo, self.gnkt_number_combo, self.fluid_edit, drilling_contractor_combo, fluid_project)

        well_data.pause = False
        self.close()
        return work_list

    def gnkt_work(self,
                  roof_plast, sole_plast, need_drilling_mud_combo, volume_drilling_mud_edit, acid_true_edit,
                  acid_edit, acid_volume_edit, acid_proc_edit, pressure_edit, plast_combo, gnkt_number_combo,
                  fluid_work_insert, drilling_contractor_combo, fluid_project):
        from krs import volume_jamming_well, volume_pod_NKT
        from work_py.alone_oreration import volume_vn_nkt

        block_gnvp_list = events_gnvp_frez(self.distance, float(fluid_work_insert))

        if gnkt_number_combo == 'ГНКТ №2':
            gnkt_number = gnkt_data.gnkt_2
        elif gnkt_number_combo == 'ГНКТ №1':
            gnkt_number = gnkt_data.gnkt_1

        V_gntk = round(gnkt_number.gnkt_length * 0.74 / 1000, 1)

        shoe_nkt = sum(list(well_data.dict_nkt.values()))


        fluid_work, well_data.fluid_work_short = GnoWindow.calc_work_fluid(fluid_work_insert)

        if need_drilling_mud_combo == 'нужно':
            volume_drilling_mud_edit = volume_drilling_mud_edit

        volume_well_jumping = round(volume_drilling_mud_edit*1.2, 1)
        volume_vn_nkt = round(volume_vn_nkt(well_data.dict_nkt) * 1.2, 1)
        volume_well_at_shoe = round(volume_jamming_well(self, shoe_nkt) * 1.2, 1) - volume_vn_nkt
        volume_current_shoe_nkt = round(volume_pod_NKT(self)*1.2, 1) - volume_vn_nkt

        gnkt_bopz = [
            [None, 'ЦЕЛЬ ПРОГРАММЫ', None, None, None, None, None, None, None, None, None, None],
            [None, 1,
             f'Спуск ГНКТ. ВЫМЫВ БУРОВОГО РАСТВОРА в V-{volume_drilling_mud_edit}м3 ({drilling_contractor_combo}). '
             f'Нормализация забоя до гл. {well_data.current_bottom}м. '
             f'Проведение кислотной обработки {acid_proc_edit}% {acid_edit} в V={acid_volume_edit}м3. Глушение скважины '
             f'{fluid_project}г/см3 в объеме {volume_well_jumping}м3',
             None, None, None, None, None, None, None, None, None],
            [None, 2,
             'Внимание: Для проведения технологических операций завоз жидкости производить с ПНТЖ, согласованного с '
             'Заказчиком Перед началом работ согласовать с Заказчиком пункт утилизации жидкости.',
             None, None, None, None, None, None, None, None, None],
            [None,
             'ПОРЯДОК ПРОВЕДЕНИЯ РАБОТ', None, None, None, None, None, None, None, None, None, None],
            [None,
             'п.п', None, None, None, None, None, None, None, None, None, 'Ответственный'],
            [None, 1,
             'Ознакомить бригаду с планом работ и режимными параметрами дизайна по промывке и СПО. Провести инструктаж '
             'по промышленной безопасности',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 2,
             'Принять скважину у Заказчика по акту (состояние ф/арматуры и кустовой площадки.)',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 3,
             'Расставить оборудование и технику согласно «Типовой схемы расстановки оборудования и спецтехники при '
             'проведении капитального ремонта скважин с использованием установки «Койлтюбинг».',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 4,
             f'Произвести завоз технологической жидкости в V не менее 10м3 плотностью {fluid_work}. Солевой раствор '
             'солевой раствор в объеме ГНКТ', None, None, None, None, None, None, None, None, 'Мастер ГНКТ. Заказчик'],
            [None, 5,
             'При наличии, согласно плана заказа Н2S, добавить в завезенную промывочную жидкость '
             'нейтрализатора сероводорода "Реком-102" в концентрации 0,5л на 10м³',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ. Заказчик'],
            [None, 6, 'Внимание: при проведении работ по ОПЗ с кислотными составами, весь состав вахты обязан применять'
                      ' СИЗ (Инструкция П1-01.03 И-0128 ЮЛ-305 ООО"Башнефть-Добыча")',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 7,
             'Примечание: на месте проведения работ по ОПЗ кислотами и их смесями должен быть аварийный запас '
             'спецодежды, спецобуви и других средств индивидуальной защиты, запас чистой пресной воды и средств '
             'нейтрализации кислоты (мел, известь, хлорамин).',
             None, None, None, None, None, None, None, None, None],
            [None, 'МОНТАЖ И ОПРЕССОВКА', None, None, None, None, None, None, None, None, None, None],
            [None, 8,
             'Собрать Компоновку Низа Колонны-1 далее КНК-1: (насадка-промывочная D-38мм + сдвоенный обратный клапан.)',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 9,
             'Произвести монтаж 4-х секционного превентора БП 80-70.00.00.000 (700атм) и инжектора на устье скважины '
             'согласно «Схемы обвязки №5 устья противовыбросовым оборудованием при производстве работ по промывке '
             'скважины с установкой «ГНКТ» утвержденная главным инженером  {well_data.dict_contractor[well_data.contractor]["Дата ПВО"]}г. Произвести обвязку установки '
             'ГНКТ, насосно-компрессорного агрегата, желобной циркуляционной системы.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 10,
             'Внимание: Все требования ПБ и ОТ должны быть доведены до сведения работников, персонал должен быть '
             'проинформирован о начале проведения опрессовок. Все опрессовки производить согласно инструкции опрессовки'
             ' ПВО и инструкции опрессовки нагнетательной и выкидной линии перед производством работ на скважине с '
             'Колтюбинговыми установками.', None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 11,
             'При отрицательной температуре окружающей среды, нагреть до t - 50C и прокачать по ГНКТ солевой раствор '
             'в объеме ГНКТ для предотвращения замерзания раствора внутри г/трубы (получения ледяной пробки).',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 12,
             f'При закрытой центральной задвижке фондовой арматуры опрессовать ГНКТ и все нагнетательные '
             f'линии на {round(well_data.max_expected_pressure._value*1.5, 1)}атм. Опрессовать ПВО, '
             f'обратные клапана и выкидную линию от устья скважины до '
             f'желобной ёмкости (надёжно закрепить, оборудовать дроссельными задвижками) опрессовать на '
             f'{well_data.max_expected_pressure._value} '
             f'атм с выдержкой 30мин. Опрессовку ПВО зафиксировать в вахтовом журнале. Установить на малом и большом '
             f'затрубе технологический манометр. Провести УТЗ и инструктаж. Опрессовку проводить в присутствии мастера, '
             f'бурильщика, машиниста подъемника и представителя супервайзерской службы. Получить разрешение на '
             f'проведение работ.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 'СПУСК ГНКТ В СКВАЖИНУ', None, None, None, None, None, None, None, None, None, None],
            [None, 21, 'Открыв скважину и записав число оборотов задвижки – зафиксировать дату и время. '
                       'Спустить КНК-1 в скважину с ПЕРИОДИЧЕСКОЙ прокачкой рабочей жидкостью и проверкой веса на '
                       'подъём до получения посадки с целью определения глубины текущего забоя.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 22,
             f'ВНИМАНИЕ: При получении посадки до гл. {shoe_nkt}м и наличии разгрузки на промывочный '
             f'инструмент более '
             f'500кг  (уведомить Заказчика – составить АКТ на посадку). Приподнять КНК-1 на 20м выше глубины посадки. '
             f'Произвести вывод НКА на рабочий режим, восстановить устойчивую циркуляцию промывочной жидкости '
             f'(расход 180-190л/мин), произвести промывку лифта НКТ до гл.{shoe_nkt}м с постоянным контролем промывочной'
             f' жидкости в обратной ёмкости на наличие мех. примесей. Скорость спуска при промывке НКТ до гл.{shoe_nkt}м '
             f'не более 5м/мин. Контрольная проверка веса при вымыве  - через каждые 100м промывки на высоту не менее '
             f'5-10м со скоростью подъёма ГНКТ при проверке веса не более 5м/мин. Внимание: после промывки НКТ до '
             f'гл.{shoe_nkt}м приподнять ГТ на 20м выше пакера и промыться до выхода чистой тех. жидкости (без мех.примесей)'
             f' и только после этого продолжить промывку ниже пакера',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 23,
             f'Произвести допуск компоновки с промывкой со скоростью 2 м/мин, с проверкой веса на подъём со скоростью '
             f'не более 3 м/мин через каждые 10-20м интервала промывки до глубины {well_data.current_bottom}м. В случае отсутствия проходки, '
             f'согласовать максимально достигнутый забой с Заказчиком.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 'Вымыв бурового раствора', None, None, None, None, None, None, None, None, None, None],
            [None, 24,
             'Подать заявку не позднее, чем за 12ч., и не ранее, чем за 24ч. до требуемого времени вывоза '
             f'на вывоз бурового раствора в  объеме {volume_drilling_mud_edit}м3 подрядчику по бурению '
             f'({drilling_contractor_combo}) \nПРИМЕЧАНИЕ: \n-в '
             'эксплуатационном бурении, если на соседней скважине куста находится буровая бригада, заявку на вывоз ОБР '
             'следует передать мастеру буровой бригады, предварительно получив визу Бурового супервайзера;\n-Буровой '
             'мастер обязан принять заявку для исполнения либо принять ОБР в емкость для сбора ОБР, либо в шламовый '
             'амбар с регистрацией объема ОБР в Журнале учета с пометкой «объем освоения, скв. ____»',
             None, None, None, None, None, None, None, None, 'мастер ГНКТ, буровая компания'],
            [None, 25,
             f'После отбивки текущего забоя произвести подъем КНК -1 до гл.{shoe_nkt}м.',
             None, None, None, None, None, None,
             None, None, 'Мастер ГНКТ'],
            [None, 26,
             f'Произвести Вымыв бурового раствора по большому затрубу в объеме {volume_drilling_mud_edit}м3 тех '
             f'жидкостью уд.весом {fluid_work} до '
             f'чистой жидкости. Произвести вымыв бурового раствора по малому затрубу в объеме '
             f'{round(shoe_nkt*3/1000, 1)}м3',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 28, f'Произвести подъем КНК-1 до гл.{shoe_nkt}м.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 'КИСЛОТНАЯ ОРАБОТКА', None, None, None, None, None, None, None, None, None, None],
            [None, 29,
             f'Произвести БСКО пласта {plast_combo} в интервале {roof_plast}-{sole_plast}м в объеме '
             f'{acid_volume_edit}м3 не превышая давление закачки 80атм, по тех. плану подрядчика по ОПЗ ООО  '
             f'"Крезол-НефтеСервис": установить КНК-1 на глубину {well_data.current_bottom-2}м (2м выше текущего забоя).'
             f' На глубине {well_data.current_bottom-2}м начать закачку кислотного раствора на циркуляции (при '
             f'открытом малом затрубе) в объеме {V_gntk}м3 (Vгнкт), закрыть малый затруб и продолжить закачку с '
             f'продавкой на пласт (при закрытом малом затрубе), оставшегося кислотного состава + тех.жидкость в '
             f'объеме {V_gntk + 0.5}м3 с одновременным подъемом КНК до гл. {roof_plast}м, равномерно распределяя '
             f'весь объем кислоты по всему интервалу обработки. Закачку кислоты в пласт производить при давлении '
             f'закачки не более {pressure_edit}атм, при росте давления более '
             f'{pressure_edit}атм, Подъём КНК-1 на безопасное расстояние (не глубже {shoe_nkt-20}м). дальнейшие работы '
             f'согласовать с Закачиком. Составить акт',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 31,
             f'По истечении 2х часов, произвести допуск КНК-1 на г/трубе в скважину «без циркуляции» до гл.  '
            f' {well_data.current_bottom}м. Забой должен соответствовать – {well_data.current_bottom}м.'
             f' Составить АКТ на забой совмесно с '
             f'представителем Заказчика. '
             f'При отсутствии нормализованного забоя на гл.{well_data.current_bottom}м (по согласованию с Заказчиком) '
             f'- провести работы по нормализации забоя.', None, None, None, None, None, None, None, None,
             'Мастер ГНКТ представитель Заказчика'],
            [None, 32,
             f'При наличии забоя на гл.{well_data.current_bottom}м, по согласованию с Заказчиком замещение на жидкость '
             f'глушения с одновременным подъемом КНК-1 на ГНКТ до устья. ',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 33,
             'Произвести замер избыточного давления в течении 2ч при условии заполнения ствола ствола '
             f'жидкостью уд.весом {fluid_work}. Произвести перерасчет забойного давления, Согласовать с заказчиком '
             f'глушение скважин и необходимый удельный вес жидкости глушения, допустить КНК до '
             f'{well_data.current_bottom}м. Произвести перевод на тех жидкость расчетного удельного веса '
             f'(предварительно {fluid_project}г/см3) в объеме {volume_well_jumping}м3 '
             '((объем ствола э/к + объем открытого ствола и минут объем НКТ  + 20 % запаса), вывести циркуляцию '
             'с большого затруба  с ПРОТЯЖКОЙ ГНКТ СНИЗУ ВВЕРХ  с выходом циркуляции по большому затрубу до башмака '
             f'НКТ до гл. {shoe_nkt}м в объеме открытого ствола {volume_current_shoe_nkt}м3. '
             f'В башмаке НКТ Н={shoe_nkt}м промыть до выхода жидкости '
             f'глушения по большому затрубу в объеме {volume_well_at_shoe}м3. '
             f'Заместить на жидкость глушения НКТ в объеме {volume_vn_nkt}м3.  '
             'Тех отстой 2ч. В случае отрицательного результата по глушению скважины произвести перерасчет ЖГС и '
             'повторить операцию. ПРИ ПРОВЕДЕНИИ ВЕСТИ ГЛУШЕНИЯ КОНТРОЛЬ ЗА БАЛАНСОМ МЕЖДУ ОБЪЕМОМ ЗАКАЧИВАЕМОЙ И '
             'ВЫХОДЯЩЕЙ ЖИДКОСТЬЮ', None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 34,
             'Закрыв скважину и записав число оборотов задвижки – зафиксировать дату и время.', None, None, None,
             None, None, None, None, None, 'Мастер ГНКТ представитель Заказчика'],
            [None, 'ДЕМОНТАЖ И ОСВОБОЖДЕНИЕ ТЕРРИТОРИИ', None, None, None, None, None, None, None, None, None, None],
            [None, 35,
             'После закрытия задвижки - отдуть г/трубу азотом.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 36,
             'Сдать скважину представителю Заказчика Составить АКТ.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 'Ограничения веса и скоростей при СПО', None, None, None, None, None, None, None, None, None, None],
            [None, 14,
             'Максимальный расчётный вес ГНКТ при подъёме с забоя – 3745кг; при спуске –3064кг.; в '
             'неподвижном состоянии - 3405кг.', None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 15,
             f'Скорость спуска по интервалам:\nв устьевом оборудовании не более 0.5м/мин;                              '
             f'\n в интервале 2 -{shoe_nkt-20}м не '
             f'более 10-15м/мин (первичный-последующий спуск);                                  '
             f'\nв интервале {shoe_nkt-20}-{shoe_nkt+20}м не более 2м/мин;                              '
             f'\nв интервале '
             f'{shoe_nkt+20}-{well_data.current_bottom}м  не более 2-5 м/мин;',
             None, None, None, None, None, None, None, None, 'Мастер, бурильщик ГНКТ'],
            [None, 16,
             'Скорость подъёма по интервалам:\n в интервале'
               f' {well_data.current_bottom}-{shoe_nkt} не более 2 м/мин;                                   '
             f'\nв интервале {shoe_nkt}-2м не более 15-20 '
             f'м/мин;                             \nв устьевом'
               ' оборудовании не более 0.5 м/мин.', None, None, None, None, None, None, None, None,
             'Мастер, бурильщик ГНКТ'],
            [None, 17,
             'В процессе спуска производить приподъёмы для проверки веса на высоту не менее 20м со скоростью не более '
             '5м/мин через каждые 300-500м спуска (первичный-последующий спуск).',
             None, None, None, None, None, None, None, None, 'Мастер, бурильщик ГНКТ'],
            [None, 18, 'Перед каждой промывкой и после проверять веса ГТ (вверх, вниз, собств.)', None, None, None,
             None, None, None, None, None, 'Мастер, бурильщик ГНКТ'],
            [None, 19,
             'Не допускать увеличение нагрузки на г/трубу в процессе спуска. РАЗГРУЗКА Г/ТРУБЫ НЕ БОЛЕЕ 500 кг от '
             'собственного веса на этой глубине.',
             None, None, None, None, None, None, None, None, 'Мастер, бурильщик ГНКТ'],
            [None, 20,
             'При проведении технологического отстоя - не оставлять ГНКТ без движения: производить расхаживания '
             'г/трубы на 20м вверх и на 20м вниз со скоростью СПО не более 3м/мин. При отрицательной температуре '
             'окружающей среды, во избежании получения ледяной пробки в г/трубе при проведении тех.отстоя ни в '
             'коем случае не прекращать минимальную циркуляцию жидкости по г/трубе.',
             None, None, None, None, None, None, None, None, 'Мастер, бурильщик ГНКТ'],
            [None, 'Контроль выхода малого затруба', None, None, None, None, None, None, None, None, None, None],
            [None, 37, 
             'Во время промывки - выход малого затруба постоянно должен находиться под контролем. На желобной ёмкости '
             'постоянно осуществляется наблюдение за наличием мех. примесей на выходной линии. \nПеред началом '
             'промывки – необходимо отрегулировать штуцерный монифольд так, как это необходимо – уровень промывочной '
             'жидкости в циркуляционной ёмкости не должен уменьшаться. Уровень жидкости должен находиться под '
             'постоянным наблюдением, чтобы избежать потери жидкости в пласт. Во время промывки уровень жидкости '
             'должен немного увеличиваться или оставаться неизменным. \nПромывку от проппанта производить со '
             'скоростью не более 2м/мин, с проверкой веса на подъём через каждые 30м промывки, не превышая скорость '
             'подъёма г/трубы 3м/мин.', None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], 
            [None, 'Действия при приватах ГНКТ.', None, None, None, None, None, None, None, None, None, None], 
            [None, 38, 
             'ВНИМАНИЕ: При наличии посадок КНК - спуск производить с остановками для промежуточных '
             'промывок. В случае прихвата ГНКТ в скважине - проинформировсть ответственного представителя Заказчика и '
             f'руководство ГНКТ {well_data.contractor}. Дальнейшие действия производить в присутствии представителя Заказчика '
             'с составлением АКТа согласно "Плана-Схемы действий при прихватах ГНКТ" ТЕХНОЛОГИЧЕСКОЙ ИНСТРУКЦИИ ОАО '
             '«Башнефть добыча»', None, None, None, None, None, None, None, None, 
             'Мастер ГНКТ, предст.Заказчика Мастер по сложным работам ГНКТ'], 
            [None, 'Использование хим. реагентов в процессе работ', 
             None, None, None, None, None, None, None, None, None, None], 
            [None, 39, 
             'При отрицательных температурах окружающего воздуха перед открытием задвижки прокачать по ГНКТ '
             '(горячий солевой раствор в объеме ГНКТ) для предотвращения замерзания раствора внутри ГНКТ '
             '(получения ледяной пробки). ВНИМАНИЕ: Во время промывки возможен резкий вынос большого объёма '
             'проппанта из пласта, что может привести к потере циркуляции и последующему прихвату ГНКТ. '
             'Данную ситуацию можно проследить; при этом вес ГНКТ резко понизиться, а циркуляционное давление начнёт '
             'повышаться. а) Необходимо спуск г/трубы приостановить – произвести промывку с добавлением понизителя '
             'трения (0.4-1 л/м3) до стабилизации рабочего давления, но не менее 4 пачек по 4 м3 каждая. Продолжить'
             ' промывку. б) В случае поглощения промывочной жидкости в процессе промывки интервала перфорации - '
             'производить прокачку по г/трубе (вязких пачек V-от 2 м3 до 4 м3), а на забое (пачку V- 4 м)3 и '
             'сопровождение вязкой пачки в пакер через каждые 2м промывки интервала до полного выноса '
             'проппанта на желобную ёмкость.', None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], 
            [None, 40, 
             'После закрытия задвижки - приготовить и прокачать по г/трубе по циркуляции на желобную ёмкость пачку – '
             '(ингибитора коррозии в объёме 40л.) - для недопустимости коррозийных отложений в г/трубе. '
             'Предположительный расход хим.реагентов на скважину: \n1) Понизитель трения Лубритал - 30л '
             '(концентрация 1л/м3)\n2) Загуститель ВГ-4 - 20л (для загеливания тех жидкости и прокачки вязких пачек '
             'концентрация 5кг/м3)\n3) Лимонная кислота - 300кг (для разложения геля 1 кг/м3, для кислотных ванн '
             '100кг/м3)\n4) Ингибитор коррозии - 40л (концентрация 1л/м3)', 
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
        ]
        for row in block_gnvp_list[::-1]:
            gnkt_bopz.insert(0, row)

        # number_punkt = 1
        # for i in range(3, len(gnkt_bopz)):  # нумерация работ
        #     if len(str(gnkt_bopz[i][1])) <= 3 and gnkt_bopz[i][1] != '№':
        #         gnkt_bopz[i][1] = number_punkt
        #         number_punkt += 1
        #     else:
        #         number_punkt = 1

        return gnkt_bopz


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet()
    window = GnktBopz()
    window.show()
    sys.exit(app.exec_())
