import sys

import block_name
import main
import krs
import openpyxl as op
import self
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from PyQt6.QtWidgets import QInputDialog, QMessageBox


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


class CreatePZ:
    head_column_additional = 0
    shoe_column_additional = 0
    column_additional_diametr = 0
    column_additional_wall_thickness = 0
    expected_pick_up = {}
    work_pervorations = []
    work_pervorations_dict = {}
    paker_do = {}
    column_additional = False
    values = []
    H_F_paker_do = {}
    H_F_paker_do['do'] = 0
    H_F_paker_do['posle'] = 0


    len_razdel_1 = 0

    cat_P_1 = []
    dict_sucker_rod = {32: 0, 25: 0, 22: 0, 19: 0}
    dict_sucker_rod_po = {}
    H2S_pr = []
    cat_H2S_list = []
    H2S_mg = []
    dict_nkt = {}
    dict_nkt_po = {}
    dict_sucker_rod = {}
    dict_sucker_rod_po = {}
    row_expected = []
    rowHeights = []
    old_version = False
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    def open_excel_file(self, fname, work_plan):

        wb = load_workbook('fname, data_only=True')
        ws = wb.active
        CreatePZ.image_finder = wb.drawing.drawings_finder

        curator_list = ['ОР', 'ГТМ', 'ГРР', 'ГО']
        # curator = 'ОР'
        curator, ok = QInputDialog.getItem(self, 'Выбор кураторов ремонта', 'Введите сектор кураторов региона',
                                            curator_list, 0, False)
        if ok and curator:
           CreatePZ.curator = curator
        else:
            QMessageBox.information(self, 'fdf', 'qqwq')

        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            ws.row_dimensions[row_ind].hidden = False
            if 'Категория скважины' in row:
                CreatePZ.cat_well_min = row_ind + 1  # индекс начала категории
                print(f'индекс категории {CreatePZ.cat_well_min}')

            elif 'План-заказ' in row:
                ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'
                cat_well_max = row_ind - 1
                data_well_min = row_ind + 1

            elif 'IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in row or 'IX. Мероприятия по предотвращению аварий, инцидентов и осложнений:' in row:
                CreatePZ.data_well_max = row_ind
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
                    index_bottomhole = row_ind
                    try:
                        CreatePZ.bottomhole_artificial = float(row[col + 5])
                        n = 1
                        while CreatePZ.bottomhole_artificial == None:
                            CreatePZ.bottomhole_artificial = row[col + 5 + n]
                            n += 1
                            CreatePZ.bottomhole_artificial = float(row[col + 5 + n])

                    except:
                        CreatePZ.bottomhole_artificial, ok = QInputDialog.getDouble(self, 'Искусственный забой', 'Введите искусственный забой по скважине, 1000, 50, 4000, 1)  ')
                elif 'Текущий забой ' == value:
                    try:
                        CreatePZ.current_bottom = float(row[col + 2])
                    except:
                        CreatePZ.current_bottom, ok = QInputDialog.getDouble(self,'Текущий забоя', 'Введите Текущий забой равен', 1000, 1, 4000, 1)
                elif 'месторождение ' == value:
                    CreatePZ.oilfield = row[col + 2]

                elif value == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':  # Определение данных по колонне

                    data_main_production_string = (ws.cell(row=row_ind + 2, column=col + 1).value).split('(мм),', )
                    if len(data_main_production_string) == 3:
                        try:
                            CreatePZ.column_diametr = float(data_main_production_string[0])
                        except:
                            CreatePZ.column_diametr = QInputDialog.getInt(self, 'диаметр основной колонны', 'Введите диаметр основной колонны', 146, 80, 276)
                        try:
                            CreatePZ.column_wall_thickness = float(data_main_production_string[1][1:])
                        except:
                            CreatePZ.column_wall_thickness = QInputDialog.getDouble(self, 'Толщина стенки', 'Введите толщины стенки ЭК', 7.7, 5, 15, 1)
                        try:
                            CreatePZ.shoe_column = float(CreatePZ.without_b(data_main_production_string[2]))

                        except:
                            CreatePZ.shoe_column = QInputDialog.getInt(self, 'Башмак колонны: ',  'Башмак колонны: ', 1000, 20, 4000, 1)


                elif '9. Максимальный зенитный угол' == value:
                    try:
                        CreatePZ.max_angle = row[col + 1]
                        n = 1
                        while CreatePZ.max_angle == None:
                            CreatePZ.max_angle = row[col + n]
                            n += 1
                    except:
                        CreatePZ.max_angle, ok = QInputDialog.getDouble(self, 'Максимальный зенитный угол /'
                                                                          '','Введите максимальный зенитный угол', 25, 1, 100, 2)

                elif '9. Максимальный зенитный угол' in row and value == 'на глубине':
                    try:
                        CreatePZ.max_h_angle = row[col + 1]
                    except:
                        CreatePZ.max_h_angle, ok = QInputDialog.getint(self, 'Глубина максимального угла', 'Введите глубину максимального зетного угла: ', 500, 1, 4000)
                elif 'цех' == value and 'назначение ' in row:
                    cdng = row[col + 1]
                    CreatePZ.cdng = cdng

                elif 'плотн.воды' == value:
                    if CreatePZ.curator == 'ОР':
                        CreatePZ.water_cut = 100 # Обводненность скважины
                    else:
                        try:
                            CreatePZ.water_cut = float(row[col - 1])  # обводненность
                        except:
                            CreatePZ.water_cut = QInputDialog.getInt(self, 'Обводненность', 'Введите обводненность скважинной продукции', 50, 0, 100)
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
                    CreatePZ.cat_H2S_list.append(int(CreatePZ.cat_H2S_1))
                elif 'по газовому фактору' == value:
                    CreatePZ.cat_GF_1 = row[col + 1]
                    n = 1
                    while CreatePZ.cat_GF_1 == None:
                        CreatePZ.cat_GF_1 = row[col + n]
                        n += 1

                elif value == 'м3/т':
                    CreatePZ.gaz_f_pr = row[col - 1]

                elif '6. Конструкция хвостовика' == value:
                    column_add_index = row_ind + 3
                    CreatePZ.data_column_additional = ws.cell(row=row_ind + 3, column=col + 2).value
                    # print(f'хв{CreatePZ.data_column_additional}, {CreatePZ.column_additional, CreatePZ.without_b(CreatePZ.data_column_additional)}')
                    if isinstance(CreatePZ.without_b(CreatePZ.data_column_additional), int) == True:
                        CreatePZ.column_additional = True
                    print(CreatePZ.column_additional)
                    if CreatePZ.column_additional == True:
                        try:
                            CreatePZ.head_column_additional = float(CreatePZ.data_column_additional.split('-')[0])
                        except:
                            CreatePZ.head_column_additional, ok = QInputDialog.getInt(self, 'голова доп колонны', 'введите глубину головы доп колонны', 600, 0, 3500)
                        try:
                            CreatePZ.shoe_column_additional = CreatePZ.data_column_additional.split('-')[1]
                        except:
                            CreatePZ.shoe_column_additional, ok = QInputDialog.getInt(self, ',башмак доп колонны', 'введите глубину башмак доп колонны', 600, 0, 3500)
                        try:
                            CreatePZ.column_additional_diametr = ws.cell(row=row_ind + 3, column=col + 4).value
                        except:
                            CreatePZ.column_additional_diametr, ok = QInputDialog.getInt(self, ',диаметр доп колонны', 'введите внешний диаметр доп колонны', 600, 0, 3500)
                        try:
                            CreatePZ.column_additional_wall_thickness = ws.cell(row=row_ind + 3, column=col + 6).value
                        except:
                            CreatePZ.column_additional_wall_thickness, ok = QInputDialog.getInt(self, ',толщина стенки доп колонны', 'введите толщину стенки доп колонны', 600, 0, 3500)
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
                        CreatePZ.max_expected_pressure, ok = QInputDialog.getInt(self, 'Максимальное ожидаемое давление', 'Введите максимально ожидамое давление на устье: ', 80, 0, 200)

                elif 'Максимально допустимое давление опрессовки э/колонны' == value:
                    try:
                        CreatePZ.max_admissible_pressure = row[col + 1]
                        n = 1
                        while CreatePZ.max_admissible_pressure == None:
                            CreatePZ.max_admissible_pressure = row[col + n]
                            n += 1
                    except:
                        CreatePZ.max_admissible_pressure, ok = QInputDialog.getInt(self, 'Максимальное допустимое давление опрессовки э/колонны', 'Введите максимально допустимое давление опрессовки э/колонны: ', 80, 0, 200)

                elif value == 'Пакер' and row[col + 2] == 'типоразмер':
                    CreatePZ.paker_do['do'] = row[col + 4]
                    if CreatePZ.old_version == True:
                        CreatePZ.paker_do['posle'] = row[col + 8]
                    else:
                        CreatePZ.paker_do['posle'] = row[col + 9]

                elif value == 'Н посадки, м':
                    try:
                        CreatePZ.H_F_paker_do['do'] = float(row[col + 2])
                        if CreatePZ.old_version == True:
                            CreatePZ.H_F_paker_do['posle'] = float(row[col + 6])
                        else:
                            CreatePZ.H_F_paker_do['posle'] = float(row[col + 7])

                    except:
                        # CreatePZ.H_F_paker_do_1, ok = QInputDialog.getInt(self, 'Глубина посадки фондового пакера до ремонта', 'Глубина посадки фондового пакера до ремонта', 500, 0, CreatePZ.bottomhole_artificial)
                        if CreatePZ.paker_do['do'] != None:
                            H_F_paker_do_1, ok = QInputDialog.getInt(self,'Глубина посадки фондового пакера после ремонта','Глубина посадки фондового пакера после ремонта', 1000, 0, int(CreatePZ.bottomhole_artificial))
                            CreatePZ.H_F_paker_do['do'] = H_F_paker_do_1
                        if CreatePZ.paker_do['posle'] != None:
                            H_F_paker_do_2, ok = QInputDialog.getInt(self, 'Глубина посадки фондового пакера',
                                                                            'Глубина посадки фондового пакера до ремонта', 1000, 0,
                                                                            int(CreatePZ.bottomhole_artificial))
                            CreatePZ.paker_do['posle'] = H_F_paker_do_2
                elif 2 in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_H2S_list:
                    if 'мг/дм3' == value or 'мг/л' == value:
                        try:
                            CreatePZ.H2S_mg.append(float(row[col - 1]))
                        except:
                            CreatePZ.H2S_mg.append(float(QInputDialog.getDouble(self, 'Сероводород', 'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)))

                    elif '%' == value:
                        try:
                            CreatePZ.H2S_pr.append(float(row[col - 1]))
                        except:
                            CreatePZ.H2S_pr.append(float(QInputDialog.getDouble(self, 'Сероводород', 'Введите содержание сероводорода в %', 50, 0, 1000, 2)))

        CreatePZ.image_finder = wb.dr



        if curator == 'ОР':
            # print(data_x_min, data_x_max)
            for row in range(data_x_min + 1, data_x_max+1):
                expected_list = []
                for col in range(1, 12):

                    if ws.cell(row=row, column=col).value != None:
                        if type(ws.cell(row=row, column=col).value) == int:
                            expected_list.append(ws.cell(row=row, column=col).value)
                        # else:
                        #     if ws.cell(row=row, column=col).value.isnumeric() == True:
                        #         expected_list.append(ws.cell(row=row, column=col).value)
                # if len(expected_list) != 0:
                #     CreatePZ.expected_pick_up[expected_list[0]] = expected_list[1]

        for row in range(pipes_ind + 1, condition_of_wells):  # словарь  количества НКТ и метраж
            if ws.cell(row=row, column=3).value == 'План':

                a_plan = row

        for row in range(pipes_ind + 1, condition_of_wells):
            key = ws.cell(row=row, column=4).value
            value = ws.cell(row=row, column=7).value
            if key != None and row < a_plan:
                CreatePZ.dict_nkt[key] = CreatePZ.dict_nkt.get(key, 0) + value
            if key != None and row >= a_plan:
                CreatePZ.dict_nkt_po[key] = CreatePZ.dict_nkt_po.get(key, 0) + value

        try:
            CreatePZ.shoe_nkt = sum(CreatePZ.dict_nkt.values())
            CreatePZ.shoe_nkt > CreatePZ.bottomhole_artificial
        except:
            print('НКТ ниже забоя')

        try:
            for row in range(sucker_rod_ind, pipes_ind - 1):
                if ws.cell(row=row, column=3).value == 'План':
                    b_plan = row
            for row in range(sucker_rod_ind + 1, pipes_ind - 1):
                key = ws.cell(row=row, column=4).value
                value = ws.cell(row=row, column=7).value
                if key != None and row < b_plan:

                    self.dict_sucker_rod[key] = self.dict_sucker_rod.get(key, 0) + value
                    if key != None and row >= b_plan:
                        self.dict_sucker_rod_po[key] = self.dict_sucker_rod_po.get(key, 0) + value
                # self.dict_sucker_rod = dict_sucker_rod
                # self.dict_sucker_rod_po = dict_sucker_rod_po
        except:
            print('штанги отсутствуют')
        perforations_intervals = []
        print(f' индекс ПВР{data_pvr_min+2, data_pvr_max+1}')
        for row in range(data_pvr_min+2, data_pvr_max + 2):  # Сортировка интервала перфорации
            lst = []
            for i in range(2, 12):
                lst.append(ws.cell(row=row, column=i).value)
            perforations_intervals.append(lst)
        # perforations_intervals = sorted(perforations_intervals, key=lambda x: x[3])

        for row in perforations_intervals:

            if CreatePZ.H_F_paker_do['do'] != None:
                if int(row[2]) > CreatePZ.H_F_paker_do['do'] and row[5] == None and int(row[2]) <=CreatePZ.current_bottom and CreatePZ.old_version == False:
                    CreatePZ.work_pervorations.append(row)

                    CreatePZ.work_pervorations_dict[row[2]] = row[3]
                elif int(row[2]) > CreatePZ.H_F_paker_do['do'] and CreatePZ.old_version == True and int(row[2]) <=CreatePZ.current_bottom:
                    CreatePZ.work_pervorations.append(row)
                    CreatePZ.work_pervorations_dict[row[2]] = row[3]
            else:
                if row[5] == None and int(row[2]) <= CreatePZ.current_bottom and CreatePZ.old_version == False:
                    CreatePZ.work_pervorations.append(row)
                    CreatePZ.work_pervorations_dict[row[2]] = row[3]
                elif CreatePZ.old_version == True and int(row[2]) <= CreatePZ.current_bottom:
                    CreatePZ.work_pervorations.append(row)
                    CreatePZ.work_pervorations_dict[row[2]] = row[3]
        print(CreatePZ.work_pervorations)
        print(CreatePZ.work_pervorations_dict)

        for j in range(data_x_min, data_x_max):  # Ожидаемые показатели после ремонта
            lst = []
            for i in range(0, 12):
                lst.append(ws.cell(row=j + 1, column=i + 1).value)
            CreatePZ.row_expected.append(lst)


        plan.delete_rows_pz(self, ws)
        CreatePZ.region = block_name.region(cdng)
        razdel_1 = block_name.razdel_1(self)

        # wb2 = op.Workbook()
        # ws2 = wb2.get_sheet_by_name('Sheet')
        # ws2.title = "План работ"
        #
        # bound = []
        # for _range in ws.merged_cells.ranges:
        #     boundaries = range_boundaries(str(_range))
        #     # elif data_pvr_min + 2 <= boundaries[1] <= data_pvr_max + 2:
        #     #     bound.append(boundaries)
        #     #     # ws2.unmerge_cells(start_column=boundaries[0], start_row=boundaries[1] + len(self.razdel_1) + 1,
        #     #     #                end_column=boundaries[2], end_row=boundaries[3] + len(self.razdel_1) + 1)
        #
        #     if boundaries[1] > CreatePZ.data_well_max + 1 and boundaries[1] >= cat_well_min:
        #
        #         bound.append(boundaries)
        #     else:
        #         ws2.merge_cells(start_column=boundaries[0], start_row=boundaries[1] + len(razdel_1) + 1,
        #                         end_column=boundaries[2], end_row=boundaries[3] + len(razdel_1) + 1)
        #

        for i in range(1, len(razdel_1)):  # Добавлением подписантов на вверху
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = razdel_1[i - 1][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
            ws.merge_cells(start_row=i, start_column=8, end_row=i, end_column=13)
        CreatePZ.ins_ind = 0
        # wb.save(f'as.xlsx')
        # list_block = [cat_well_min,  CreatePZ.data_well_max]

        # head = plan.head_ind(cat_well_min, CreatePZ.data_well_max + 1)
        #
        # plan.copy_row(ws, ws2, CreatePZ.ins_ind, head)
        CreatePZ.ins_ind += CreatePZ.data_well_max  - CreatePZ.cat_well_min + 19
        print(f' индекс вставки ГНВП{CreatePZ.ins_ind}')
        dict_events_gnvp = {}
        dict_events_gnvp['krs'] = events_gnvp
        dict_events_gnvp['gnkt_opz'] = events_gnvp_gnkt

        for i in range(CreatePZ.ins_ind, CreatePZ.ins_ind + len(dict_events_gnvp[work_plan]) - 1):
            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)

            if i == (CreatePZ.ins_ind + 13 or i == CreatePZ.ins_ind + 28) and work_plan == 'krs':

                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                vertical='center')
                ws.cell(row=i, column=2).font = Font(name='Arial', size=13, bold=True)
                ws.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]
            elif i == CreatePZ.ins_ind + 11 and work_plan == 'gnkt_opz':
                print(work_plan)
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
        CreatePZ.ins_ind += len(dict_events_gnvp[work_plan])



        ws.row_dimensions[2].height = 30
        ws.row_dimensions[6].height = 30

        # data_main_production_string = ws.cell(row=int(ind_data_main_production_string[1:])+1, column=int(ind_data_main_production_string[0])+2).value
        CreatePZ.insert_gnvp(ws, work_plan, ins_gnvp)



        for i in range(len(CreatePZ.row_expected)):  # Добавление  показатели после ремонта
            for j in range(1, 12):
                if i == 1:
                    ws.cell(row=i + CreatePZ.ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                    ws.cell(row=i + CreatePZ.ins_ind, column=j).alignment = Alignment(wrap_text=False, horizontal='center',
                                                                              vertical='center')
                    ws.cell(row=i + CreatePZ.ins_ind, column=j).value = CreatePZ.row_expected[i - 1][j - 1]
                else:
                    ws.cell(row=i + CreatePZ.ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                    ws.cell(row=i + CreatePZ.ins_ind, column=j).alignment = Alignment(wrap_text=False, horizontal='left',
                                                                              vertical='center')
                    ws.cell(row=i + CreatePZ.ins_ind, column=j).value = CreatePZ.row_expected[i - 1][j - 1]
        ws.merge_cells(start_column=2, start_row=CreatePZ.ins_ind + 1, end_column=12, end_row=CreatePZ.ins_ind + 1)
        if 2 in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_H2S_list:
            H2S = True
        else:
            H2S = False
        if work_plan == 'gnkt_opz':
            CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                                 'Введите забой до которого нужно нормализовать')
            gnkt_work1 = gnkt_work(self)
            CreatePZ.ins_ind += 2
            CreatePZ.count_row_height(ws, gnkt_work1, CreatePZ.ins_ind)
            CreatePZ.itog_ind_min = CreatePZ.ins_ind

            CreatePZ.ins_ind += len(gnkt_work1) - 3

        elif work_plan == 'krs':
            CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                                 'Введите забой до которого нужно нормализовать')
            krs_work1 = krs.work_krs(self)
            CreatePZ.ins_ind += 2
            CreatePZ.count_row_height(ws, krs_work1, CreatePZ.ins_ind)
            CreatePZ.itog_ind_min = CreatePZ.ins_ind

            CreatePZ.ins_ind += len(krs_work1) - 3
            print('План работ на КРС')
        else:
            print('План другого')

        CreatePZ.itog_ind_max = CreatePZ.ins_ind
        for i in range(CreatePZ.ins_ind + 2 + 1, len(itog_1()) + CreatePZ.ins_ind + 2):  # Добавлением итогов
            if i < CreatePZ.ins_ind + 2 + 1 + 6:
                for j in range(1, 13):
                    ws.cell(row=i, column=j).value = itog_1()[i - CreatePZ.ins_ind - 2 - 1][j - 1]
                    if j != 1:
                        ws.cell(row=i, column=j).border = CreatePZ.thin_border
                        ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=11)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                vertical='center')
            else:
                for j in range(1, 13):
                    ws.row_dimensions[i].height = 55
                    ws.cell(row=i, column=j).value = itog_1()[i - CreatePZ.ins_ind - 2 - 1][j - 1]
                    ws.cell(row=i, column=j).border = CreatePZ.thin_border
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                    ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                    vertical='center')

                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                ws.cell(row=i + CreatePZ.ins_ind, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                          vertical='center')

        CreatePZ.ins_ind += len(itog_1()) + 2

        curator_sel = block_name.curator_sel(self, CreatePZ.curator, CreatePZ.region)
        curator_ved_sel = block_name.curator_sel(self, CreatePZ.curator, CreatePZ.region)
        podp_down = block_name.pop_down(self, CreatePZ.region, curator_sel)
        for i in range(1 + CreatePZ.ins_ind, 1 + CreatePZ.ins_ind + len(podp_down)):  # Добавлением подписантов внизу
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = podp_down[i - 1 - CreatePZ.ins_ind][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            if i in [1 + CreatePZ.ins_ind + 7, 1 + CreatePZ.ins_ind + 8, 1 + CreatePZ.ins_ind + 9, 1 + CreatePZ.ins_ind + 10, 1 + CreatePZ.ins_ind + 11,
                     1 + CreatePZ.ins_ind + 12, 1 + CreatePZ.ins_ind + 13, 1 + CreatePZ.ins_ind + 14]:
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=5)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, vertical='top', horizontal='left')
                if i == 1 + CreatePZ.ins_ind + 11:
                    ws.row_dimensions[i].height = 55
        CreatePZ.ins_ind += len(podp_down)
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

        if 2 in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_H2S_list:
            ws3 = wb.create_sheet('Sheet1')
            ws3.title = "Расчет необходимого количества поглотителя H2S"
            ws3 = wb["Расчет необходимого количества поглотителя H2S"]
            calc_H2S(ws3, CreatePZ.H2S_pr, CreatePZ.H2S_mg)

            ws3.page_setup.fitToPage = True
            # ws3.page_setup.fitToHeight = True
            # ws3.page_setup.fitToWidth = True
            ws3.print_area = 'A1:A10'

        else:
            print(f'{CreatePZ.cat_H2S_list} Расчет поглотителя сероводорода не требуется')

        ws.print_area = f'B1:L{CreatePZ.ins_ind}'
        # ws.page_setup.fitToPage = True
        # ws.page_setup.fitToHeight = False
        ws.page_setup.fitToWidth = True
        # ws.print_options.horizontalCentered = True

        try:
            for row_index, row in enumerate(ws.iter_rows()):
                if row_index in [i for i in range(column_add_index+4, index_bottomhole+5)]:
                    if all(cell.value == None for cell in row):
                        ws.row_dimensions[row_index].hidden = True
            print(' Скрытие ячеек сделано')
        except:
            print('нет скрытых ячеек')


        wb.save(f'{CreatePZ.well_number} {CreatePZ.well_area} {work_plan}.xlsx')
        return ws


    def insert_gnvp(ws, work_plan, ins_gnvp):
        rowHeights_gnvp = [None,115.0, 155.5, 110.25, 36.0, 52.25, 36.25, 36.0, 45.25, 36.25, 165.75, 38.5, 30.25, 30.5,
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
        print(f' индекс вставки высоты {ins_gnvp-2}')
        for index_row, row in enumerate(ws.iter_rows()):  # Копирование высоты строки
            if index_row + ins_gnvp <= len(dict_rowHeights[work_plan]) + ins_gnvp:
                ws.row_dimensions[index_row + ins_gnvp -2].height = dict_rowHeights[work_plan][index_row - 1]
            for col_ind, col in enumerate(row):
                if col_ind <= 12:
                    ws.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind]
                else:
                    break

    def without_b(a):
        b = ''
        if a != None:
            for i in range(len(str(a))):
                if str(a)[i] in '0123456789':
                    b += str(a)[i]
        return b

    def count_row_height(ws, work_list, ins_ind):
        for i in range(ins_ind + 1, len(work_list) + ins_ind):  # Добавлением работ
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = work_list[i - ins_ind - 1][j - 1]
                if j != 1:
                    ws.cell(row=i, column=j).border = CreatePZ.thin_border
                if j == 11:
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=11, bold=False)
                else:
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            if i == ins_ind + 1:
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                vertical='center')

            else:
                ws.merge_cells(start_row=i, start_column=3, end_row=i, end_column=10)
            ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                            vertical='center')
            ws.cell(row=i, column=11).alignment = Alignment(wrap_text=True, horizontal='center',
                                                             vertical='center')
            ws.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                             vertical='center')
            ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                            vertical='center')

        row_count = []
        for row in work_list:
            count_val = []
            for col in row:
                if col != None:
                    count_val.append(len(str(col)))
                else:
                    count_val.append(2)
            row_count.append(max(count_val) / 6)
        print(f'высота строк работ {ins_ind}')
        for index_row, row in enumerate(row_count):  # Копирование высоты строки
            if index_row >= 3:
                ws.row_dimensions[index_row + ins_ind].height = row_count[index_row - 1]

        ws.column_dimensions[get_column_letter(11)].width = 15
        ws.column_dimensions[get_column_letter(12)].width = 15
        ws.column_dimensions[get_column_letter(7)].width = 20

        return 'Высота изменена'

        # ws2.unmerge_cells(start_column=2, start_row=self.ins_ind, end_column=12, end_row=self.ins_ind)


fname = 'Копия 2327 Манчаровского м-я (ПЗ) 11092023.xlsx'
# print(CreatePZ.open_excel_file(fname, fname, work_plan='gnkt_opz'))