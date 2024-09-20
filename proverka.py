import psycopg2
from PyQt5.QtWidgets import QMessageBox
from openpyxl.reader.excel import load_workbook

import well_data
import openpyxl






wb = load_workbook('912.xlsx', data_only=True)
name_list = wb.sheetnames
ws = wb.active
lll = []
for row_ind, row in enumerate(ws.iter_rows(values_only=True, max_col=11, min_row=156, max_row=180)):
    ll = []
    for col_ind, col in enumerate(row):
        ll.append(col)
    lll.append(ll)


print(lll)