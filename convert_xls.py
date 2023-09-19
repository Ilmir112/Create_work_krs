# Задача: конвертация эксель из xls в xlsx
# Все остальные библиотеки работают вкось
# Эксель должен быть установлен на компе!!!

# pip bloks
##     python -m pip install --upgrade pywin32

# import bloks
import os

import win32com.client as win32

# config bloks
path =os.getcwd()
format_files = ('.xls')

pred_prefiks_file_name = ''

# relise bloks
for root, dirs, files in os.walk(path):
    for file in files:
        if(file.endswith(format_files, 0, len(file))):
##            print(os.path.join(file))## - этот вариант выводит только имя файла
            print(file)
##        print(os.path.join(root, file))## - этот вариант выводит полный путь и имя файла
            # -------делаем через COM объект -----------------------------
            excel = win32.gencache.EnsureDispatch('Excel.Application')
            wb = excel.Workbooks.Open(os.path.join(root, file))
            wb.SaveAs(pred_prefiks_file_name+os.path.join(root, file)+'x', FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
            wb.Close()                               #FileFormat = 56 is for .xls extension
            excel.Application.Quit()

input("Работа завершена. Тисни ентер.")