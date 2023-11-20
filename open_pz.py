import sys
from zipfile import ZipFile

from PIL import Image
import block_name
from main import MyWindow
import krs
import openpyxl as op
import self
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from PyQt5.QtWidgets import QInputDialog, QMessageBox

from copy import copy
from openpyxl.utils.cell import range_boundaries
# from main import MyWindow
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
from block_name import region_p, region_dict
from cdng import events_gnvp, itog_1, events_gnvp_gnkt
import plan
from H2S import calc_H2S
from gnkt_opz import gnkt_work


class CreatePZ(MyWindow):
    gipsInWell = False
    grpPlan = False
    nktOpressTrue = False
    bottomhole_drill = 0
    open_trunk_well = False
    normOfTime = 0
    lift_ecn_can = False
    lift_ecn_can_addition = False
    column_passability = False
    column_additional_passability = False
    template_depth = 0
    nkt_diam = 73
    b_plan = 0

    dict_perforation = {}
    dict_perforation_project = {}
    itog_ind_min = 0
    gaz_f_pr = []
    paker_layout = 0
    paker_diam_dict = {
        82: (88, 92),
        88: (92.1, 97),
        92: (97.1, 102),
        100: (102.1, 109),
        104: (109, 115),
        112: (118, 120),
        114: (120.1, 121.9),
        116: (122, 123.9),
        118: (124, 127.9),
        122: (128, 133),
        136: (144, 148),
        142: (148.1, 154),
        145: (154.1, 164),
        158: (166, 176),
        182: (190.6, 203.6),
        204: (215, 221)
    }
    column_additional_diametr = 0
    column_additional_wall_thickness = 0
    shoe_column_additional = 0
    column_diametr = 0
    column_wall_thickness = 0
    shoe_column = 0
    bottomhole_artificial = 0
    max_expected_pressure = 0
    head_column_additional = 0
    leakiness_Count = 0
    expected_pick_up = {}
    current_bottom = 0
    fluid_work = 0
    work_pervorations_approved = False
    dict_leakiness = {}
    leakiness = False
    dict_work_pervorations = {}
    work_pervorations = []
    work_pervorations_dict = {}
    paker_do = {'do': 0, 'posle': 0}
    column_additional = False
    well_number = None
    well_area = None
    values = []
    H_F_paker_do = {'do': 0, 'posle': 0}
    perforation_roof = current_bottom
    perforation_sole = 0
    dict_pump = {'do': '0', 'posle': '0'}
    leakiness_number = 0
    dict_pump_h = {'do': 0, 'posle': 0}
    ins_ind = 0
    len_razdel_1 = 0
    cat_P_1 = []
    dict_sucker_rod = {32: 0, 25: 0, 22: 0, 19: 0}
    dict_sucker_rod_po = {32: 0, 25: 0, 22: 0, 19: 0}
    H2S_pr = []
    cat_H2S_list = []
    H2S_mg = []
    lift_key = 0
    max_admissible_pressure = 0
    dict_nkt = {}
    dict_nkt_po = {}
    dict_sucker_rod = {}
    dict_sucker_rod_po = {}
    row_expected = []
    rowHeights = []
    plast_work = []
    plast_all = []
    cat_well_min = []
    bvo = False
    old_version = False
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    def __init__(self, dict_perforation_project, work_pervorations_dict, ins_ind_border, wb, ws, parent=None):
        super(MyWindow, self).__init__(parent)
        # self.lift_ecn_can_addition = lift_ecn_can_addition
        self.dict_perforation_project = dict_perforation_project
        self.work_pervorations_dict = work_pervorations_dict
        self.ins_ind_border = ins_ind_border
        self.wb = wb
        self.ws = ws
    def open_excel_file(self, fname, work_plan):
        global wb, ws
        wb = load_workbook(fname, data_only=True)
        name_list = wb.sheetnames
        # print(name_list)
        ws = wb.active
        for sheet in name_list:
            if sheet in wb.sheetnames and sheet != 'наряд-заказ КРС':
                wb.remove(wb[sheet])
        # print(wb.sheetnames)

        # zip = ZipFile(fname)
        # zip.extractall()



        # for cell in ws:
        #     if cell.has_image:
        #         image_cell_coordinate = cell.coordinate
        #         print(f'координаты изображениея {image_cell_coordinate}')
        #         break

        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            ws.row_dimensions[row_ind].hidden = False
            if 'Категория скважины' in row:
                CreatePZ.cat_well_min.append(row_ind + 1)  # индекс начала категории
                # print(f'индекс категории {CreatePZ.cat_well_min[0]}')

            elif 'План-заказ' in row:
                ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'
                CreatePZ.cat_well_max = row_ind - 1
                data_well_min = row_ind + 1

            elif 'IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in row or 'IX. Мероприятия по предотвращению аварий, инцидентов и осложнений:' in row:
                CreatePZ.data_well_max = row_ind
            elif 'X. Ожидаемые показатели после ремонта:' in row:
                CreatePZ.data_x_min = row_ind
            elif 'ШТАНГИ' in row:
                sucker_rod = True
                sucker_rod_ind = row_ind
                # sucker_rod_ind = self.sucker_rod_ind
            elif 'НКТ' in row:
                pipes_ind = row_ind
                # pipes_ind = self.pipes_ind
            elif 'ХI Планируемый объём работ:' in row or 'ХI. Планируемый объём работ:' in row or 'ХIII Планируемый объём работ:' in row \
                    or 'ХI Планируемый объём работ:' in row:
                CreatePZ.data_x_max = row_ind
            elif 'II. История эксплуатации скважины' in row:
                data_pvr_max = row_ind - 2
            elif 'III. Состояние скважины к началу ремонта ' in row:
                condition_of_wells = row_ind

            for col, value in enumerate(row):
                if value != None:

                    if 'площадь' == value:  # определение номера скважины
                        CreatePZ.well_number = row[col - 1]
                        # self.well_number = well_number
                        CreatePZ.well_area = row[col + 1]
                        # self.well_area = well_area
                    elif '11. Эксплуатационные горизонты и интервалы перфорации:' == value:
                        data_pvr_min = row_ind + 2
                    elif 'к ГРП' in str(value):
                        CreatePZ.grpPlan = True
                    elif '7. Пробуренный забой' == value:
                        index_bottomhole = row_ind

                        try:
                            CreatePZ.bottomhole_drill = float(row[col + 2])
                            n = 1
                            while CreatePZ.bottomhole_drill == None:
                                CreatePZ.bottomhole_drill = row[col + 2 + n]
                                n += 1
                                CreatePZ.bottomhole_drill = float(row[col + 2 + n])

                        except:
                            CreatePZ.bottomhole_drill, ok = QInputDialog.getDouble(self, 'Пробуренный забой',
                                                                                        'Введите Пробуренный забой по скважине, 1000, 50, 4000, 1)  ')
                        try:
                            CreatePZ.bottomhole_artificial = float(row[col + 5])
                            n = 1
                            while CreatePZ.bottomhole_artificial == None:
                                CreatePZ.bottomhole_artificial = row[col + 5 + n]
                                n += 1
                                CreatePZ.bottomhole_artificial = float(row[col + 5 + n])

                        except:
                            CreatePZ.bottomhole_artificial, ok = QInputDialog.getDouble(self, 'Искусственный забой',
                                                                                        'Введите искусственный забой по скважине, 1000, 50, 4000, 1)  ')
                    elif 'Текущий забой ' == value:
                        try:
                            CreatePZ.current_bottom = float(row[col + 2])
                            n = 1
                            while CreatePZ.current_bottom == None:
                                CreatePZ.current_bottom = row[col + n]
                                n += 1
                                CreatePZ.current_bottom = float(row[col + n])
                            print(f'Текущий забой {CreatePZ.current_bottom}')
                        except:
                            CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Текущий забоя',
                                                                                 'Введите Текущий забой равен', 1000, 1,
                                                                                 4000, 1)
                    elif 'месторождение ' == value:
                        CreatePZ.oilfield = row[col + 2]

                    elif value == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':  # Определение данных по колонне

                        data_main_production_string = (ws.cell(row=row_ind + 2, column=col + 1).value).split('(мм),', )
                        print(len(data_main_production_string))
                        if len(data_main_production_string) == 3:
                            try:
                                CreatePZ.column_diametr = float(data_main_production_string[0])
                                print('хкрня')
                            except:
                                CreatePZ.column_diametr = QInputDialog.getInt(self, 'диаметр основной колонны',
                                                                              'Введите диаметр основной колонны', 146, 80,
                                                                              276)[0]
                                print(f'диаметр ЭК {CreatePZ.column_diametr}')
                            try:
                                CreatePZ.column_wall_thickness = float(data_main_production_string[1][1:])
                            except:
                                CreatePZ.column_wall_thickness = QInputDialog.getDouble(self, 'Толщина стенки',
                                                                                        'Введите толщины стенки ЭК', 7.7, 5,
                                                                                        15, 1)[0]
                            #     print(CreatePZ.column_wall_thickness)
                            print(len(data_main_production_string[-1].split('(м)')), data_main_production_string[-1].split('(м)'))

                            if len(data_main_production_string[-1].split('-')) == 2:
                                # print(len(data_main_production_string[-1].split('-')))

                                CreatePZ.shoe_column = CreatePZ.without_b(
                                    data_main_production_string[-1].split('-')[-1])
                            elif len(data_main_production_string[-1].split('(м)')) == 2:
                                CreatePZ.shoe_column = CreatePZ.without_b(data_main_production_string[-1])

                            else:
                                CreatePZ.shoe_column = QInputDialog.getInt(self, 'Башмак колонны: ', 'Башмак колонны: ',
                                                                           1000, 20, 4000, 1)[0]
                        else:
                            CreatePZ.column_diametr = QInputDialog.getInt(self, 'диаметр основной колонны',
                                                                          'Введите диаметр основной колонны', 146, 80, 276)[0]
                            CreatePZ.column_wall_thickness = QInputDialog.getDouble(self, 'Толщина стенки',
                                                                                    'Введите толщины стенки ЭК', 7.7, 5,
                                                                                    15, 1)[0]
                            CreatePZ.shoe_column = QInputDialog.getInt(self, 'Башмак колонны: ', 'Башмак колонны: ',
                                                                       1000, 20, 4000, 1)[0]
                    elif 'гипс' in str(value):

                        CreatePZ.gipsInWell = True
                    elif 'нэк' in str(value).lower() or 'негерм' in str(value).lower() or 'нарушение э' in str(value).lower():
                        CreatePZ.leakiness_Count += 1
                        CreatePZ.leakiness = True

                    elif '9. Максимальный зенитный угол' == value:
                        try:
                            CreatePZ.max_angle = row[col + 1]
                            n = 1
                            while CreatePZ.max_angle == None:
                                CreatePZ.max_angle = row[col + n]
                                n += 1
                        except:
                            CreatePZ.max_angle, ok = QInputDialog.getDouble(self, 'Максимальный зенитный угол /'
                                                                                  '', 'Введите максимальный зенитный угол',
                                                                            25, 1, 100, 2)[0]
                    elif 'по H2S' in row and ('мг/л' in row or 'мг/дм3' in row):
                        if value == 'мг/л' or 'мг/дм3':
                            if CreatePZ.if_None(row[col - 1]) == 'отсут':
                                CreatePZ.H2S_mg.append(0)
                            else:
                                CreatePZ.H2S_mg.append(row[col - 1])
                    elif '%' in row:

                        if value == '%':
                            print(row_ind)
                            if CreatePZ.if_None(row[col - 1]) == 'отсут':
                                CreatePZ.H2S_pr.append(0)
                            else:
                                CreatePZ.H2S_pr.append(row[col - 1])

                        print(f'H2s % {CreatePZ.H2S_pr}')
                    elif 'по H2S' in row and ('мг/м3' in row):

                        if len(CreatePZ.H2S_mg) == 0 and 'мг/м3' == value:
                            CreatePZ.H2S_mg.append(float(row[col - 1] / 1000))


                    elif '9. Максимальный зенитный угол' in row and value == 'на глубине':
                        try:
                            CreatePZ.max_h_angle = row[col + 1]
                        except:
                            CreatePZ.max_h_angle, ok = QInputDialog.getint(self, 'Глубина максимального угла',
                                                                           'Введите глубину максимального зетного угла: ',
                                                                           500, 1, 4000)
                    elif 'цех' == value:
                        cdng = row[col + 1]
                        CreatePZ.cdng = cdng
                        print(f' ЦДНГ {CreatePZ.cdng}')
                    elif 'плотн.воды' == value:

                        try:
                            CreatePZ.water_cut = float(row[col - 1])  # обводненность
                        except:
                            CreatePZ.water_cut = QInputDialog.getInt(self, 'Обводненность',
                                                                     'Введите обводненность скважинной продукции', 50,
                                                                     0, 100)[0]


                    elif value == 'м3/т':
                        CreatePZ.gaz_f_pr.append(row[col - 1])


                    elif '6. Конструкция хвостовика' == value:
                        column_add_index = row_ind + 3
                        CreatePZ.data_column_additional = ws.cell(row=row_ind + 3, column=col + 2).value

                        # print(f'хв{CreatePZ.data_column_additional}, {CreatePZ.column_additional}')

                        if CreatePZ.if_None(CreatePZ.data_column_additional) != 'отсут':
                            if len(CreatePZ.data_column_additional.split('-')) > 1:
                                CreatePZ.column_additional = True
                                print(f' в скважине дополнительная колонны {CreatePZ.data_column_additional}')

                        # print(CreatePZ.column_additional)
                        if CreatePZ.column_additional == True:
                            try:
                                CreatePZ.head_column_additional = float(CreatePZ.data_column_additional.split('-')[0])
                            except:
                                CreatePZ.head_column_additional, ok = QInputDialog.getInt(self, 'голова доп колонны',
                                                                                          'введите глубину головы доп колонны',
                                                                                          600, 0, 3500)
                            try:
                                CreatePZ.shoe_column_additional = float(CreatePZ.data_column_additional.split('-')[1])
                                print(f'доп колонна {CreatePZ.shoe_column_additional}')
                            except:
                                CreatePZ.shoe_column_additional, ok = QInputDialog.getInt(self, ',башмак доп колонны',
                                                                                          'введите глубину башмак доп колонны',
                                                                                          600, 0, 3500)
                            if ws.cell(row=row_ind + 3, column=col + 4).value.split('x') == 2:
                                CreatePZ.column_additional_diametr = CreatePZ.without_b(ws.cell(row=row_ind + 3, column=col + 4).value.split('x')[0])
                                CreatePZ.column_additional_wall_thickness = CreatePZ.without_b(ws.cell(row=row_ind + 3, column=col + 4).value.split('x')[1])
                        try:
                            CreatePZ.column_additional_diametr = float(CreatePZ.without_b(ws.cell(row=row_ind + 3, column=col + 4).value))
                            print(f' диаметр доп колонны {CreatePZ.column_additional_diametr}')
                        except:
                            CreatePZ.column_additional_diametr, ok = QInputDialog.getInt(self, ',диаметр доп колонны',
                                                                                         'введите внешний диаметр доп колонны',
                                                                                         600, 0, 3500)
                        try:
                            CreatePZ.column_additional_wall_thickness = float(CreatePZ.without_b(ws.cell(row=row_ind + 3, column=col + 6).value))
                            print(f'толщина стенки доп колонны {CreatePZ.column_additional_wall_thickness} ')
                        except:
                            CreatePZ.column_additional_wall_thickness, ok = QInputDialog.getInt(self,
                                                                                                ',толщина стенки доп колонны',
                                                                                                'введите толщину стенки доп колонны',
                                                                                                600, 0, 3500)
                        if CreatePZ.column_additional_diametr >= 170 or str(CreatePZ.column_additional_wall_thickness) == '0':
                            CreatePZ.column_additional_diametr, ok = QInputDialog.getInt(self, ',диаметр доп колонны',
                                                                                         'введите внешний диаметр доп колонны',
                                                                                         114, 70, 170)
                            CreatePZ.column_additional_wall_thickness, ok = QInputDialog.getDouble(self,
                                                                                                ',толщина стенки доп колонны',
                                                                                                'введите толщину стенки доп колонны',
                                                                                                6.4, 4, 12, 1)

                    elif 'Дата вскрытия/отключения' == value:
                        CreatePZ.old_version = True
                    elif 'Максимально ожидаемое давление на устье' == value:
                        try:
                            CreatePZ.max_expected_pressure = row[col + 1]
                            n = 1
                            while CreatePZ.max_expected_pressure == None:
                                CreatePZ.max_expected_pressure = row[col + n]
                                n += 1
                        except:
                            CreatePZ.max_expected_pressure, ok = QInputDialog.getInt(self,
                                                                                     'Максимальное ожидаемое давление',
                                                                                     'Введите максимально ожидамое давление на устье: ',
                                                                                     80, 0, 200)

                    elif 'Максимально допустимое давление опрессовки э/колонны' == value or 'Максимально допустимое давление на э/колонну' == value:
                        try:
                            CreatePZ.max_admissible_pressure = row[col + 1]
                            n = 1
                            while CreatePZ.max_admissible_pressure == None:
                                CreatePZ.max_admissible_pressure = row[col + n]
                                n += 1
                        except:
                            CreatePZ.max_admissible_pressure, ok = QInputDialog.getInt(self,
                                                                                       'Максимальное допустимое давление опрессовки э/колонны',
                                                                                       'Введите максимально допустимое давление опрессовки э/колонны: ',
                                                                                       80, 0, 200)

                    elif value == 'Пакер' and row[col + 2] == 'типоразмер':

                        CreatePZ.paker_do['do'] = CreatePZ.if_None(row[col + 4])
                        if CreatePZ.old_version == False:

                            CreatePZ.paker_do['posle'] = CreatePZ.if_None(row[col + 9])
                        elif CreatePZ.old_version == True:
                            CreatePZ.paker_do['posle'] = CreatePZ.if_None(row[col +8])

                    elif value == 'Насос' and row[col + 2] == 'типоразмер':
                        if CreatePZ.if_None(row[col + 4]) != 'отсут':
                            try:
                                CreatePZ.dict_pump['do'] = CreatePZ.if_None(row[col + 4]).split('/')
                            except:
                                CreatePZ.dict_pump['do'] = CreatePZ.if_None(row[col + 4])

                        if CreatePZ.old_version == True and CreatePZ.if_None(row[col + 8]) != 'отсут':
                            try:
                                CreatePZ.dict_pump['posle'] = CreatePZ.if_None(row[col + 8]).split('/')
                            except:
                                CreatePZ.dict_pump['posle'] = CreatePZ.if_None(row[col + 8])
                        elif CreatePZ.old_version == False and CreatePZ.if_None(row[col + 9]) != 'отсут':
                            try:
                                CreatePZ.dict_pump['posle'] = CreatePZ.if_None(row[col + 9]).split('/')
                            except:
                                CreatePZ.dict_pump['posle'] = CreatePZ.if_None(row[col + 9])

                        # print(f' ячейка {ws.cell(row=row_ind + 5, column=col + 3).value}')
                        if ws.cell(row=row_ind + 5, column=col + 3).value == 'Нсп, м':
                            try:

                                CreatePZ.dict_pump_h['do'] = CreatePZ.without_b(ws.cell(row=row_ind + 5, column=col + 5).value)
                                print(f' глубина насос до {CreatePZ.dict_pump_h["do"]}')
                            except:
                                CreatePZ.dict_pump_h['do'] = CreatePZ.without_b(
                                    ws.cell(row=row_ind + 5, column=col + 5).value)
                            if CreatePZ.old_version == True:
                                try:
                                    CreatePZ.dict_pump_h['posle'] = CreatePZ.without_b(
                                        ws.cell(row=row_ind + 5, column=col + 9).value).split('/')
                                except:
                                    CreatePZ.dict_pump_h['posle'] = CreatePZ.without_b(
                                        ws.cell(row=row_ind + 5, column=col + 9).value)
                            else:
                                try:
                                    CreatePZ.dict_pump_h['posle'] = CreatePZ.without_b(
                                        ws.cell(row=row_ind + 5, column=col + 10).value).split('/')
                                except:
                                    CreatePZ.dict_pump_h['posle'] = CreatePZ.without_b(
                                        ws.cell(row=row_ind + 5, column=col + 10).value)

                    elif value == 'Н посадки, м':
                        if CreatePZ.paker_do['do'] != 'отсут':
                            try:
                                CreatePZ.H_F_paker_do['do'] = CreatePZ.without_b(row[col + 2])
                            except:
                                H_F_paker_do_2, ok = QInputDialog.getInt(self, 'Глубина посадки фондового пакера',
                                                                         'Глубина посадки фондового пакера до ремонта',
                                                                         1000, 0,
                                                                         int(CreatePZ.bottomhole_artificial))
                                CreatePZ.H_F_paker_do['do'] = H_F_paker_do_2
                        if CreatePZ.paker_do['posle'] != 'отсут':
                            try:
                                if CreatePZ.old_version:
                                    CreatePZ.H_F_paker_do['posle'] = CreatePZ.without_b(row[col + 6])

                                else:
                                    CreatePZ.H_F_paker_do['posle'] = CreatePZ.without_b(row[col + 7])

                            except:
                                H_F_paker_do_2, ok = QInputDialog.getInt(self, 'Глубина посадки фондового пакера',
                                                                         'Глубина посадки фондового пакера после ремонта',
                                                                         1000, 0,
                                                                         int(CreatePZ.bottomhole_artificial))
                                CreatePZ.paker_do['posle'] = H_F_paker_do_2

        if CreatePZ.grpPlan:
            grpPlan_quest = QMessageBox.question(self, 'Подготовка к ГРП', 'Программа определела что в скважине'
                                                                              f'планируется ГРП, верно ли?')
            if grpPlan_quest == QMessageBox.StandardButton.Yes:

                CreatePZ.grpPlan = krs.get_leakiness(self)

            else:
                CreatePZ.grpPlan = False


        print(f'CreatePZ {CreatePZ.H2S_pr}')
        if CreatePZ.leakiness == True:
            leakiness_quest = QMessageBox.question(self, 'нарушение колонны', 'Программа определела что в скважине'
                                                                              f'есть нарушение - {CreatePZ.leakiness_Count}, верно ли?')
            if leakiness_quest == QMessageBox.StandardButton.Yes:

                CreatePZ.leakiness = krs.get_leakiness(self)

            else:
                CreatePZ.leakiness = False

        if CreatePZ.gipsInWell == True:
            gips_true_quest = QMessageBox.question(self, 'Гипсовые отложения',
                                                   'Программа определела что скважина осложнена гипсовыми отложениями '
                                                   'и требуется предварительно определить забой на НКТ, верно ли это?')

            if gips_true_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.gipsInWell = True
            else:
                CreatePZ.gipsInWell = False

        curator_list = ['ОР', 'ГТМ', 'ГРР', 'ГО', 'ВНС']
        curator = ['ОР' if CreatePZ.if_None(CreatePZ.dict_pump['posle'][0]) == '0' else 'ГТМ'][0]
        print(f'куратор {curator, CreatePZ.if_None(CreatePZ.dict_pump["do"][0])}')

        CreatePZ.curator, ok = QInputDialog.getItem(self, 'Выбор кураторов ремонта', 'Введите сектор кураторов региона',
                                                    curator_list, curator_list.index(curator), False)
        if CreatePZ.column_additional == False and CreatePZ.shoe_column < CreatePZ.current_bottom:
            CreatePZ.open_trunk_well = True
        elif CreatePZ.column_additional == True and CreatePZ.shoe_column_additional < CreatePZ.current_bottom:
            CreatePZ.open_trunk_well = True


        print(f' ГРП - {CreatePZ.grpPlan}')
        print(f' глубина насоса {CreatePZ.dict_pump_h}')
        print(f' насоса {CreatePZ.dict_pump}')
        print(f'пакер {CreatePZ.paker_do}')
        print(f'глубина пакер {CreatePZ.H_F_paker_do}')
        print(f' диам колонны {CreatePZ.column_diametr}')
        print(f' гипс в скважине {CreatePZ.gipsInWell}')
        print(f'{CreatePZ.column_additional == False},{("ЭЦН" in str(CreatePZ.dict_pump["posle"][0]).upper() or "ВНН" in str(CreatePZ.dict_pump["posle"][0]).upper())}')
        try:
            if CreatePZ.column_additional == False and ('ЭЦН' in str(CreatePZ.dict_pump["posle"][0]).upper() or 'ВНН' in str(CreatePZ.dict_pump["posle"][0]).upper()):
                print(f'{CreatePZ.column_additional == False},{("ЭЦН" in str(CreatePZ.dict_pump["posle"][0]).upper() or "ВНН" in str(CreatePZ.dict_pump["posle"][0]).upper())}')

                CreatePZ.lift_ecn_can = True
            elif CreatePZ.column_additional == True:
                if ('ЭЦН' in str(CreatePZ.dict_pump['posle'][0]).upper() or 'ВНН' in str(CreatePZ.dict_pump['posle'][0]).upper())\
                        and CreatePZ.dict_pump_h["posle"] > CreatePZ.head_column_additional:
                    CreatePZ.lift_ecn_can = True

                elif ('ЭЦН' in str(CreatePZ.dict_pump['posle'][0].upper()) or 'ВНН' in str(CreatePZ.dict_pump[
                    'posle'][0].upper())) and CreatePZ.dict_pump_h["posle"] > CreatePZ.head_column_additional:

                    CreatePZ.lift_ecn_can_addition = True
            print(f' ЭЦН длина" {CreatePZ.lift_ecn_can, CreatePZ.lift_ecn_can_addition, "ЭЦН" in str(CreatePZ.dict_pump["posle"][0]).upper()}')
        except:
            print('ЭЦН отсутствует')
        # print(f'fh {len(CreatePZ.H2S_mg)}')
        for row in range(CreatePZ.cat_well_min[0], CreatePZ.cat_well_max+1):
            if 'по Pпл' == ws.cell(row=row, column=2).value:
                for column in range(1, 13):
                    col = ws.cell(row=row, column=column).value

                    if str(col) in ['1', '2', '3']:
                        CreatePZ.cat_P_1.append(int(col))
            if 'по H2S' == ws.cell(row=row, column=2).value:
                CreatePZ.cat_H2S_list = []
                for column in range(1, 13):
                    col = ws.cell(row=row, column=column).value

                    if str(col) in ['1', '2', '3']:
                        CreatePZ.cat_H2S_list.append(int(col))
                #
                # elif 'по газовому фактору' in str(col):
                #
                #     if str(col) in ['1', '2', '3']:
                #         CreatePZ.gaz_f_pr.append(int(col))
            if '1' in CreatePZ.cat_H2S_list or '2' in CreatePZ.cat_H2S_list:
                if len(CreatePZ.H2S_mg) == 0:

                    H2S_mg = QInputDialog.getDouble(self, 'Сероводород',
                                                    'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                    H2S_mg_true_quest = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
                    CreatePZ.H2S_mg.append(H2S_mg)
                    while  H2S_mg_true_quest == QMessageBox.StandardButton.Yes:
                        H2S_mg = QInputDialog.getDouble(self, 'Сероводород',
                                                        'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                        H2S_mg_true_quest = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
                        CreatePZ.H2S_mg.append(H2S_mg)
                if len(CreatePZ.H2S_pr) == 0:

                    H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                                    'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                    H2S_pr_true_quest = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
                    CreatePZ.H2S_mg.append(H2S_pr)
                    while H2S_pr_true_quest == QMessageBox.StandardButton.Yes:
                        H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                                        'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                        H2S_pr_true_quest = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
                        CreatePZ.H2S_mg.append(H2S_pr)
        if CreatePZ.curator == 'ОР':
            try:
                    # print(CreatePZ.data_x_min, CreatePZ.data_x_max)
                # expected_list = []
                for row in range(CreatePZ.data_x_min + 2, CreatePZ.data_x_max + 1):
                    for col in range(1, 12):
                        if 'прием' in str(ws.cell(row=row, column=col).value).strip().lower() or 'q' in str(ws.cell(row=row, column=col).value).strip().lower() :
                            Qpr = ws.cell(row=row, column=col + 1).value
                            print(f' приемис {Qpr}')
                            n = 1
                            while Qpr == None:
                                ws.cell(row=row, column=col + n).value
                                n += 1
                                Qpr = ws.cell(row=row, column=col +n).value
                            print(f'после {Qpr}')


                        elif 'зак' in str(ws.cell(row=row, column=col).value).strip().lower() or 'давл' in str(ws.cell(row=row, column=col).value).strip().lower():
                            Pzak = ws.cell(row=row, column=col + 1).value
                            n = 1
                            while Pzak == None:

                                n += 1
                                Pzak = ws.cell(row=row, column=col + n).value
                                print(f'pзака {Pzak}')


                CreatePZ.expected_pick_up[Qpr] = Pzak
                print(f' ожидаемые показатели {CreatePZ.expected_pick_up}')

            except:
                print('ошибка при определении плановых показателей')
                expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                     f'Ожидаемая приемистость по пласту ',
                                                     100, 0,
                                                     1600)
                expected_P, ok = QInputDialog.getInt(self, f'Ожидаемое Давление закачки',
                                                     f'Ожидаемое Давление закачки по пласту ',
                                                     100, 0,
                                                     250)
                CreatePZ.expected_pick_up[expected_Q] = expected_P
            print(f' Ожидаемые {CreatePZ.expected_pick_up}')
        # print(f' индекс нкт {pipes_ind + 1, condition_of_wells}')


        for row in range(pipes_ind + 1, condition_of_wells):  # словарь  количества НКТ и метраж
            if ws.cell(row=row, column=3).value == 'План':

                CreatePZ.a_plan = row
        # print(f'индекс {CreatePZ.a_plan}')
        for row in range(pipes_ind + 1, condition_of_wells):
            key = ws.cell(row=row, column=4).value
            value = CreatePZ.without_b(ws.cell(row=row, column=7).value)
            if key != None and row < CreatePZ.a_plan:
                CreatePZ.dict_nkt[key] = CreatePZ.dict_nkt.get(key, 0) + int(value)
            elif key != None and row >= CreatePZ.a_plan:
                CreatePZ.dict_nkt_po[key] = CreatePZ.dict_nkt_po.get(key, 0) + int(value)

        try:
            CreatePZ.shoe_nkt = int(sum(CreatePZ.dict_nkt.values()))
            CreatePZ.shoe_nkt > CreatePZ.bottomhole_artificial
        except:
            print('НКТ ниже забоя')
        # print(f' индекс штанг{sucker_rod_ind, pipes_ind}')
        try:
            for row in range(sucker_rod_ind, pipes_ind - 1):
                if ws.cell(row=row, column=3).value == 'План':
                    CreatePZ.b_plan = row
                    print(f'b_plan {CreatePZ.b_plan}')

            for row in range(sucker_rod_ind + 1, pipes_ind - 1):

                key = ws.cell(row=row, column=4).value
                value = ws.cell(row=row, column=7).value
                if CreatePZ.if_None(key) != 'отсут' and row < CreatePZ.b_plan:

                    CreatePZ.dict_sucker_rod[key] = CreatePZ.dict_sucker_rod.get(key, 0) + int(CreatePZ.without_b(value))
                elif CreatePZ.if_None(key) != 'отсут' and row >= CreatePZ.b_plan:
                    CreatePZ.dict_sucker_rod_po[key] = CreatePZ.dict_sucker_rod_po.get(key, 0) + int(CreatePZ.without_b(value))
                # self.dict_sucker_rod = dict_sucker_rod
                # self.dict_sucker_rod_po = dict_sucker_rod_po
            print(f' штанги на спуск {CreatePZ.dict_sucker_rod_po}')
        except:
            print('штанги отсутствуют')
        perforations_intervals = []
        pervoration_list = []
        CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                             'Введите забой до которого нужно нормализовать', CreatePZ.current_bottom)
        # print(f' индекс ПВР{data_pvr_min+2, data_pvr_max+1}')
        for row in range(data_pvr_min + 2, data_pvr_max + 2):  # Сортировка интервала перфорации
            lst = []
            for i in range(2, 13):
                lst.append(ws.cell(row=row, column=i).value)
            # print(ws.cell(row=row, column=6).value)
            if CreatePZ.old_version == True and isinstance(ws.cell(row=row, column=6).value, datetime) == True:
                lst.insert(5, None)
            elif CreatePZ.old_version == True and isinstance(ws.cell(row=row, column=6).value,
                                                             datetime) == False and ws.cell(row=row,
                                                                                            column=5).value != None:
                lst.insert(5, 'отключен')
            if all([str(i).strip() == 'None' or i == None for i in lst]) == False:
                perforations_intervals.append(lst)
            # perforations_intervals = sorted(perforations_intervals, key=lambda x: x[3])

        # perf_dict = {'вертикаль': None, 'кровля': None, 'подошва': None, 'вскрытие': None, 'отключение': None,
        #              'отв': None, 'заряд': None, 'удлинение': None, 'давление': None, 'замер': None}

        for ind, row in enumerate(perforations_intervals):
            try:
                krovlya_perf = float(row[2])

            except:

                krovlya_perf = 0

            plast = row[0]
            if plast == None:
                plast = perforations_intervals[ind - 1][0]
                # print(f' после {plast}')
                perforations_intervals[ind][0] = perforations_intervals[ind - 1][0]

            # print(row, any([str((i)).lower() == 'проект' for i in row]), all([str(i).strip() == None for i in row]) == False)
            if any([str((i)).lower() == 'проект' for i in row]) == False and all(
                    [str(i).strip() == None for i in row]) == False and krs.is_number(row[2]) == True and krs.is_number(float(row[3])) == True:

                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('вертикаль', set()).add(row[1])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отрайбироно', False)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('интервал', set()).add((round(float(row[2]), 1), round(float(row[3]), 1)))
                # print(f'отклю{row[5], CreatePZ.current_bottom, krovlya_perf}')
                # print(f'{CreatePZ.current_bottom > krovlya_perf, row[5] == None}')
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('вскрытие', set()).add(row[4])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', set()).add(row[5])
                if ind > 5:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('удлинение', set()).add(row[8])
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('давление', set()).add(row[9])
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('замер', set()).add(row[10])

                if CreatePZ.current_bottom > krovlya_perf and CreatePZ.if_None(row[5]) == 'отсут' and \
                        krs.is_number(row[2]) == True and krs.is_number(float(row[3])) == True:  # Определение работающих интервалов перфораци
                    # print(f'отклю{row[5], CreatePZ.current_bottom, row[2]}')
                    if CreatePZ.perforation_roof <= krovlya_perf:
                        CreatePZ.perforation_roof = krovlya_perf
                    if CreatePZ.perforation_sole <= float(row[3]):
                        CreatePZ.perforation_sole = float(row[3])
                    CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('вертикаль', set()).add(row[1])

                    CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('интервал', set()).add(
                        (round(float(row[2]), 1), round(float(row[3]), 1)))
                    CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('отрайбироно', False)
                    CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                    CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('вскрытие', set()).add(row[4])
                    CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('отключение', set()).add(row[5])
                    if ind > 5:
                        CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                        CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                        CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('удлинение', set()).add(row[8])
                        CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('давление', set()).add(row[9])
                        CreatePZ.dict_work_pervorations.setdefault(plast, {}).setdefault('замер', set()).add(row[10])


            elif any([str((i)).lower() == 'проект' for i in row]) == True and all(
                    [str(i).strip() == None for i in row]) == False and krs.is_number(row[2]) == True and krs.is_number(float(row[3])) == True:  # Определение проеткных интервалов перфорации

                self.dict_perforation_project.setdefault(plast, {}).setdefault('вертикаль', set()).add(row[1])
                self.dict_perforation_project.setdefault(plast, {}).setdefault('интервал', set()).add((round(float(row[2]), 1), round(float(row[3]), 1)))
                self.dict_perforation_project.setdefault(plast, {}).setdefault('вскрытие', set()).add(row[4])
                self.dict_perforation_project.setdefault(plast, {}).setdefault('отключение', set()).add(row[5])
                if ind > 5:
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('удлинение', set()).add(row[8])
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('давление', set()).add(row[9])
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('замер', set()).add(row[10])

        CreatePZ.dict_perforation_project = self.dict_perforation_project
        print(f'проект {self.dict_perforation_project}')
        print(f'все ПВР {CreatePZ.dict_perforation}')
        print(f'работающие интервалы {CreatePZ.dict_work_pervorations}')
        if CreatePZ.column_diametr < 110:
            CreatePZ.nkt_diam = 60
        # Определение работающих интервалов перфорации и заполнения в словарь

        try:

            CreatePZ.plast_work = list(CreatePZ.dict_work_pervorations.keys())
            CreatePZ.plast_all = list(CreatePZ.dict_perforation.keys())
            # print(CreatePZ.plast_all)
            # print(f' vf{CreatePZ.dict_perforation[CreatePZ.plast_all[0]]["интервал"][0][0]}')
            CreatePZ.perforation_roof = min(min(
                [min(CreatePZ.dict_work_pervorations[i]['интервал']) for i in CreatePZ.plast_work]))
            CreatePZ.perforation_sole = max(max(
                [max(CreatePZ.dict_work_pervorations[i]['интервал']) for i in CreatePZ.plast_work]))
            print(f'мин {CreatePZ.perforation_roof}, мак {CreatePZ.perforation_sole}')
            CreatePZ.perforation_roof_all = min(min(
                [min(CreatePZ.dict_perforation[i]['интервал']) for i in CreatePZ.plast_all]))
            print(CreatePZ.perforation_roof_all)
        except:
            perf_true_quest = QMessageBox.question(self, 'Программа',
                                                   'Программа определили,что в скважине интервалов перфорации нет, верно ли?')
            if perf_true_quest == QMessageBox.StandardButton.Yes:
                acid_true_quest = True
                self.dict_work_pervorations = {}
            else:
                perf_true_quest = False
                CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                                     'Введите забой до которого нужно нормализовать')

                CreatePZ.plast_work = list(CreatePZ.dict_work_pervorations.keys())
                CreatePZ.plast_all = list(CreatePZ.dict_perforation.keys())
                # print(CreatePZ.plast_all)
                # print(f' vf{CreatePZ.dict_perforation[CreatePZ.plast_all[0]]["интервал"][0][0]}')
                CreatePZ.perforation_roof = min(min(
                    [min(CreatePZ.dict_work_pervorations[i]['интервал']) for i in CreatePZ.plast_work]))
                CreatePZ.perforation_sole = max(max(
                    [max(CreatePZ.dict_work_pervorations[i]['интервал']) for i in CreatePZ.plast_work]))
                print(f'мин {CreatePZ.perforation_roof}, мак {CreatePZ.perforation_sole}')

        try:
            for j in range(CreatePZ.data_x_min, CreatePZ.data_x_max):  # Ожидаемые показатели после ремонта
                lst = []
                for i in range(0, 12):
                    lst.append(ws.cell(row=j + 1, column=i + 1).value)
                CreatePZ.row_expected.append(lst)
        except:
            pass
        if '1' in CreatePZ.cat_P_1 or '1' in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_P_1 or 1 in CreatePZ.cat_H2S_list:
            CreatePZ.bvo = True
        print(f'БВО {CreatePZ.bvo}')
        print(CreatePZ.cat_P_1, CreatePZ.cat_H2S_list)

        plan.delete_rows_pz(self, ws)
        CreatePZ.region = block_name.region(cdng)
        razdel_1 = block_name.razdel_1(self)

        for i in range(1, len(razdel_1)):  # Добавлением подписантов на вверху
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = razdel_1[i - 1][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
            ws.merge_cells(start_row=i, start_column=8, end_row=i, end_column=13)
        CreatePZ.ins_ind = 0

        # list_block = [cat_well_min,  CreatePZ.data_well_max]

        # head = plan.head_ind(cat_well_min, CreatePZ.data_well_max + 1)
        #
        # plan.copy_row(ws, ws2, CreatePZ.ins_ind, head)
        CreatePZ.ins_ind += CreatePZ.data_well_max - CreatePZ.cat_well_min[0] + 19
        # print(f' индекс вставки ГНВП{CreatePZ.ins_ind}')
        dict_events_gnvp = {}
        dict_events_gnvp['krs'] = events_gnvp()
        dict_events_gnvp['gnkt_opz'] = events_gnvp_gnkt()

        for i in range(CreatePZ.ins_ind, CreatePZ.ins_ind + len(dict_events_gnvp[work_plan]) - 1):
            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)

            if i == (CreatePZ.ins_ind + 13 or i == CreatePZ.ins_ind + 28) and work_plan == 'krs':

                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                               vertical='center')
                ws.cell(row=i, column=2).font = Font(name='Arial', size=13, bold=True)
                ws.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]
            elif i == CreatePZ.ins_ind + 11 and work_plan == 'gnkt_opz':
                # print(work_plan)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                               vertical='center')
                ws.cell(row=i, column=2).font = Font(name='Arial', size=11, bold=True)
                ws.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]
            else:
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                               vertical='top')
                ws.cell(row=i, column=2).font = Font(name='Arial', size=12)

                ws.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]
        ins_gnvp = CreatePZ.ins_ind
        CreatePZ.ins_ind += len(dict_events_gnvp[work_plan]) - 1

        ws.row_dimensions[2].height = 30
        ws.row_dimensions[6].height = 30

        # data_main_production_string = ws.cell(row=int(ind_data_main_production_string[1:])+1, column=int(ind_data_main_production_string[0])+2).value
        CreatePZ.insert_gnvp(ws, work_plan, ins_gnvp)

        # print(CreatePZ.row_expected)
        if len(CreatePZ.row_expected) !=0:
            for i in range(1, len(CreatePZ.row_expected) + 1):  # Добавление  показатели после ремонта
                ws.row_dimensions[CreatePZ.ins_ind + i - 1].height = None
                for j in range(1, 12):
                    if i == 1:
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).alignment = Alignment(wrap_text=False,
                                                                                          horizontal='center',
                                                                                          vertical='center')
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).value = CreatePZ.row_expected[i - 1][j - 1]
                    else:
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).alignment = Alignment(wrap_text=False,
                                                                                          horizontal='left',
                                                                                          vertical='center')
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).value = CreatePZ.row_expected[i - 1][j - 1]
            ws.merge_cells(start_column=2, start_row=CreatePZ.ins_ind + 1, end_column=12, end_row=CreatePZ.ins_ind + 1)
            CreatePZ.ins_ind += len(CreatePZ.row_expected)
            # print(f' индекс до работ {CreatePZ.ins_ind}')
            # if work_plan == 'gnkt_opz':

            # CreatePZ.gnkt_work1 = gnkt_work(self)
        self.ins_ind_border = CreatePZ.ins_ind
            # CreatePZ.count_row_height(ws, gnkt_work1, CreatePZ.ins_ind)
            # CreatePZ.itog_ind_min = CreatePZ.ins_ind
            # CreatePZ.ins_ind += len(gnkt_work1)
            #
            # CreatePZ.addItog(self, ws, CreatePZ.ins_ind, CreatePZ.itog_ind_min)


        # elif work_plan == 'krs':
            # leakiness_quest = QMessageBox.question(self, 'нарушение колонны', 'Есть ли нарушение по скважине?')
            # if leakiness_quest == QMessageBox.StandardButton.Yes:
            #     CreatePZ.column_leakiness = True
            #     CreatePZ.leakiness = krs.get_leakiness(self)
            #
            # else:
            #     CreatePZ.column_leakiness = False
            # print(f'нарушения {CreatePZ.leakiness}')

            # CreatePZ.gnkt_work1 = krs.work_krs(self)

            # CreatePZ.count_row_height(ws, krs_work1, CreatePZ.ins_ind)
            # CreatePZ.itog_ind_min = CreatePZ.ins_ind
            # CreatePZ.ins_ind += len(krs_work1)
            # self.ins_ind_border = CreatePZ.ins_ind

            # print('План работ на КРС')
        # else:
        #     print('План другого')
        # print(f' индекс до итогов {CreatePZ.ins_ind}')
        # wb.save(f'a.xlsx')
        # CreatePZ.itog_ind_max = CreatePZ.ins_ind
        # CreatePZ.ins_ind += 1


        if 2 in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_H2S_list:
            ws3 = wb.create_sheet('Sheet1')
            ws3.title = "Расчет необходимого количества поглотителя H2S"
            ws3 = wb["Расчет необходимого количества поглотителя H2S"]
            calc_H2S(ws3, CreatePZ.H2S_pr, CreatePZ.H2S_mg)
            ws3.sheet_visibility = 'hidden'
            # ws3.page_setup.fitToPage = True
            # ws3.page_setup.fitToHeight = True
            # ws3.page_setup.fitToWidth = True
            ws3.print_area = 'A1:A10'

        else:
            print(f'{CreatePZ.cat_H2S_list} Расчет поглотителя сероводорода не требуется')

        # ws.print_area = f'B1:L{CreatePZ.ins_ind}'
        # # ws.page_setup.fitToPage = True
        # ws.page_setup.fitToHeight = False
        # ws.page_setup.fitToWidth = True
        # ws.print_options.horizontalCentered = True

        try:
            for row_index, row in enumerate(ws.iter_rows()):
                if row_index in [i for i in range(column_add_index + 4, index_bottomhole + 5)]:
                    if all(cell.value == None for cell in row):
                        ws.row_dimensions[row_index].hidden = True
            print(' Скрытие ячеек сделано')
        except:
            print('нет скрытых ячеек')

        self.ws = ws
        self.wb = wb
        # wb.save(f'{CreatePZ.well_number} {CreatePZ.well_area} {work_plan}.xlsx')
        return self.ws

    def addItog(self, ws, ins_ind):
        print(ins_ind, self.table_widget.rowCount()-ins_ind+1)
        ws.delete_rows(ins_ind, self.table_widget.rowCount()-ins_ind+1)
        for i in range(ins_ind, len(itog_1(self)) + ins_ind):  # Добавлением итогов
            if i < ins_ind + 6:
                for j in range(1, 13):
                    ws.cell(row=i, column=j).value = itog_1(self)[i - ins_ind][j - 1]
                    if j != 1:
                        ws.cell(row=i, column=j).border = CreatePZ.thin_border
                        ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=11)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                               vertical='center')
            else:
                for j in range(1, 13):
                    ws.row_dimensions[i].height = 55

                    ws.cell(row=i, column=j).value = itog_1(self)[i - ins_ind][j - 1]
                    ws.cell(row=i, column=j).border = CreatePZ.thin_border
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                    ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                   vertical='center')

                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                ws.cell(row=i + ins_ind, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                                  vertical='center')

        ins_ind += len(itog_1(self)) + 2

        curator_sel = block_name.curator_sel(self, CreatePZ.curator, CreatePZ.region)
        curator_ved_sel = block_name.curator_sel(self, CreatePZ.curator, CreatePZ.region)
        podp_down = block_name.pop_down(self, CreatePZ.region, curator_sel)
        for i in range(1 + ins_ind, 1 + ins_ind + len(podp_down)):  # Добавлением подписантов внизу
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = podp_down[i - 1 - ins_ind][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            if i in [1 + ins_ind + 7, 1 + ins_ind + 8, 1 + ins_ind + 9,
                     1 + ins_ind + 10, 1 + ins_ind + 11,
                     1 + ins_ind + 12, 1 + ins_ind + 13, 1 + ins_ind + 14]:
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=6)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')
                if i == 1 + ins_ind + 11:
                    ws.row_dimensions[i].height = 55
        ins_ind += len(podp_down)
    def insert_gnvp(ws, work_plan, ins_gnvp):
        rowHeights_gnvp = [None, 115.0, 155.5, 110.25, 36.0, 52.25, 36.25, 36.0, 45.25, 36.25, 165.75, 38.5, 30.25,
                           30.5,
                           18.0, 36, 281.75, 115.75, 65.0, 55.75, 33.0, 33.0, 30.25, 47.0, 57.25, 45.75, 30.75, 350.25,
                           31.0, 51.75, 51.25, 87.25]
        rowHeights_gnvp_opz = [None, 95.0, 145.5, 25, 25.0, 52.25, 25.25, 20.0, 140.25, 36.25, 36.75, 20.5, 20.25, 20.5,
                               110.0, 60.5, 46.75, 36.75, 36.0, 36.75, 48.0, 36.0, 38.25]
        dict_rowHeights = {}
        dict_rowHeights['krs'] = rowHeights_gnvp
        dict_rowHeights['gnkt_opz'] = rowHeights_gnvp_opz
        # CreatePZ.rowHeights = CreatePZ.rowHeights + dict_rowHeights[work_plan]

        colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]
        # print(f' f {len(dict_rowHeights[work_plan])}')
        # print(f' индекс вставки высоты {ins_gnvp-2}')
        for index_row, row in enumerate(ws.iter_rows()):  # Копирование высоты строки
            if index_row + ins_gnvp <= len(dict_rowHeights[work_plan]) + ins_gnvp:
                ws.row_dimensions[index_row + ins_gnvp - 2].height = dict_rowHeights[work_plan][index_row - 1]
            for col_ind, col in enumerate(row):
                if col_ind <= 12:
                    ws.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind]
                else:
                    break

    def is_valid_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def if_None(value):
        if isinstance(value, datetime):
            return value
        elif value == None or 'отсут' in str(value).lower() or value == '-' or value == 0:
            return 'отсут'
        else:
            return value

    def without_b(a):

        if isinstance(a, int) == True or isinstance(a, float) == True:
            return a
        elif a == '-' or a == 'отсутствует' or a == 'отсутв' or a == 'отсут' or a == None:
            return '0'
        elif len(a.split('/')) == 2:
            lst = []
            for i in a.split('/'):
                b = ''
                for i in a:
                    if i in '0123456789.x':
                        b = str(b) + i
                    lst.append(b)
            return lst
        elif len(a.split('-')) == 2:
            lst = []
            for i in a.split('-'):
                print(i)
                lst.append(float(i.replace(',','.').strip()))
            return lst[0]
        else:
            b = 0
            for i in a:
                if i in '0123456789,.x':
                    b = str(b) + i

            return float(b.replace(',','.'))

    def count_row_height(ws, work_list, ins_ind, merged_cells_dict):
        from main import MyWindow

        text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 90: (301, 400), 110: (401, 500),
                           130: (501, 600), 150: (601, 700), 170: (701, 800), 190: (801, 900),  210: (901, 1500)}

        for i in range(ins_ind + 1, len(work_list) + ins_ind + 1):  # Добавлением работ
            # print(f'кол-ство строк рабочих{ins_ind, len(work_list), i - ins_ind, i}')
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = work_list[i - ins_ind - 1][j - 1]
                if j != 1:
                    ws.cell(row=i, column=j).border = CreatePZ.thin_border
                if j == 11:
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=11, bold=False)
                else:
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)


            ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                           vertical='center')
            ws.cell(row=i, column=11).alignment = Alignment(wrap_text=True, horizontal='center',
                                                            vertical='center')
            ws.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                            vertical='center')
            ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                           vertical='center')
        for i, row_data in enumerate(work_list):
            for column, data in enumerate(row_data):
                if column == 2:
                    if data != None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:

                                ws.row_dimensions[i + 1 + ins_ind].height = int(key)
        for row, col in merged_cells_dict.items():
            if len(col) != 2:
                # print(row)
                ws.merge_cells(start_row=row+1, start_column=3, end_row=row+1, end_column=10)
        # print(f'высота строк работ {ins_ind}')



        ws.column_dimensions[get_column_letter(11)].width = 20
        ws.column_dimensions[get_column_letter(12)].width = 20
        ws.column_dimensions[get_column_letter(7)].width = 20

        return 'Высота изменена'

        # ws2.unmerge_cells(start_column=2, start_row=self.ins_ind, end_column=12, end_row=self.ins_ind)


fname = 'Копия 2327 Манчаровского м-я (ПЗ) 11092023.xlsx'
# print(CreatePZ.open_excel_file(fname, fname, work_plan='gnkt_opz'))
