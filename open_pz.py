import sys


import openpyxl as op
import self
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from copy import copy
from openpyxl.utils.cell import range_boundaries
import name
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
import plan
import H2S

fname = '6147.xlsx'


class Create_PZ:
    column_additional = False

    cat_well_min = 0
    cat_well_max = 0
    values = []
    data_well_min = 0
    data_well_max = 0
    data_x_min = 0
    data_x_max = 0
    data_pvr_min = 0
    data_pvr_max = 0
    perforations_intervals = []
    head_column_additional = 0
    shoe_column_additional = 0
    column_additional_diametr = 0
    column_additional_wall_thickness = 0
    column_additional_diametr = 0
    column_additional_wall_thickness = 0
    data_column_additional = 0

    bottomhole_artificial = 0
    art_bottom_well = ''
    current_bottom = ''
    cdng = ''
    H2S_mg = []

    gaz_f_pr = ''

    water_cut = 100
    region = ''
    well_number = 0
    well_area =''
    column_diametr = 0
    column_wall_thickness = 0
    shoe_column = 0
    dict_nkt = {0: 0}
    dict_nkt_po = {}
    dict_sucker_rod = {32:0, 25: 0, 22: 0, 19: 0}
    dict_sucker_rod_po = {}
    H2S_pr = []


    # values1 = []
    def open_excel_file(self, fname, ):

        wb = op.load_workbook(fname, data_only=True)
        ws = wb.active
        max_rows = ws.max_row
        wb2 = op.Workbook()
        ws2 = wb2.get_sheet_by_name('Sheet')
        ws2.title = "План работ"
        ws3 = wb2.create_sheet('Sheet1')
        ws3.title = "Расчет необходимого количества поглотителя H2S"

        # curator = input('Введите сектор кураторов региона, ОР или ГТМ, или ГРР или ГО:  ')
        curator = 'ГТМ'
        sucker_rod_ind = 0
        sucker_rod_ind_cancel = 0
        condition_of_wells = 0
        pipes_ind = ''
        well_number = 0
        well_area = ''
        H2S_pr = []
        H2S_mg = []
        dict_nkt = {}
        dict_nkt_po ={}
        dict_sucker_rod = {}
        dict_sucker_rod_po = {}
        row_expected = []
        perforations_intervals = []
        current_datetime = datetime.today()
        region_dict = {
            'ИГМ': ['АкЦДНГ 01', 'АкЦДНГ 02', 'АкЦДНГ 03', 'ИЦДНГ 01', 'ИЦДНГ 02', 'ИЦДНГ 03', 'ИЦДНГ 04', 'ИЦДНГ 05'],
            'ТГМ': ['ОЦДНГ 01', 'ОЦДНГ 02', 'ОЦДНГ 03', 'ТЦДНГ 01', 'ТЦДНГ 02', 'ТЦДНГ 03'],
            'КГМ': ['КЦДНГ 01', 'КЦДНГ 02', 'КЦДНГ 03', 'КЦДНГ 04', 'КЦДНГ 05', 'КЦДНГ 06', 'КЦДНГ 07', 'КЦДНГ 08'],
            'ЧГМ': ['УЦДНГ 01', 'УЦДНГ 02', 'УЦДНГ 03', 'УЦДНГ 04', 'ЧЦДНГ 01', 'ЧЦДНГ 02', 'ЧЦДНГ 03', 'ЧЦППД'],
            'АГМ': ['АЦДНГ 01', 'АЦДНГ 02', 'АЦДНГ 03', 'АЦДНГ 04', 'ЮЦДНГ 01', 'ЮЦДНГ 02', 'ЮЦДНГ 03']
        }

        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            if 'Категория скважины' in row:
                self.cat_well_min = row_ind + 1  # индекс начала категории

            elif 'План-заказ' in row:
                ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'
                self.cat_well_max = row_ind - 1
                self.data_well_min = row_ind + 1
            elif 'IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in row:
                self.data_well_max = row_ind - 1
            elif 'X. Ожидаемые показатели после ремонта:' in row:
                self.data_x_min = row_ind
            elif 'ШТАНГИ' in row:
                self.sucker_rod_ind = row_ind
                sucker_rod_ind = self.sucker_rod_ind
            elif 'НКТ' in row:
                self.pipes_ind = row_ind
                pipes_ind = self.pipes_ind
            elif 'ХI Планируемый объём работ:' in row:
                self.data_x_max = row_ind
            elif 'II. История эксплуатации скважины' in row:
                self.data_pvr_max = row_ind - 2
            elif 'III. Состояние скважины к началу ремонта ' in row:
                condition_of_wells = row_ind
            for col, value in enumerate(row):
                if 'площадь' == value:  # определение номера скважины
                    well_number =  row[col - 1]
                    self.well_number =well_number
                    well_area = row[col + 1]
                    self.well_area = well_area
                elif '11. Эксплуатационные горизонты и интервалы перфорации:' == value:
                    self.data_pvr_min = row_ind + 2

                elif '7. Пробуренный забой' == value:
                    try:
                        self.bottomhole_artificial = float(row[col + 5])
                    except:
                        self.bottomhole_artificial = float(input('Искусственный забой равен:  '))
                elif 'Текущий забой ' == value:
                    try:
                        self.current_bottom = float(row[col + 2])
                    except:
                        self.current_bottom = float(input('Текущий забой равен: '))
                elif 'месторождение ' == value:
                    self.oilfield = row[col + 2]

                elif value == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':  # Определение данных по колонне

                    data_main_production_string = (ws.cell(row=row_ind + 2, column=col + 1).value).split('(мм),', )
                    if len(data_main_production_string) == 3:
                        try:
                            self.column_diametr = float(data_main_production_string[0])
                        except:
                            self.column_diametr = float(input('диаметр колонны основной:'))
                        try:
                            self.column_wall_thickness = float(data_main_production_string[1][1:])
                        except:
                            self.column_wall_thickness = float(input('Толщина стенки:'))
                        try:
                            self.shoe_column = float(data_main_production_string[-1].strip().replace('(м)', '')[4:])
                            print(self.shoe_column)
                        except:
                            self.shoe_column = float(input('Башмак колонны: '))


                elif '9. Максимальный зенитный угол' == value:
                    try:
                        self.max_angle = row[col + 1]
                        n = 1
                        while self.max_angle == None:
                            self.max_angle = row[col + n]
                            n += 1
                    except:
                        self.max_angle = float(input('Введите максимальный зенитный угол: '))


                elif '9. Максимальный зенитный угол' in row and value == 'на глубине':
                    try:
                        self.max_h_angle = row[col + 1]
                    except:
                        self.max_h_angle = int(input('Введите глубину максимального зетного угла: '))
                elif 'цех' == value and 'назначение ' in row:
                    self.cdng = row[col + 1]
                elif 'плотн.воды' == value:
                    self.water_cut = row[col - 1]
                elif 'по Pпл' == value:
                    self.cat_P_1 = row[col + 1]
                    n = 1
                    while self.cat_P_1 == None:
                        self.cat_P_1 = row[col + n]
                        n += 1
                elif 'по H2S' == value:
                    self.cat_H2S_1 = row[col + 1]
                    n = 1
                    while self.cat_H2S_1 == None:
                        self.cat_H2S_1 = row[col + n]
                        n += 1
                elif 'по газовому фактору' == value:
                    Create_PZ.cat_H2S_1 = row[col + 1]
                    n = 1
                    while self.cat_H2S_1 == None:
                        Create_PZ.cat_H2S_1 = row[col + n]
                        n += 1
                elif 'мг/дм3' == value or 'мг/л' == value:
                    H2S_mg.append(row[col-1])
                elif '%' == value:

                    H2S_pr.append(row[col-1])
                elif value == 'м3/т':

                    self.gaz_f_pr = row[col-1]

                elif '6. Конструкция хвостовика' == value:
                    self.data_column_additional = ws.cell(row=row_ind + 3, column=col + 2).value
                    if self.data_column_additional != None or self.data_column_additional != '-':
                        self.column_additional = True
                    try:
                        self.head_column_additional = float(self.data_column_additional.split('-')[0])

                        self.shoe_column_additional = self.data_column_additional.split('-')[1]
                        self.column_additional_diametr = ws.cell(row=row_ind + 3, column=col + 4).value
                        self.column_additional_wall_thickness = ws.cell(row=row_ind + 3, column=col + 6).value
                    except:
                        self.head_column_additional = 0

                        self.shoe_column_additional = 0
                        self.column_additional_diametr = 0
                        self.column_additional_wall_thickness = 0
                        print('Доп колонна отсутствует')

                elif 'Максимально ожидаемое давление на устье' == value:
                    try:
                        self.max_expected_pressure = row[col + 1]
                        n = 1
                        while self.max_expected_pressure == None:
                            self.max_expected_pressure = row[col + n]
                            n += 1
                    except:
                        self.max_expected_pressure = int(input('Введите максимально ожидамое давление на устье: '))
                elif 'Максимально допустимое давление опрессовки э/колонны' == value:
                    try:
                        self.max_admissible_pressure = row[col + 1]
                        n = 1
                        while self.max_admissible_pressure == None:
                            self.max_admissible_pressure = row[col + n]
                            n += 1
                    except:
                        self.max_admissible_pressure = int(input('Введите максимально ожидаемое давление на устье: '))
                elif value == 'Пакер' and row[col + 2] == 'типоразмер':
                    self.paker_do = row[col + 4]
                    self.H_F_paker_do = ws.cell(row=row_ind + 4, column=col + 5).value

        list_block_append = [self.cat_well_min, self.data_well_min + 1, self.data_well_max]
        self.region = ''.join([key for key, value in region_dict.items() if self.cdng in value])

        gi_region = [''.join(name.region_p[self.region][0].keys()), ''.join(name.region_p[self.region][0].values())]
        gg_region = [''.join(name.region_p[self.region][1].keys()), ''.join(name.region_p[self.region][1].values())]
        ruk_orm = [''.join(name.region_p[self.region][2].keys()), ''.join(name.region_p[self.region][2].values())]
        ruk_pto = [''.join(name.region_p[self.region][4].keys()), ''.join(name.region_p[self.region][4].values())]
        rum_gtm = [''.join(name.region_p[self.region][3].keys()), ''.join(name.region_p[self.region][3].values())]
        ruk_usrs_krs = [''.join(name.region_p[self.region][5].keys()), ''.join(name.region_p[self.region][5].values())]
        ruk_go = [''.join(name.region_p[self.region][6].keys()), ''.join(name.region_p[self.region][6].values())]
        ved_gtm = [''.join(name.region_p[self.region][7].keys()), ''.join(name.region_p[self.region][7].values())]
        ved_orm = [''.join(name.region_p[self.region][8].keys()), ''.join(name.region_p[self.region][8].values())]
        nach_tkrs = ['А.Р.Габдулхаков ', 'З.К. Алиев', 'М.К.Алиев']
        if self.region == 'ЧГМ' or self.region == 'ТГМ':
            nach_tkrs = nach_tkrs[0]
        elif self.region == 'КГМ' or self.region == 'АГМ':
            nach_tkrs = nach_tkrs[1]
        elif self.region == 'ИГМ':
            nach_tkrs = nach_tkrs[2]

        razdel_1 = [[None, 'СОГЛАСОВАНО:', None, None, None, None, None, None, 'УТВЕРЖДАЕМ:', None, None, None],
                    [None, gi_region[0], None, None, None, None, None,
                     None, 'Главный Инженер ООО "Ойл-Сервис"', None, None, None],
                    [None, f'____________{gi_region[1]}', None, None, None, None, None, None,
                     '_____________А.Р. Хасаншин', None, None, None],
                    [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
                     f'"____"_____________________{current_datetime.year}г.', None, None, None],
                    [None, None, None, None, None, None, None, None, None, None, None, None],
                    [None, gg_region[0], None, None, None,
                     None, None,
                     None, 'Главный геолог ООО "Ойл-Сервис"', None, None, None],
                    [None, f'_____________{gg_region[1]}', None, None, None, None, None, None,
                     '_____________Д.Д. Шамигулов', None, '',
                     None],
                    [None, f'"____"_____________________{current_datetime.year}г.', None, None, '', None, None, None,
                     f'"____"_____________________{current_datetime.year}г.', None, None, None],
                    [None, None, None, None, None, None, None, None, None, None, None, None],
                    [None, 'Представитель подрядчика по ГРП', None, None, None, None, None, None, None, None, None,
                     None],
                    [None, '_____________', None, None, None, None, None, None, None, None, None, None],
                    [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
                     None, None, None,
                     None],
                    [None, 'Районный инженер Башкирского ', None, None, None, None, None, None, None, None, None, None],
                    [None, 'военизированного отряда ', None, None, None, None, None, None, None, None, None, None],
                    [None, '_____________', None, None, None, None, None, None, None, None, None, None],
                    [None, f'"____"_____________________{current_datetime.year}г.', None, None, None, None, None, None,
                     None, None, None,
                     None]]

        print(self.region)
        for j in range(self.data_x_min, self.data_x_max):  # Ожидаемые показатели после ремонта
            lst = []
            for i in range(0, 12):
                lst.append(ws.cell(row=j + 1, column=i + 1).value)
            row_expected.append(lst)

        bound = []
        for _range in ws.merged_cells.ranges:
            boundaries = range_boundaries(str(_range))
            if self.data_pvr_min + 2 <= boundaries[1] <= self.data_pvr_max + 2:
                bound.append(boundaries)
                # ws2.unmerge_cells(start_column=boundaries[0], start_row=boundaries[1] + len(self.razdel_1) + 1,
                #                end_column=boundaries[2], end_row=boundaries[3] + len(self.razdel_1) + 1)
            elif boundaries[1] >= self.data_well_max + 3:
                bound.append(boundaries)
            else:
                ws2.merge_cells(start_column=boundaries[0], start_row=boundaries[1] + len(razdel_1) + 1,
                                end_column=boundaries[2], end_row=boundaries[3] + len(razdel_1) + 1)

        for j in range(self.data_pvr_min, self.data_pvr_max):  # Сортировка интервала перфорации
            lst = []
            for i in range(1, 12):
                if type(ws.cell(row=j + 1, column=i + 1).value) == float:
                    lst.append(round(ws.cell(row=j + 1, column=i + 1).value, 1))
                else:
                    lst.append(ws.cell(row=j + 2, column=i + 1).value)
            perforations_intervals.append(lst)
        perforations_intervals = sorted(perforations_intervals, key=lambda x: x[3])

        self.ins_ind = len(razdel_1) + self.cat_well_min
        # print(self.ins_ind)
        for i in range(1, len(list_block_append)):  # цикл добавления блоков план-заказов
            head = plan.head_ind(list_block_append[i - 1], list_block_append[i] + 2)
            name_values = razdel_1
            index_row = list_block_append[i - 1]
            self.ins_ind += (list_block_append[i] + 2 - list_block_append[i - 1])
            # print(self.ins_ind)
            plan.copy_row(ws, ws2, name_values, index_row, head)


        thin_border = Border(left=Side(style='thin'),
                             right=Side(style='thin'),
                             top=Side(style='thin'),
                             bottom=Side(style='thin'))

        for row in range(sucker_rod_ind, pipes_ind- 1):
            if ws.cell(row=row, column=3).value == 'План':
                b_plan = row
        for row in range(sucker_rod_ind+1, pipes_ind - 1):
            key = ws.cell(row=row, column=4).value
            value = ws.cell(row=row, column=7).value
            if key != None and row < b_plan:
                print(key)
                dict_sucker_rod[key] = dict_sucker_rod.get(key, 0) + value
            if key != None and row >= b_plan:
                dict_sucker_rod_po[key] = dict_sucker_rod_po.get(key, 0) + value

        for row in range(pipes_ind+1, condition_of_wells): # словарь  количества НКТ и метраж
            if ws.cell(row=row, column=3).value == 'План':
                a_plan = row
        for row in range(pipes_ind + 1, condition_of_wells):
            key = ws.cell(row=row, column=4).value
            value = ws.cell(row=row, column=7).value
            if key != None and row < a_plan:
                dict_nkt[key] = dict_nkt.get(key, 0) + value
            if  key != None and row >= a_plan:
                dict_nkt_po[key] =dict_nkt_po.get(key, 0) + value
        self.dict_nkt_po = dict_nkt_po
        self.dict_nkt =dict_nkt
        self.dict_sucker_rod =dict_sucker_rod
        self.dict_sucker_rod_po = dict_sucker_rod_po


        for i in range(1, len(perforations_intervals) + 1):  # Добавление данных по интервалу перфорации
            for j in range(1, 12):
                ws2.cell(row=i + self.data_pvr_min + len(razdel_1) + 2, column=j + 1).border = thin_border
                ws2.cell(row=i + self.data_pvr_min + len(razdel_1) + 2, column=j + 1).font = 'Arial'
                ws2.cell(row=i + self.data_pvr_min + len(razdel_1) + 2, column=j + 1).alignment = Alignment(
                    wrap_text=True)
                ws2.cell(row=i + self.data_pvr_min + len(razdel_1) + 2, column=j + 1).value = \
                perforations_intervals[i - 1][j - 1]
        # print(list_block_append[-1] - 4 - len(self.razdel_1))
        for i in range(self.ins_ind, self.ins_ind + len(name.events_gnvp)):
            ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)

            for j in range(2):
                if i == self.ins_ind + 13 or i == self.ins_ind + 28:
                    ws2.cell(row=i, column=1 + 1).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
                    ws2.cell(row=i, column=1 + 1).font = Font(name='Arial', size=13, bold=True)

                    ws2.cell(row=i, column=1 + 1).value = name.events_gnvp[i - self.ins_ind][j]
                else:
                    ws2.cell(row=i, column=j + 1).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                        vertical='top')
                    ws2.cell(row=i, column=j + 1).font = Font(name='Arial', size=12)

                    ws2.cell(row=i, column=j + 1).value = name.events_gnvp[i - self.ins_ind][j]
        self.ins_ind += len(name.events_gnvp) - 1

        for i in range(1, len(razdel_1)):  # Добавлением подписантов на вверху
            for j in range(1, 13):
                ws2.cell(row=i, column=j).value = razdel_1[i - 1][j - 1]
                ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
        for i in range(1, 16):
            ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
            ws2.merge_cells(start_row=i, start_column=9, end_row=i, end_column=13)

        ws2.row_dimensions[2].height = 30
        ws2.row_dimensions[6].height = 30

        # data_main_production_string = ws.cell(row=int(ind_data_main_production_string[1:])+1, column=int(ind_data_main_production_string[0])+2).value

        rowHeights_gnvp = [95.0, 155.5, 110.25, 36.0, 52.25, 36.25, 36.0, 45.25, 20.25, 135.75, 38.5, 30.25, 30.5,
                           18.0, 50.5, 21.75, 240.75, 125.0, 66.75, 48.0, 33.0, 38.25, 45.0, 32.25, 45.75, 30.75, 32.25,
                           310.0, 21.75, 50.25, 57.25, 78.75, 64.5, 25.0, 25.0, 25.0, 25.0]

        rowHeights = [ws.row_dimensions[i + 1].height for i in range(self.data_well_max + 2)] + rowHeights_gnvp
        colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]

        for index_row, row in enumerate(ws2.iter_rows()):  # Копирование высоты строки
            if len(rowHeights) >= index_row:
                ws2.row_dimensions[index_row + len(razdel_1) + 1].height = rowHeights[index_row - 1]
            for col_ind, col in enumerate(row):

                if col_ind <= 12:
                    ws2.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind]
                else:
                    break
        ws2.unmerge_cells(start_column=2, start_row=self.ins_ind, end_column=12, end_row=self.ins_ind)

        row_expected = row_expected[::-1]
        for i in range(len(row_expected)):  # Добавление данных по интервалу перфорации
            for j in range(1, 13):
                ws2.cell(row=i + self.ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                ws2.cell(row=i + self.ins_ind, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                               vertical='center')
                ws2.cell(row=i + self.ins_ind, column=j).value = row_expected[i - 1][j - 1]

            ws2.merge_cells(start_column=2, start_row=self.ins_ind, end_column=12, end_row=self.ins_ind)
        print(self.ins_ind)
        itog_1 = [[None, 'ИТОГО:', None, None, None, None, None, None, None, None, None, 226.2],
                  [None, 'Герметизация ,  разгерметизация  устья  скважины', None, None, None, None, None, None, None,
                   None, None, 3.6],
                  [None, 'Заправка ДВС', None, None, None, None, None, None, None, None, None, 1.3],
                  [None, 'ПЗР в начале и конце смены с заполнением вахтового журнала', None, None, None, None, None,
                   None, None, None, None, 5.9],
                  [None, 'Непредвиденные  работы  : ', None, None, None, None, None, None, None, None, None, 10.6],
                  [None, 'ВСЕГО  :', None, None, None, None, None, None, None, None, None, 247.6],
                  [None,
                   'Примечания: В соответствии с регламентом на производство КРС – заблаговременно подавать заявки на необходимое оборудование, а так же вызывать представителя Заказчика на геофизические работы, ПВР, установку пакера, срыв планшайбы, опрессовку колонны и другие технологические операции, прием скважины в ремонт и сдача из ремонта.',
                   None, None, None, None, None, None, None, None, None, None],
                  [None, 'ПРИМЕЧАНИЕ:', None, ' ', None, None, None, None, None, None, None, None],
                  [None,
                   '  При незначительных изменениях в плане работ (изменении компоновки подземного оборудования, объемов закачки и т.д.)  и доп. работах в виде единичных СПО, технол.операций и др. возможна работа без доп. плана - по письму Заказчика.     ',
                   None, None, None, None, None, None, None, None, None, None],
                  [None, 'поглощения жидкости не допускать', None, None, None, None, None, None, None, None, None,
                   None],
                  [None, 'Ответственный за соблюдением и создание безопасных условий работ – мастера КPС ', None, None,
                   None, None, None, None, None, None, None, None]]

        for i in range(self.ins_ind + 2 + 1, len(itog_1) + self.ins_ind + 2):  # Добавлением итогов
            for j in range(1, 13):
                ws2.cell(row=i, column=j).value = itog_1[i - self.ins_ind - 2 - 1][j - 1]
                ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
        for i in range(1, 16):
            ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
            ws2.merge_cells(start_row=i, start_column=9, end_row=i, end_column=13)
        self.ins_ind += len(itog_1) + 2

        def curator_sel(curator):
            if curator == 'ОР':
                return ruk_orm
            elif curator == 'ГТМ':
                return rum_gtm
            elif curator == 'ГО':
                return ruk_go

        def curator_ved_sel(curator):
            if curator == 'ГТМ' and self.region == 'ЧГМ' or curator == 'ГТМ' and \
                    self.region == 'КГМ' or curator == 'ОР' and self.region == 'КГМ':
                return ved_gtm
            elif curator == 'ОР' and self.region == 'ЧГМ':
                return ved_orm
            else:
                return None

        podp_down = [
            [None, None, None, None, None, None, '"_____"__________________', None, f'{current_datetime.year}г.', None,
             None, None],
            [None, 'План работ составил Ведущий геолог Ойл-сервис', None, None, None, None, None, None, None,
             '/И.М. Зуфаров/', None, None],
            [None, None, None, None, None, None, None, None, None, '     дата подписания', None, None],
            [None, None, 'Начальник ЦТКРС ООО  " Ойл-Сервис"', None, None, None, None, None, None,
             ''.join(nach_tkrs), None, None],
            [None, None, None, None, None, None, None, None, None, '     дата подписания', None, None],
            [None, ' ', 'Согласовано:', None, None, None, None, None, None, None, None, None],
            [None, '', None, None, None, None, '', None, None, '', None, None],
            [None, None, None, None, None, None, '', None, None, '', None, None],
            [None, curator_sel(curator)[0], None, None, None, None, '___________________', None, None,
             curator_sel(curator)[1], None, None],
            [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
             None],
            [None, ruk_pto[0], None, None, None, None, None, None, None,
             ruk_pto[1], None, ' '],
            [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
             None],
            [None, ruk_usrs_krs[0], None, None, None, None,
             None, None, None, ruk_usrs_krs[1], None, None],
            [None, None, None, None, None, None, '"___"___________', None, None, '     дата подписания', None,
             None],
            [None, ''.join(curator_ved_sel(curator)[0]), None, None, None, None, None, None, None,
             ''.join(curator_ved_sel(curator)[1]), None, None],
            [None, None, None, None, None, None,
             ''.join(['"___"___________' if self.region == 'КГМ' or self.region == 'ЧГМ' else None]), None, None,
             ''.join(['Дата подписания' if self.region == 'КГМ' or self.region == 'ЧГМ' else None]), None,
             None],
            [None, 'Замечания:', None, None, None, None, None, None, None, None, None, None],
            [None, '1.', '______________________________________________________', None, None, None, None, None, None,
             None, None, None],
            [None, '2.', '______________________________________________________', None, None, None, None, None, None,
             None, None, None],
            [None, '3.', '______________________________________________________', None, None, None, None, None, None,
             None, None, None],
            [None, '4.', '______________________________________________________', None, None, None, None, None, None,
             None, None, None],
            [None, '5.', '______________________________________________________', None, None, None, None, None, None,
             None, None, None],
            [None, None, None, 'Проинструктированы, с планом работ ознакомлены:                         ', None,
             None, None, None, None, None, None, None],
            [None, None, 'Мастер бригады', None, None, None, 'Инструктаж провел мастер бригады ООО "Ойл-Сервис"',
             None, None, None, None, None],
            [None, None, 'Мастер бригады', None, None, None, None, None, None, None, 'подпись', None],
            [None, 'Бурильщик ООО "Ойл-Сервис"', None, None,
             '_____________________Бурильщик ООО "Ойл-Сервис"________________________', None, None, None, None,
             None, None, None],
            [None, 'Пом.бур-ка ООО "Ойл-Сервис"', None, None,
             '_____________________Пом.бур-ка ООО "Ойл-Сервис"_______________________', None, None, None, None,
             None, None, None],
            [None, 'Пом.бур-ка ООО "Ойл-Сервис"', None, None,
             '_____________________Пом.бур-ка ООО "Ойл-Сервис"_______________________', None, None, None, None,
             None, None, None],
            [None, None, 'Машинист', None,
             '_____________________ Машинист                      ________________________', None, None, None,
             None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None]]
        for i in range(1 + self.ins_ind, 1 + self.ins_ind + len(podp_down)):  # Добавлением итогов
            for j in range(1, 13):
                ws2.cell(row=i, column=j).value = podp_down[i - 1 - self.ins_ind][j - 1]
                ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
        for i in range(1, 16):
            ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
            ws2.merge_cells(start_row=i, start_column=9, end_row=i, end_column=13)

        # print(f' номер скважины -{self.well_number}' \
        #       f' месторождение скважины - {self.oilfield} ' \
        #       f' площадь - {self.well_area}' \
        #       f' ЦДНГ - {self.cdng}' \
        #       f' диаметр колонны - {self.column_diametr}  {self.column_wall_thickness} - {self.shoe_column}' \
        #       f' искусственный забой {self.bottomhole_artificial}'
        #       f' макс угол {self.max_angle} на глубине  {self.max_h_angle}' \
        #       f' {self.data_column_additional}' \
        #       f' доп колонна {self.head_column_additional} - {self.shoe_column_additional}'
        #       f'по Рпл - {self.cat_P_1},'
        #       f'по H2S - {int(self.cat_H2S_1)},'
        #       f' Диаметр доп коллоны - {self.column_additional_diametr} - {self.column_additional_wall_thickness},'
        #       f' Максимальное давление опрессовки - {self.max_expected_pressure},'
        #       f' максимальное ожидаемое давление - {self.max_admissible_pressure},'
        #       f' Фондовый пакер в скважине {self.paker_do} на глубине {self.H_F_paker_do}')
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

        print()
        H2S.calc_H2S(self, wb2, H2S_pr, H2S_mg)

        wb2.save(f'{self.well_number} {self.well_area}.xlsx')
        return ws2




print(Create_PZ.open_excel_file(self, 'Копия ПЗ 3682 ПиП.xlsx'))
