# Создание нового Excel-файла
import json
import  re
import openpyxl
import psycopg2
from openpyxl.styles import Font, Border, PatternFill, Color
from openpyxl.utils import get_column_letter

import well_data

well_number = '2101'
area_well = 'Копей-Кубовская'

def read_excel_in_base(well_number, area_well):
    conn = psycopg2.connect(**well_data.postgres_params_data_well)
    cursor = conn.cursor()

    cursor.execute("SELECT excel_json FROM wells WHERE well_number = %s AND area_well = %s",
                   (well_number, area_well))
    data_well = cursor.fetchall()

    if cursor:
        cursor.close()
    if conn:
        conn.close()

    dict_well = json.loads(data_well[len(data_well)-1][0])
    data = dict_well['data']

    rowHeights = dict_well['rowHeights']
    colWidth = dict_well['colWidth']
    boundaries_dict = dict_well['merged_cells']
    return data, rowHeights, colWidth, boundaries_dict

def insert_data_new_excel_file(data, rowHeights, colWidth, boundaries_dict):
    wb_new = openpyxl.Workbook()
    sheet_new = wb_new.active


    for row_index, row_data in data.items():
        for col_index, cell_data in enumerate(row_data, 1):
            cell = sheet_new.cell(row=int(row_index), column=int(col_index))
            if cell_data:
                cell.value = cell_data['value']

    for key, value in boundaries_dict.items():
        sheet_new.merge_cells(start_column=value[0], start_row=value[1],
                           end_column=value[2], end_row=value[3])

    # Восстановление данных и стилей из словаря
    for row_index, row_data in data.items():

        for col_index, cell_data in enumerate(row_data, 1):
            cell = sheet_new.cell(row=int(row_index), column=int(col_index))

            # Получение строки RGB из JSON
            rgb_string = cell_data['fill']['color']

            # Извлечение значений R, G, B с помощью регулярных выражений
            match = re.match(r"RGB\((\d+), (\d+), (\d+)\)", rgb_string)
            if match:
                r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))

                # Создание объекта Color
                hex_color = f'{r:02X}{g:02X}{b:02X}'
                color = Color(rgb=hex_color)

                # Создание объекта заливки
                fill = PatternFill(patternType='solid', fgColor=color)
                cell.fill = fill
            cell.font = Font(name=cell_data['font']['name'], size=cell_data['font']['size'],
                             bold=cell_data['font']['bold'], italic=cell_data['font']['italic'])

            cell.border = openpyxl.styles.Border(left=openpyxl.styles.Side(style=cell_data['borders']['left']),
                                                 right=openpyxl.styles.Side(style=cell_data['borders']['right']),
                                                 top=openpyxl.styles.Side(style=cell_data['borders']['top']),
                                                 bottom=openpyxl.styles.Side(style=cell_data['borders']['bottom']))


            cell.alignment = openpyxl.styles.Alignment(horizontal=cell_data['alignment']['horizontal'],
                                                       vertical=cell_data['alignment']['vertical'],
                                                       wrap_text=cell_data['alignment']['wrap_text'])



    for col in range(13):
        sheet_new.column_dimensions[get_column_letter(col + 1)].width = colWidth[col]

    for index_row, row in enumerate(sheet_new.iter_rows()):  # Копирование высоты строки
        if all([col is None for col in row]):
            sheet_new.row_dimensions[index_row].hidden = True
        sheet_new.row_dimensions[index_row].height = rowHeights[index_row-1]

    # Сохранение нового Excel-файла
    wb_new.save('new_excel_file.xlsx')

data, rowHeights, colWidth, boundaries_dict = read_excel_in_base(well_number, area_well)
insert_data_new_excel_file(data, rowHeights, colWidth, boundaries_dict)




