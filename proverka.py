import openpyxl
from openpyxl.utils.cell import coordinate_from_string
from data_base.work_with_base import ClassifierWell

def excel_to_html(excel_file):
    """Преобразует Excel-файл с объединенными ячейками в HTML-код."""

    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active

    # Получаем список всех объединенных диапазонов
    merged_ranges = worksheet.merged_cells.ranges

    # Создаем HTML-код для таблицы
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Таблица из Excel</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }

            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: center;
            }

            th {
                background-color: #f2f2f2;
            }

            .merged {
                text-align: center;
            }
        </style>
    </head>
    <body>
        <table>
            <thead>
    '''

    # Заголовки столбцов
    for col_num in range(1, worksheet.max_column + 1):
        html += f'<th>{worksheet.cell(row=1, column=col_num).value}</th>'

    html += '''
            </thead>
            <tbody>
    '''

    # Данные
    for row_num in range(2, worksheet.max_row + 1):
        html += '<tr>'

        for col_num in range(1, worksheet.max_column + 1):
            cell = worksheet.cell(row=row_num, column=col_num)

            # Проверяем, является ли ячейка частью объединенной
            is_merged = False
            for merged_range in merged_ranges:
                if cell.coordinate in merged_range:
                    is_merged = True
                    break

            if is_merged:
                # Получаем координаты первой ячейки объединенного диапазона
                first_cell = coordinate_from_string(merged_range.coord[0])
                first_row = first_cell[1]
                first_col = first_cell[0]

                # Вычисляем colspan и rowspan
                colspan = merged_range.coord[1].split(':')[1][0] - merged_range.coord[0].split(':')[0][0] + 1
                rowspan = int(merged_range.coord[1].split(':')[1][1:]) - int(merged_range.coord[0].split(':')[0][1:]) + 1

                # Добавляем объединенную ячейку
                html += f'<td colspan="{colspan}" rowspan="{rowspan}" class="merged">{worksheet.cell(row=first_row, column=first_col).value}</td>'
            else:
                # Добавляем обычную ячейку
                html += f'<td>{cell.value}</td>'

        html += '</tr>'

    html += '''
            </tbody>
        </table>
    </body>
    </html>
    '''

    return html

# # Пример использования
# excel_file = 'data.xlsx'
# html_code = excel_to_html(excel_file)
#
# # Сохранение HTML-кода в файл
# with open('data.html', 'w') as f:
#     f.write(html_code)

guery = f'CREATE TABLE chemistry ' \
        f'(well_number TEXT,'\
        f'well_area TEXT,'\
        f'region TEXT,'\
        f'costumer TEXT,'\
        f'contractor TEXT,'\
        f'work_plan TEXT,'\
        f'type_kr TEXT,'\
        f'today DATE,'\
        f'cement FLOAT,'\
        f'HCl FLOAT,'\
        f'HF FLOAT,'\
        f'NaOH FLOAT,'\
        f'VT_SKO FLOAT,'\
        f'clay FLOAT,'\
        f'sand FLOAT,'\
        f'RPK FLOAT,'\
        f'RPP FLOAT,'\
        f'RKI FLOAT,'\
        f'ELAN FLOAT,'\
        f'ASPO FLOAT,'\
        f'RIR_2C FLOAT,'\
        f'RIR_OVP FLOAT,'\
        f'gidrofabizator FLOAT,'\
        f'norm_time FLOAT,'\
        f'fluid TEXT)'

#
# {'пункт': [], 'цемент': 0, 'HCl': 0, 'HF': 0, 'NaOH': 0, 'ВТ СКО': 0,
#                          'Глина': 0, 'растворитель': 0, 'уд.вес': 0,
#                          'песок': 0, 'РПК': 0, 'РПП': 0, "извлекаемый пакер": 0, "ЕЛАН": 0}


ClassifierWell.insert_database('well_data', "data_work", guery)