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




wb = load_workbook('D:\Documents\Create_work_krs\Копия Поглотитель сероводорода.xlsx', data_only=True)
name_list = wb.sheetnames
ws = wb.active
lll = []
for row_ind, row in enumerate(ws.iter_rows(values_only=True, max_col=5)):


    if row[0] not in [None, 'Скважины']:
        well_number = row[0]
        well_area = row[1].replace('ое', 'ая')
        rezult = get_tables_starting_with(well_number, well_area)
        if rezult:

            ws.cell(row=row_ind+ 1, column=4).value = rezult[0]
            if rezult[0] != '3':
                aaaa = rezult[1][10:]
                ws.cell(row=row_ind + 1, column=5).value = 'Применялся'
                ws.cell(row=row_ind + 1, column=6).value = aaaa
            else:
                ws.cell(row=row_ind + 1, column=5).value = 'Не применялся'


wb.save('12236.xlsx')