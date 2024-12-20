import openpyxl
from openpyxl.utils.cell import coordinate_from_string
import json
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




wb = openpyxl.load_workbook('Копия Телефоны АР (00000002).xlsx')
ws = wb.active

dict_tel = {}
for row_ind, row in enumerate(ws.iter_rows(values_only=True, min_row=1, max_row=300, max_col=8)):
    for col in row:
        if col == 'Начальник':
            dict_tel.setdefault(
                'ОАО "Башнефть"', {}).setdefault(
                "регион", {}).setdefault(
                row[0], {}).setdefault("ЦДНГ", {}).setdefault(row[1], {}).setdefault("Начальник", {
                "post": row[2], "surname": row[3], "telephone": row[4], "email": row[5]})
        if col == 'Заместитель начальника':
            dict_tel.setdefault(
                'ОАО "Башнефть"', {}).setdefault(
                "регион", {}).setdefault(
                row[0], {}).setdefault("ЦДНГ", {}).setdefault(row[1], {}).setdefault("Заместитель начальника", {
                "post": row[2], "surname": row[3], "telephone": row[4], "email": row[5]})
        if col == 'Ведущий геолог':
            dict_tel.setdefault(
                'ОАО "Башнефть"', {}).setdefault(
                "регион", {}).setdefault(
                row[0], {}).setdefault("ЦДНГ", {}).setdefault(row[1], {}).setdefault("Ведущий геолог", {
                "post": row[2], "surname": row[3], "telephone": row[4], "email": row[5]})
        if col == 'Ведущий инженер-технолог':
            dict_tel.setdefault(
                'ОАО "Башнефть"', {}).setdefault(
                "регион", {}).setdefault(
                row[0], {}).setdefault("ЦДНГ", {}).setdefault(row[1], {}).setdefault("Ведущий инженер-технолог", {
                "post": row[2], "surname": row[3], "telephone": row[4], "email": row[5]})

print(json.dumps(dict_tel['ОАО "Башнефть"']["регион"]["ТГМ"], indent=4,ensure_ascii=False))



