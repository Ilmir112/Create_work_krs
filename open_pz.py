import sys

import openpyxl as op
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from copy import copy
from openpyxl.utils.cell import range_boundaries
import name
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
import plan


fname = '6147.xlsx'


# values1 = []
def open_excel_file(fname):

    wb = op.load_workbook(fname, data_only=True)
    ws = wb.active

    wb2 = op.Workbook()
    ws2 = wb2.get_sheet_by_name('Sheet')
    ws2.title = "План работ"

    column_additional = False

    max_rows = ws.max_row
    cat_well_min = ''
    cat_well_max = ''
    values = []
    data_well_min = ''
    data_well_max = ''
    data_x_min = ''
    data_x_max = ''
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
    row_expected = []
    for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
        if 'Категория скважины' in row:
            cat_well_min = row_ind +1 # индекс начала категории
        elif 'План-заказ' in row:
            ws.cell(row = row_ind + 1, column = 2).value = 'ПЛАН РАБОТ'
            cat_well_max = row_ind - 1
            data_well_min = row_ind + 1
        elif 'IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in row:
            data_well_max = row_ind - 1
        elif 'X. Ожидаемые показатели после ремонта:' in row:
            data_x_min = row_ind

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

    list_block_append = [cat_well_min, data_well_min+1, data_well_max]

    for j in range(data_x_min, data_x_max): # Ожидаемые показатели после ремонта
        lst = []
        for i in range(0, 12):
           lst.append(ws.cell(row=j+1, column=i + 1).value)
        row_expected.append(lst)

    bound = []
    for _range in ws.merged_cells.ranges:
        boundaries = range_boundaries(str(_range))
        if data_pvr_min+2 <= boundaries[1] <= data_pvr_max+2:
            bound.append(boundaries)
            # ws2.unmerge_cells(start_column=boundaries[0], start_row=boundaries[1] + len(name.razdel_1) + 1,
            #                end_column=boundaries[2], end_row=boundaries[3] + len(name.razdel_1) + 1)
        elif boundaries[1] >= data_well_max+3:
            bound.append(boundaries)
        else:
            ws2.merge_cells(start_column=boundaries[0], start_row=boundaries[1]+len(name.razdel_1)+1,
                        end_column=boundaries[2], end_row=boundaries[3]+len(name.razdel_1)+1)


    for j in range(data_pvr_min, data_pvr_max): # Сортировка интервала перфорации
        lst = []
        for i in range(1,12):
            if type(ws.cell(row=j+1, column=i+1).value) == float:
                lst.append(round(ws.cell(row=j+1, column=i+1).value, 1))
            else:
                lst.append(ws.cell(row=j+2, column=i+1).value)
        perforations_intervals.append(lst)
    perforations_intervals = sorted(perforations_intervals, key = lambda x: x[3])

    ins_ind = len(name.razdel_1) + cat_well_min
    print(ins_ind)
    for i in range(1, len(list_block_append)): # цикл добавления блоков план-заказов
        head = plan.head_ind(list_block_append[i-1], list_block_append[i]+2)
        name_values = name.razdel_1
        index_row = list_block_append[i-1]
        ins_ind += (list_block_append[i]+2-list_block_append[i-1])
        print(ins_ind)
        plan.copy_row(ws, ws2, name_values, index_row, head)


    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    for i in range(1, len(perforations_intervals)+1):  # Добавление данных по интервалу перфорации
        for j in range(1, 12):

            ws2.cell(row=i + data_pvr_min + len(name.razdel_1) + 2, column=j + 1).border = thin_border
            ws2.cell(row=i + data_pvr_min + len(name.razdel_1) + 2, column=j + 1).font = 'Arial'
            ws2.cell(row=i + data_pvr_min + len(name.razdel_1) + 2, column=j + 1).alignment = Alignment(wrap_text=True)
            ws2.cell(row=i+data_pvr_min + len(name.razdel_1)+2, column=j+1).value = perforations_intervals[i-1][j-1]
    print(list_block_append[-1] - 4 - len(name.razdel_1))
    for i in range(ins_ind, ins_ind + len(name.events_gnvp)):
        ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)

        for j in range(2):

            if i == ins_ind + 13 or i == ins_ind + 28:
                ws2.cell(row=i, column=1 + 1).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
                ws2.cell(row=i, column=1 + 1).font = Font(name='Arial',size = 13, bold = True)

                ws2.cell(row=i, column=1 + 1).value = name.events_gnvp[i - ins_ind][j]
            else:
                ws2.cell(row=i, column=j + 1).alignment = Alignment(wrap_text=True, horizontal='left', vertical='top')
                ws2.cell(row=i, column=j + 1).font = Font(name='Arial',size = 12)

                ws2.cell(row=i, column=j + 1 ).value = name.events_gnvp[i-ins_ind][j]
    ins_ind += len(name.events_gnvp)-1

    for i in range(1, len(name.razdel_1)): # Добавлением подписантов на вверху
        for j in range(1, 13):

            ws2.cell(row = i, column = j).value = name.razdel_1[i-1][j-1]
            ws2.cell(row=i, column=j).font = Font(name='Arial',size = 13, bold = False)
    for i in range(1, 16):
        ws2.merge_cells(start_row=i, start_column = 2, end_row =i, end_column = 7)
        ws2.merge_cells(start_row=i, start_column=9, end_row=i, end_column=13)




    ws2.row_dimensions[2].height = 30
    ws2.row_dimensions[6].height = 30

    for row in range(1, 16):
       for col in range(1, 13):
            ws2.cell(row = row, column = col).alignment = ws2.cell(row = row, column = col).alignment.copy(wrapText=True)
            ws2.cell(row= row, column=j + col).font = 'Arial'
    lst2 = []
    for j in range(1, max_rows):
        lst3 = []
        for i in range(1, 13):
            lst3.append(ws2.cell(row=j, column = i).value)
        lst2.append(lst3)
    #print(lst2)
    # data_main_production_string = ws.cell(row=int(ind_data_main_production_string[1:])+1, column=int(ind_data_main_production_string[0])+2).value

    rowHeights_gnvp = [95.0, 155.5, 110.25, 36.0, 52.25, 36.25, 36.0, 45.25, 20.25, 135.75, 38.5, 30.25, 30.5,
                       18.0, 50.5, 21.75, 240.75, 125.0, 66.75, 48.0, 33.0, 38.25, 45.0, 32.25, 45.75, 30.75, 32.25,
                       310.0, 21.75, 50.25, 57.25, 78.75, 64.5, 25.0, 25.0, 25.0, 25.0]

    rowHeights = [ws.row_dimensions[i + 1].height  for i in range(data_well_max+2)] + rowHeights_gnvp
    colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]

    for index_row, row in enumerate(ws2.iter_rows()): # Копирование высоты строки
       if len(rowHeights) >= index_row:
           ws2.row_dimensions[index_row+len(name.razdel_1)+1].height = rowHeights[index_row-1]
       for col_ind, col in enumerate(row):

           if col_ind <= 12:
               ws2.column_dimensions[get_column_letter(col_ind+1)].width = colWidth[col_ind]
           else:
               break
    ws2.unmerge_cells(start_column=2, start_row=ins_ind,end_column=12, end_row=ins_ind)
    print(ins_ind)
    row_expected = row_expected[::-1]
    for i in range(len(row_expected)):  # Добавление данных по интервалу перфорации
        for j in range(1, 13):
            ws2.cell(row=i+ins_ind, column=j).font = Font(name='Arial',size = 13, bold = True)
            ws2.cell(row=i+ins_ind, column=j).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
            ws2.cell(row=i+ins_ind, column=j).value = row_expected[i-1][j-1]

        ws2.merge_cells(start_column=2, start_row=ins_ind, end_column=12, end_row=ins_ind)
    print(row_expected)


    # print(f' номер скважины -{well_number}'\
    #       f' месторождение скважины - {oilfield} '\
    #       f' площадь - {well_area}'\
    #       f' ЦДНГ - {cdng}'
    #       f' диаметр колонны - {column_diametr}  {wall_thickness} - {shoe_column}'
    #       f' макс угол {max_angle} на глубине  {max_h_angle}'\
    #       f' {data_column_additional}'\
    #       f' доп колонна {head_column_additional} - {shoe_column_additional}'
    #       f'по Рпл - {cat_P_1},'
    #       f'по H2S - {int(cat_H2S_1)},'
    #       f' Диаметр доп коллоны - {column_additional_diametr} - {column_additional_wall_thickness},'
    #       f' Максимальное давление опрессовки - {max_expected_pressure},'
    #       f' максимальное ожидаемое давление - {max_admissible_pressure },'
    #       f' Фондовый пакер в скважине {paker_do} на глубине {H_F_paker_do}')


    wb2.save('123.xlsx')
print(open_excel_file('Копия 212г ГОНС.xlsx'))

# imp