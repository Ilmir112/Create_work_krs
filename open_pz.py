import os

from PIL import Image
import block_name
import main
import plan
import krs

from datetime import datetime, time
from openpyxl import Workbook, load_workbook
from PyQt5 import QtCore
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QDialog, QMainWindow
from openpyxl_image_loader import SheetImageLoader
from openpyxl.drawing.image import Image
from openpyxl.drawing.spreadsheet_drawing import AbsoluteAnchor
from openpyxl.drawing.xdr import XDRPoint2D, XDRPositiveSize2D
from openpyxl.utils.units import pixels_to_EMU, cm_to_EMU


from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment

from cdng import events_gnvp, itog_1, events_gnvp_gnkt

from work_py.gnkt_frez import Work_with_gnkt


class CreatePZ(QMainWindow):
    Qoil = 0
    gipsInWell = False
    grpPlan = False
    nktOpressTrue = False
    bottomhole_drill = 0
    open_trunk_well = False
    normOfTime = 0
    lift_ecn_can = False
    pause = True
    curator = '0'
    lift_ecn_can_addition = False
    column_passability = False
    column_additional_passability = False
    template_depth = 0
    nkt_diam = 73
    b_plan = 0
    column_direction_True = False
    expected_Q = 0
    expected_P = 0
    plast_select = ''
    dict_perforation = {}
    dict_perforation_project = {}
    itog_ind_min = 0
    kat_pvo = 2
    gaz_f_pr = []
    paker_diametr = 0
    cat_gaz_f_pr = []
    paker_layout = 0

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
    static_level = 0
    dinamic_level = 0
    work_perforations_approved = False
    dict_leakiness = {}
    dict_perforation_short = {}

    leakiness = False
    emergency_well = False
    emergency_count = 0
    skm_interval = []
    work_perforations = []
    work_perforations_dict = {}
    paker_do = {"do": 0, "posle": 0}
    column_additional = False
    well_number = None
    well_area = None
    values = []
    H_F_paker_do = {"do": 0, "posle": 0}
    paker2_do = {"do": 0, "posle": 0}
    H_F_paker2_do = {"do": 0, "posle": 0}
    perforation_roof = 50000
    perforation_sole = 0
    dict_pump_SHGN = {"do": '0', "posle": '0'}
    dict_pump_ECN = {"do": '0', "posle": '0'}
    dict_pump_SHGN_h = {"do": '0', "posle": '0'}
    dict_pump_ECN_h = {"do": '0', "posle": '0'}
    dict_pump = {"do": '0', "posle": '0'}
    leakiness_interval = []
    dict_pump_h = {"do": 0, "posle": 0}
    ins_ind = 0
    number_dp = ''
    len_razdel_1 = 0
    count_template = 0
    well_volume_in_PZ = []
    cat_P_1 = []
    costumer = 'ОАО "Башнефть"'
    contractor = 'ООО "Ойл-Сервис'
    dict_contractor = {'ООО "Ойл-Сервис':
                      {
                          'Дата ПВО': '15.10.2021г'
                      }}
    countAcid = 0

    swabTypeComboIndex = 1
    swabTrueEditType = 1
    data_x_max = 0
    drilling_interval = []
    max_angle = 0
    data_x_min = 0
    pakerTwoSKO = False
    privyazkaSKO = 0
    H2S_pr = []
    pipes_ind = 0
    sucker_rod_ind = 0
    cat_H2S_list = []
    H2S_mg = []
    H2S_mg_m3 = []
    lift_key = 0
    max_admissible_pressure = 0
    region = ''
    dict_nkt = {}
    dict_nkt_po = {}
    data_well_max = 0
    data_pvr_max = 0
    dict_sucker_rod = {}
    dict_sucker_rod_po = {}
    row_expected = []
    rowHeights = []
    plast_project = []
    plast_work = []



    well_oilfield = 0
    template_depth_addition = 0
    condition_of_wells = 0
    cat_well_min = 0
    cat_well_max = 0
    well_volume_in_PZ = []
    bvo = False
    old_version = True
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    image_list = []

    def __init__(self, wb, ws, data_window, perforation_correct_window2,  parent=None):
        super(QMainWindow, self).__init__()
        # self.lift_ecn_can_addition = lift_ecn_can_addition
        self.wb = wb
        self.ws = ws
        self.data_window = data_window
        self.perforation_correct_window2 = perforation_correct_window2




    def open_excel_file(self, ws, work_plan):
        old_index = 0
        from data_correct import DataWindow
        from perforation_correct import PerforationCorrect

        CreatePZ.work_plan = work_plan
        ws = self.ws


        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            ws.row_dimensions[row_ind].hidden = False
            if 'Категория скважины' in row:
                CreatePZ.cat_well_min = row_ind + 1  # индекс начала категории

            elif any(['ПЛАН РАБОТ' in str(col) for col in row]):
                CreatePZ.number_dp, ok = QInputDialog.getText(None, 'Номер дополнительного плана работ',
                                                     'Введите номер дополнительного плана работ')
                ws.cell(row=row_ind + 1, column=2).value = f'ДОПОЛНИТЕЛЬНЫЙ ПЛАН РАБОТ № {CreatePZ.number_dp}'
                print(f'номер доп плана {CreatePZ.number_dp}')
                CreatePZ.cat_well_max = row_ind - 1
                data_well_min = row_ind + 1

            # elif any(['Порядок работы' in str(col) for col in row]):
            #     CreatePZ.data_x_max = row_ind+1


            elif 'План-заказ' in row:
                ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'
                CreatePZ.cat_well_max = row_ind - 1
                data_well_min = row_ind + 1


            elif any(['IX. Мероприятия по предотвращению' in str(col) for col in row]) or \
                any(['IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in str(col) for col in row]):
                CreatePZ.data_well_max = row_ind

            elif any(['Ожидаемые показатели после' in str(col) for col in row]):
                CreatePZ.data_x_min = row_ind
                # print(f' индекс Ожидаемые показатели {CreatePZ.data_x_min}')


            elif 'ШТАНГИ' in row and 'До ремонта' in row:
                sucker_rod = True
                CreatePZ.sucker_rod_ind = row_ind
                # CreatePZ.sucker_rod_ind = self.sucker_rod_ind

            elif 'НКТ' in row and 'До ремонта' in row:
                CreatePZ.pipes_ind = row_ind
                # pipes_ind = self.pipes_ind

            elif 'ХI Планируемый объём работ:' in row or 'ХI. Планируемый объём работ:' in row or 'ХIII Планируемый объём работ:' in row \
                    or 'ХI Планируемый объём работ:' in row or 'Порядок работы' in row:
                CreatePZ.data_x_max = row_ind


            elif 'II. История эксплуатации скважины' in row:
                CreatePZ.data_pvr_max = row_ind

            elif 'III. Состояние скважины к началу ремонта ' in row:
                CreatePZ.condition_of_wells = row_ind

            for col, value in enumerate(row):
                if not value is None and col <= 12:
                    if 'площадь' == value:  # определение номера скважины
                        CreatePZ.well_number = row[col - 1]
                        CreatePZ.well_area = row[col + 1]
                    elif 'месторождение ' == value:  # определение номера скважины
                        CreatePZ.well_oilfield = row[col + 2]
                        # print(f'местрождение {CreatePZ.well_oilfield}')

                    elif 'Инв. №' == value:
                        CreatePZ.inv_number = row[col + 1]

                    elif '11. Эксплуатационные горизонты и интервалы перфорации:' == value:
                        data_pvr_min = row_ind + 2
                    elif 'к ГРП' in str(value):
                        CreatePZ.grpPlan = True
                    elif 'пробуренный забой' in str(value).lower():
                        index_bottomhole = row_ind
                        CreatePZ.bottomhole_drill = row[col + 2]
                        n = 1
                        while CreatePZ.bottomhole_drill is None:
                            CreatePZ.bottomhole_drill = row[col + 2 + n]
                            n += 1
                            CreatePZ.bottomhole_drill = row[col + 2 + n]
                        CreatePZ.bottomhole_artificial = row[col + 5]
                        n = 1
                        while CreatePZ.bottomhole_artificial is None:
                            CreatePZ.bottomhole_artificial = row[col + 5 + n]
                            n += 1
                            CreatePZ.bottomhole_artificial = float(row[col + 5 + n])
                    elif 'текущий забой' in str(
                            value).lower() and len(value) < 15:  # and any(['способ' in str(column).lower() for column in row]) == True:
                        CreatePZ.current_bottom = row[col + 2]
                        CreatePZ.bottom = row[col + 2]

                        n = 2
                        while CreatePZ.current_bottom is None or n == 3:
                            # print(n)
                            CreatePZ.current_bottom = row[col + n]
                            CreatePZ.bottom = row[col + n]
                            n += 1
                        print(f'забой {CreatePZ.bottom}')


                    elif 'месторождение ' == value:
                        CreatePZ.oilfield = row[col + 2]

                    elif 'Направление' in str(value) and 'Шахтное направление' not in str(value) and \
                            CreatePZ.if_None(ws.cell(row=row_ind + 1, column=col + 4).value) != 'отсут':
                        CreatePZ.column_direction_True = True
                        print(f'направление32323 {ws.cell(row=row_ind + 1, column=col + 4).value,  ws.cell(row=row_ind + 1, column=col + 4).value not in ["-", "(мм), (мм), -(м)", None]}')

                        try:
                            column_direction_data = ws.cell(row=row_ind + 1, column=col + 4).value.split('(мм),')
                            # print(f'направление32 {column_direction_data, len(column_direction_data)}')
                            # print(f' dfdf {float(column_direction_data)}')
                            try:
                                CreatePZ.column_direction_diametr = float(column_direction_data[0])
                            except:
                                CreatePZ.column_direction_diametr = 'не корректно'
                            # print(f' dfdf {CreatePZ.column_direction_diametr}')
                            try:
                                CreatePZ.column_direction_wall_thickness = float(column_direction_data[1])
                            except:
                                CreatePZ.column_direction_wall_thickness = 'не корректно'
                            try:
                                CreatePZ.column_direction_lenght = float(
                                    column_direction_data[2].split('-')[1].replace('(м)', ''))

                            except:
                                CreatePZ.column_direction_lenght = 'не корректно'
                        except:
                            CreatePZ.column_direction_diametr = 'не корректно'
                            CreatePZ.column_direction_wall_thickness = 'не корректно'
                            CreatePZ.column_direction_lenght = 'не корректно'
                    elif 'Кондуктор' in str(value) and \
                            ws.cell(row=row_ind + 1, column=col + 4).value not in ['-', '(мм), (мм), -(м)', None]:

                        try:
                            column_conductor_data = (ws.cell(row=row_ind + 1, column=col + 4).value).split('(мм),', )
                            print(f' конж {column_conductor_data}')
                            try:
                                CreatePZ.column_conductor_diametr = float(column_conductor_data[0])
                            except:
                                CreatePZ.column_conductor_diametr = 'не корректно'
                            try:
                                CreatePZ.column_conductor_wall_thickness = float(column_conductor_data[1])
                            except:
                                CreatePZ.column_conductor_wall_thickness = 'не корректно'
                            try:
                                print(f'ff{column_conductor_data[2].split("-")}')
                                CreatePZ.column_conductor_lenght = float(
                                    column_conductor_data[2].split('-')[1].replace('(м)', ''))
                            except:
                                CreatePZ.column_conductor_lenght = 'не корректно'

                        except:
                            CreatePZ.column_conductor_diametr = 'не корректно'
                            CreatePZ.column_conductor_wall_thickness = 'не корректно'
                            CreatePZ.column_conductor_lenght = 'не корректно'
                    elif any(['Кондуктор' in str(value) for value in row]):
                        for ind, value in enumerate(row):
                            if 'Уровень цемента' in str(value):

                                CreatePZ.level_cement_conductor = row[ind + 2].split('-')[0].replace(' ', '')

                    elif any(['Направление' in str(value) for value in row]):
                        for ind, value in enumerate(row):
                            if 'Уровень цемента' in str(value):
                                CreatePZ.level_cement_direction = row[ind + 2].split('-')[0].replace(' ', '')

                    elif 'колонная головка' in str(value):
                        CreatePZ.column_head_m = row[col + 4]


                    elif value == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':  # Определение данных по колонне
                        data_main_production_string = (ws.cell(row=row_ind + 2, column=col + 1).value).split('(мм),', )
                        try:
                            if len(data_main_production_string) == 3:
                                CreatePZ.column_diametr = float(data_main_production_string[0])
                                CreatePZ.column_wall_thickness = float(data_main_production_string[1])
                                if len(data_main_production_string[-1].split('-')) == 2:

                                    CreatePZ.shoe_column = CreatePZ.without_b(
                                        data_main_production_string[-1].split('-')[-1])
                                elif len(data_main_production_string[-1].split('(м)')) == 2:
                                    CreatePZ.shoe_column = CreatePZ.without_b(data_main_production_string[-1])
                        except ValueError:
                            pass


                    elif 'гипс' in str(value).lower() or 'гидратн' in str(value).lower():
                        CreatePZ.gipsInWell = True

                    elif '9. Максимальный зенитный угол' == value:
                        CreatePZ.max_angle = row[col + 1]
                        n = 1
                        while CreatePZ.max_angle is None:
                            CreatePZ.max_angle = row[col + n]
                            n += 1
                        CreatePZ.max_angle_H = row[col + 7]
                        n = 7
                        while str(CreatePZ.max_angle_H).isdigit() is False:
                            CreatePZ.max_angle_H = row[col + n]
                            n += 1

                    elif '10. Расстояние от стола ротора до среза муфты э/колонны ' == value:
                        CreatePZ.stol_rotora = row[col + 4]
                        # print(f'стол ротора {CreatePZ.stol_rotora}')
                        n = 4
                        while CreatePZ.stol_rotora is None or n > 15:
                            CreatePZ.stol_rotora = row[col + n]
                            n += 1

                    elif 'Начало бурения' == value:
                        CreatePZ.date_drilling_run = str(row[col + 2])
                    elif 'Конец бурения' == value:
                        CreatePZ.date_drilling_cancel = str(row[col + 2])
                        n = 1
                        while CreatePZ.date_drilling_cancel is None or n > 15:
                            CreatePZ.date_drilling_cancel = str(row[col + n])
                            n += 1
                    elif 'Уровень цемента за колонной' in str(value):
                        CreatePZ.level_cement_column = row[col + 2]
                        n = 1
                        while CreatePZ.level_cement_column is None or n > 15:
                            CreatePZ.level_cement_column = row[col + n]
                            n += 1

                    elif 'Рмкп ( э/к и' in str(value):
                        CreatePZ.pressuar_mkp = row[col + 2]
                        n = 1
                        while CreatePZ.pressuar_mkp is None or n > 15:
                            CreatePZ.pressuar_mkp = row[col + n]
                            n += 1

                    elif value == 'мг/л' or value == 'мг/дм3':
                        if CreatePZ.if_None(row[col - 1]) != 'отсут':
                            CreatePZ.H2S_mg.append(float(str(row[col - 1]).replace(',', '.')))
                        else:
                            CreatePZ.H2S_mg.append(0)
                        # print(f'мг/k {CreatePZ.H2S_mg}')
                    elif value == '%':
                        # print(row_ind)
                        if CreatePZ.if_None(row[col - 1]) != 'отсут':
                            CreatePZ.H2S_pr.append(float(str(row[col - 1]).replace(',', '.')))
                        else:
                            CreatePZ.H2S_pr.append(0)
                    elif 'мг/м3' == value:
                        if CreatePZ.if_None(row[col - 1]) != 'отсут':
                            CreatePZ.H2S_mg_m3.append(float(str(row[col - 1]).replace(',', '.')) / 1000)
                        else:
                            CreatePZ.H2S_mg_m3.append(0)


                    elif 'Vжг' in str(value):
                        try:
                            well_volume_in_PZ = str(row[col + 1]).replace(',', '.')
                            # print(f'строка {well_volume_in_PZ}')
                            n = 1
                            while well_volume_in_PZ == None or n < 10:
                                well = str(row[col + 1 + n]).replace(',', '.')
                                if well in [int, float]:
                                    well_volume_in_PZ = float(row[col + 1 + n].replace(',', '.'))
                                n += 1
                            CreatePZ.well_volume_in_PZ.append(float(well_volume_in_PZ))
                        except:
                            well_volume_in_PZ, _ = QInputDialog.getDouble(None, 'Объем глушения',
                                                                       'ВВедите объем глушения согласно ПЗ', 50, 1, 70)
                            CreatePZ.well_volume_in_PZ.append(well_volume_in_PZ)


                    elif '9. Максимальный зенитный угол' in row and value == 'на глубине':
                        try:
                            CreatePZ.max_h_angle = row[col + 1]
                        except:
                            CreatePZ.max_h_angle, ok = QInputDialog.getDouble(self, 'Глубина максимального угла',
                                                                           'Введите глубину максимального зетного угла: ',
                                                                           0, 1, 100, 1)
                    elif 'цех' == value:
                        cdng = row[col + 1]
                        CreatePZ.cdng = cdng
                        # print(f' ЦДНГ {CreatePZ.cdng}')


                    elif value == 'м3/т':
                        if str(row[col - 1]).replace('.', '').replace(',', '').isdigit():
                            CreatePZ.gaz_f_pr.append(float((str(row[col - 1]).replace(',', ''))))


                    elif '6. Конструкция хвостовика' in str(value):
                        CreatePZ.data_column_additional = ws.cell(row=row_ind + 3, column=col + 2).value

                        if CreatePZ.if_None(CreatePZ.data_column_additional) != 'отсут':
                            CreatePZ.column_additional = True
                            # print(f' в скважине дополнительная колонны {CreatePZ.data_column_additional}')

                        # print(CreatePZ.column_additional)
                        if CreatePZ.column_additional == True:
                            try:
                                CreatePZ.head_column_additional = float(CreatePZ.data_column_additional.split('-')[0])
                            except:
                                CreatePZ.head_column_additional = ws.cell(row=row_ind + 3, column=col + 2).value
                            try:
                                CreatePZ.shoe_column_additional = float(CreatePZ.data_column_additional.split('-')[1])
                                # print(f'доп колонна {CreatePZ.shoe_column_additional}')
                            except:
                                CreatePZ.shoe_column_additional= ws.cell(row=row_ind + 3, column=col + 3).value
                            try:
                                if ws.cell(row=row_ind + 3, column=col + 4).value.split('x') == 2:
                                    CreatePZ.column_additional_diametr = CreatePZ.without_b(
                                        ws.cell(row=row_ind + 3, column=col + 4).value.split('x')[0])
                                    CreatePZ.column_additional_wall_thickness = CreatePZ.without_b(
                                        ws.cell(row=row_ind + 3, column=col + 4).value.split('x')[1])
                            except:
                                pass
                            try:
                                CreatePZ.column_additional_diametr = float(
                                    CreatePZ.without_b(ws.cell(row=row_ind + 3, column=col + 4).value))
                                # print(f' диаметр доп колонны {CreatePZ.column_additional_diametr}')
                            except:
                                CreatePZ.column_additional_diametr = 'не корректно'
                            try:
                                CreatePZ.column_additional_wall_thickness = float(
                                    CreatePZ.without_b(ws.cell(row=row_ind + 3, column=col + 6).value))
                                if CreatePZ.column_additional_wall_thickness == 0:
                                    CreatePZ.column_additional_wall_thickness = 'не корректно'
                            except:
                                CreatePZ.column_additional_wall_thickness = 'не корретно'


                    elif any(['вскрытия' == str(value) for value in row]) \
                            and any(['отключения' == str(value) for value in row]):

                        CreatePZ.old_version = False
                        old_index = 1

                    elif 'Максимально ожидаемое давление на устье' == value:
                        CreatePZ.max_expected_pressure = row[col + 1]
                        n = 1
                        while CreatePZ.max_expected_pressure is None:
                            CreatePZ.max_expected_pressure = row[col + n]
                            n += 1

                    elif 'плотн.' in str(value):
                        CreatePZ.water_cut = row[col - 1]  # обводненность


                    elif 'Максимально допустимое давление опрессовки э/колонны' == value or 'Максимально допустимое давление на э/колонну' == value:
                        CreatePZ.max_admissible_pressure = row[col + 1]
                        n = 1
                        while CreatePZ.max_admissible_pressure is None:
                            CreatePZ.max_admissible_pressure = row[col + n]
                            n += 1

                    elif 'Пакер' in str(value) and 'типоразмер' in str(row[col + 2]):
                        try:
                            CreatePZ.paker_do["do"] = (row[col + 4]).split('/')[0]
                            CreatePZ.paker2_do["do"] = (row[col + 4]).split('/')[1]
                        except:
                            CreatePZ.paker_do["do"] = CreatePZ.if_None(row[col + 4])
                            n = 1
                            while CreatePZ.paker_do["do"] is None:
                                CreatePZ.max_admissible_pressure = row[col + 4 + n]
                                n += 1
                        try:
                            CreatePZ.paker_do["posle"] = CreatePZ.paker_do["posle"].split('/')[0]
                            CreatePZ.paker2_do["posle"] = CreatePZ.paker_do["posle"].split('/')[1]
                        except:
                            CreatePZ.paker_do["posle"] = CreatePZ.if_None(row[col + 8 + old_index])
                            n = 0
                            while CreatePZ.paker_do["posle"] is None:
                                CreatePZ.CreatePZ.paker_do["posle"] = row[col + 8 + old_index + n]
                                n += 1

                    elif value == 'Насос' and row[col + 2] == 'типоразмер':


                        if CreatePZ.if_None(row[col + 4]) != 'отсут':
                            if ('НВ' in str(row[col + 4]).upper() or 'ШГН' in str(row[col + 4]).upper() \
                                    or 'НН' in str(row[col + 4]).upper()) or 'RHAM' in str(row[col + 4]).upper():
                                CreatePZ.dict_pump_SHGN["do"] = row[col + 4]
                                n = 0
                                while CreatePZ.dict_pump_SHGN["do"] is None:
                                    CreatePZ.dict_pump_SHGN["do"] = row[col + 4 + n]
                                    # print(f'насос ШГН {row[col + 4 + n]}')
                                    n += 1

                            if ('ЭЦН' in str(row[col + 4]).upper() or 'ВНН' in str(row[col + 4]).upper()):
                                CreatePZ.dict_pump_ECN["do"] = row[col + 4]
                                n = 0
                                while CreatePZ.dict_pump_ECN["do"] is None:
                                    CreatePZ.dict_pump_ECN["do"] = row[col + 4 + n]
                                    n += 1

                        if CreatePZ.if_None(row[col + 8 + old_index]) != 'отсут':

                            if ('НВ' in str(row[col + 8 + old_index]).upper() or 'ШГН' in str(
                                    row[col + 8 + old_index]).upper() \
                                    or 'НН' in str(row[col + 8 + old_index]).upper()) \
                                    or 'RHAM' in str(row[col + 4]).upper():
                                CreatePZ.dict_pump_SHGN["posle"] = row[col + 8 + old_index]
                                n = 0
                                while CreatePZ.dict_pump_SHGN["posle"] is None or n == 12:
                                    CreatePZ.dict_pump_SHGN["posle"] = row[col + 8 + old_index + n]
                                    n += 1
                            if ('ЭЦН' in str(row[col + 8 + old_index]).upper() or 'ВНН' in str(
                                    row[col + 8 + old_index]).upper()):
                                CreatePZ.dict_pump_ECN["posle"] = row[col + 8 + old_index]
                                n = 0
                                while CreatePZ.dict_pump_ECN["posle"] is None or n == 12:
                                    CreatePZ.dict_pump_ECN["posle"] = row[col + 8 + old_index + n]
                                    n += 1

                        # print(f' ячейка {ws.cell(row=row_ind + 5, column=col + 3).value}')

                        if ws.cell(row=row_ind + 5, column=col + 3).value == 'Нсп, м':
                            if CreatePZ.dict_pump_ECN["do"] != 0:
                                # print(f' Спуск ЭЦН ТРУ {CreatePZ.if_None(CreatePZ.dict_pump_ECN["do"])}')
                                CreatePZ.dict_pump_ECN_h["do"] = ws.cell(row=row_ind + 5, column=col + 5).value

                            if CreatePZ.dict_pump_SHGN["do"] != 0:
                                CreatePZ.dict_pump_SHGN_h["do"] = ws.cell(row=row_ind + 5, column=col + 5).value
                            if CreatePZ.dict_pump_ECN["posle"] != 0:
                                CreatePZ.dict_pump_ECN_h["posle"] = ws.cell(row=row_ind + 5,
                                                                            column=col + 9 + old_index).value
                            if CreatePZ.dict_pump_SHGN["posle"] != 0:
                                CreatePZ.dict_pump_SHGN_h["posle"] = ws.cell(row=row_ind + 5,
                                                                             column=col + 9 + old_index).value

                    elif value == 'Н посадки, м':
                        try:
                            if CreatePZ.paker_do["do"] != 0:
                                # print(CreatePZ.without_b(row[col + 2]))
                                CreatePZ.H_F_paker_do["do"] = CreatePZ.without_b(row[col + 2])[0]
                                CreatePZ.H_F_paker2_do["do"] = CreatePZ.without_b(row[col + 2])[1]
                        except:
                            if CreatePZ.paker_do["do"] != 0:
                                CreatePZ.H_F_paker_do["do"] = CreatePZ.without_b(row[col + 2])
                        try:
                            if CreatePZ.paker_do["posle"] != 0:
                                CreatePZ.H_F_paker_do["posle"] = CreatePZ.without_b(row[col + 6 + old_index])[0]
                                CreatePZ.H_F_paker2_do["posle"] = CreatePZ.without_b(row[col + 6 + old_index])[1]
                        except:
                            if CreatePZ.paker_do["posle"] != 0:
                                CreatePZ.H_F_paker_do["posle"] = CreatePZ.without_b(row[col + 6 + old_index])

                    elif "Hст " in str(value):
                        CreatePZ.static_level = row[col + 1]
                        # print()
                    elif "Ндин " in str(value):
                        CreatePZ.dinamic_level = row[col + 1]
        try:
            CreatePZ.water_cut = float(CreatePZ.water_cut)  # обводненность
            if CreatePZ.curator != 'ОР':
                CreatePZ.water_cut = CreatePZ.proc_water
            else:
                CreatePZ.water_cut = 100
        except:
            CreatePZ.water_cut, ok = QInputDialog.getInt(self, 'Обводненность',
                                                         'Введите обводненность скважинной продукции',
                                                         100,
                                                         0, 100)
        CreatePZ.region = block_name.region(cdng)
        thread = main.ExcelWorker()
        print(f'CreatePZ.region {CreatePZ.region, CreatePZ.well_number, CreatePZ.well_area}')
        CreatePZ.without_damping = thread.check_well_existence(CreatePZ.well_number, CreatePZ.well_area, CreatePZ.region)


        if len(CreatePZ.H2S_mg) == 0:
            CreatePZ.H2S_mg = CreatePZ.H2S_mg_m3

        if CreatePZ.condition_of_wells == 0:
            CreatePZ.condition_of_wells, ok = QInputDialog.getInt(self, 'индекс копирования',
                                                                  'Программа не смогла определить строку n\ III. Состояние скважины к началу ремонта ',
                                                                  0, 0, 800)

        if CreatePZ.cat_well_min == 0:
            cat_well_min, ok = QInputDialog.getInt(self, 'индекс начала копирования',
                                                   'Программа не смогла определить строку начала копирования',
                                                   0, 0, 800)
            CreatePZ.cat_well_min.append(cat_well_min)
        if CreatePZ.cat_well_max == 0:
            cat_well_max, ok = QInputDialog.getInt(self, 'индекс начала копирования',
                                                   'Программа не смогла определить строку начала копирования',
                                                   0, 0, 800)
            CreatePZ.cat_well_max = cat_well_max

        if CreatePZ.data_well_max == 0:
            CreatePZ.data_well_max, ok = QInputDialog.getInt(self, 'индекс окончания копирования',
                                                          'Программа не смогла определить строку окончания копирования',
                                                          0, 0, 800)
        if CreatePZ.data_x_max == 0:
            CreatePZ.data_x_max, _ = QInputDialog.getInt(self, 'индекс окончания копирования ожидаемых показателей',
                                                          'Программа не смогла определить строку окончания копирования'
                                                          ' ожидаемых показателей',
                                                          0, 0, 800)
        if CreatePZ.data_x_min == 0:
            CreatePZ.data_x_min = QInputDialog.getInt(self, 'индекс начала копирования ожидаемых показателей',
                                                          'Программа не смогла определить строку начала копирования'
                                                          ' ожидаемых показателей',
                                                          0, 0, 800)

        if str(CreatePZ.well_number) in ['1436', '756', '1235', '2517', '2529', '655', '2525', '751',
                                         '1371', '1293', '1420', '296', '321', '351', '186', '815', '135', '226', '377',
                                         '249']:
            QMessageBox.warning(self, 'Канатные технологии', f'Скважина согласована на канатные технологии')

        if CreatePZ.grpPlan:
            grpPlan_quest = QMessageBox.question(self, 'Подготовка к ГРП', 'Программа определела что в скважине'
                                                                           f'планируется ГРП, верно ли?')
            if grpPlan_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.grpPlan = True
            else:
                CreatePZ.grpPlan = False
        if CreatePZ.data_pvr_max == 0:
            CreatePZ.data_pvr_max = QInputDialog.getInt(self, 'Отсутствует строка', 'Отсутствует строка "II. История эксплуатации скважины". необходимо ввести окончания строки с перфорацией', 0, 10, 300)[0]
        # print(CreatePZ.dict_pump_ECN, CreatePZ.dict_pump_SHGN, CreatePZ.dict_pump_ECN_h, CreatePZ.H_F_paker_do)
        # print()
        # Определение наличия по скважине нарушений

        for row in range(CreatePZ.cat_well_min, CreatePZ.cat_well_max):
            for col in range(1, 13):
                value = str(ws.cell(row=row, column=col).value)
                if 'первая' in str(value):
                    CreatePZ.bvo = True

        for row in range(CreatePZ.data_pvr_max, CreatePZ.data_well_max):
            for col in range(1, 13):
                value = str(ws.cell(row=row, column=col).value)
                if 'нэк' in str(
                        value).lower() or 'негерм' in value.lower() or 'нарушение э' in value.lower() or 'нарушение г' in value.lower():
                    CreatePZ.leakiness_Count += 1
                    CreatePZ.leakiness = True
                if (
                        'авар' in value.lower() or 'не проход' in value.lower() or 'расхаж' in value.lower() or 'лар' in value) \
                        and 'акт о расследовании аварии прилагается' not in value:
                    CreatePZ.emergency_well = True
                    CreatePZ.emergency_count += 1

        if CreatePZ.leakiness == True:
            leakiness_quest = QMessageBox.question(self, 'нарушение колонны', 'Программа определела что в скважине'
                                                                              f'есть нарушение - {CreatePZ.leakiness_Count}, верно ли?')
            if leakiness_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.leakiness = True
                krs.get_leakiness(self)

            else:
                CreatePZ.leakiness = False

        if CreatePZ.emergency_well == True:
            emergency_quest = QMessageBox.question(self, 'Аварийные работы ', 'Программа определела что в скважине'
                                                                              f'авария - {CreatePZ.emergency_count}, верно ли?')
            if emergency_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.emergency_well = True
            else:
                CreatePZ.emergency_well = False

        if CreatePZ.gipsInWell == True:
            gips_true_quest = QMessageBox.question(self, 'Гипсовые отложения',
                                                   'Программа определела что скважина осложнена гипсовыми отложениями '
                                                   'и требуется предварительно определить забой на НКТ, верно ли это?')

            if gips_true_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.gipsInWell = True
            else:
                CreatePZ.gipsInWell = False


        # Копирование изображения
        image_loader = SheetImageLoader(ws)

        for row in range(1, CreatePZ.data_well_max):
            for col in range(1, 12):
                try:
                    image = image_loader.get(f'{get_column_letter(col)}{row}')
                    image.save(f'imageFiles/image_work/image{get_column_letter(col)}{row}.png')
                    image_size = image.size
                    image_path = f'imageFiles/image_work/image{get_column_letter(col)}{row}.png'

                    coord = f'{get_column_letter(col)}{row + 17 - CreatePZ.cat_well_min}'

                    CreatePZ.image_list.append((image_path, coord, image_size))

                except:
                    pass



        print(CreatePZ.image_list)
        print(f' ГРП - {CreatePZ.grpPlan}')
        print(f' глубина насоса ШГН {CreatePZ.dict_pump_SHGN_h}')
        print(f' насоса {CreatePZ.dict_pump_SHGN}')
        print(f'пакер {CreatePZ.paker_do}')
        print(f'глубина пакер {CreatePZ.H_F_paker_do}')
        print(f' диам колонны {CreatePZ.column_diametr}')
        print(f' гипс в скважине {CreatePZ.gipsInWell}')
        # print(
        #     f'{CreatePZ.column_additional == False},{("ЭЦН" in str(CreatePZ.dict_pump["posle"]).upper() or "ВНН" in str(CreatePZ.dict_pump["posle"][0]).upper())}')
        # print(f'Pdd {str(CreatePZ.dict_pump["posle"]).upper()}')

        # print(f'fh {CreatePZ.cat_well_min, CreatePZ.cat_well_max}')
        for row in range(CreatePZ.cat_well_min, CreatePZ.cat_well_max + 1):
            # for col in range(1, 13):
            #     print(f' строка {ws.cell(row=row, column=col).value}')
            if 'по Pпл' in str(ws.cell(row=row, column=2).value):
                for column in range(1, 13):
                    col = ws.cell(row=row, column=column).value
                    if str(col) in ['1', '2', '3']:
                        CreatePZ.cat_P_1.append(int(col))
            if 'по H2S' in str(ws.cell(row=row, column=2).value) and 'по H2S' not in str(ws.cell(row=row - 1, column=2).value):
                for column in range(1, 13):
                    col = ws.cell(row=row, column=column).value
                    # print(str(col))
                    if str(col) in ['1', '2', '3']:
                        CreatePZ.cat_H2S_list.append(int(col))
            if 'газовому фактору' in str(ws.cell(row=row, column=2).value):
                for column in range(1, 13):
                    col = ws.cell(row=row, column=column).value
                    # print(str(col))
                    if str(col) in ['1', '2', '3']:
                        CreatePZ.cat_gaz_f_pr.append(int(col))

        for row in range(CreatePZ.cat_well_min, CreatePZ.cat_well_max + 1):
            if CreatePZ.cat_H2S_list[0] in [1, 2]:
                if len(CreatePZ.H2S_mg) == 0:

                    H2S_mg = float(QInputDialog.getDouble(self, 'Сероводород',
                                                    'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)[0])
                    CreatePZ.H2S_mg.append(H2S_mg)

                if len(CreatePZ.H2S_pr) == 0:
                    H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                                    'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                    CreatePZ.H2S_mg.append(H2S_pr)



        # print(f' индекс нкт {CreatePZ.pipes_ind + 1, CreatePZ.condition_of_wells}')
        a_plan = 0

        if CreatePZ.pipes_ind == 0:
            CreatePZ.pipes_ind, ok = QInputDialog.getDouble(self, 'Индекс НКТ до ремонта',
                                                        'Программа не могла определить начала строки с ПЗ НКТ - до ремонта')
        for row in range(CreatePZ.pipes_ind + 1, CreatePZ.condition_of_wells):  # словарь  количества НКТ и метраж
            if ws.cell(row=row, column=3).value == 'План' or str(
                    ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                a_plan = row
        if a_plan == 0:
            a_plan, ok = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                                         'Программа не могла определить начала строку с ПЗ НКТ - план')
        # print(f'индекс a_plan {a_plan}')
        for row in range(CreatePZ.pipes_ind + 1, CreatePZ.condition_of_wells + 1):
            # print(str(ws.cell(row=row, column=4).value))
            key = str(ws.cell(row=row, column=4).value)
            if key != str(None) and key != '-' and "Диам" not in key:
                value = CreatePZ.without_b(ws.cell(row=row, column=7).value)
                if not key is None and row < a_plan:
                    CreatePZ.dict_nkt[key] = CreatePZ.dict_nkt.get(key, 0) + round(float(value), 1)
                elif not key is None and row >= a_plan:
                    CreatePZ.dict_nkt_po[key] = CreatePZ.dict_nkt_po.get(key, 0) + round(float(value), 1)
            # print(f'индекс a_plan {CreatePZ.dict_nkt}')
        CreatePZ.shoe_nkt = float(sum(CreatePZ.dict_nkt.values()))

        if CreatePZ.shoe_nkt > float(CreatePZ.current_bottom):
            mes = QMessageBox.warning(None, 'Ошибка', 'Башмак НКТ ниже забоя')

        # print(f' индекс штанг{CreatePZ.sucker_rod_ind, CreatePZ.pipes_ind}')
        if CreatePZ.sucker_rod_ind == 0:
            CreatePZ.sucker_rod_ind, ok = QInputDialog.getInt(self, 'Индекс штанги до ремонта',
                                             'Программа не могла определить начала строки с ПЗ штанги - до ремонта')


        if CreatePZ.sucker_rod_ind != 0:
            print(CreatePZ.sucker_rod_ind, CreatePZ.pipes_ind)
            for row in range(CreatePZ.sucker_rod_ind, CreatePZ.pipes_ind):
                if ws.cell(row=row, column=3).value == 'План' or str(
                        ws.cell(row=row, column=3).value).lower() == 'после ремонта':

                    CreatePZ.b_plan = row
                    # print(f'b_plan {CreatePZ.b_plan}')
            if CreatePZ.b_plan == 0:
                CreatePZ.b_plan, ok = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                                             'Программа не могла определить начала строку с ПЗ штанги - план')

            for row in range(CreatePZ.sucker_rod_ind + 1, CreatePZ.pipes_ind):

                key = str(ws.cell(row=row, column=4).value).replace(' ','')
                value = ws.cell(row=row, column=7).value
                if key != str(None) and key != '-' and key != '':
                    if CreatePZ.if_None(key) != 'отсут' and row < CreatePZ.b_plan:

                        CreatePZ.dict_sucker_rod[key] = CreatePZ.dict_sucker_rod.get(key, 0) + int(
                            CreatePZ.without_b(value + 1))
                    elif CreatePZ.if_None(key) != 'отсут' and row >= CreatePZ.b_plan and key:
                        CreatePZ.dict_sucker_rod_po[key] = CreatePZ.dict_sucker_rod_po.get(key, 0) + int(
                            CreatePZ.without_b(value))
                # self.dict_sucker_rod = dict_sucker_rod
                # self.dict_sucker_rod_po = dict_sucker_rod_po
        # print(f' штанги на спуск {CreatePZ.dict_sucker_rod_po}')
        # except:
        #     mes = QMessageBox.warning(self, 'Штанги отсутствуют', 'блок со штангами отсутствует')
        perforations_intervals = []

        # print(f' индекс ПВР{data_pvr_min+1, data_pvr_max + 1}')
        for row in range(data_pvr_min, CreatePZ.data_pvr_max + 2):  # Сортировка интервала перфорации
            lst = []
            # print(ws.cell(row=row, column=3).value)
            if ws.cell(row=row, column=4).value in [float, int] or \
                    str(ws.cell(row=row, column=4).value).replace('.','').replace(',','').isdigit():

                for i in range(2, 13):
                    lst.append(ws.cell(row=row, column=i).value)


                # print(ws.cell(row=row, column=6).value)
                if CreatePZ.old_version is True and isinstance(ws.cell(row=row, column=6).value, datetime) is True:
                    lst.insert(5, None)
                elif CreatePZ.old_version is True and isinstance(ws.cell(row=row, column=6).value,
                                                                 datetime) == False and not ws.cell(row=row,
                                                                                                    column=5).value is None:
                    lst.insert(5, 'отключен')
                if all([str(i).strip() == 'None' or i is None for i in lst]) == False:
                    perforations_intervals.append(lst)
        # print(f' интервалы {perforations_intervals}')
        for ind, row in enumerate(sorted(perforations_intervals, key = lambda x: x[2])):
            # print(row)
            # krovlya_perf = float(row[2])

            # print(f'кровля ПВР {krovlya_perf}')
            plast = row[0]
            if plast is None:
                plast = perforations_intervals[ind - 1][0]
                # print(f' после {plast}')
                perforations_intervals[ind][0] = perforations_intervals[ind - 1][0]

            # print(row, any([str((i)).lower() == 'проект' for i in row]), all([str(i).strip() is None for i in row]) == False)
            if any(['проект' in str((i)).lower() or 'не пер' in str((i)).lower() for i in row]) is False and all(
                    [str(i).strip() is None for i in row]) is False and krs.is_number(row[2]) is True \
                    and krs.is_number(float(str(row[3]))) is True:
                # print(f'5 {row}')

                if krs.is_number(str(row[1]).replace(',', '.')) is True:
                    CreatePZ.dict_perforation.setdefault(plast,
                                                         {}).setdefault('вертикаль',
                                                                        set()).add(float(str(row[1]).replace(',', '.')))
                if  any(['фильтр' in str(i).lower() for i in row]):
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', True)
                else:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                roof_int = round(float(str(row[2]).replace(',', '.')), 1)
                sole_int = round(float(str(row[3]).replace(',', '.')), 1)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('интервал', set()).add((roof_int, sole_int))
                CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('интервал', set()).add(
                    (roof_int, sole_int))
                # for interval in list(CreatePZ.dict_perforation[plast]["интервал"]):
                    # print(interval)
                    # print(f' эни {(interval[0],(roof_int, sole_int), interval[1])}, {interval[0] < roof_int < interval[1] or interval[0] < sole_int < interval[1]}')
                if any([interval[0] < roof_int < interval[1] or interval[0] < sole_int < interval[1] for interval in
                       list(CreatePZ.dict_perforation[plast]['интервал'])]):
                    # print(f'интервалы {CreatePZ.dict_perforation[plast]["интервал"]}')
                    for perf_int in [sorted(list(CreatePZ.dict_perforation[plast]['интервал']), key = lambda x:x[0], reverse=False),
                                     sorted(list(CreatePZ.dict_perforation[plast]['интервал']), key = lambda x:x[0], reverse=True)]:
                        for interval in sorted(perf_int):
                            # print(f'{interval[0], interval[1]},проверяемый {roof_int, sole_int}')
                            # print(interval[0] < roof_int < interval[1], interval[0] < sole_int < interval[1] )
                            if interval[0] < roof_int < interval[1] is False and interval[0] < sole_int < interval[
                                1] is False:
                                # print(f'удаление1 {roof_int, sole_int}, добавление{interval[0], sole_int}')
                                CreatePZ.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation[plast]['интервал'].add((roof_int, round(interval[1])))
                                CreatePZ.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].add((roof_int, round(interval[1],1)))

                            elif interval[0] < roof_int < interval[1] is False and interval[0] < sole_int < interval[1]:
                                # print(f'удаление2 {roof_int, sole_int}, добавление{interval[0], sole_int}')
                                CreatePZ.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation[plast]['интервал'].add((round(interval[0], 1), sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].add((round(interval[0],1), sole_int))

                            elif interval[0] < roof_int < interval[1] and interval[0] < sole_int < interval[1] is False:
                                # print(f'удаление3 {roof_int, sole_int}, добавление{roof_int, round(interval[1],1)}')
                                CreatePZ.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation[plast]['интервал'].add((roof_int, round(interval[1],1)))
                                CreatePZ.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].add((roof_int, round(interval[1],1)))

                            elif interval[0] < roof_int < interval[1] and interval[0] < sole_int < interval[1]:
                                # print(f'удаление {roof_int, sole_int}')
                                CreatePZ.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))


                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('вскрытие', set()).add(row[4])
                # print(f'отключе {isinstance(row[5], datetime) == True, old_index} ggg {isinstance(row[6], datetime) == True, CreatePZ.old_version, old_index}')
                if row[5] is None or row[5] == '-':
                    # print(f'отключение {plast, row[5], row[5] != "-"}')
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', False)

                else:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', True)
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', True)

                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                if row[8] != None:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('удлинение', set()).add(row[8])

                zhgs = 1.01
                if str(row[9]).replace(',','').replace('.', '').isdigit() and row[1]:
                    data_p = float(str(row[9]).replace(',','.'))
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('давление',
                                                                               set()).add(round(data_p, 1))
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     set()).add(round(data_p, 1))
                    zhgs = krs.calculationFluidWork(float(row[1]), float(data_p))
                else:
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     set()).add('0')
                if zhgs:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(zhgs)
                if row[10]:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('замер', set()).add(row[10])





            elif any([str((i)).lower() == 'проект' for i in row]) == True and all(
                    [str(i).strip() is None for i in row]) == False and krs.is_number(row[2]) == True \
                    and krs.is_number(float(str(row[2]).replace(',', '.'))) == True:  # Определение проектных интервалов перфорации
                if row[1] != None:
                    CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('вертикаль',
                                                                                       set()).add(round(float(row[1]), 1))
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('интервал', set()).add(
                    (round(float(str(row[2]).replace(',', '.')), 1), round(float(str(row[3]).replace(',', '.')), 1)))
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                if row[8] != None:
                    CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('удлинение', set()).add(round(float(row[8]), 1))
                if row[9] != None:
                    # print(f'давление {row[9]}')
                    CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('давление', set()).add(
                        round(float(row[9]), 1))
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(
                    krs.calculationFluidWork(row[1], row[9]))

            # print(f'проект{CreatePZ.dict_perforation_project[plast]}')
        # print(f'раб{CreatePZ.dict_perforation}')

        # print(f'до {CreatePZ.dict_perforation}')

        CreatePZ.dict_perforation_project = self.dict_perforation_project
        if len(CreatePZ.dict_perforation_project) != 0:
            CreatePZ.plast_project = list(CreatePZ.dict_perforation_project.keys())


        # Определение работающих интервалов перфорации и заполнения в словарь
        # вызов окна для проверки корректности данных
        if self.data_window is None:
            self.data_window = DataWindow(self)
            self.data_window.setWindowTitle("Сверка данных")
            self.data_window.setGeometry(200, 400, 300, 400)

            self.data_window.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            self.data_window = None


        if CreatePZ.shoe_column < CreatePZ.current_bottom and CreatePZ.column_additional is False:
            CreatePZ.open_trunk_well = True
        elif CreatePZ.shoe_column_additional < CreatePZ.current_bottom and CreatePZ.column_additional:
            CreatePZ.open_trunk_well = True

        CreatePZ.nkt_diam = 73 if CreatePZ.column_diametr > 110 else 60
        CreatePZ.nkt_template = 59.6 if CreatePZ.column_diametr > 110 else 47.9
        print(CreatePZ.nkt_template)

        curator_list = ['ОР', 'ГТМ', 'ГРР', 'ГО', 'ВНС']
        curator = ['ГТМ'
                   if (CreatePZ.dict_pump_SHGN["posle"] != 0 and CreatePZ.dict_pump_ECN["posle"] == 0)
                      or (CreatePZ.dict_pump_SHGN["posle"] == 0 and CreatePZ.dict_pump_ECN["posle"] != 0)
                      or (CreatePZ.dict_pump_SHGN["posle"] != 0 and CreatePZ.dict_pump_ECN["posle"] != 0)
                   else 'ОР'][0]

        CreatePZ.curator, ok = QInputDialog.getItem(None, 'Выбор кураторов ремонта', 'Введите сектор кураторов региона',
                                                    curator_list, curator_list.index(curator), False)
        # print(f'куратор {CreatePZ.curator, CreatePZ.if_None(CreatePZ.dict_pump["posle"])}')

        CreatePZ.definition_plast_work(self)
        print(f'работающие пласты {CreatePZ.plast_work}')
        print(f'кровля , подошва пласты {CreatePZ.perforation_sole}')

        try:
            if CreatePZ.curator == 'ОР':
                for row in range(CreatePZ.data_x_min + 2, CreatePZ.data_x_max + 1):
                    for col in range(1, 12):

                        if 'прием' in str(ws.cell(row=row, column=col).value).lower() or 'qж' in str(
                                ws.cell(row=row, column=col).value).lower():
                            Qpr = ws.cell(row=row, column=col + 1).value
                            # print(f' приемис {Qpr}')
                            n = 1
                            while Qpr is None:
                                ws.cell(row=row, column=col + n).value
                                n += 1
                                Qpr = ws.cell(row=row, column=col + n).value
                            CreatePZ.expected_Q = Qpr
                        elif 'зак' in str(ws.cell(row=row, column=col).value).lower() or 'давл' in str(
                                ws.cell(row=row, column=col).value).lower() or 'P' in str(
                            ws.cell(row=row, column=col).value).lower():
                            # print('lfdktybt pfrf')
                            Pzak = ws.cell(row=row, column=col + 1).value
                            n = 1
                            while Pzak is None:
                                n += 1
                                Pzak = ws.cell(row=row, column=col + n).value
                            CreatePZ.expected_P = Pzak

                    CreatePZ.expected_pick_up[Qpr] = Pzak
                    print(f' ожидаемые показатели {CreatePZ.expected_pick_up}')
            else:
                for row in range(CreatePZ.data_x_min + 2, CreatePZ.data_x_max + 1):
                    for col in range(1, 12):
                        if 'qж' in str(ws.cell(row=row, column=col).value).strip().lower():
                            Qwater = ws.cell(row=row, column=col + 1).value
                            # print(f' приемис {Qpr}')
                            n = 1
                            while Qwater is None or n > 12:
                                n += 1
                                Qwater = ws.cell(row=row, column=col + n).value
                            CreatePZ.Qwater = Qwater
                        elif 'qн' in str(ws.cell(row=row, column=col).value).strip().lower():
                            Qoil = ws.cell(row=row, column=col + 1).value
                            # print(f' приемис {Qpr}')
                            n = 1
                            while Qoil is None or n > 12:
                                n += 1
                                Qoil = ws.cell(row=row, column=col + n).value
                            CreatePZ.Qoil = Qoil
                        elif 'воды' in str(ws.cell(row=row, column=col).value).strip().lower():
                            proc_water = ws.cell(row=row, column=col + 1).value
                            # print(f' приемис {Qpr}')
                            n = 1
                            while proc_water is None or n > 12:
                                n += 1
                                proc_water = ws.cell(row=row, column=col + n).value
                            CreatePZ.proc_water = proc_water
        except:
            print('ошибка при определении плановых показателей')
            if CreatePZ.curator == 'OP':
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

        if work_plan != "gnkt_frez":
            if self.perforation_correct_window2 is None:
                self.perforation_correct_window2 = PerforationCorrect(self)
                self.perforation_correct_window2.setWindowTitle("Сверка данных перфорации")
                self.perforation_correct_window2.setGeometry(200, 400, 100, 400)

                self.perforation_correct_window2.show()
                CreatePZ.pause_app(self)
                CreatePZ.pause = True
                self.perforation_correct_window2 = None
                CreatePZ.definition_plast_work(self)
            else:
                self.perforation_correct_window2.close()
                self.perforation_correct_window2 = None







        if len(CreatePZ.plast_work) == 0:
            perf_true_quest = QMessageBox.question(self, 'Программа',
                                                   'Программа определили,что в скважине интервалов перфорации нет, верно ли?')
            if perf_true_quest == QMessageBox.StandardButton.Yes:
                for plast in CreatePZ.plast_all:
                    CreatePZ.dict_perforation[plast]['отключение'] = True
                    CreatePZ.dict_perforation[plast]['отрайбировано'] = False
                    CreatePZ.dict_perforation[plast]['Прошаблонировано'] = False
                    CreatePZ.dict_perforation_short = {}

            else:
                plast_work = set()
                CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                                     'Введите забой до которого нужно нормализовать')
                for plast, value in CreatePZ.dict_perforation.items():

                    perf_work_quest = QMessageBox.question(self, 'Добавление работающих интервалов перфорации',
                                                           f'Является ли данный интервал {CreatePZ.dict_perforation[plast]["интервал"]} работающим?')
                    if perf_work_quest == QMessageBox.StandardButton.No:
                        CreatePZ.dict_perforation[plast]['отключение'] = True
                    else:
                        plast_work.add(plast)
                        CreatePZ.dict_perforation[plast]['отключение'] = False
                    CreatePZ.dict_perforation[plast]['отрайбировано'] = False
                    CreatePZ.dict_perforation[plast]['Прошаблонировано'] = False
                CreatePZ.plast_work = list(plast_work)
                # print(f'все интервалы {CreatePZ.plast_all}')
                # print(f'раб интервалы {CreatePZ.plast_work}')
                CreatePZ.perforation_roof = CreatePZ.current_bottom
                for plast in CreatePZ.plast_work:
                    for interval in CreatePZ.dict_perforation[plast]['интервал']:
                        interval = list(interval)
                        if CreatePZ.perforation_roof > interval[0]:
                            CreatePZ.perforation_roof = interval[0]

                # print(f'кровля ПВР раб {CreatePZ.perforation_roof}')


        # without_damping = krs.without_damping(self)
        # print(without_damping)


        for j in range(CreatePZ.data_x_min, CreatePZ.data_x_max):  # Ожидаемые показатели после ремонта
            lst = []
            for i in range(0, 12):
                lst.append(ws.cell(row=j + 1, column=i + 1).value)
            CreatePZ.row_expected.append(lst)

        if '1' in CreatePZ.cat_P_1 or '1' in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_P_1 or 1 in CreatePZ.cat_H2S_list:
            CreatePZ.bvo = True
        # print(f'БВО {CreatePZ.bvo}')
        # print(CreatePZ.cat_P_1, CreatePZ.cat_H2S_list)

        # if CreatePZ.work_plan == 'gnkt_frez':
        #     if self.rir_window is None:
        #         CreatePZ.countAcid = 0
        #         print(f' окно2 СКО ')
        #         self.rir_window = Work_with_gnkt(ws)
        #         self.rir_window.setGeometry(200, 400, 300, 400)
        #         self.rir_window.show()
        #         CreatePZ.pause_app(self)
        #         CreatePZ.pause = True
        #         self.rir_window = None
        #     else:
        #         self.rir_window.close()  # Close window.
        #         self.rir_window is None

        if CreatePZ.work_plan != 'gnkt_frez':
            print(f'план работ {CreatePZ.work_plan}')
            plan.delete_rows_pz(self, ws)

            razdel_1 = block_name.razdel_1(self, CreatePZ.region)

            for i in range(1, len(razdel_1)):  # Добавлением подписантов на вверху
                for j in range(1, 13):
                    ws.cell(row=i, column=j).value = razdel_1[i - 1][j - 1]
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
                ws.merge_cells(start_row=i, start_column=8, end_row=i, end_column=13)
            CreatePZ.ins_ind = 0

            CreatePZ.ins_ind += CreatePZ.data_well_max - CreatePZ.cat_well_min + 19
            # print(f' индекс вставки ГНВП{CreatePZ.ins_ind}')
            dict_events_gnvp = {}
            dict_events_gnvp['krs'] = events_gnvp()
            dict_events_gnvp['gnkt_opz'] = events_gnvp_gnkt()
            dict_events_gnvp['dop_plan'] = events_gnvp()
            # if work_plan != 'dop_plan':
            text_width_dict = {20: (0, 100), 30: (101, 200), 40: (201, 300), 60: (301, 400), 70: (401, 500),
                               90: (501, 600), 110: (601, 700), 120: (701, 800), 130: (801, 900),
                               150: (901, 1500), 270: (1500, 2300)}



            for i in range(CreatePZ.ins_ind, CreatePZ.ins_ind + len(dict_events_gnvp[work_plan]) - 1):
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                data = ws.cell(row=i, column=2)
                data.value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]

                if 'Мероприятия' in str(data.value) or \
                        'Меры по предупреждению' in str(data.value) or \
                        "о недопустимости нецелевого расхода" in str(data.value):
                    data.alignment = Alignment(wrap_text=True, horizontal='center',
                                                                   vertical='center')
                    data.font = Font(name='Arial', size=13, bold=True)

                else:
                    data.alignment = Alignment(wrap_text=True, horizontal='left',
                                                                   vertical='top')
                    data.font = Font(name='Arial', size=12)

                # print(f'ГНВП -{data.value , len(data.value), len(dict_events_gnvp[work_plan])}')
                if not data.value is None:
                    text = data.value
                    for key, value in text_width_dict.items():
                        if value[0] <= len(text) <= value[1]:
                            ws.row_dimensions[i].height = int(key)

            ins_gnvp = CreatePZ.ins_ind
            CreatePZ.ins_ind += len(dict_events_gnvp[work_plan]) - 1

            ws.row_dimensions[2].height = 30
            ws.row_dimensions[6].height = 30

            # data_main_production_string = ws.cell(row=int(ind_data_main_production_string[1:])+1, column=int(ind_data_main_production_string[0])+2).value


            # print(CreatePZ.row_expected)
            if len(CreatePZ.row_expected) != 0:
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

                self.ins_ind_border = CreatePZ.ins_ind
                # wb.save(f"{CreatePZ.well_number}  1 {CreatePZ.well_area} {CreatePZ.cat_P_1}.xlsx")



            # wb.save(f'{CreatePZ.well_number} {CreatePZ.well_area} {work_plan}.xlsx')
            return ws

    def addItog(self, ws, ins_ind, work_plan):

        ws.delete_rows(ins_ind, self.table_widget.rowCount() - ins_ind + 1)
        if work_plan != 'gnkt_frez':
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
                        ws.row_dimensions[i].height = 50

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
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=False, vertical='bottom', horizontal='left')
                ws.row_dimensions[i - 1].height = 30

                if i == 1 + ins_ind + 11:
                    ws.row_dimensions[i].height = 55
        ins_ind += len(podp_down)





    def is_valid_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def if_None(value):
        if isinstance(value, datetime):
            return value
        elif value is None or 'отс' in str(value).lower() or str(value).replace(' ', '') == '-' \
                or value == 0 or str(value).replace(' ', '') == '':
            return 'отсут'
        else:
            return value

    def without_b(a):
        if isinstance(a, int) is True or isinstance(a, float) is True:
            return a
        elif a == '-' or a == 'отсутствует' or a == 'отсутв' or a == 'отсут' or a is None:
            return '0'

        elif len(a.split('/')) == 2:

            lst = []
            for i in a.split('/'):
                b = ''
                for j in i:
                    if j in '0123456789.x':
                        b = str(b) + j
                    elif j == ',':
                        b = str(b) + '.'

                lst.append(float(b))

            return lst
        elif len(a.split('-')) == 2:
            lst = []
            for i in a.split('-'):
                # print(i)
                lst.append(float(i.replace(',', '.').strip()))
            return lst[0]
        else:
            b = 0
            for i in a:
                i.replace(',', '.')
                if i in '0123456789,.x':
                    b = str(b) + i
                print(a, b)

            return float(b)

    def definition_plast_work(self):
        # Определение работающих пластов
        plast_work = set()
        perforation_roof = CreatePZ.current_bottom
        perforation_sole = 0

        for plast, value in CreatePZ.dict_perforation.items():
            for interval in value['интервал']:
                # print(f' интервалы ПВР {plast, interval[0], CreatePZ.dict_perforation[plast]["отключение"]}')
                # print(CreatePZ.perforation_roof >= interval[0])
                if CreatePZ.current_bottom >= interval[0] and CreatePZ.dict_perforation[plast]["отключение"] is False:
                    plast_work.add(plast)

                if CreatePZ.dict_perforation[plast]["отключение"] is False:
                    roof = min(list(map(lambda x: x[0], list(CreatePZ.dict_perforation[plast]['интервал']))))
                    sole = max(list(map(lambda x: x[1], list(CreatePZ.dict_perforation[plast]['интервал']))))
                    CreatePZ.dict_perforation[plast]["кровля"] = roof
                    CreatePZ.dict_perforation[plast]["подошва"] = sole
                    if perforation_roof >= roof:
                        perforation_roof = roof
                    if perforation_sole < sole:
                        perforation_sole = sole

                else:

                    CreatePZ.dict_perforation[plast]["кровля"] = \
                        min(list(map(lambda x: x[0], list(CreatePZ.dict_perforation[plast]['интервал']))))
                    CreatePZ.dict_perforation[plast]["подошва"] = \
                        max(list(map(lambda x: x[1], list(CreatePZ.dict_perforation[plast]['интервал']))))

        CreatePZ.perforation_roof = perforation_roof
        CreatePZ.perforation_sole = perforation_sole
        # print(CreatePZ.dict_perforation)
        CreatePZ.plast_all = list(CreatePZ.dict_perforation.keys())
        CreatePZ.plast_work = list(plast_work)

        if CreatePZ.column_additional:
            if CreatePZ.current_bottom > CreatePZ.shoe_column_additional:
                CreatePZ.open_trunk_well = True
            else:
                CreatePZ.open_trunk_well = False
        else:
            if CreatePZ.current_bottom > CreatePZ.shoe_column:
                CreatePZ.open_trunk_well = True
            else:
                CreatePZ.open_trunk_well = False
    def pause_app(self):
        while CreatePZ.pause == True:
            QtCore.QCoreApplication.instance().processEvents()

    def count_row_height(ws, ws2, work_list, merged_cells_dict, ind_ins):
        from openpyxl.utils.cell import range_boundaries, get_column_letter

        boundaries_dict = {}

        text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 95: (301, 400), 110: (401, 500),
                           130: (501, 600), 150: (601, 700), 170: (701, 800), 190: (801, 900), 210: (901, 1500)}
        for ind, _range in enumerate(ws.merged_cells.ranges):
            boundaries_dict[ind] = range_boundaries(str(_range))

        rowHeights1 = [ws.row_dimensions[i].height for i in range(ws.max_row)]
        colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]
        # print(colWidth)
        for i, row_data in enumerate(work_list):
            for column, data in enumerate(row_data):
                if column == 2:
                    if not data is None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                ws2.row_dimensions[i + 1].height = int(key)

        for i in range(1, len(work_list) + 1):  # Добавлением работ
            for j in range(1, 13):
                cell = ws2.cell(row=i, column=j)
                if cell and str(cell) != str(work_list[i - 1][j - 1]):
                    if str(work_list[i - 1][j - 1]).replace('.','').isdigit() and \
                            str(work_list[i - 1][j - 1]).count('.') != 2:
                        cell.value = str(work_list[i - 1][j - 1]).replace('.',',')
                        # print(f'цифры {cell.value}')
                    else:
                        cell.value = work_list[i - 1][j - 1]
                    if i >= ind_ins:
                        if j != 1:
                            cell.border = CreatePZ.thin_border
                        if j == 11:
                            cell.font = Font(name='Arial', size=11, bold=False)
                        # if j == 12:
                        #     cell.value = work_list[i - 1][j - 1]
                        else:
                            cell.font = Font(name='Arial', size=13, bold=False)
                        ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
                        ws2.cell(row=i, column=11).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')
                        ws2.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')
                        ws2.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                        vertical='center')
                        if 'примечание' in str(cell.value).lower() \
                                or 'заявку оформить за 16 часов' in str(cell.value).lower() \
                                or 'ЗАДАЧА 2.9.' in str(cell.value).upper() \
                                or 'ВСЕ ТЕХНОЛОГИЧЕСКИЕ ОПЕРАЦИИ' in str(cell.value).upper() \
                                or 'за 48 часов до спуска' in str(cell.value).upper():
                            # print('есть жирный')
                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                        elif 'порядок работы' in str(cell.value).lower() or\
                            'Наименование работ' in str(cell.value):
                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                            ws2.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')
        # print(merged_cells_dict)
        for row, col in merged_cells_dict.items():
            if len(col) != 2:
                # print(row)
                ws2.merge_cells(start_row=row+1, start_column=3, end_row=row+1, end_column=10)
        for key, value in boundaries_dict.items():
            # print(value)
            ws2.merge_cells(start_column=value[0], start_row=value[1],
                            end_column=value[2], end_row=value[3])

        head = plan.head_ind(0, ind_ins)
        # print(f'head - {head}')

        plan.copy_true_ws(ws, ws2, head)

        # вставка сохраненных изображение по координатам ячеек
        if CreatePZ.image_list:
            for img in CreatePZ.image_list:
                logo = Image(img[0])
                logo.width, logo.height = img[2][0]*0.48, img[2][1]*0.72
                ws2.add_image(logo, img[1])


        # print(f'высота строк работ {ins_ind}')
        # print(f'высота строк работ {len(rowHeights1)}')
        for index_row, row in enumerate(ws2.iter_rows()):  # Копирование высоты строки
            if all([col is None for col in row]):
                ws2.row_dimensions[index_row].hidden = True
            try:
                if index_row < ind_ins:
                    ws2.row_dimensions[index_row].height = rowHeights1[index_row]
            except:
                pass
            if index_row == 2:
                for col_ind, col in enumerate(row):
                    if col_ind <= 12:
                        ws2.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind]
        ws2.column_dimensions[get_column_letter(11)].width = 20
        ws2.column_dimensions[get_column_letter(12)].width = 20

        ws2.column_dimensions[get_column_letter(6)].width = 18



        # ws2.column_dimensions[get_column_letter(6)].width = 25

        # # Копирование изображения
        # for image in CreatePZ.image_list:
        #     ws2.add_image(image)

        return 'Высота изменена'

        # ws2.unmerge_cells(start_column=2, start_row=self.ins_ind, end_column=12, end_row=self.ins_ind)