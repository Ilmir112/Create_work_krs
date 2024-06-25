# Получите список имен всех листов в файле
from openpyxl.reader.excel import load_workbook

file = '335г Мустафинское ГНКТ, БСКО.xlsx'

workbook = load_workbook(filename=file)
sheets = workbook.sheetnames
a = []
# Перебор листов и вывод их содержимого
for sheet_name in sheets:
    sheet = workbook[sheet_name]

    # Перебор строк и столбцов
    for row in sheet.iter_rows(values_only=True):
        a.append(list(row[:12]))

print(a)