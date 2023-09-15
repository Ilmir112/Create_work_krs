
import sys

import block_name
import main
import openpyxl as op
import self
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter

from copy import copy
from openpyxl.utils.cell import range_boundaries
# from main import MyWindow
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
from block_name import  region_p, region_dict
from cdng import events_gnvp, itog_1, events_gnvp_gnkt
import plan
from H2S import calc_H2S
from gnkt_opz import gnkt_work

class CreatePZ:
    data_well_max = 0
    razdel_1 = ''
    expected_pick_up = {}
    work_pervorations = []
    work_pervorations_dict ={}
    data = None
    cat_well_min = None
    cat_well_max = None
    data_well_min = 0
    data_well_max = 0
    data_x_min = 0
    data_x_max = 0
    data_pvr_min = 0
    data_pvr_max = 0
    head_column_additional = 0
    shoe_column_additional = 0
    column_additional_diametr = 0
    column_additional_wall_thickness = 0
    paker_do = ''
    data_column_additional = 0
    bottomhole_artificial = 0
    art_bottom_well = ''
    current_bottom = ''
    gaz_f_pr = ''
    region = ''
    well_number = 0
    well_area = ''
    column_diametr = 0
    column_wall_thickness = 0
    shoe_column = 0
    column_additional = False
    values = []
    H_F_paker_do = []
    cat_H2S_list  = []
    cat_P_1 = []
    # dict_nkt = {0: 0}
    # dict_nkt_po = {}
    # dict_nkt_po = {}
    dict_sucker_rod = {32:0, 25: 0, 22: 0, 19: 0}
    dict_sucker_rod_po = {}

    cdng = ''
    # curator = input('Введите сектор кураторов региона, ОР или ГТМ, или ГРР или ГО:  ')
    curator = 'ОР'
    sucker_rod_ind = 0
    sucker_rod = False
    sucker_rod_ind_cancel = 0
    condition_of_wells = 0
    pipes_ind = ''
    itog_ind_min = 0
    itog_ind_max = 0
    well_number = 0
    well_area = ''
    H2S_pr = []
    cat_H2S_list = []
    H2S_mg = []
    dict_nkt = {}
    dict_nkt_po = {}
    dict_sucker_rod = {}
    dict_sucker_rod_po = {}
    row_expected = []
    #     self.perforations_intervals = []
    #     self.razdel_1 = ''

    # def __init__(self, fname, cat_well_min, data_well_max, cdng):
    #     self.fname = fname
    #     self.data = None
    #     self.cat_well_min = None
    #     self.cat_well_max = None
    #     self.data_well_min = 0
    #     self.data_well_max = data_well_max
    #     self.data_x_min = 0
    #     self.data_x_max = 0
    #     self.data_pvr_min = 0
    #     self.data_pvr_max = 0
    #     self.head_column_additional = 0
    #     self.shoe_column_additional = 0
    #     self.column_additional_diametr = 0
    #     self.column_additional_wall_thickness = 0
    #     self.paker_do = ''
    #     self.data_column_additional = 0
    #     self.bottomhole_artificial = 0
    #     self.art_bottom_well = ''
    #     self.current_bottom = ''
    #     self.gaz_f_pr = ''
    #     self.region = ''
    #     self.well_number = 0
    #     self.well_area = ''
    #     self.column_diametr = 0
    #     self.column_wall_thickness = 0
    #     self.shoe_column = 0
    #     self.column_additional = False
    #     self.values = []
    #     self.H_F_paker_do = []
    #     self.cat_H2S_list  = []
    #     self.cat_P_1 = 0
    #     self.dict_nkt = {0: 0}
    #     self.dict_nkt_po = {}
    #     self.dict_sucker_rod = {32:0, 25: 0, 22: 0, 19: 0}
    #     self.dict_sucker_rod_po = {}
    #
    #     self.cdng = cdng
    #     # curator = input('Введите сектор кураторов региона, ОР или ГТМ, или ГРР или ГО:  ')
    #     curator = 'ГТМ'
    #     self.sucker_rod_ind = 0
    #     self.sucker_rod = False
    #     self.sucker_rod_ind_cancel = 0
    #     self.condition_of_wells = 0
    #     self.pipes_ind = ''
    #     self.well_number = 0
    #     self.well_area = ''
    #     self.H2S_pr = []
    #     self.cat_H2S_list = []
    #     self.H2S_mg = []
    #     self.dict_nkt = {}
    #     self.dict_nkt_po = {}
    #     self.dict_sucker_rod = {}
    #     self.dict_sucker_rod_po = {}
    row_expected = []
    #     self.perforations_intervals = []
    #     self.razdel_1 = ''

    def open_excel_file(self, fname, work_plan='gnkt_opz'):

        wb = op.load_workbook(fname, data_only=True)
        ws = wb.active

        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            if 'Категория скважины' in row:
                cat_well_min = row_ind + 1  # индекс начала категории
                print(cat_well_min)

            elif 'План-заказ' in row:
                ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'
                cat_well_max = row_ind - 1
                data_well_min = row_ind + 1

            elif 'VIII. Вид и категория ремонта, его шифр' in row:
                CreatePZ.data_well_max = row_ind + 1
            elif 'X. Ожидаемые показатели после ремонта:' in row:
                data_x_min = row_ind
            elif 'ШТАНГИ' in row:
                sucker_rod = True
                sucker_rod_ind = row_ind
                # sucker_rod_ind = self.sucker_rod_ind
            elif 'НКТ' in row:
                pipes_ind = row_ind
                # pipes_ind = self.pipes_ind
            elif 'ХI Планируемый объём работ:' in row:
                data_x_max = row_ind
            elif 'II. История эксплуатации скважины' in row:
                data_pvr_max = row_ind - 2
            elif 'III. Состояние скважины к началу ремонта ' in row:
                condition_of_wells = row_ind
            for col, value in enumerate(row):
                if 'площадь' == value:  # определение номера скважины
                    CreatePZ.well_number = row[col - 1]
                    # self.well_number = well_number
                    CreatePZ.well_area = row[col + 1]
                    # self.well_area = well_area
                elif '11. Эксплуатационные горизонты и интервалы перфорации:' == value:
                    data_pvr_min = row_ind + 2

                elif '7. Пробуренный забой' == value:
                    try:
                        CreatePZ.bottomhole_artificial = float(row[col + 5])
                        n = 1
                        while CreatePZ.bottomhole_artificial== None:
                            CreatePZ.bottomhole_artificial = row[col +5 + n]
                            n += 1
                            CreatePZ.bottomhole_artificial = float(row[col +5 + n])

                    except:
                        CreatePZ.bottomhole_artificial = float(input('Искусственный забой равен:  '))
                elif 'Текущий забой ' == value:
                    try:
                        CreatePZ.current_bottom = float(row[col + 2])
                    except:
                        CreatePZ.current_bottom = float(input('Текущий забой равен: '))
                elif 'месторождение ' == value:
                    CreatePZ.oilfield = row[col + 2]

                elif value == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':  # Определение данных по колонне

                    data_main_production_string = (ws.cell(row=row_ind + 2, column=col + 1).value).split('(мм),', )
                    if len(data_main_production_string) == 3:
                        try:
                            CreatePZ.column_diametr = float(data_main_production_string[0])
                        except:
                            CreatePZ.column_diametr = float(input('диаметр колонны основной:'))
                        try:
                            CreatePZ.column_wall_thickness = float(data_main_production_string[1][1:])
                        except:
                            CreatePZ.column_wall_thickness = float(input('Толщина стенки:'))
                        try:
                            CreatePZ.shoe_column = float(CreatePZ.without_b(data_main_production_string[2]))

                        except:
                            CreatePZ.shoe_column = float(input('Башмак колонны: '))


                elif '9. Максимальный зенитный угол' == value:
                    try:
                        CreatePZ.max_angle = row[col + 1]
                        n = 1
                        while CreatePZ.max_angle == None:
                            CreatePZ.max_angle = row[col + n]
                            n += 1
                    except:
                        CreatePZ.max_angle = float(input('Введите максимальный зенитный угол: '))


                elif '9. Максимальный зенитный угол' in row and value == 'на глубине':
                    try:
                        CreatePZ.max_h_angle = row[col + 1]
                    except:
                        CreatePZ.max_h_angle = int(input('Введите глубину максимального зетного угла: '))
                elif 'цех' == value and 'назначение ' in row:
                    cdng = row[col + 1]
                    CreatePZ.cdng = cdng




                elif 'плотн.воды' == value:
                    if CreatePZ.curator == 'ОР':
                        CreatePZ.water_cut = 100
                    else:
                        try:
                            CreatePZ.water_cut =float(row[col - 1]) # обводненность
                        except:
                            CreatePZ.water_cut = float(input('ВВедите обводненность скважинной продукции: '))
                elif 'по Pпл' == value:
                    cat_P_1 = row[col + 1]
                    n = 1
                    while cat_P_1 == None:
                        cat_P_1 = row[col + n]
                        n += 1
                    CreatePZ.cat_P_1.append(cat_P_1)
                elif 'по H2S' == value:

                    CreatePZ.cat_H2S_1 = row[col + 1]
                    n = 1
                    while CreatePZ.cat_H2S_1 == None:
                        CreatePZ.cat_H2S_1 = row[col + n]
                        n += 1
                    CreatePZ.cat_H2S_list.append(CreatePZ.cat_H2S_1)
                elif 'по газовому фактору' == value:
                    CreatePZ.cat_GF_1 = row[col + 1]
                    n = 1
                    while CreatePZ.cat_GF_1 == None:
                        CreatePZ.cat_GF_1 = row[col + n]
                        n += 1
                elif 'мг/дм3' == value or 'мг/л' == value:
                    CreatePZ.H2S_mg.append(row[col - 1])


                elif '%' == value:

                    CreatePZ.H2S_pr.append(row[col - 1])
                elif value == 'м3/т':

                    CreatePZ.gaz_f_pr = row[col - 1]

                elif '6. Конструкция хвостовика' == value:
                    CreatePZ.data_column_additional = ws.cell(row=row_ind + 3, column=col + 2).value
                    if CreatePZ.data_column_additional != None or \
                            CreatePZ.data_column_additional != '-':
                        CreatePZ.column_additional = True
                    try:
                        CreatePZ.head_column_additional = float(CreatePZ.data_column_additional.split('-')[0])

                        CreatePZ.shoe_column_additional = CreatePZ.data_column_additional.split('-')[1]
                        CreatePZ.column_additional_diametr = ws.cell(row=row_ind + 3, column=col + 4).value
                        CreatePZ.column_additional_wall_thickness = ws.cell(row=row_ind + 3, column=col + 6).value
                    except:
                        CreatePZ.head_column_additional = 0

                        CreatePZ.shoe_column_additional = 0
                        CreatePZ.column_additional_diametr = 0
                        CreatePZ.column_additional_wall_thickness = 0
                        print('Доп колонна отсутствует')

                elif 'Максимально ожидаемое давление на устье' == value:
                    try:

                        CreatePZ.max_expected_pressure = row[col + 1]
                        n = 1
                        while CreatePZ.max_expected_pressure == None:
                            CreatePZ.max_expected_pressure = row[col + n]
                            n += 1

                    except:
                        CreatePZ.max_expected_pressure = int(input('Введите максимально ожидамое давление на устье: '))

                elif 'Максимально допустимое давление опрессовки э/колонны' == value:
                    try:
                        CreatePZ.max_admissible_pressure = row[col + 1]
                        n = 1
                        while CreatePZ.max_admissible_pressure == None:
                            CreatePZ.max_admissible_pressure = row[col + n]
                            n += 1
                    except:
                        CreatePZ.max_admissible_pressure = int(input('Введите максимально ожидаемое давление на устье: '))
                elif value == 'Пакер' and row[col + 2] == 'типоразмер':
                    CreatePZ.paker_do = row[col + 4]
                    try:
                        CreatePZ.H_F_paker_do = int(ws.cell(row=row_ind + 4, column=col + 5).value)
                    except:
                        CreatePZ.H_F_paker_do =int(input('Глубина посадки фондового пакера: '))


        for row in range(data_x_min + 1, data_x_max):
            expected_list = []
            for col in range(1, 12):

                if ws.cell(row= row, column = col).value != None:
                    if ws.cell(row= row, column = col).value.isnumeric() == True:
                        expected_list.append(ws.cell(row= row, column = col).value)
            if len(expected_list) !=0:
                CreatePZ.expected_pick_up[expected_list[0]] = expected_list[1]




        for row in range(pipes_ind + 1, condition_of_wells):  # словарь  количества НКТ и метраж
            if ws.cell(row=row, column=3).value == 'План':
                a_plan = row
        dict_nkt ={}
        dict_nkt_po = {}
        for row in range(pipes_ind + 1, condition_of_wells):
            key = ws.cell(row=row, column=4).value
            value = ws.cell(row=row, column=7).value
            if key != None and row < a_plan:
                dict_nkt[key] = dict_nkt.get(key, 0) + value
            if key != None and row >= a_plan:
                dict_nkt_po[key] = dict_nkt_po.get(key, 0) + value
        CreatePZ.dict_nkt =dict_nkt
        CreatePZ.dict_nkt_po = dict_nkt_po

        try:
            for row in range(sucker_rod_ind, pipes_ind - 1):
                if ws.cell(row=row, column=3).value == 'План':
                    b_plan = row
            for row in range(sucker_rod_ind + 1, pipes_ind - 1):
                key = ws.cell(row=row, column=4).value
                value = ws.cell(row=row, column=7).value
                if key != None and row < b_plan:
                    print(key)
                    self.dict_sucker_rod[key] = self.dict_sucker_rod.get(key, 0) + value
                    if key != None and row >= b_plan:
                        self.dict_sucker_rod_po[key] = self.dict_sucker_rod_po.get(key, 0) + value
                # self.dict_sucker_rod = dict_sucker_rod
                # self.dict_sucker_rod_po = dict_sucker_rod_po
        except:
            print('штанги отсутствуют')
        perforations_intervals = []
        for j in range(data_pvr_min, data_pvr_max):  # Сортировка интервала перфорации
            lst = []
            for i in range(1, 12):
                if type(ws.cell(row=j + 1, column=i + 1).value) == float:
                    lst.append(round(ws.cell(row=j + 1, column=i + 1).value, 1))
                else:
                    lst.append(ws.cell(row=j + 2, column=i + 1).value)
            perforations_intervals.append(lst)
        perforations_intervals = sorted(perforations_intervals, key=lambda x: x[3])


        for row in perforations_intervals:
            if int(row[2]) > CreatePZ.H_F_paker_do and row[5] == None:
                CreatePZ.work_pervorations.append(row)
                CreatePZ.work_pervorations_dict[row[2]] = row[3]
        print(CreatePZ.work_pervorations_dict)

        CreatePZ.region = block_name.region(cdng)

        razdel_1 = block_name.razdel_1(self, CreatePZ.region)


        wb2 = op.Workbook()
        ws2 = wb2.get_sheet_by_name('Sheet')
        ws2.title = "План работ"


        bound = []
        for _range in ws.merged_cells.ranges:
            boundaries = range_boundaries(str(_range))
            if data_pvr_min + 2 <= boundaries[1] <= data_pvr_max + 2:
                bound.append(boundaries)
                # ws2.unmerge_cells(start_column=boundaries[0], start_row=boundaries[1] + len(self.razdel_1) + 1,
                #                end_column=boundaries[2], end_row=boundaries[3] + len(self.razdel_1) + 1)
            elif boundaries[1] >= CreatePZ.data_well_max + 3:
                bound.append(boundaries)
            else:
                ws2.merge_cells(start_column=boundaries[0], start_row=boundaries[1] + len(razdel_1) + 1,
                                end_column=boundaries[2], end_row=boundaries[3] + len(razdel_1) + 1 )
        for i in range(12, 22):
            ws2.row_dimensions[i].height = 5
        for i in range(1, len(razdel_1)):  # Добавлением подписантов на вверху
            for j in range(1, 13):
                ws2.cell(row=i, column=j).value = razdel_1[i - 1][j - 1]
                ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
            ws2.merge_cells(start_row=i, start_column=8, end_row=i, end_column=13)
        ins_ind = len(razdel_1) + cat_well_min

        list_block = [cat_well_min, data_well_min + 1, CreatePZ.data_well_max]
        print(list_block)

        for i in range(1, len(list_block)):  # цикл добавления блоков план-заказов
            head = plan.head_ind(list_block[i - 1], list_block[i] + 2)
            name_values = razdel_1
            index_row = list_block[i - 1]
            ins_ind += (list_block[i] + 2 - list_block[i - 1])

            plan.copy_row(ws, ws2, name_values, index_row, head)


        thin_border = Border(left=Side(style='thin'),
                             right=Side(style='thin'),
                             top=Side(style='thin'),
                             bottom=Side(style='thin'))

        for i in range(1, len(perforations_intervals) + 1):  # Добавление данных по интервалу перфорации
            for j in range(1, 12):
                ws2.cell(row=i + data_pvr_min + len(razdel_1) + 2, column=j + 1).border = thin_border
                ws2.cell(row=i + data_pvr_min + len(razdel_1) + 2, column=j + 1).font = 'Arial'
                ws2.cell(row=i + data_pvr_min + len(razdel_1) + 2, column=j + 1).alignment = Alignment(
                    wrap_text=True)
                ws2.cell(row=i + data_pvr_min + len(razdel_1) + 2, column=j + 1).value = \
                    perforations_intervals[i - 1][j - 1]


        dict_events_gnvp = {}
        dict_events_gnvp['krs'] = events_gnvp
        dict_events_gnvp['gnkt_opz'] =events_gnvp_gnkt
        for i in range(ins_ind, ins_ind + len(dict_events_gnvp[work_plan])-1):
            ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)


            if i == (ins_ind + 13 or i == ins_ind + 28) and work_plan == 'krs':
                print(work_plan == 'krs')
                ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                    vertical='center')
                ws2.cell(row=i, column=2).font = Font(name='Arial', size=13, bold=True)
                ws2.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - ins_ind][1]
            elif i == ins_ind + 11 and work_plan == 'gnkt_opz':
                print(work_plan)
                ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                    vertical='center')
                ws2.cell(row=i, column=2).font = Font(name='Arial', size=11, bold=True)
                ws2.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - ins_ind][1]
            else:
                ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                    vertical='top')
                ws2.cell(row=i, column=2).font = Font(name='Arial', size=12)

                ws2.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - ins_ind][1]
        ins_ind += len(dict_events_gnvp[work_plan]) - 1




        ws2.row_dimensions[2].height = 30
        ws2.row_dimensions[6].height = 30

        # data_main_production_string = ws.cell(row=int(ind_data_main_production_string[1:])+1, column=int(ind_data_main_production_string[0])+2).value
        CreatePZ.insert_gnvp(ws, ws2, work_plan)

        for j in range(data_x_min, data_x_max):  # Ожидаемые показатели после ремонта
            lst = []
            for i in range(0, 12):
                lst.append(ws.cell(row=j + 1, column=i + 1).value)
            CreatePZ.row_expected.append(lst)

        for i in range(len(CreatePZ.row_expected)):  # Добавление  показатели после ремонта
            for j in range(1, 12):
                if i == 1:
                    ws2.cell(row=i + ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                    ws2.cell(row=i + ins_ind, column=j).alignment = Alignment(wrap_text=False, horizontal='left',
                                                                                   vertical='center')
                    ws2.cell(row=i + ins_ind, column=j).value = CreatePZ.row_expected[i - 1][j - 1]
                else:
                    ws2.cell(row=i + ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                    ws2.cell(row=i + ins_ind, column=j).alignment = Alignment(wrap_text=False, horizontal='left',
                                                                                   vertical='center')
                    ws2.cell(row=i + ins_ind, column=j).value = CreatePZ.row_expected[i - 1][j - 1]
        ws2.merge_cells(start_column=2, start_row=ins_ind + 1, end_column=12, end_row=ins_ind + 1)
        if 2 in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_H2S_list:
            H2S = True
        else:
            H2S = False

        gnkt_work1 = gnkt_work(self, CreatePZ.H_F_paker_do, H2S, CreatePZ.max_expected_pressure, CreatePZ.max_admissible_pressure)

        ins_ind += 3
        CreatePZ.count_row_height(ws2, gnkt_work1, ins_ind)
        CreatePZ.itog_ind_min = ins_ind
        for i in range(ins_ind + 1 , len(gnkt_work1) + ins_ind ):  # Добавлением работ

            for j in range(1, 13):
                ws2.cell(row=i, column=j).value = gnkt_work1[i - ins_ind-1][j - 1]

                if j != 1:
                    ws2.cell(row=i, column=j).border = thin_border
                if j == 11:
                    ws2.cell(row=i, column=j).font = Font(name='Arial', size=12, bold=False)
                else:
                    ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            if i ==  ins_ind+1:
                ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                               vertical='center')

            elif i == ins_ind+2:
                ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=10)
                ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                vertical='center')
            else:
                ws2.merge_cells(start_row=i, start_column=3, end_row=i, end_column=10)
            ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                           vertical='center')
            ws2.cell(row=i, column=11).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                           vertical='center')
            ws2.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                            vertical='center')
            ws2.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                           vertical='center')


        ins_ind += len(gnkt_work1) -3
        CreatePZ.itog_ind_max = ins_ind
        for i in range(ins_ind + 2 + 1, len(itog_1()) + ins_ind + 2):  # Добавлением итогов
            if i < ins_ind + 2 + 1 +6:
                for j in range(1, 13):
                    ws2.cell(row=i, column=j).value = itog_1()[i - ins_ind - 2 - 1][j - 1]
                    if j != 1:
                        ws2.cell(row=i, column=j).border = thin_border
                        ws2.cell(row=i, column=j).font =  Font(name='Arial', size=13, bold=False)
                ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=11)
                ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                               vertical='center')
            else:
                for j in range(1, 13):
                    ws2.row_dimensions[i].height = 55
                    ws2.cell(row=i, column=j).value = itog_1()[i - ins_ind - 2 - 1][j - 1]
                    ws2.cell(row=i, column=j).border = thin_border
                    ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                    ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                    vertical='center')

                ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                ws2.cell(row=i + ins_ind, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                               vertical='center')

        ins_ind += len(itog_1()) + 2

        curator_sel = block_name.curator_sel(self, CreatePZ.curator, CreatePZ.region)
        curator_ved_sel = block_name.curator_sel(self, CreatePZ.curator, CreatePZ.region)
        podp_down = block_name.pop_down(self, CreatePZ.region,curator_sel, curator_ved_sel)
        for i in range(1 + ins_ind, 1 + ins_ind + len(podp_down)):  # Добавлением подписантов внизу
            for j in range(1, 13):
                ws2.cell(row=i, column=j).value = podp_down[i - 1 - ins_ind][j - 1]
                ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            if i in [1 + ins_ind + 7, 1 + ins_ind + 8, 1 + ins_ind + 9, 1 + ins_ind +10, 1 + ins_ind + 11, 1 + ins_ind + 12, 1 + ins_ind + 13, 1 + ins_ind + 14]:
                ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=5)
                ws2.cell(row = i, column = 2).alignment = Alignment(wrap_text=True, vertical= 'top', horizontal= 'left')
                if i == 1 + ins_ind + 11:
                    ws2.row_dimensions[i].height = 55

        # for row in range(1, 16):
        #    for col in range(1, 13):
        #         ws2.cell(row = row, column = col).alignment = ws2.cell(row = row, column = col).alignment.copy(wrapText=True)
        #         ws2.cell(row= row, column=j + col).font = 'Arial'
        # lst2 = []
        # for j in range(1, max_rows):
        #     lst3 = []
        #     for i in range(1, 13):
        #         lst3.append(ws2.cell(row=j, column = i).value)
        #     lst2.append(lst3)
        #

        if 2 in CreatePZ.cat_H2S_list or '2' in CreatePZ.cat_H2S_list:
            print(CreatePZ.H2S_pr, CreatePZ.H2S_mg)
            calc_H2S(wb2, CreatePZ.H2S_pr, CreatePZ.H2S_mg)


        else:

            print(f'{CreatePZ.cat_H2S_list} Расчет поглотителя сероводорода не требуется')


        wb2.save(f'{CreatePZ.well_number} {CreatePZ.well_area} {work_plan}.xlsx')
        return ws2




    def insert_gnvp(ws, ws2, work_plan):
        rowHeights_gnvp = [95.0, 155.5, 110.25, 36.0, 52.25, 36.25, 36.0, 45.25, 20.25, 135.75, 38.5, 30.25, 30.5,
                           18.0, 50.5, 21.75, 240.75, 125.0, 66.75, 48.0, 33.0, 38.25, 45.0, 32.25, 45.75, 30.75, 32.25,
                           310.0, 21.75, 50.25, 57.25, 78.75, 64.5, 25.0, 25.0, 25.0, 25.0]
        rowHeights_gnvp_opz = [95.0, 155.5, 36, 36.0, 52.25, 20.25, 20.0, 120.25, 36.25, 36.75, 20.5, 20.25, 20.5,
                               110.0, 60.5, 46.75, 36.75, 36.0, 36.75, 48.0, 36.0, 38.25, ]
        dict_rowHeights ={}
        dict_rowHeights['krs'] = rowHeights_gnvp
        dict_rowHeights['gnkt_opz'] = rowHeights_gnvp_opz
        rowHeights = [ws.row_dimensions[i + 1].height for i in range(CreatePZ.data_well_max + 2)]  + dict_rowHeights[work_plan]

        colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]
        # print(f' f {len(dict_rowHeights[work_plan])}')
        for index_row, row in enumerate(ws2.iter_rows()):  # Копирование высоты строки
            if len(rowHeights) >= index_row:
                ws2.row_dimensions[index_row + len(block_name.razdel_1(self, CreatePZ.region)) + 1].height = rowHeights[index_row - 1]
            for col_ind, col in enumerate(row):

                if col_ind <= 12:
                    ws2.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind]
                else:
                    break

    def without_b(a):
        b = ''
        for i in range(len(a)):
            if a[i] in '0123456789':
                b += a[i]
        return b

    def count_row_height(ws2, values, ins_int):
        row_count = []
        for row in values:
            count_val = []
            for col in row:
                if col != None:
                    count_val.append(len(str(col)))
                else:
                    count_val.append(2)
            row_count.append(max(count_val)/4.7)

        for index_row, row in enumerate(row_count):  # Копирование высоты строки
            if row_count[index_row - 1] >40:
                ws2.row_dimensions[index_row +  ins_int].height = row_count[index_row - 1]

        ws2.column_dimensions[get_column_letter(11)].width = 25

        return 'Высота изменена'

        # ws2.unmerge_cells(start_column=2, start_row=self.ins_ind, end_column=12, end_row=self.ins_ind)
fname = 'Копия 2327 Манчаровского м-я (ПЗ) 11092023.xlsx'
print(CreatePZ.open_excel_file(fname, fname, work_plan='gnkt_opz'))
