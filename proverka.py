import json

import openpyxl
from openpyxl.utils.cell import range_boundaries, get_column_letter
from copy import copy
# Открываем Excel файл
wb = openpyxl.load_workbook('property_excel/template_gis.xlsx')

# Выбираем активный лист
ws = wb.active
boundaries_dict = {}
values_list = []
for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
    row_list = []
    if row_ind < 90:
        for index_col, col in enumerate(row[:41]):
            row_list.append(col)
    values_list.append(row_list)
for row in values_list:
    print(f'{row},')

