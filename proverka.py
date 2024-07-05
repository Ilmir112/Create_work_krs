import openpyxl

# Открываем Excel файл
workbook = openpyxl.load_workbook('D:/Documents/Desktop/ПЗ/Копия 1329 ПНЛГ.xlsx')
sheet = workbook.active

# Создаем список, в котором будем хранить данные из Excel файла
data_list = []

# Итерируемся по строкам в Excel файле и сохраняем данные в список
for ind, row in enumerate(sheet.iter_rows(values_only=True)):
    if ind > 185 and ind < 223:
        data_list.append(list(row[:12]))

# Выводим список с данными
print(data_list)
