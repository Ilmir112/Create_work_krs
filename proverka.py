import json

import openpyxl

# Открываем Excel файл
from openpyxl.utils import range_boundaries, get_column_letter

wb = openpyxl.load_workbook('property_excel/tepmpale_gnkt_osv_grp.xlsx')

# Выбираем активный лист
ws = wb.active
boundaries_dict = {}
values_list = []
for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
    row_list = []
    if row_ind < 90:
        for index_col, col in enumerate(row[:23]):
            row_list.append(col)
    values_list.append(row_list)
# for row in values_list:
#     print(f'{row},')

colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 25)] + [None]
print(colWidth)


