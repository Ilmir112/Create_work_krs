
import sys
import openpyxl
import krs
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QTableWidget, \
    QLineEdit, QFileDialog, QToolBar, QPushButton, QMessageBox, QInputDialog
from PyQt5 import QtCore, QtWidgets
from datetime import datetime
from openpyxl.utils import get_column_letter
from PyQt5.QtCore import Qt
from openpyxl.workbook import Workbook
from openpyxl.styles import Border, Side



from openpyxl.drawing.image import Image

from H2S import calc_H2S


class MyWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.initUI()
        self.new_window = None
        self.acid_windowPaker = None
        self.acid_windowPaker2 = None
        self.data_window = None
        self.ws = None
        self.ins_ind = None
        self.perforation_list = []
        self.dict_perforation_project = {}

        self.ins_ind_border = None
        self.work_plan = 0

    def initUI(self):

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 400, 500, 400)

        self.table_widget = None

        self.createMenuBar()
        self.le = QLineEdit()

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.saveFileButton = QPushButton("Сохранить проект")
        self.saveFileButton.clicked.connect(self.save_to_excel)
        self.toolbar.addWidget(self.saveFileButton)

        self.correctDataButton = QPushButton("Скорректировать данные")
        self.correctDataButton.clicked.connect(self.correctData)
        self.toolbar.addWidget(self.correctDataButton)

        self.correctPVRButton = QPushButton("Скорректировать раотающие ПВР")
        self.correctPVRButton.clicked.connect(self.correctPVR)
        self.toolbar.addWidget(self.correctPVRButton)

        self.closeFileButton = QPushButton("Закрыть проект")
        self.closeFileButton.clicked.connect(self.close_file)
        self.toolbar.addWidget(self.closeFileButton)

    def createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        self.fileMenu = QMenu('&Файл', self)
        self.classifierMenu = QMenu('&Классификатор', self)
        self.menuBar.addMenu(self.fileMenu)
        self.menuBar.addMenu(self.classifierMenu)

        self.create_file = self.fileMenu.addMenu('&Создать')
        self.create_KRS = self.create_file.addAction('План КРС', self.action_clicked)
        self.create_GNKT = self.create_file.addMenu('&План ГНКТ')
        self.create_GNKT_OPZ = self.create_GNKT.addAction('ОПЗ', self.action_clicked)
        self.create_GNKT_frez = self.create_GNKT.addAction('Фрезерование', self.action_clicked)
        self.create_GNKT_GRP = self.create_GNKT.addAction('Освоение после ГРП', self.action_clicked)
        self.create_PRS = self.create_file.addAction('План ПРС', self.action_clicked)
        self.open_file = self.fileMenu.addAction('Открыть', self.action_clicked)
        self.save_file = self.fileMenu.addAction('Сохранить', self.action_clicked)
        self.save_file_as = self.fileMenu.addAction('Сохранить как', self.action_clicked)

        class_well = self.classifierMenu.addAction('&классификатор')
        list_without_jamming = self.classifierMenu.addAction('&Перечень без глушения')

    @QtCore.pyqtSlot()
    def action_clicked(self):
        from open_pz import CreatePZ
        action = self.sender()
        if action == self.create_KRS:
            self.tableWidgetOpen()
            self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                               "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            try:
                self.work_plan = 'krs'
                CreatePZ.pause = True
                sheet = CreatePZ.open_excel_file(self, self.fname[0], self.work_plan)
                self.copy_pz(sheet)

            except FileNotFoundError:
                print('Файл не найден')

        elif action == self.create_GNKT_OPZ:
            self.tableWidgetOpen()

            self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Выберите файл', '.',
                                                               "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")

            try:
                self.work_plan = 'gnkt_opz'
                sheet = CreatePZ.open_excel_file(self, self.fname[0], self.work_plan)
                self.copy_pz(sheet)

            except FileNotFoundError:
                print('Файл не найден')

            # if action == self.save_file:
            #     open_pz.open_excel_file().wb.save("test_unmerge.xlsx")
        elif action == self.save_file:
            self.save_to_excel

        elif action == self.save_file_as:
            self.saveFileDialog(self.wb2)

    def tableWidgetOpen(self):
        if self.table_widget is None:
            self.table_widget = QTableWidget()

            self.table_widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
            self.table_widget.customContextMenuRequested.connect(self.openContextMenu)
            self.setCentralWidget(self.table_widget)
            self.model = self.table_widget.model()

            # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
            # Указанная строка и столбец - это ячейка, которая была нажата.
            self.table_widget.cellPressed[int, int].connect(self.clickedRowColumn)

    def saveFileDialog(self, wb2):
        from open_pz import CreatePZ
        fileName, _ = QFileDialog.getSaveFileName(self, "Save excel-file", "", "Excel Files (*.xls)")
        if fileName:
            wb2.save(f"{CreatePZ.well_number} {CreatePZ.well_area} {CreatePZ.cat_P_1} категории.xlsx)")

    def save_to_excel(self):
        from open_pz import CreatePZ

        wb2 = Workbook()
        ws2 = wb2.get_sheet_by_name('Sheet')
        ws2.title = "План работ"
        print(f'открытие wb2')

        ins_ind = self.ins_ind_border

        merged_cells = []  # Список индексов объединения ячеек

        work_list = []
        for row in range(self.table_widget.rowCount()):
            row_lst = []
            # self.ins_ind_border += 1
            for column in range(self.table_widget.columnCount()):
                if self.table_widget.rowSpan(row, column) > 1 or self.table_widget.columnSpan(row, column) > 1:
                    merged_cells.append((row, column))
                item = self.table_widget.item(row, column)
                if not item is None:
                    row_lst.append(item.text())
                    # print(item.text())
                else:
                    row_lst.append("")

            work_list.append(row_lst)

        merged_cells_dict = {}

        for row in merged_cells:
            if row[0] >= ins_ind:
                merged_cells_dict.setdefault(row[0], []).append(row[1])
        # print(CreatePZ.ins_ind)
        for i in range(2, len(work_list)):  # нумерация работ
            if i >= ins_ind+2:
                work_list[i][1] = i - 1- ins_ind
                if krs.is_number(work_list[i][11]) == True:
                    CreatePZ.normOfTime += float(work_list[i][11])
        print(f'строки {self.ws.max_row}')
        CreatePZ.count_row_height(self.ws, ws2, work_list, merged_cells_dict,  ins_ind)
        itog_ind_min = CreatePZ.itog_ind_min + len(work_list)
        CreatePZ.addItog(self, ws2, self.table_widget.rowCount() + 1)
        try:
            ws2.print_area = f'B1:L{self.table_widget.rowCount()+45}'
            ws2.page_setup.fitToPage = True
            ws2.page_setup.fitToHeight = False
            ws2.page_setup.fitToWidth = True
            ws2.print_options.horizontalCentered = True
            if 2 in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_H2S_list:
                ws3 = wb2.create_sheet('Sheet1')
                ws3.title = "Расчет необходимого количества поглотителя H2S"
                ws3 = wb2["Расчет необходимого количества поглотителя H2S"]
                calc_H2S(ws3, CreatePZ.H2S_pr, CreatePZ.H2S_mg)
                ws3.hide = True
                # ws3.page_setup.fitToPage = True
                # ws3.page_setup.fitToHeight = True
                # ws3.page_setup.fitToWidth = True
                ws3.print_area = 'A1:A10'
            else:
                print(f'{CreatePZ.cat_H2S_list} Расчет поглотителя сероводорода не требуется')
            for row_ind, row in enumerate(ws2.iter_rows(values_only=True)):

                if 15 < row_ind < 100:

                    if all(cell in [None, '']  for cell in row) \
                            and ('Интервалы темпа' not in str(ws2.cell(row=row_ind, column=2).value)\
                                     and 'Замечания к эксплуатационному периоду' not in str(ws2.cell(row=row_ind, column=2).value)):
                        # print(row_ind+1, ('Интервалы темпа' not in str(ws2.cell(row=row_ind, column=2).value)), str(ws2.cell(row=row_ind, column=2).value))
                        ws2.row_dimensions[row_ind+1].hidden = True
                for col, value in enumerate(row):
                    if 'Зуфаров' in str(value):
                        coordinate = f'{get_column_letter(col - 2)}{row_ind - 1}'
                        break

            self.insert_image(ws2, 'imageFiles/Зуфаров.png', coordinate)
            self.insert_image(ws2, 'imageFiles/Хасаншин.png', 'H1')
            self.insert_image(ws2, 'imageFiles/Шамигулов.png', 'H4')
            path = 'D:\Documents\Desktop\ГТМ'
            filenames = f"{CreatePZ.well_number} {CreatePZ.well_area} кат {CreatePZ.cat_P_1}.xlsx"
            full_path = path + '/' + filenames
            print(ws2.max_row)
            if wb2:
                wb2.close()
                wb2.save(full_path)
        except Exception as e:
            print(e)

        finally:
            if self.wb:
                self.wb.close()

            print("Table data saved to Excel")

    def close_file(self):
        from open_pz import CreatePZ
        if not self.table_widget is None:
            self.table_widget.close()
            self.table_widget = None
            CreatePZ.gipsInWell = False
            CreatePZ.grpPlan = False
            CreatePZ.nktOpressTrue = False
            CreatePZ.bottomhole_drill = 0
            CreatePZ.open_trunk_well = False
            CreatePZ.normOfTime = 0
            CreatePZ.lift_ecn_can = False
            CreatePZ.pause = True
            CreatePZ.curator = '0'
            CreatePZ.lift_ecn_can_addition = False
            CreatePZ.column_passability = False
            CreatePZ.column_additional_passability = False
            CreatePZ.template_depth = 0
            CreatePZ.nkt_diam = 73
            CreatePZ.b_plan = 0
            CreatePZ.expected_Q = 0
            CreatePZ.expected_P = 0
            CreatePZ.plast_select = ''
            CreatePZ.dict_perforation = {}
            CreatePZ.dict_perforation_project = {}
            CreatePZ.itog_ind_min = 0
            CreatePZ.kat_pvo = 2
            CreatePZ.gaz_f_pr = []
            CreatePZ.paker_layout = 0

            CreatePZ.column_additional_diametr = 0
            CreatePZ.column_additional_wall_thickness = 0
            CreatePZ.shoe_column_additional = 0
            CreatePZ.column_diametr = 0
            CreatePZ.column_wall_thickness = 0
            CreatePZ.shoe_column = 0
            CreatePZ.bottomhole_artificial = 0
            CreatePZ.max_expected_pressure = 0
            CreatePZ.head_column_additional = 0
            CreatePZ.leakiness_Count = 0
            CreatePZ.expected_pick_up = {}
            CreatePZ.current_bottom = 0
            CreatePZ.fluid_work = 0
            CreatePZ.static_level = 0
            CreatePZ.dinamic_level = 0
            CreatePZ.work_perforations_approved = False
            CreatePZ.dict_leakiness = {}
            CreatePZ.leakiness = False
            CreatePZ.emergency_well = False
            CreatePZ.emergency_count = 0

            CreatePZ.work_perforations = []
            CreatePZ.work_perforations_dict = {}
            CreatePZ.paker_do = {"do": 0, "posle": 0}
            CreatePZ.column_additional = False
            CreatePZ.well_number = None
            CreatePZ.well_area = None
            CreatePZ.values = []
            CreatePZ. H_F_paker_do = {"do": 0, "posle": 0}
            CreatePZ.paker2_do = {"do": 0, "posle": 0}
            CreatePZ.H_F_paker2_do = {"do": 0, "posle": 0}
            CreatePZ.perforation_roof = 50000
            CreatePZ.perforation_sole = 0
            CreatePZ.dict_pump_SHGN = {"do": '0', "posle": '0'}
            CreatePZ.dict_pump_ECN = {"do": '0', "posle": '0'}
            CreatePZ.dict_pump_SHGN_h = {"do": '0', "posle": '0'}
            CreatePZ.dict_pump_ECN_h = {"do": '0', "posle": '0'}
            CreatePZ.dict_pump = {"do": '0', "posle": '0'}
            CreatePZ.leakiness_interval = []
            CreatePZ.dict_pump_h = {"do": 0, "posle": 0}
            CreatePZ.ins_ind = 0
            CreatePZ.len_razdel_1 = 0
            CreatePZ.cat_P_1 = []
            CreatePZ.countAcid = 0
            CreatePZ.swabTypeComboIndex = 1
            CreatePZ.swabTrueEditType = 1
            CreatePZ.data_x_max = 0
            CreatePZ.drilling_interval = []
            CreatePZ.max_angle = 0
            CreatePZ.pakerTwoSKO = False
            CreatePZ.privyazkaSKO = 0
            CreatePZ.H2S_pr = []
            CreatePZ.cat_H2S_list = []
            CreatePZ.H2S_mg = []
            CreatePZ.lift_key = 0
            CreatePZ.max_admissible_pressure = 0
            CreatePZ.region = ''
            CreatePZ.dict_nkt = {}
            CreatePZ.dict_nkt_po = {}
            CreatePZ.data_well_max = 0
            CreatePZ.data_pvr_max = 0
            CreatePZ.dict_sucker_rod = {}
            CreatePZ.dict_sucker_rod_po = {}
            CreatePZ.row_expected = []
            CreatePZ.rowHeights = []
            CreatePZ.plast_project = []
            CreatePZ.plast_work = []
            CreatePZ.plast_all = []
            CreatePZ.condition_of_wells = 0
            CreatePZ.cat_well_min = []
            CreatePZ.bvo = False
            CreatePZ.old_version = False
            CreatePZ.image_list = []


        print("Closing current file")

    def insert_image(self, ws, file, coordinate):
        # Загружаем изображение с помощью библиотеки Pillow
        img = openpyxl.drawing.image.Image(file)
        img.width = 200
        img.height = 180
        img.anchor = coordinate
        ws.add_image(img, coordinate)

    def openContextMenu(self, position):
        from open_pz import CreatePZ
        from work_py.template_work import template_ek_without_skm, template_ek

        context_menu = QMenu(self)

        action_menu = context_menu.addMenu("вид работ")
        geophysical = action_menu.addMenu("Геофизические работы")

        perforation_action = QAction("Перфорация", self)
        geophysical.addAction(perforation_action)
        perforation_action.triggered.connect(self.perforationNewWindow)

        geophysical_action = QAction("Геофизические исследования", self)
        geophysical.addAction(geophysical_action)
        geophysical_action.triggered.connect(self.GeophysicalNewWindow)

        rgd_menu = geophysical.addMenu("РГД")
        rgdWithoutPaker_action = QAction("РГД по колонне", self)
        rgd_menu.addAction(rgdWithoutPaker_action)
        rgdWithoutPaker_action.triggered.connect(self.rgdWithoutPaker_action)

        privyazka_action = QAction("Привязка НКТ", self)
        geophysical.addAction(privyazka_action)
        privyazka_action.triggered.connect(self.privyazkaNKT)

        definitionBottomGKLM_action = QAction("Отбивка забоя по ЭК", self)
        geophysical.addAction(definitionBottomGKLM_action)
        definitionBottomGKLM_action.triggered.connect(self.definitionBottomGKLM)

        vp_action = QAction("Установка ВП", self)
        geophysical.addAction(vp_action)
        vp_action.triggered.connect(self.vp_action)

        czh_action = QAction("Установка цементными желонками", self)
        geophysical.addAction(czh_action)
        czh_action.triggered.connect(self.czh_action)

        swibbing_action = QAction("Свабирование со пакером", self)
        geophysical.addAction(swibbing_action)
        swibbing_action.triggered.connect(self.swibbing_with_paker)

        swibbing2_action = QAction("Свабирование с двумя пакерами", self)
        geophysical.addAction(swibbing2_action)
        swibbing2_action.triggered.connect(self.swibbing2_with_paker)

        swabbing_opy_action = QAction("ГИС ОПУ", self)
        geophysical.addAction(swabbing_opy_action)
        swabbing_opy_action.triggered.connect(self.swabbing_opy)

        swibbingVoronka_action = QAction("Свабирование со воронкой", self)
        geophysical.addAction(swibbingVoronka_action)
        swibbingVoronka_action.triggered.connect(self.swibbing_with_voronka)

        kompressVoronka_action = QAction("Освоение компрессором с воронкой", self)
        geophysical.addAction(kompressVoronka_action)
        kompressVoronka_action.triggered.connect(self.kompress_with_voronka)

        del_menu = context_menu.addMenu('удаление строки')
        emptyString_action = QAction("добавить пустую строку", self)
        del_menu.addAction(emptyString_action)
        emptyString_action.triggered.connect(self.emptyString)

        gnkt_menu = context_menu.addMenu("ГНКТ")
        gnkt_opz_action = QAction("ГНКТ ОПЗ", self)
        gnkt_menu.addAction(gnkt_opz_action)
        gnkt_opz_action.triggered.connect(self.gnkt_opz)

        gnkt_opz_action = QAction("ГНКТ Освоение после ГРП", self)
        gnkt_menu.addAction(gnkt_opz_action)
        gnkt_opz_action.triggered.connect(self.gnkt_after_grp)

        deleteString_action = QAction("Удалить строку", self)
        del_menu.addAction(deleteString_action)
        deleteString_action.triggered.connect(self.deleteString)

        opressovka_action = QAction("Опрессовка колонны", self)
        action_menu.addAction(opressovka_action)
        opressovka_action.triggered.connect(self.pressureTest)

        template_with_skm = QAction("шаблон c СКМ", self)
        template_menu = action_menu.addMenu('Шаблоны')
        template_menu.addAction(template_with_skm)
        template_with_skm.triggered.connect(self.template_with_skm)

        template_pero = QAction("проходиость по перу", self)

        template_menu.addAction(template_pero)
        template_pero.triggered.connect(self.template_pero)

        ryber_action = QAction("Райбирование", self)
        action_menu.addAction(ryber_action)
        ryber_action.triggered.connect(self.ryberAdd)

        drilling_menu = action_menu.addMenu('Бурение')

        drilling_action_nkt = QAction("бурение на НКТ", self)
        drilling_menu.addAction(drilling_action_nkt)
        drilling_action_nkt.triggered.connect(self.drilling_action_nkt)

        drilling_SBT_action = QAction("бурение на СБТ", self)
        drilling_menu.addAction(drilling_SBT_action)
        drilling_SBT_action.triggered.connect(self.drilling_SBT_action)

        template_without_skm = QAction("шаблон без СКМ", self)
        template_menu.addAction(template_without_skm)
        template_without_skm.triggered.connect(self.template_without_skm)

        emergency_menu = action_menu.addMenu('Аварийные работы')

        magnet_action = QAction("магнит", self)
        emergency_menu.addAction(magnet_action)
        magnet_action.triggered.connect(self.magnet_action)

        larNKT_action = QAction("печать + ЛАР", self)
        emergency_menu.addAction(larNKT_action)
        larNKT_action.triggered.connect(self.larNKT_action)

        acid_menu = action_menu.addMenu('Кислотная обработка')
        acid_action1paker = QAction("окно на одном пакере", self)
        acid_menu.addAction(acid_action1paker)
        acid_action1paker.triggered.connect(self.acidPakerNewWindow)

        acid_action2paker = QAction("окно на двух пакерах", self)
        acid_menu.addAction(acid_action2paker)
        acid_action2paker.triggered.connect(self.acid2PakerNewWindow)

        # acid_action_1paker = QAction("на одном пакере", self)
        # acid_menu.addAction(acid_action_1paker)
        # acid_action_1paker.triggered.connect(self.acid_action_1paker)
        #
        # acid_action_2paker = QAction("на двух пакерах", self)
        # acid_menu.addAction(acid_action_2paker)
        # acid_action_2paker.triggered.connect(self.acid_action_2paker)

        acid_action_gons = QAction("ГОНС", self)
        acid_menu.addAction(acid_action_gons)
        acid_action_gons.triggered.connect(self.acid_action_gons)

        sand_menu = action_menu.addMenu('песчанный мост')
        filling_action = QAction('Отсыпка песком')
        sand_menu.addAction(filling_action)
        filling_action.triggered.connect(self.filling_sand)

        washing_action = QAction('вымыв песка')
        sand_menu.addAction(washing_action)
        washing_action.triggered.connect(self.washing_sand)

        grp_menu = action_menu.addMenu('ГРП')
        grpWithPaker_action = QAction('ГРП с одним пакером')
        grp_menu.addAction(grpWithPaker_action)
        grpWithPaker_action.triggered.connect(self.grpWithPaker)

        grpWithGpp_action = QAction('ГРП с ГПП')
        grp_menu.addAction(grpWithGpp_action)
        grpWithGpp_action.triggered.connect(self.grpWithGpp)

        alone_menu = action_menu.addMenu('одиночные операции')

        mkp_action = QAction('Ревизия МКП')
        alone_menu.addAction(mkp_action)
        mkp_action.triggered.connect(self.mkp_revision)

        konte_action = QAction('Канатные технологии')
        alone_menu.addAction(konte_action)
        konte_action.triggered.connect(self.konte_action)

        definition_Q_action = QAction("Определение приемитости по НКТ", self)
        alone_menu.addAction(definition_Q_action)
        definition_Q_action.triggered.connect(self.definition_Q)

        definition_Q_NEK_action = QAction("Определение приемитости по затрубу", self)
        alone_menu.addAction(definition_Q_NEK_action)
        definition_Q_NEK_action.triggered.connect(self.definition_Q_nek)

        kot_action = QAction('Система обратных клапанов')
        alone_menu.addAction(kot_action)
        kot_action.triggered.connect(self.kot_work)

        fluid_change_action = QAction('Изменение удельного веса')
        alone_menu.addAction(fluid_change_action)
        fluid_change_action.triggered.connect(self.fluid_change_action)

        pvo_cat1_action = QAction('Монтаж первой категории')
        alone_menu.addAction(pvo_cat1_action)
        pvo_cat1_action.triggered.connect(self.pvo_cat1)

        rir_menu = action_menu.addMenu('РИР')

        pakerIzvlek_menu = rir_menu.addMenu('извлекаемый пакер')
        pakerIzvlek_action = QAction('Установка пакера')
        pakerIzvlek_menu.addAction(pakerIzvlek_action)
        pakerIzvlek_action.triggered.connect(self.pakerIzvlek_action)

        izvlek_action = QAction('извлечение')
        pakerIzvlek_menu.addAction(izvlek_action)
        izvlek_action.triggered.connect(self.izvlek_action)

        rirWithPero_action = QAction('РИР на пере')
        rir_menu.addAction(rirWithPero_action)
        rirWithPero_action.triggered.connect(self.rirWithPero)

        rirWithPaker_action = QAction('РИР на пакере')
        rir_menu.addAction(rirWithPaker_action)
        rirWithPaker_action.triggered.connect(self.rirWithPaker)

        rirWithRpk_action = QAction('РИР с РПК')
        rir_menu.addAction(rirWithRpk_action)
        rirWithRpk_action.triggered.connect(self.rirWithRpk)

        rirWithRpp_action = QAction('РИР с глухим пакером')
        rir_menu.addAction(rirWithRpp_action)
        rirWithRpp_action.triggered.connect(self.rirWithRpp)

        claySolision_action = QAction('Глинистый раствор в ЭК')
        rir_menu.addAction(claySolision_action)
        claySolision_action.triggered.connect(self.claySolision)


        gno_menu = action_menu.addAction('Спуск фондового оборудования')
        gno_menu.triggered.connect(self.gno_bottom)

        context_menu.exec_(self.mapToGlobal(position))

    def clickedRowColumn(self, r, c):
        from open_pz import CreatePZ
        self.ins_ind = r + 1
        CreatePZ.ins_ind = r + 1
        print(f' выбранная строка {self.ins_ind}')

    def drilling_SBT_action(self):
        from work_py.drilling import drilling_sbt
        drilling_work_list = drilling_sbt(self)
        self.populate_row(self.ins_ind, drilling_work_list)

    def drilling_action_nkt(self):
        from work_py.drilling import drilling_nkt
        drilling_work_list = drilling_nkt(self)
        self.populate_row(self.ins_ind, drilling_work_list)

    def magnet_action(self):
        from work_py.emergencyWork import magnetWork
        magnet_work_list = magnetWork(self)
        self.populate_row(self.ins_ind, magnet_work_list)

    def larNKT_action(self):
        from work_py.emergencyWork import emergencyNKT
        emergencyNKT_list = emergencyNKT(self)
        self.populate_row(self.ins_ind, emergencyNKT_list)

    def rgdWithoutPaker_action(self):
        from work_py.rgdVcht import rgdWithoutPaker
        rgdWithoutPaker_list = rgdWithoutPaker(self)
        self.populate_row(self.ins_ind, rgdWithoutPaker_list)

    def definitionBottomGKLM(self):
        from work_py.alone_oreration import definitionBottomGKLM
        definitionBottomGKLM_list = definitionBottomGKLM(self)
        self.populate_row(self.ins_ind, definitionBottomGKLM_list)

    def privyazkaNKT(self):
        from work_py.alone_oreration import privyazkaNKT
        privyazkaNKT_list = privyazkaNKT(self)
        self.populate_row(self.ins_ind, privyazkaNKT_list)

    def definition_Q(self):
        from work_py.alone_oreration import definition_Q
        definition_Q_list = definition_Q(self)
        self.populate_row(self.ins_ind, definition_Q_list)

    def definition_Q_nek(self):
        from work_py.alone_oreration import definition_Q_nek
        definition_Q_list = definition_Q_nek(self)
        self.populate_row(self.ins_ind, definition_Q_list)

    def kot_work(self):
        from work_py.alone_oreration import kot_work
        kot_work_list = kot_work(self)
        self.populate_row(self.ins_ind, kot_work_list)

    def konte_action(self):
        from work_py.alone_oreration import konte
        konte_work_list = konte(self)
        self.populate_row(self.ins_ind, konte_work_list)

    def mkp_revision(self):
        from work_py.mkp import mkp_revision
        mkp_work_list = mkp_revision(self)
        self.populate_row(self.ins_ind, mkp_work_list)

    def acid_action_gons(self):
        from work_py.acids import acidGons
        acidGons_work_list = acidGons(self)
        self.populate_row(self.ins_ind, acidGons_work_list)

    def izvlek_action(self):
        from work_py.rir import izvlech_paker
        izvlech_paker_work_list = izvlech_paker(self)
        self.populate_row(self.ins_ind, izvlech_paker_work_list)

    def pakerIzvlek_action(self):
        from work_py.rir import rir_izvelPaker
        rir_izvelPaker_work_list = rir_izvelPaker(self)
        self.populate_row(self.ins_ind, rir_izvelPaker_work_list)

    def pvo_cat1(self):
        from work_py.alone_oreration import pvo_cat1
        pvo_cat1_work_list = pvo_cat1(self)
        self.populate_row(self.ins_ind, pvo_cat1_work_list)

    def fluid_change_action(self):
        from work_py.alone_oreration import fluid_change
        fluid_change_work_list = fluid_change(self)
        self.populate_row(self.ins_ind, fluid_change_work_list)

    def rirWithRpk(self):
        from work_py.rir import rir_rpk
        rirRpk_work_list = rir_rpk(self)
        self.populate_row(self.ins_ind, rirRpk_work_list)

    def rirWithRpp(self):
        from work_py.rir import rir_rpp
        rirRpp_work_list = rir_rpp(self)
        self.populate_row(self.ins_ind, rirRpp_work_list)

    def claySolision(self):
        from work_py.claySolution import claySolutionDef
        rirRpp_work_list = claySolutionDef(self)
        self.populate_row(self.ins_ind, rirRpp_work_list)
    def rirWithPaker(self):
        from work_py.rir import rir_paker
        rir_paker_work_list = rir_paker(self)
        self.populate_row(self.ins_ind, rir_paker_work_list)

    def rirWithPero(self):
        from work_py.rir import rirWithPero
        rirWithPero_work_list = rirWithPero(self)
        self.populate_row(self.ins_ind, rirWithPero_work_list)

    def grpWithPaker(self):
        from work_py.grp import grpPaker

        print('Вставился ГРП с пакером')
        grpPaker_work_list = grpPaker(self)
        self.populate_row(self.ins_ind, grpPaker_work_list)

    def grpWithGpp(self):
        from work_py.grp import grpGpp

        print('Вставился ГРП с ГПП')
        grpGpp_work_list = grpGpp(self)
        self.populate_row(self.ins_ind, grpGpp_work_list)

    def filling_sand(self):
        from work_py.sand_filling import sandFilling

        print('Вставился отсыпка песком')
        filling_work_list = sandFilling(self)
        self.populate_row(self.ins_ind, filling_work_list)

    def washing_sand(self):
        from work_py.sand_filling import sandWashing

        print('Вставился отсыпка песком')
        washing_work_list = sandWashing(self)
        self.populate_row(self.ins_ind, washing_work_list)

    def deleteString(self):
        selected_ranges = self.table_widget.selectedRanges()
        selected_rows = []

        # Получение индексов выбранных строк
        for selected_range in selected_ranges:
            top_row = selected_range.topRow()
            bottom_row = selected_range.bottomRow()

            for row in range(top_row, bottom_row + 1):
                if row not in selected_rows:
                    selected_rows.append(row)

        # Удаление выбранных строк в обратном порядке
        selected_rows.sort(reverse=True)
        print(selected_rows)
        for row in selected_rows:
            self.table_widget.removeRow(row)

    def emptyString(self):
        ryber_work_list = [[None, None, None, None, None, None, None, None, None, None, None, None]]
        self.populate_row(self.ins_ind, ryber_work_list)

    def vp_action(self):
        from work_py.vp_cm import vp

        print('Вставился ВП')
        vp_work_list = vp(self)
        self.populate_row(self.ins_ind, vp_work_list)

    def czh_action(self):
        from work_py.vp_cm import czh

        print('Вставился ВП')
        vp_work_list = czh(self)
        self.populate_row(self.ins_ind, vp_work_list)

    def swibbing_with_paker(self):
        from work_py.swabbing import swabbing_with_paker

        print('Вставился Сваб с пакером')
        swab_work_list = swabbing_with_paker(self, 10, 1)
        self.populate_row(self.ins_ind, swab_work_list)

    def swibbing2_with_paker(self):
        from work_py.swabbing import swabbing_with_2paker

        print('Вставился Сваб с пакером')
        swab_work_list = swabbing_with_2paker(self)
        self.populate_row(self.ins_ind, swab_work_list)

    def swabbing_opy(self):
        from work_py.swabbing import swabbing_opy

        print('Вставился ОПУ')
        swabbing_opy_list = swabbing_opy(self)
        self.populate_row(self.ins_ind, swabbing_opy_list)

    def kompress_with_voronka(self):
        from work_py.kompress import kompress

        print('Вставился компрессор с воронкой')
        kompress_work_list = kompress(self)
        self.populate_row(self.ins_ind, kompress_work_list)

    def swibbing_with_voronka(self):

        from work_py.swabbing import swabbing_with_voronka

        print('Вставился Сваб с воронкой')
        swab_work_list = swabbing_with_voronka(self)
        self.populate_row(self.ins_ind, swab_work_list)

    def ryberAdd(self):
        from work_py.raiding import Raid

        print('Вставился райбер')
        ryber_work_list = Raid.raidingColumn(self)
        self.populate_row(self.ins_ind, ryber_work_list)

    def gnkt_after_grp(self):
        from gnkt_after_grp import gnkt_work
        gnkt_work_list = gnkt_work(self)
        self.populate_row(self.ins_ind, gnkt_work_list)

    def gnkt_opz(self):
        from gnkt_opz import gnkt_work

        print('Вставился ГНКТ')
        ryber_work_list = gnkt_work(self)
        self.populate_row(self.ins_ind, ryber_work_list)

    def gno_bottom(self):
        from work_py.descent_gno import gno_down

        print('Вставился ГНО')
        gno_work_list = gno_down(self)
        self.populate_row(self.ins_ind, gno_work_list)

    def acid_action_1paker(self):
        from work_py.acids_work import acid_work
        from open_pz import CreatePZ
        if len(CreatePZ.plast_work) == 0:
            msc = QMessageBox.information(self, 'Внимание', 'Отсутствуют рабочие интервалы перфорации')
            return
        CreatePZ.paker_layout = 1
        print('Вставился кислотная обработка на одном пакере ')
        acid_work_list = acid_work(self)
        if acid_work_list != None:
            self.populate_row(self.ins_ind, acid_work_list)

    def acid_action_2paker(self):
        from work_py.acids import acid_work
        from open_pz import CreatePZ

        if len(CreatePZ.plast_work) == 0:
            msc = QMessageBox.information(self, 'Внимание', 'Отсутствуют рабочие интервалы перфорации')
            return
        CreatePZ.paker_layout = 2
        print('Вставился кислотная обработка на двух пакере ')
        acid_work_list = acid_work(self)
        if acid_work_list != None:
            self.populate_row(self.ins_ind, acid_work_list)

    def pressureTest(self):
        from work_py.opressovka import paker_list

        print('Вставился опрессовка пакером')
        pressure_work1 = paker_list(self)
        print(f'индекс {self.ins_ind, len(pressure_work1)}')
        self.populate_row(self.ins_ind, pressure_work1)

    def template_pero(self):
        from work_py.template_work import pero


        template_pero_list = pero(self)
        self.populate_row(self.ins_ind, template_pero_list)


    def template_with_skm(self):
        from work_py.template_work import template_ek
        from open_pz import CreatePZ
        template_ek_list = template_ek(self)
        print(f'индекс {self.ins_ind, len(template_ek_list)}')
        self.populate_row(self.ins_ind, template_ek_list)
        CreatePZ.ins_ind += len(template_ek_list) + 1

    def template_without_skm(self):
        from work_py.template_work import template_ek_without_skm
        from open_pz import CreatePZ

        template_ek_list = template_ek_without_skm(self)
        print()
        print(f'индекс {self.ins_ind, len(template_ek_list)}')
        self.populate_row(self.ins_ind, template_ek_list)
        CreatePZ.ins_ind += len(template_ek_list) + 1

    def populate_row(self, ins_ind, work_list):

        text_width_dict = {20: (0, 100), 40: (101, 200), 60: (201, 300), 80: (301, 400), 100: (401, 500),
                           120: (501, 600), 140: (601, 700), 160: (701, 800), 180: (801, 1500)}

        for i, row_data in enumerate(work_list):
            row = ins_ind + i
            self.table_widget.insertRow(row)

            self.table_widget.setSpan(i + ins_ind, 2, 1, 8)
            for column, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                # widget = QtWidgets.QLabel(str())
                # widget.setStyleSheet('border: 0.5px solid black; font: Arial 14px')

                # self.table_widget.setCellWidget(row, column, widget)

                if not data is None:
                    self.table_widget.setItem(row, column, item)

                else:
                    self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(str('')))

                if column == 2:
                    if not data is None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                text_width = key
                                self.table_widget.setRowHeight(row, int(text_width))

        # self.table_widget.setEditTriggers(QTableWidget.AnyKeyPressed)
        # self.table_widget.resizeColumnsToContents()
        # self.table_widget.resizeRowsToContents()

    def acid2PakerNewWindow(self):
        from work_py.acid_2paker import AcidPakerWindow
        from open_pz import CreatePZ
        print(f' окно СКО ')

        if self.acid_windowPaker2 is None:
            CreatePZ.countAcid = 0
            print(f' окно2 СКО ')
            self.acid_windowPaker2 = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, 0)
            self.acid_windowPaker2.setGeometry(200, 400, 300, 400)
            self.acid_windowPaker2.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            self.acid_windowPaker2 = None
            self.reply2_acid()

    def acidPakerNewWindow(self):
        from work_py.acid_paker import AcidPakerWindow
        from open_pz import CreatePZ
        print(f' окно СКО ')

        if self.acid_windowPaker is None:
            CreatePZ.countAcid = 0
            print(f' окно2 СКО ')
            self.acid_windowPaker = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, 0)
            self.acid_windowPaker.setGeometry(200, 400, 300, 400)
            self.acid_windowPaker.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            CreatePZ.countAcid = 0
            self.acid_windowPaker = None
            self.reply_acid()

    def reply2_acid(self):
        from open_pz import CreatePZ
        from work_py.acid_2paker import AcidPakerWindow

        acid_true_quest = QMessageBox.question(self, 'Необходимость кислоты',
                                               'Нужно ли планировать кислоту на следующий объет?')
        if acid_true_quest == QMessageBox.StandardButton.Yes:
            if self.acid_windowPaker2 is None:
                CreatePZ.countAcid = 1
                print(f' окно2 СКО ')
                self.acid_windowPaker2 = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, CreatePZ.countAcid)
                self.acid_windowPaker2.setGeometry(100, 400, 100, 400)
                self.acid_windowPaker2.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.acid_windowPaker2 = None
                self.reply2_acid()
        else:
            if  self.acid_windowPaker2 is None:
                CreatePZ.countAcid = 2
                print(f' окно2 СКО ')
                self.acid_windowPaker2 = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, CreatePZ.countAcid)
                self.acid_windowPaker2.setGeometry(100, 400, 100, 400)
                self.acid_windowPaker2.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.acid_windowPaker2 = None

    def reply_acid(self):
        from open_pz import CreatePZ
        from work_py.acid_paker import AcidPakerWindow

        acid_true_quest = QMessageBox.question(self, 'Необходимость кислоты',
                                               'Нужно ли планировать кислоту на следующий объет?')
        if acid_true_quest == QMessageBox.StandardButton.Yes:
            if self.acid_windowPaker is None:
                CreatePZ.countAcid = 1
                print(f' окно2 СКО ')
                self.acid_windowPaker = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, CreatePZ.countAcid)
                self.acid_windowPaker.setGeometry(100, 400, 100, 400)
                self.acid_windowPaker.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.acid_windowPaker = None
                self.reply_acid()
        else:
            if self.acid_windowPaker is None:
                CreatePZ.countAcid = 2
                print(f' окно2 СКО ')
                self.acid_windowPaker = AcidPakerWindow(self.table_widget, CreatePZ.ins_ind, CreatePZ.countAcid)
                self.acid_windowPaker.setGeometry(100, 400, 100, 400)
                self.acid_windowPaker.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.acid_windowPaker = None

    def GeophysicalNewWindow(self):
        from work_py.geophysic import GeophysicWindow

        if self.new_window is None:
            self.new_window = GeophysicWindow(self.table_widget, self.ins_ind)
            self.new_window.setWindowTitle("Геофизические исследования")
            self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def correctPVR(self):
        from open_pz import CreatePZ
        plast_work = set()
        CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                             'Введите забой до которого нужно нормализовать')
        for plast, value in CreatePZ.dict_perforation.items():
            for interval in value['интервал']:
                if CreatePZ.current_bottom >= interval[0]:
                    perf_work_quest = QMessageBox.question(self, 'Добавление работающих интервалов перфорации',
                                                           f'Является ли данный интервал {CreatePZ.dict_perforation[plast]["интервал"]} работающим?')
                    if perf_work_quest == QMessageBox.StandardButton.No:
                        CreatePZ.dict_perforation[plast]['отключение'] = True
                    else:
                        plast_work.add(plast)
                        CreatePZ.dict_perforation[plast]['отключение'] = False
                elif CreatePZ.perforation_roof <= interval[0] and CreatePZ.dict_perforation[plast][
                    "отключение"] == False:
                    CreatePZ.perforation_roof = interval[0]
                elif CreatePZ.perforation_sole >= interval[1] and CreatePZ.dict_perforation[plast][
                    "отключение"] == False:
                    CreatePZ.perforation_sole = interval[1]
                elif CreatePZ.perforation_roof_all <= interval[0]:
                    CreatePZ.perforation_roof_all = interval[0]
                break
        CreatePZ.plast_work = list(plast_work)
        print(f'работающий пласты  {CreatePZ.plast_work}')

    def correctData(self):
        from data_correct import DataWindow

        if self.new_window is None:

            self.new_window = DataWindow()
            self.new_window.setWindowTitle("Окно корректировки")
            self.new_window.setGeometry(100, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def perforationNewWindow(self):
        from work_py.perforation import PerforationWindow
        from open_pz import CreatePZ

        if len(CreatePZ.cat_P_1) > 1:
            if CreatePZ.cat_P_1[1] == 1 and CreatePZ.kat_pvo != 1:
                msc = QMessageBox.information(self, 'Внимание', 'Не произведен монтаж первой категории')
                return

        if self.new_window is None:

            self.new_window = PerforationWindow(self.table_widget, self.ins_ind,
                                                self.dict_perforation_project)
            self.new_window.setWindowTitle("Перфорация")
            self.new_window.setGeometry(200, 400, 300, 400)
            self.new_window.show()

        else:
            self.new_window.close()  # Close window.
            self.new_window = None  # Discard reference.

    def insertPerf(self):

        self.populate_row(self.ins_ind, self.perforation_list)

    def copy_pz(self, sheet):
        from gnkt_opz import gnkt_work
        from krs import work_krs
        rows = sheet.max_row
        merged_cells = sheet.merged_cells

        self.table_widget.setRowCount(rows)
        self.table_widget.setColumnCount(12)
        rowHeights_exit = [sheet.row_dimensions[i + 1].height if sheet.row_dimensions[i + 1].height is not None else 18
                           for i in range(sheet.max_row)]

        for row in range(1, rows + 1):
            if row > 1 and row < rows - 1:
                self.table_widget.setRowHeight(row, int(rowHeights_exit[row]))
            for col in range(1, 12 + 1):
                if not sheet.cell(row=row, column=col).value is None:
                    if isinstance(sheet.cell(row=row, column=col).value, float) and row > 25:
                        cell_value = str(round(sheet.cell(row=row, column=col).value, 2))
                    elif isinstance(sheet.cell(row=row, column=col).value, datetime):
                        cell_value = sheet.cell(row=row, column=col).value.strftime('%d.%m.%Y')
                    else:
                        cell_value = str(sheet.cell(row=row, column=col).value)
                    cell = sheet[f'{get_column_letter(col + 1)}{row + 1}']
                    cell_style = cell._style

                    item = QtWidgets.QTableWidgetItem(str(cell_value))
                    # item.setData(10, cell_style)
                    # item.setData(10, cell_style)

                    self.table_widget.setItem(row - 1, col - 1, item)
                    # Проверяем, является ли текущая ячейка объединенной
                    for merged_cell in merged_cells:
                        if row in range(merged_cell.min_row, merged_cell.max_row + 1) and \
                                col in range(merged_cell.min_col, merged_cell.max_col + 1):
                            # Устанавливаем количество объединяемых строк и столбцов для текущей ячейки
                            self.table_widget.setSpan(row - 1, col - 1,
                                                      merged_cell.max_row - merged_cell.min_row + 1,
                                                      merged_cell.max_col - merged_cell.min_col + 1)
        # print(f' njj {self.work_plan}')
        if self.work_plan == 'krs':
            self.populate_row(self.table_widget.rowCount(), work_krs(self))
        # elif self.work_plan == 'gnkt-opz':
        #     from open_pz import CreatePZ
        #     # print(CreatePZ.gnkt_work1)
        #     # self.populate_row(self.table_widget.rowCount(),  CreatePZ.gnkt_work1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
