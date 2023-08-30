import sys
import openpyxl as op
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from copy import copy
from openpyxl.utils.cell import range_boundaries
import name
from openpyxl.utils.cell import get_column_letter
# file_path = '6147.xlsx'


fname = '6147.xlsx'


# values1 = []
def open_excel_file(fname):

    wb = op.load_workbook(fname, data_only=True)
    ws = wb.active

    wb2 = op.Workbook()
    ws2 = wb2.active

    column_additional = False

    max_rows = ws.max_row
    cat_well_min = ''
    cat_well_max = ''
    values = []
    data_well_min = ''
    data_well_max = ''
    data_X_min = ''
    data_X_max = ''
    data_pvr_min = ''
    data_pvr_max = ''
    perforations_intervals = []
    head_column_additional = ''
    shoe_column_additional = ''
    column_additional_diametr = ''
    column_additional_wall_thickness = ''
    column_additional_diametr = ''
    column_additional_wall_thickness = ''
    data_column_additional = ''
    bottomhole_artificial = ''

    for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
        if 'Категория скважины' in row:
            cat_well_min = row_ind  # индекс начала категории
        elif 'План-заказ' in row:
            ws.cell(row = row_ind + 1, column = 2).value = 'ПЛАН РАБОТ'
            cat_well_max = row_ind - 1
            data_well_min = row_ind + 1
        elif 'IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in row:
            data_well_max = row_ind -1
        elif 'X. Ожидаемые показатели после ремонта:' in row:
            data_X_min = row_ind
        elif 'ХI Планируемый объём работ:' in row:
            data_x_max = row_ind


        elif 'II. История эксплуатации скважины' in row:
            data_pvr_max = row_ind - 2


        elif '7. Пробуренный забой' in row:
            try:
                bottomhole_artificial = row[5]
            except:
                bottomhole_artificial = row[6]

        for col, value in enumerate(row):

            if 'площадь' == value: # определение номера скважины
                well_number = row[col-1]
                well_area = row[col+1]
            elif '11. Эксплуатационные горизонты и интервалы перфорации:' == value:
                data_pvr_min = row_ind + 2
            elif 'месторождение ' == value:
                oilfield = row[col+2]
            elif value == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))': # Определение данных по колонне

                data_main_production_string = (ws.cell(row = row_ind+2, column = col+1).value).split('(мм)',)
                if len(data_main_production_string) == 3:
                    column_diametr = data_main_production_string[0]
                    wall_thickness = data_main_production_string[1][1:]
                    shoe_column = data_main_production_string[-1].strip().replace('(м)', '')

            elif '9. Максимальный зенитный угол' == value:
                max_angle = row[col+1]
                n = 1
                while max_angle == None:
                    max_angle = row[col + n]
                    n += 1
            elif '9. Максимальный зенитный угол' in row and value == 'на глубине':
                max_h_angle = row[col+1]
            elif 'цех' == value and 'назначение ' in row:
                cdng = row[col+1]

            elif 'по Pпл' == value:
                cat_P_1 = row[col + 1]
                n = 1
                while cat_P_1 == None:
                    cat_P_1 = row[col + n]
                    n += 1
            elif 'по H2S' == value:
                cat_H2S_1 = row[col + 1]
                n = 1
                while cat_H2S_1 == None:
                    cat_H2S_1 = row[col + n]
                    n += 1



            elif '6. Конструкция хвостовика' == value:
                data_column_additional = ws.cell(row=row_ind+3, column = col + 2).value
                if data_column_additional != None or data_column_additional != '-':
                    column_additional = True
                try:
                    head_column_additional =  data_column_additional.split('-')[0]
                    shoe_column_additional = data_column_additional.split('-')[1]
                except:
                    print('Доп колонна отсутствует')
                column_additional_diametr = ws.cell(row=row_ind+3, column = col + 4).value
                column_additional_wall_thickness = ws.cell(row=row_ind+3, column = col + 6).value
            elif 'Максимально ожидаемое давление на устье' == value:
                max_expected_pressure = row[col + 1]
                n = 1
                while  max_expected_pressure == None:
                    max_expected_pressure = row[col+n]
                    n += 1
            elif 'Максимально допустимое давление опрессовки э/колонны' == value:
                max_admissible_pressure = row[col + 1]
                n = 1
                while  max_admissible_pressure  == None:
                    max_admissible_pressure  = row[col+n]
                    n += 1
            elif value == 'Пакер' and row[col + 2] == 'типоразмер':

                paker_do = row[col+4]
                H_F_paker_do = ws.cell(row=row_ind+4, column = col+5).value


    for j in range(data_pvr_min, data_pvr_max): # Сортировка интервала перфорации
        lst = []
        for i in range(11):
            if type(ws.cell(row=j+2, column=i+1).value) == float:
                lst.append(round(ws.cell(row=j+2, column=i+1).value, 1))
            else:
                lst.append(ws.cell(row=j+2, column=i+1).value)
        perforations_intervals.append(lst)

    # sorted_perforations_intervals = sorted(perforations_intervals, key = lambda x: x[3])
    head = f'A{cat_well_min}:S{data_x_max}'
    print(head)
    for _range in ws.merged_cells.ranges:
        boundaries = range_boundaries(str(_range))
        ws2.merge_cells(start_column=boundaries[0], start_row=boundaries[1]+len(name.razdel_1)+1,
                        end_column=boundaries[2], end_row=boundaries[3]+len(name.razdel_1)+1)

    for row_number, row in enumerate(ws[head]):
        for col_number, cell in enumerate(row):
            ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1, cell.value)
            if cell.has_style:
                ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1).font = copy(cell.font)
                ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1).fill = copy(cell.fill)
                ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1).border = copy(cell.border)
                ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1).number_format = copy(cell.number_format)
                ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1).protection = copy(cell.protection)
                ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1).alignment = copy(cell.alignment)
                ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1).quotePrefix = copy(cell.quotePrefix)
                ws2.cell(row_number + 1 + len(name.razdel_1) + cat_well_min, col_number + 1).pivotButton = copy(cell.pivotButton)





    for i in range(1, len(name.razdel_1)): # Добавлением подписантов на вверху
        for j in range(1, 13):
            ws2.cell(row = i, column = j).value = name.razdel_1[i-1][j-1]
    for i in range(1, 16):
        ws2.merge_cells(start_row=i, start_column = 2, end_row =i, end_column = 7)
        ws2.merge_cells(start_row=i, start_column=9, end_row=i, end_column=13)

    for i in range(data_x_max, len(name.itog_1)+data_x_max+1): # Добавлением подписантов на внизу

        for j in range(1, 13):
            ws2.cell(row = i+data_x_max+1, column = j).value = name.itog_1[i+data_x_max+1][j-1]



    ws2.row_dimensions[2].height = 25
    ws2.row_dimensions[6].height = 25

    for row in range(1, 16):

        for col in range(1, 13):
            ws2.cell(row = row, column = col).alignment = ws2.cell(row = row, column = col).alignment.copy(wrapText=True)
    lst2 = []
    for j in range(1, max_rows):

        lst3 = []
        for i in range(1, 13):
            lst3.append(ws2.cell(row=j, column = i).value)
        lst2.append(lst3)
    # print(lst2)
    # data_main_production_string = ws.cell(row=int(ind_data_main_production_string[1:])+1, column=int(ind_data_main_production_string[0])+2).value
    for i in range(1, 15):
        ws2.column_dimensions[get_column_letter(i)].width = 15


    print(f' номер скважины -{well_number}'\
          f' месторождение скважины - {oilfield} '\
          f' площадь - {well_area}'\
          f' ЦДНГ - {cdng}' 
          f' диаметр колонны - {column_diametr}  {wall_thickness} - {shoe_column}'
          f' макс угол {max_angle} на глубине  {max_h_angle}'\
          f' {data_column_additional}'\
          f' доп колонна {head_column_additional} - {shoe_column_additional}'
          f'по Рпл - {cat_P_1},'
          f'по H2S - {int(cat_H2S_1)},'
          f' Диаметр доп коллоны - {column_additional_diametr} - {column_additional_wall_thickness},'
          f' Максимальное давление опрессовки - {max_expected_pressure},'
          f' максимальное ожидаемое давление - {max_admissible_pressure },'
          f' Фондовый пакер в скважине {paker_do} на глубине {H_F_paker_do}')


    wb2.save('123.xlsx')
print(open_excel_file('Копия 212г ГОНС.xlsx'))

