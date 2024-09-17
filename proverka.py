import psycopg2
from PyQt5.QtWidgets import QMessageBox
from openpyxl.reader.excel import load_workbook

import well_data
import openpyxl

def get_tables_starting_with(well_number, well_area):
    from data_base.work_with_base import connect_to_db, get_table_creation_time
    """
    Возвращает список таблиц, имена которых начинаются с заданного префикса.
    """
    prefix = well_number + ' ' + well_area
    if 'Ойл' in well_data.contractor:
        contractor = 'ОЙЛ'
    elif 'РН' in well_data.contractor:
        contractor = 'РН'

    if prefix != '':
        if well_data.connect_in_base:
            conn = psycopg2.connect(**well_data.postgres_conn_work_well)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name LIKE %s
                """, (prefix + '%',))

            tables = cursor.fetchall()
            if tables:
                tables = tables[0][0]
                print(tables)

                cursor1 = conn.cursor()
                cursor1.execute(f'SELECT * FROM "{tables}"')
                result = cursor1.fetchall()
                if result:
                    return result[3][9], result[3][7]




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