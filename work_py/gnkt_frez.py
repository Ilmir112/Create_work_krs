from datetime import datetime

from PyQt5.QtWidgets import QInputDialog, QMainWindow, QTabWidget, QWidget, QTableWidget, QApplication
# from PyQt5.uic.properties import QtWidgets
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from PyQt5 import QtCore, QtWidgets

import block_name
import main
import plan
from block_name import razdel_1
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

from gnkt_data.gnkt_data import dict_saddles


# class TabPage_SO(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
# class TabWidget(QTabWidget):
#     def __init__(self):
#         super().__init__()
#         self.addTab(TabPage_SO(self), 'Титульный лист')
#         self.addTab(TabPage_SO(self), 'Схема')
#         self.addTab(TabPage_SO(self), 'Ход работ')

class Work_with_gnkt(QMainWindow):
    wb_gnkt_frez = Workbook()

    def __init__(self, ws, tabWidget, table_title, table_schema, table_widget):

        from open_pz import CreatePZ
        super(QMainWindow, self).__init__()
        self.table_widget = table_widget
        self.table_title = table_title
        self.table_schema = table_schema

        self.dict_perforation = CreatePZ.dict_perforation
        self.ws = ws
        # self.tabWidget = tabWidget
        # self.table_title = table_widget

        # self.tabWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        # self.tabWidget.customContextMenuRequested.connect(self.openContextMenu)
        # self.setCentralWidget(self.table_title)
        # self.model = self.tabWidget.model()
        #
        # # Этот сигнал испускается всякий раз, когда ячейка в таблице нажата.
        # # Указанная строка и столбец - это ячейка, которая была нажата.
        # self.tabWidget.cellPressed[int, int].connect(self.clickedRowColumn)

        self.ws_title = Work_with_gnkt.wb_gnkt_frez.create_sheet(title="Титульник")

        self.ws_schema = Work_with_gnkt.wb_gnkt_frez.create_sheet(title="Схема")
        self.ws_work = Work_with_gnkt.wb_gnkt_frez.create_sheet(title="Ход работ")

        head = plan.head_ind(CreatePZ.cat_well_min, CreatePZ.cat_well_max + 1)
        # print(f'ff  {head}')p
        # print(self.ws)
        plan.copy_true_ws(self.ws, self.ws_title, head)

        create_title = self.create_title_list(self.ws_title)
        schema_well = self.schema_well(self.ws_schema)

        main.MyWindow.copy_pz(self, self.ws_title, table_title, 13, 'gnkt_frez', 1)
        main.MyWindow.copy_pz(self, self.ws_schema, table_schema, 47, 'gnkt_frez', 2)
        main.MyWindow.copy_pz(self, self.ws_work, table_widget, 12, 'gnkt_frez', 3)
        work_well = self.work_gnkt_frez()
        main.MyWindow.populate_row(self, 0, work_well, table_widget)

        # self.count_row_height(self.ws_work, work_well)#
        # Work_with_gnkt.wb_gnkt_frez.save(f"{CreatePZ.well_number} {CreatePZ.well_area} {CreatePZ.cat_P_1} категории.xlsx")
        # print('файл сохранен')

    def count_row_height(ws2, work_list, sheet_name):
        from openpyxl.utils.cell import range_boundaries, get_column_letter

        text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 90: (301, 400), 110: (401, 500),
                           130: (501, 600), 150: (601, 700), 170: (701, 800), 190: (801, 900), 210: (901, 1500)}

        boundaries_dict = {}

        for ind, _range in enumerate(ws2.merged_cells.ranges):
            boundaries_dict[ind] = range_boundaries(str(_range))

        for key, value in boundaries_dict.items():
            ws2.unmerge_cells(start_column=value[0], start_row=value[1],
                              end_column=value[2], end_row=value[3])

        for i in range(1, len(work_list) + 1):  # Добавлением работ
            for j in range(1, 13):
                cell = ws2.cell(row=i, column=j)

                if cell and str(cell) != str(work_list[i - 1][j - 1]):
                    if str(work_list[i - 1][j - 1]).replace('.', '').isdigit() and \
                            str(work_list[i - 1][j - 1]).count('.') != 2:
                        cell.value = str(work_list[i - 1][j - 1]).replace('.', ',')
                        # print(f'цифры {cell.value}')
                    else:
                        cell.value = work_list[i - 1][j - 1]
                    if sheet_name.lower() == 'ход работ':
                        if j == 11:
                            cell.font = Font(name='Arial', size=11, bold=False)
                        # if j == 12:
                        #     cell.value = work_list[i - 1][j - 1]
                        else:
                            cell.font = Font(name='Arial', size=13, bold=False)
                        ws2.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
                        ws2.cell(row=i, column=11).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')
                        ws2.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                         vertical='center')
                        ws2.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                        vertical='center')
                        if 'примечание' in str(cell.value).lower() \
                                or 'заявку оформить за 16 часов' in str(cell.value).lower() \
                                or 'ЗАДАЧА 2.9.' in str(cell.value).upper() \
                                or 'ВСЕ ТЕХНОЛОГИЧЕСКИЕ ОПЕРАЦИИ' in str(cell.value).upper() \
                                or 'за 48 часов до спуска' in str(cell.value).upper():
                            # print('есть жирный')
                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                        elif 'порядок работы' in str(cell.value).lower() or \
                                'Наименование работ' in str(cell.value):
                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                            ws2.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                            vertical='center')
        # print(merged_cells_dict)

        for key, value in boundaries_dict.items():
            # print(value)
            ws2.merge_cells(start_column=value[0], start_row=value[1],
                            end_column=value[2], end_row=value[3])

        print(f'{sheet_name} - вставлена')

    def save_to_gnkt(self):
        from open_pz import CreatePZ

        sheets = ["Титульник", 'Схема', 'Ход работ']
        tables = [self.table_title, self.table_schema, self.table_widget]

        for i, sheet_name in enumerate(sheets):
            worksheet = Work_with_gnkt.wb_gnkt_frez[sheet_name]
            table = tables[i]

            work_list = []
            for row in range(table.rowCount()):
                row_lst = []
                # self.ins_ind_border += 1
                for column in range(table.columnCount()):

                    item = table.item(row, column)
                    if not item is None:

                        row_lst.append(item.text())
                        # print(item.text())
                    else:
                        row_lst.append("")
                work_list.append(row_lst)
            Work_with_gnkt.count_row_height(worksheet, work_list, sheet_name)

        # path = 'workiii'
        path = 'D:\Documents\Desktop\ГТМ'
        filenames = f"{CreatePZ.well_number} {CreatePZ.well_area} кат {CreatePZ.cat_P_1} {self.work_plan}.xlsx"
        full_path = path + '/' + filenames
        # print(f'10 - {ws2.max_row}')
        # print(wb2.path)
        # print(f' кате {CreatePZ.cat_P_1}')
        if 1 in CreatePZ.cat_P_1 or 1 in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_gaz_f_pr:
            ws5 = Work_with_gnkt.wb_gnkt_frez.create_sheet('Sheet1')
            ws5.title = "Схемы ПВО"
            ws5 = Work_with_gnkt.wb_gnkt_frez["Схемы ПВО"]
            Work_with_gnkt.wb_gnkt_frez.move_sheet(ws5, offset=-1)
            # schema_list = self.check_pvo_schema(ws5, ins_ind + 2)

        if Work_with_gnkt.wb_gnkt_frez:
            Work_with_gnkt.wb_gnkt_frez.remove(Work_with_gnkt.wb_gnkt_frez['Sheet'])
            Work_with_gnkt.wb_gnkt_frez.save(full_path)
            Work_with_gnkt.wb_gnkt_frez.close()
            print(f"Table data saved to Excel {full_path} {CreatePZ.number_dp}")
        if self.wb:
            self.wb.close()

    def create_title_list(self, ws2):
        from open_pz import CreatePZ

        CreatePZ.region = block_name.region(CreatePZ.cdng)
        self.region = CreatePZ.region

        title_list = [
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, 'ООО «Башнефть-Добыча»', None, None, None, None, None, None, None, None, None, None],
            [None, None, None, f'{CreatePZ.cdng}', None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, 'ПЛАН РАБОТ НА СКВАЖИНЕ С ПОМОЩЬЮ УСТАНОВКИ С ГИБКОЙ ТРУБОЙ', None, None, None,
             None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, '№ скважины:', f'{CreatePZ.well_number}', 'куст:', None, 'Месторождение:', None, None,
             CreatePZ.well_oilfield, None, None],
            [None, None, 'инв. №:', CreatePZ.inv_number, None, None, None, None, 'Площадь: ', CreatePZ.well_area, None,
             1],
            [None, None, None, None, None, None, None, None, None, None, None, None]]

        razdel = razdel_1(self, self.region)
        for row in razdel:  # Добавлением работ
            title_list.append(row)

        for row in [
            [None, None, None, None, None, "дата", datetime.now().strftime('%d.%m.%Y'), None, None, None, None]]:
            title_list.insert(-1, row)
        # print(title_list)
        index_insert = 11
        ws2.cell(row=1, column=2).alignment = Alignment(wrap_text=False, horizontal='left',
                                                        vertical='center')
        ws2.cell(row=1, column=4).alignment = Alignment(wrap_text=False, horizontal='left',
                                                        vertical='center')
        # ws2.column_dimensions[get_column_letter(1)].width = 15
        # ws2.column_dimensions[get_column_letter(2)].width = 20
        # ws2.column_dimensions[get_column_letter(3)].width = 20
        a = None
        for row in range(len(title_list)):  # Добавлением работ
            if row not in range(8, 13):
                ws2.row_dimensions[row].height = 35
            for col in range(1, 12):
                ws2.column_dimensions[get_column_letter(col)].width = 15
                cell = ws2.cell(row=row + index_insert, column=col)
                # print(f' Х {title_list[i ][col - 1]}')
                if title_list[row - 1][col - 1] != None:
                    ws2.cell(row=row + index_insert, column=col).value = str(title_list[row - 1][col - 1])
                ws2.cell(row=row + index_insert, column=col).font = Font(name='Arial', size=11, bold=False)
                ws2.cell(row=row + index_insert, column=col).alignment = Alignment(wrap_text=False, horizontal='left',
                                                                                   vertical='center')
                if 'ПЛАН РАБОТ' in str(title_list[row - 1][col - 1]):
                    ws2.merge_cells(start_row=row + index_insert, start_column=2, end_row=row + index_insert,
                                    end_column=10)
                    ws2.cell(row=row + index_insert, column=col).font = Font(name='Arial', size=14, bold=True)
                    ws2.cell(row=row + index_insert, column=col).alignment = Alignment(wrap_text=False,
                                                                                       horizontal='center',
                                                                                       vertical='center')
                if 'СОГЛАСОВАНО:' in str(title_list[row - 1][col - 1]):
                    a = row + index_insert

            # for row in range(len(title_list)):  # Добавлением работ
            if a:
                if a > row:
                    print(f'сссооссоссо {row + index_insert}')
                    ws2.merge_cells(start_row=row + index_insert, start_column=2, end_row=row + index_insert,
                                    end_column=5)
                    ws2.merge_cells(start_row=row + index_insert, start_column=8, end_row=row + index_insert,
                                    end_column=11)

        ws2.print_area = f'B1:j{44}'
        ws2.page_setup.fitToPage = True
        ws2.page_setup.fitToHeight = False
        ws2.page_setup.fitToWidth = True
        ws2.print_options.horizontalCentered = True
        # зададим размер листа
        ws2.page_setup.paperSize = ws2.PAPERSIZE_A4

    def schema_well(self, ws3):
        from open_pz import CreatePZ
        from krs import volume_vn_nkt, well_volume

        boundaries_dict = {0: (13, 13, 14, 14), 1: (43, 12, 45, 12), 2: (40, 16, 42, 16), 3: (7, 19, 12, 19),
                           4: (17, 21, 18, 21), 5: (19, 21, 20, 21), 6: (13, 10, 30, 10), 7: (15, 15, 16, 15),
                           8: (1, 1, 49, 2), 9: (46, 19, 48, 19), 10: (27, 15, 28, 15), 11: (29, 15, 30, 15),
                           12: (40, 11, 42, 11), 13: (33, 5, 48, 5), 14: (23, 15, 26, 15), 15: (13, 16, 14, 16),
                           16: (15, 16, 16, 16), 17: (9, 34, 48, 34), 18: (19, 19, 20, 19), 19: (27, 16, 28, 16),
                           20: (29, 19, 30, 19), 21: (13, 18, 14, 18), 22: (40, 13, 42, 13), 23: (23, 16, 26, 16),
                           25: (27, 18, 28, 18), 26: (13, 17, 14, 17), 27: (15, 17, 16, 17),
                           28: (17, 17, 18, 17), 29: (32, 8, 39, 8), 30: (40, 15, 42, 15), 31: (19, 20, 20, 20),
                           32: (21, 20, 22, 20), 33: (21, 14, 22, 14), 34: (13, 19, 14, 19),
                           36: (11, 13, 12, 13), 37: (43, 7, 48, 7), 38: (37, 3, 48, 3), 39: (7, 6, 12, 11), 40:
                               (27, 22, 28, 22), 41: (19, 22, 20, 22), 42: (32, 18, 39, 18), 43: (21, 22, 22, 22),
                           44: (46, 23, 48, 23), 45: (7, 18, 12, 18), 47: (43, 8, 48, 8),
                           48: (13, 7, 30, 7), 49: (46, 15, 48, 15), 50: (43, 14, 45, 14), 51: (40, 18, 42, 18),
                           52: (17, 23, 18, 23), 53: (43, 10, 48, 10), 54: (29, 14, 30, 14),
                           56: (40, 8, 42, 8), 57: (29, 23, 30, 23), 58: (43, 13, 45, 13), 59: (7, 20, 12, 20),
                           60: (15, 13, 16, 14), 61: (40, 17, 42, 17), 62: (17, 13, 18, 14), 63: (43, 9, 48, 9),
                           64: (13, 8, 30, 8), 65: (27, 13, 30, 13), 67: (13, 21, 14, 21),
                           68: (15, 21, 16, 21), 69: (40, 10, 42, 10), 70: (17, 15, 18, 15), 71: (43, 15, 45, 15),
                           72: (32, 12, 39, 12), 73: (7, 22, 12, 22), 74: (40, 19, 42, 19), 75: (32, 21, 39, 21),
                           76: (46, 17, 48, 17), 77: (21, 18, 22, 18), 78: (46, 22, 48, 22), 79: (7, 12, 12, 12),
                           80: (40, 9, 42, 9), 81: (7, 21, 12, 21), 82: (10, 5, 30, 5), 83: (32, 7, 39, 7),
                           85: (7, 23, 12, 23), 86: (13, 9, 30, 9), 87: (46, 12, 48, 12),
                           88: (21, 19, 22, 19), 89: (43, 16, 45, 16), 90: (2, 34, 8, 34), 91: (32, 22, 45, 22),
                           92: (27, 17, 28, 17), 94: (22, 3, 26, 3), 95: (29, 17, 30, 17), 93: (2, 36, 6, 36),
                           96: (43, 21, 48, 21), 97: (23, 18, 26, 18), 98: (13, 11, 30, 11), 99: (46, 20, 48, 20),
                           100: (15, 19, 16, 19), 101: (10, 38, 11, 38), 102: (46, 14, 48, 14), 103: (43, 18, 45, 18),
                           104: (27, 19, 28, 19), 105: (23, 17, 26, 17), 106: (43, 17, 45, 17), 107: (40, 21, 42, 21),
                           108: (23, 19, 26, 19), 109: (13, 12, 30, 12), 110: (15, 20, 16, 20), 111: (14, 3, 21, 3),
                           112: (17, 20, 18, 20), 113: (43, 19, 45, 19), 114: (32, 16, 39, 16), 115: (19, 14, 20, 14),
                           116: (15, 22, 16, 22), 117: (40, 7, 42, 7), 118: (32, 9, 39, 9), 119: (13, 15, 14, 15),
                           120: (21, 21, 22, 21), 121: (32, 15, 39, 15), 122: (32, 11, 39, 11), 123: (46, 16, 48, 16),
                           124: (7, 13, 10, 13), 125: (27, 21, 28, 21), 126: (32, 23, 45, 23), 127: (29, 21, 30, 21),
                           128: (43, 11, 48, 11), 129: (23, 13, 26, 14), 130: (13, 23, 14, 23), 131: (40, 6, 48, 6),
                           132: (19, 13, 22, 13), 133: (15, 23, 16, 23), 134: (46, 18, 48, 18), 135: (27, 23, 28, 23),
                           137: (23, 21, 26, 21), 138: (19, 16, 22, 16), 139: (32, 13, 39, 13),
                           140: (40, 20, 42, 20), 141: (19, 15, 22, 15), 142: (17, 16, 18, 16), 143: (29, 16, 30, 16),
                           144: (15, 18, 16, 18), 145: (10, 37, 11, 37), 146: (17, 18, 18, 18), 147: (19, 18, 20, 18),
                           148: (29, 18, 30, 18), 149: (7, 15, 12, 15), 150: (40, 12, 42, 12), 151: (13, 6, 30, 6),
                           152: (13, 20, 14, 20), 153: (19, 16, 22, 16), 154: (30, 3, 36, 3), 155: (32, 10, 39, 10),
                           156: (40, 14, 42, 14), 157: (17, 19, 18, 19), 158: (19, 23, 26, 23), 159: (7, 24, 48, 24),
                           160: (32, 6, 39, 6), 161: (13, 22, 14, 22), 162: (27, 20, 28, 20), 163: (7, 16, 12, 16),
                           164: (29, 20, 30, 20), 165: (19, 17, 22, 17), 166: (17, 22, 18, 22), 167: (32, 20, 39, 20),
                           168: (32, 14, 39, 14), 169: (11, 14, 12, 14), 170: (23, 20, 26, 20), 171: (29, 22, 30, 22),
                           172: (46, 13, 48, 13), 173: (43, 20, 45, 20), 174: (32, 17, 39, 17), 175: (23, 22, 26, 22),
                           176: (7, 17, 12, 17), 177: (32, 19, 39, 19), 178: (27, 14, 28, 14), 179: (9, 36, 43, 36),
                           180: (7, 14, 10, 14)}

        rowHeights1 = [None, None, 27.75, 20.25, 20.25, 20.25, 20.25, 18.0, 22.5, 22.5, 22.5, 18.0, 18.0, 20.25,
                       20.25, 20.25, 20.25, 20.25, 20.25, 20.25, 20.25, 18.0, 20.25, 35.25, 17.25, 17.25, 79.5, 60.0,
                       13.5, 13.5, 43.5, 13.5, None, 45.75, None, 74.25, None, None, None, None, None, None, 13.5,
                       12.75, 12.75, 12.75, None, None, None, None, None, None, None, 15.75, 12.75, 12.75, 12.75,
                       None, None, None, None, None, None, None, 15.75, 15.75, 12.75, 12.75, 12.75, None, None, None,
                       None, None, None, 13.5, 12.75, None, None, None, None, None, None, None, None, None, None, 13.5,
                       None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                       None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                       None, None, 134.25, None, None, None, None, None, None, None]

        colWidth = [2.28515625, 13.0, 4.5703125, 13.0, 13.0, 13.0, 5.7109375, 13.0, 13.0, 13.0, 4.7109375,
                    13.0, 5.140625, 13.0, 13.0, 13.0, 13.0, 13.0, 4.7109375, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                    13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                    13.0, 13.0, 13.0, 5.42578125, 13.0, 4.5703125, 2.28515625, 10.28515625]

        plast_work = CreatePZ.plast_all[0]
        print(plast_work, list(CreatePZ.dict_perforation[plast_work]))
        pressuar = f'{list(CreatePZ.dict_perforation[plast_work]["давление"])[0]}атм'
        pressuar1 = list(CreatePZ.dict_perforation[plast_work]["давление"])[0]
        zamer = list(CreatePZ.dict_perforation[plast_work]['замер'])[0]
        vertikal = min(map(float, list(CreatePZ.dict_perforation[plast_work]["вертикаль"])))
        zhgs = f'{list(CreatePZ.dict_perforation[plast_work]["рабочая жидкость"])[0]}г/см3'
        koef_anomal = round(float(pressuar1) * 101325 / (float(vertikal) * 9.81 * 1000), 1)
        nkt = int(list(CreatePZ.dict_nkt.keys())[0])
        lenght_nkt = sum(list(map(int, CreatePZ.dict_nkt.values())))

        bottom_first_port = max(sorted([interval for interval in CreatePZ.dict_perforation[plast_work]['интервал']],
                                       key=lambda x: x[0]))[0]

        arm_grp, ok = QInputDialog.getInt(None, 'Арматура ГРП',
                                          'ВВедите номер Арматуры ГРП', 16, 0, 500)

        gnkt_lenght, _ = QInputDialog.getInt(None, 'Длина ГНКТ',
                                             'ВВедите длину ГНКТ', 3500, 500, 10000)
        volume_vn_gnkt = round(30.2 ** 2 * 3.14 / (4 * 1000), 2)
        volume_gnkt = round(gnkt_lenght * volume_vn_gnkt / 1000, 1)

        well_volume_ek = well_volume(self, CreatePZ.head_column_additional)
        well_volume_dp = well_volume(self, CreatePZ.current_bottom) - well_volume_ek

        volume_pm_ek = round(3.14 * (CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness) ** 2 / 4 / 1000, 2)
        volume_pm_dp = round(3.14 * (CreatePZ.column_additional_diametr - 2 *
                                     CreatePZ.column_additional_wall_thickness) ** 2 / 4 / 1000, 2)

        schema_well_list = [
            ['СХЕМА СКВАЖИНЫ', None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None, None,
             '№ скважины:', None, None, None, None, None, None, None, CreatePZ.well_number, None, None, None, None,
             None, None,
             None, 'Месторождение:', None, None, None, None, None, None, CreatePZ.well_oilfield, None, None, None, None,
             None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None,
             'Данные о размерности НКТ о конструкции скважины',
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None,
             'Дополнительная информация', None, None, None, None, None, None, None, None, None, None, None, None, None,
             None],
            [None, None, None, None, None, None,
             'Оборудование \n устья скважины', None, None, None, None, None,
             'Лубрикатор + герметизатор', None, None, None, None, None, None,
             None, None, None, None, None, None, None,
             None, None, None, None, None,
             'Категория скважины по опасности', None, None, None, None, None, None, None,
             'первая [после бурения)', None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'БП 80х70', None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             'Пластовое давление', None, None, None, None, None, None, None, pressuar, None, None, zamer, None, None,
             None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'тройник 80х70-80х70 В60-В60',
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             'Содержание H2S', None, None, None, None, None, None, None, round(CreatePZ.H2S_mg[0], 5), None, None, None,
             None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             f'ФА  ГРП ГУ 180х35-89 К1ХЛ № {arm_grp}',
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             'Газовый фактор', None, None, None, None, None, None, None, CreatePZ.gaz_f_pr[0], None, None, None, None,
             None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Переходная катушка 180х21-89-3"',
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             f'Глубина пл.{plast_work} по вертикали', None, None, None, None, None, None, None, vertikal, None, None,
             None, None, None, None, None],

            [' ', None, None, None, None, None, None, None, None, None, None, None,
             'Устьевая крестовина АУЭЦН-50х14-168 ОТТМ К1 ЛЗ ХЛ №181', None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None,
             'Коэффициент  аномальности', None, None, None, None, None, None, None, koef_anomal, None, None,
             None, None, None, None, None],

            [' ', None, None, None, None, None, 'Тип КГ', None, None, None, None, None,
             CreatePZ.column_head_m, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             'Макс.угол в горизонт. участке', None, None, None, None, None, None, None, CreatePZ.max_angle, None, None,
             'на глубине', None, None, CreatePZ.max_angle_H, None],

            [None, None, None, None, None, None,
             'Диаметр канавки', None, None, None, None, None, 'Наруж.\nдиаметр',
             None, 'Толщина стенки', None, 'Внутр.\nдиаметр', None, 'Глубина', None, None, None, 'ВЦП.\nДлина ПО', None,
             None, None, 'Объем', None, None, None, None, 'Макс. интенс. набора кривизны', None, None, None, None, None,
             None, None, f'{6.21}/10м', None, None, 'на глубине', None, None, '1310', None],

            [None, None, None, None, None, None,
             'Стол ротора', None, None, None, f'{CreatePZ.stol_rotora}м', None, None, None, None, None,
             None, None, 'от', None, 'до', None, None, None, None, None, 'п.м', None, 'м3', None, None,
             'Жидкость глушения', None, None, None, None, None, None, None, zhgs, None, None, 'в объеме', None, None,
             f'{28.9}м3', None],
            [None, None, None, None, None, None, 'Направление', None, None, None, None, None,
             CreatePZ.column_direction_diametr, None, CreatePZ.column_direction_wall_thickness, None,
             CreatePZ.column_direction_diametr - 2 * CreatePZ.column_direction_wall_thickness, None,
             CreatePZ.column_direction_lenght, None, None, None, CreatePZ.level_cement_direction, None, None,
             None, None, None, None, None, None, 'Ожидаемый дебит',
             None, None, None, None, None, None, None, f'{CreatePZ.Qwater}м3/сут', None, None,
             f'{CreatePZ.Qoil}м3', None, None,
             f'{CreatePZ.proc_water}%', None],
            [None, None, None, None, None, None, 'Кондуктор', None, None, None, None, None,
             CreatePZ.column_conductor_diametr, None, CreatePZ.column_conductor_wall_thickness, None,
             CreatePZ.column_conductor_diametr - 2 * CreatePZ.column_conductor_wall_thickness,
             None, CreatePZ.column_conductor_lenght, None, None, None, CreatePZ.level_cement_conductor,
             None, None, None, None, None, None, None, None,
             'Начало / окончание бурения', None, None, None, None, None, None, None,
             self.date_dmy(CreatePZ.date_drilling_run), None, None,
             self.date_dmy(CreatePZ.date_drilling_cancel), None, None, None,
             None],
            [None, None, None, None, None, None, 'Экспл. колонна', None, None, None, None, None,
             CreatePZ.column_diametr, None, CreatePZ.column_wall_thickness, None,
             CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness, None, CreatePZ.shoe_column, None, None,
             None, CreatePZ.level_cement_column, None, None, None, volume_pm_ek, None, well_volume_ek,
             None, None, 'Р в межколонном пространстве', None, None, None, None, None, None, None,
             f'{0}атм', None, None, None, self.date_dmy(CreatePZ.date_drilling_cancel), None, None, None],
            [None, None, None, None, None, None, "Хвостовик  ''НТЦ ''ЗЭРС''", None, None, None, None,
             None, CreatePZ.column_additional_diametr, None,
             CreatePZ.column_additional_wall_thickness, None,
             CreatePZ.column_additional_diametr - 2 * CreatePZ.column_additional_wall_thickness, None,
             CreatePZ.head_column_additional, None, CreatePZ.shoe_column_additional, None, 'не цементиров.', None,
             None, None, volume_pm_dp,
             None, well_volume_dp, None, None, 'Давление опрессовки МКП', None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, f'Подвеска НКТ {nkt}мм', None, None, None, None, None, nkt, None, 6.5,
             None, nkt - 2 * 6.5, None, f'{0}-', None, f'{lenght_nkt - 0.5 - 2.6 - 3}м', None,
             f'{lenght_nkt - 0.5 - 2.6 - 3}м', None, None, None,
             volume_vn_nkt(CreatePZ.dict_nkt), None, volume_vn_nkt(CreatePZ.dict_nkt) + 0.47, None, None,
             'Давление опрессовки ЭК ', None, None, None, None,
             None, None, None, f'{CreatePZ.max_expected_pressure}атм', None, None,
             None,
             None, None, 'гермет.', None],
            [None, None, None, None, None, None, 'Гидроякорь ', None, None, None, None, None, 122, None, None, None, 71,
             None, f'{lenght_nkt}', None, f'{lenght_nkt + 1}м', None, f'{0.5}м3', None, None, None, None, None, None,
             None,
             None, 'Макс. допустимое Р опр-ки ЭК', None, None, None, None, None, None, None,
             CreatePZ.max_admissible_pressure, None, None, None,
             None, None, None, None],
            [None, None, None, None, None, None, 'Патрубок 1 шт.', None, None, None, None, None, nkt, None, 6.5, None,
             74.2, None, lenght_nkt - 5.6, None, f'{lenght_nkt - 2.6}м', None, f'{3}м', None, None, None, None,
             None, None, None, None, 'Макс. ожидаемое Р на устье скв.', None, None, None, None, None, None, None, 92.8,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, f'стингер {CreatePZ.paker_do["do"]}', None, None, None, None, None,
             None, None,
             None, None, 71, None, lenght_nkt - 2.6, None, lenght_nkt, None, f'{2.6}м', None, None, None, None,
             None, None, None, None, 'Текущий забой до ГРП ', None, None, None, None, None, None, None, None, None,
             None, None, None, None, f'{CreatePZ.current_bottom}м', None],
            [None, None, None, None, None, None, 'ГНКТ', None, None, None, None, None, 38.1, None, 3.96, None, 30.18,
             None, gnkt_lenght, None, None, None, None, None, None, None, volume_vn_gnkt, None,
             volume_gnkt, None,
             None, 'Искусственный забой  (МГРП №1 с актив.шаром 30мм)', None, None, None, None, None, None, None, None,
             None, None, None, None, None, f'{bottom_first_port}м', None]]

        ports_data = self.work_with_port(plast_work, CreatePZ.dict_perforation)
        ports_list, merge_port = self.insert_ports_data(ports_data)
        # print(ports_list)
        for row in ports_list:
            schema_well_list.append(row)

        border = Border(left=Side(border_style='dashed', color='FF000000'),
                        top=Side(border_style='dashed', color='FF000000'),
                        right=Side(border_style='dashed', color='FF000000'),
                        bottom=Side(border_style='dashed', color='FF000000'),
                        )
        border_left_top = Border(left=Side(border_style='thick', color='FF000000'),
                                 top=Side(border_style='thick', color='FF000000'),
                                 right=Side(border_style='dashed', color='FF000000'),
                                 bottom=Side(border_style='dashed', color='FF000000'),
                                 )
        border_left_bottom = Border(left=Side(border_style='thick', color='FF000000'),
                                    top=Side(border_style='dashed', color='FF000000'),
                                    right=Side(border_style='dashed', color='FF000000'),
                                    bottom=Side(border_style='thick', color='FF000000'),
                                    )
        border_right_bottom = Border(left=Side(border_style='dashed', color='FF000000'),
                                     top=Side(border_style='dashed', color='FF000000'),
                                     right=Side(border_style='thick', color='FF000000'),
                                     bottom=Side(border_style='thick', color='FF000000'),
                                     )
        border_right_top = Border(top=Side(border_style='thick', color='FF000000'),
                                  right=Side(border_style='thick', color='FF000000'))

        border_right = Border(left=Side(border_style='dashed', color='FF000000'),
                              top=Side(border_style='dashed', color='FF000000'),
                              right=Side(border_style='thick', color='FF000000'),
                              bottom=Side(border_style='dashed', color='FF000000'),
                              )
        border_left = Border(left=Side(border_style='thick', color='FF000000'),
                             top=Side(border_style='dashed', color='FF000000'),
                             right=Side(border_style='dashed', color='FF000000'),
                             bottom=Side(border_style='dashed', color='FF000000'),
                             )
        border_top = Border(left=Side(border_style='dashed', color='FF000000'),
                            top=Side(border_style='thick', color='FF000000'),
                            right=Side(border_style='dashed', color='FF000000'),
                            bottom=Side(border_style='dashed', color='FF000000'),
                            )
        border_bottom = Border(left=Side(border_style='dashed', color='FF000000'),
                               top=Side(border_style='dashed', color='FF000000'),
                               right=Side(border_style='dashed', color='FF000000'),
                               bottom=Side(border_style='thick', color='FF000000'),
                               )

        for row in range(1, len(schema_well_list) + 1):  # Добавлением работ
            # print(row, len(schema_well_list[row-1]), schema_well_list[row-1][15])
            for col in range(1, 48):
                cell = ws3.cell(row=row, column=col)

                cell.value = schema_well_list[row - 1][col - 1]
                ws3.cell(row=row, column=col).font = Font(name='Arial', size=11, bold=False)
                ws3.cell(row=row, column=col).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                    vertical='center')
                if cell.value != None and row > 24:
                    cell.border = border

        for row in range(6, 24):
            for col in range(7, 32):
                cell = ws3.cell(row=row, column=col)

                cell.border = border
                if col == 31:
                    cell.border = Border(left=Side(border_style='thick', color='FF000000'),
                                         right=Side(border_style='thick', color='FF000000'))
                if row == 6 and col != 31:
                    cell.border = border_top
                elif (row == 22) and col != 31:
                    cell.border = border_bottom
                elif (row == 23) and col != 31:
                    cell.border = border_bottom
                elif col == 7:
                    cell.border = border_left
                elif col == 30:
                    cell.border = border_right

                elif (row == 13 or row == 14) and col > 12 and col != 31:
                    cell.border = Border(left=Side(border_style='thin', color='FF000000'),
                                         top=Side(border_style='thin', color='FF000000'),
                                         right=Side(border_style='thin', color='FF000000'),
                                         bottom=Side(border_style='thin', color='FF000000'),
                                         )

            for col in range(32, 49):
                cell = ws3.cell(row=row, column=col)
                cell.border = border
                if row == 6:
                    cell.border = border_top
                elif (row == 22):
                    cell.border = border_bottom
                elif (row == 23):
                    cell.border = border_bottom
                elif (row == row and col == 32):
                    cell.border = border_left
                elif (row == row and col == 48):
                    cell.border = border_right

        ws3.cell(6, 7).border = border_left_top
        ws3.cell(6, 32).border = border_left_top
        ws3.cell(22, 7).border = border_left_bottom
        ws3.cell(23, 7).border = border_left_bottom
        ws3.cell(22, 32).border = border_left_bottom
        ws3.cell(23, 32).border = border_left_bottom

        ws3.cell(6, 30).border = border_right_top
        ws3.cell(6, 48).border = border_right_top
        ws3.cell(22, 30).border = border_left_bottom
        ws3.cell(23, 30).border = border_left_bottom
        ws3.cell(22, 48).border = border_left_bottom
        ws3.cell(23, 48).border = border_right_bottom
        ws3.cell(23, 30).border = border_right_bottom

        for key, value in merge_port.items():
            boundaries_dict[key] = value

            if key % 2 == 0:
                coordinate = f'{get_column_letter(value[0] - 1)}{value[1] + 4}'
                print(f'вставка1 ')
                column_img = f'H{value[1] + 6}'

                main.MyWindow.insert_image(self, ws3, 'imageFiles/schema_well/port.png', coordinate, 200, 200)

            for i in range(3):
                cell = ws3.cell(row=27, column=value[0] + i)
                cell2 = ws3.cell(row=28, column=value[0] + i)
                font = Font(bold=True, italic=True)
                cell.font = font
                cell2.font = font
                cell.alignment = Alignment(textRotation=90, horizontal='center', vertical='center')
                cell2.alignment = Alignment(textRotation=90, horizontal='center', vertical='center')

        # print(boundaries_dict)
        for key, value in boundaries_dict.items():
            ws3.merge_cells(start_column=value[0], start_row=value[1],
                            end_column=value[2], end_row=value[3])

        for index_row, row in enumerate(ws3.iter_rows()):  # Копирование высоты строки
            ws3.row_dimensions[index_row].height = rowHeights1[index_row - 1]

        for col_ind in range(50):  # копирование ширины столба
            ws3.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind] / 1.9

        coordinate = f'B3'
        print(f'вставка2 ')
        main.MyWindow.insert_image(self, ws3, 'imageFiles/schema_well/gorizont_1.png', coordinate, 237, 1023)
        print(column_img)
        main.MyWindow.insert_image(self, ws3, 'imageFiles/schema_well/gorizont_12.png', column_img, 1800, 120)

        ws3.print_area = f'A1:AW{37}'
        ws3.page_setup.fitToPage = True
        ws3.page_setup.fitToHeight = False
        ws3.page_setup.fitToWidth = True
        # Измените формат листа на альбомный
        ws3.page_setup.orientation = ws3.ORIENTATION_LANDSCAPE
        ws3.print_options.horizontalCentered = True
        # зададим размер листа
        ws3.page_setup.paperSize = ws3.PAPERSIZE_A4

    def work_gnkt_frez(self):

        krs_begin_gnkt = [
            [None, None, 'Порядок работы', None, None, None, None, None, None, None, None, None],
            [None, None, 'Наименование работ', None, None, None, None, None, None, None, 'Ответственный',
             'Нормы времени \n мин/час.'],
            [None, 1,
             f'Начальнику смены ЦТКРС, вызвать телефонограммой представителя Заказчика для оформления АКТа '
             f'приёма-передачи скважины в ремонт. \n'
             f'Совместно с представителем Заказчика оформить схему расстановки оборудования при КРС с обязательной '
             f'подписью представителя Заказчика на схеме.',
             None, None, None, None, None, None, None,
             'Мастер КРС, предст-ль Заказчика.', float(0.5)],
            [None, 2,
             f'Принять скважину в ремонт у Заказчика с составлением АКТа. Переезд  бригады. Подготовительные работы к '
             f'КРС. Определить технологические '
             f'точки откачки жидкости у Заказчика согласно Договора.',
             None, None, None, None, None, None, None,
             ' Предст-тель Заказчика, мастер КРС', float(0.5)],
            [None, 3,
             f'Перед началом работ по освоению, капитальному и текущему ремонту скважин бригада должна быть '
             f'ознакомлена с возможными осложнениями и авариями'
             f'в процессе работ, планом локализации и ликвидации аварии (ПЛА) и планом работ. С работниками '
             f'должен быть проведен инструктаж по выполнению работ, '
             f'связанных с применением новых технических устройств и технологий с соответствующим оформлением в '
             f'журнал инструктажей на рабочем месте ',
             None, None, None, None, None, None, None,
             'Мастер КРС', float(0.75)]]

        gnkt_work_list = [
            [None, 'Мероприятия по предотвращению аварий, инцидентов и несчастных случаев:',
             None, None, None, None, None, None, None, None, None, None],
            [None, 'Все операции при производстве работ выполнять в соответствии с действующими Федеральными нормами и'
                   ' правилами в области промышленной безопасности "Правила безопасности в нефтяной и газовой промышленности" , РД 153-39-023-97, технологической инструкцией "Требования безопасности при ведении монтажных работ и производстве текущего, капитального ремонта и освоения скважин после бурения" П2-05.01 ТИ-0001 , инструкцией «По предупреждению газонефтеводопроявлений и открытых фонтанов при бурении, освоении, геофизических исследованиях,  эксплуатации скважин, реконструкции, ремонте, техническом  перевооружении, консервации и ликвидации скважин, а также при проведении геофизических  и прострелочно-взрывных работах на скважинах» № П3-05 И-102089 ЮЛ-305, акта (наряд) допуска, мероприятий по сокращению аварийности, протоколов ГТС, молний, писем, доведённых обществом (ООО "Башнефть-Добыча") и других действующих в ООО "Башнефть-Добыча" нормативных документов.',
             None, None, None, None, None, None, None, None, None, None],
            [None, 'Мероприятия при нахождении рядом с ремонтируемой скважиной работающих скважин', None, None, None,
             None, None, None, None, None, None, None],
            [None, '№', 'Мероприятия', None, None, None, None, None, None, None, None, 'Ответственный'],
            [None, 1, 'Провести устный инструктаж бригаде по проведению ремонта с соседними работающими скважинами.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 2,
                                                                              'В схеме расстановки бригадного хозяйства обозначить опасные зоны работающих скважин (определить с Заказчиком при оформлении наряд-допуска)',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'],
            [None, 3,
                                                                                                     'Оградить работающие скважины по периметру сигнальной лентой (по одной слева, справа) в радиусе 3 метра.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 4,
             'При монтаже или демонтаже подъёмного агрегата для ремонта скважины, соседние с ремонтируемой (по одной слева, справа), эксплуатирующиеся глубинными штанговыми насосами, скважины остановить. Необходимость остановки определить с Заказчиком при приёмке скважины, отразить в наряд-допуске.',
             None, None, None, None, None, None, None, None, 'Представитель «Заказчика»'], [None, 5,
                                                                                            'Установить предупреждающие знаки на соседних работающих скважинах (по одной слева¸ справа) «Внимание! Скважина работает!»',
                                                                                            None, None, None, None,
                                                                                            None, None, None, None,
                                                                                            'Мастер ГНКТ'], [None, 6,
                                                                                                             'Не допускать проведения монтажных, погрузо-разгрузочных работ в радиусе не менее 3 метров от работающих скважин',
                                                                                                             None, None,
                                                                                                             None, None,
                                                                                                             None, None,
                                                                                                             None, None,
                                                                                                             'Мастер ГНКТ'],
            [None, 7,
             'При проведении работ по отбору проб, замеру динамических уровней и т.д в обязательном порядке информировать мастера бригады КРС о проведении данных работ.',
             None, None, None, None, None, None, None, None, 'Представитель «Заказчика»'], [None, 8,
                                                                                            'Не допускать складирования на запорной арматуре и площадках для исследования ремонтируемой скважины, а также соседних скважин инструмента, оборудования, электрокабелей, труб и т.д. и т.п.',
                                                                                            None, None, None, None,
                                                                                            None, None, None, None,
                                                                                            'Мастер ГНКТ'],
            [None, 9, 'При расстановке оборудования бригады не загромождать доступ к соседним работающим скважинам.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 10,
                                                                              'Согласовать схему расстановки оборудования и путей эвукуации с мастером ЦДНГ/ЦППД на схеме коммуникаций-приложение к наряд -допуску.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, 11,
                                                                                                     'При обнаружении на соседних скважинах пропусков нефти, газа или воды немедленно закрыть устье ремонтируемой скважины, остановить работы и сообщить о происшествии в ЦДНГ/ЦППД.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 12,
             'Установка экранирующих устройств на соседних с ремонтируемой скважиной определяется наряд-допуском, выданным Заказчиком.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 'Мероприятия по предотвращению аварий (ГНВП и открытых фонтанов)', None, None, None, None, None,
             None, None, None, None, None],
            [None, '№', 'Мероприятия', None, None, None, None, None, None, None, None, 'Ответственный'], [None, 1,
                                                                                                          'Перед началом ремонта и перед каждой сменой проводить дополнительный инструктаж по предупреждению газонефтеводопроявлений с Проведением ежесменных учебных тревог «Выброс» с записью в вахтовом журнале.',
                                                                                                          None, None,
                                                                                                          None, None,
                                                                                                          None, None,
                                                                                                          None, None,
                                                                                                          'Мастер ГНКТ'],
            [None, 2,
             'Ежедневно, перед началом работ проверять комплектность и работоспособность противовыбросового оборудования, с отметкой в журнале ежесменного осмотра оборудования.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 3, 'При перерывах в работе запрещается оставлять устье скважины открытым.', None, None, None, None,
             None, None, None, None, 'Мастер ГНКТ'], [None, 4,
                                                      'Производить замеры ГВС при спуске, промывках и освоении не реже, чем как через каждый час, с записью в журнале времени и результатов замеров ГВС. В случае возникновения газонефтеводопроявления следует прекратить все работы, загерметизировать устье скважины и сообщить об этом в службу ЦИТС ООО «ВЕТЕРАН» по тел. 8(35342)76292 и «Заказчика»',
                                                      None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, None, 'Диспетчер АЦДНГ №1 (DISP-ACDNG1@bn.rosneft.ru) +7 (34783) 79722', None, None, None, None,
             None, None, None, None, None], [None, 5,
                                             'Перед началом работ по капитальному ремонту скважин иметь в наличии в исправном состоянии средства пожаротушения в соответствии с перечнем.',
                                             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 6, 'Двухкратный запас жидкости глушения уд.веса 1,23г/см3 в объеме 57,8м3 находится на', None, None,
             None, None, None, None, None, None, 'Заказчик'], [None, None,
                                                               'ПНТЖ "Крезол" на расстоянии 18км от скважины. ООО "Ветеран" в случае необходимости (аварийного глушения) обязуется обеспечить завоз жидкости глушения на объект работ.',
                                                               None, None, None, None, None, None, None, None, None],
            [None, 7,
             'До начала работ, а также на все время выполнения работ, всю технику, принимающую участие в технологических операциях, оборудовать искрогасителями.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 8,
                                                                              'Опрессовку ПВО скважин 1ой категории производить в присутствии представителя ПФС. \nЗаявку на представителя ПФЧ подавать за 24 часа телефонограммой. \nПо окончании опрессовоки ПВО, получить разрешения от представителя ПФС.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'],
            [None, 'Мероприятия по охране окружающей среды:', None, None, None, None, None, None, None, None, None,
             None], [None, '№', 'Мероприятия', None, None, None, None, None, None, None, None, 'Ответственный'],
            [None, 1,
             'При производстве работ не допускается попадания нефтесодержащей жидкости и солевого раствора на рельеф.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 2, 'Утилизацию технологических отходов производить по договору с Заказчиком.', None, None, None,
             None, None, None, None, None, 'Мастер ГНКТ'], [None, 3,
                                                            'ТБО, образующиеся в процессе производства работ складировать в специальные контейнеры, обозначенные надписью «ТБО»',
                                                            None, None, None, None, None, None, None, None,
                                                            'Мастер ГНКТ'],
            [None, 4, 'Ежесменно проверять состояние запорной арматуры на нефтяных и водяных ёмкостях.', None, None,
             None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 5,
                                                                  'При допущенных розливах нефти и задавочной жидкости в кратчайшие сроки необходимо провести мероприятия по устранению розлива, с утилизацией нефтесодержащего материала.',
                                                                  None, None, None, None, None, None, None, None,
                                                                  'Мастер ГНКТ'],
            [None, 'ЦЕЛЬ ПРОГРАММЫ', None, None, None, None, None, None, None, None, None, None], [None,
                                                                                                   'СПО промывочной КНК-1 с промывкой до МГРП №5. СПО фрезеровочной КНК-2: фрезерование МГРП №5-№2. Тех.отстой , замер Ризб. По доп.согласованию с Заказчиком, СПО промывочной КНК-1 до текущего забоя (МГРП №1).',
                                                                                                   None, None, None,
                                                                                                   None, None, None,
                                                                                                   None, None, None,
                                                                                                   None], [None,
                                                                                                           'Внимание: Для проведения технологических операций завоз жидкости производить с ПНТЖ, согласованного с Заказчиком. Перед началом работ согласовать с Заказчиком пункт утилизации жидкости.',
                                                                                                           None, None,
                                                                                                           None, None,
                                                                                                           None, None,
                                                                                                           None, None,
                                                                                                           None, None],
            [None, 'ПОРЯДОК ПРОВЕДЕНИЯ РАБОТ', None, None, None, None, None, None, None, None, None, None],
            [None, '№', None, None, None, None, None, None, None, None, None, 'Ответственный'], [None, 1,
                                                                                                 'Ознакомить бригаду с планом работ и режимными параметрами дизайна по промывке и СПО. Провести инструктаж по промышленной безопасности',
                                                                                                 None, None, None, None,
                                                                                                 None, None, None, None,
                                                                                                 'Мастер ГНКТ'],
            [None, 2, 'Принять скважину у Заказчика по акту (состояние ф/арматуры и кустовой площадки.)', None, None,
             None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 3,
                                                                  'Расставить оборудование и технику согласно «Типовой схемы расстановки оборудования и спецтехники при проведении капитального ремонта скважин с использованием установки «Койлтюбинг».',
                                                                  None, None, None, None, None, None, None, None,
                                                                  'Мастер ГНКТ'], [None, 4,
                                                                                   'Произвести завоз технологической жидкости в объеме не менее 10м3 плотностью не более 1,02г/см3. При интенсивном самоизливе скважины в процессе работ или при отрицательной температуре окружающего воздуха, только по доп.согласованию с Заказчиком, перейти на технологическую жидкость с удельным весом до 1,18г/см3.',
                                                                                   None, None, None, None, None, None,
                                                                                   None, None, 'Мастер ГНКТ. Заказчик'],
            [None, 5,
             'При наличии, согласно плана заказа, Н2S добавить в завезенную промывочную жидкость нейтролизатор сероводорода "Реком-102" в концентрации 0.5л на 10м³',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ. Заказчик'], [None, 6,
                                                                                        'Внимание: при проведении работ по ОПЗ с кислотными составами, весь состав вахты обязан применять СИЗ (Инструкция П1-01.03 И-0128 ЮЛ-305 ООО"Башнефть-Добыча")',
                                                                                        None, None, None, None, None,
                                                                                        None, None, None,
                                                                                        'Мастер ГНКТ'], [None, None,
                                                                                                         'Примечание: на месте проведения работ по ОПЗ кислотами и их смесями должен быть аварийный запас спецодежды, спецобуви и других средств индивидуальной защиты, запас чистой пресной воды и средств нейтрализации кислоты (мел, известь, хлорамин).',
                                                                                                         None, None,
                                                                                                         None, None,
                                                                                                         None, None,
                                                                                                         None, None,
                                                                                                         None],
            [None, 'Ограничения веса и скоростей при СПО', None, None, None, None, None, None, None, None, None, None],
            [None, 7,
             'Максимальный расчётный вес ГНКТ при подъёме с забоя – 4,2т; при спуске – 0,4т; в неподвижном состоянии - 2,4т. Максимальный допустимая нагрузка на ГНКТ - 18т.',
             None, None, None, None, None, None, None, None, None], [None, 8,
                                                                     'Скорость спуска по интервалам:\nв устьевом оборудовании не более 0.5м/мин;\nв интервале 2- 1081м не более 10-15м/мин - (первичный-последующий спуск);\nв интервале 1081-1127м не более 2 м/мин;\nв интервале 1127-1439м не более 5-10 м/мин (фрез.КНК / промыв.КНК);\nв интервале установки МГРП (± 20м) не более 2 м/мин;\nв интервале 1439-1459м не более 2 м/мин;',
                                                                     None, None, None, None, None, None, None, None,
                                                                     'Мастер, бурильщик ГНКТ'], [None, 9,
                                                                                                 'Скорость подъёма по интервалам:\nв интервале 1459-1127 не более 10 м/мин; \nв интервале установки МГРП (± 20м) не более 2 м/мин;\nв интервале 1127-1081м не более 2 м/мин;\nв  интервале 1081-2м не более 12-15м/мин (первичный-последующий подъем);\nв устьевом оборудовании не более 0.5 м/мин.',
                                                                                                 None, None, None, None,
                                                                                                 None, None, None, None,
                                                                                                 'Мастер, бурильщик ГНКТ'],
            [None, 10,
             'При спуске производить приподъёмы для проверки веса на высоту не менее 20м со скоростью не более 5м/мин через каждые 300-500м (первичный-последующий спуск) в НКТ и 50-100м в ЭК.',
             None, None, None, None, None, None, None, None, 'Мастер, бурильщик ГНКТ'],
            [None, 11, 'Перед каждой промывкой и после проверять веса ГТ (вверх, вниз, собств.)', None, None, None,
             None, None, None, None, None, 'Мастер, бурильщик ГНКТ'], [None, 12,
                                                                       'При проведении технологического отстоя - не оставлять ГНКТ без движения - производить расхаживания г/трубы на 20м вверх и на 20м вниз со скоростью СПО не более 3м/мин. При отрицательной температуре окружающей среды, во избежании получения ледяной пробки в г/трубе при проведении тех.отстоя ни в коем случае не прекращать минимальную циркуляцию жидкости по г/трубе.',
                                                                       None, None, None, None, None, None, None, None,
                                                                       'Мастер, бурильщик ГНКТ'], [None, 13,
                                                                                                   'Не допускать увеличение нагрузки на г/трубу в процессе спуска. РАЗГРУЗКА Г/ТРУБЫ НЕ БОЛЕЕ 500 кг от собственного веса на этой глубине.',
                                                                                                   None, None, None,
                                                                                                   None, None, None,
                                                                                                   None, None,
                                                                                                   'Мастер, бурильщик ГНКТ'],
            [None, 'Монтаж и опрессовка', None, None, None, None, None, None, None, None, None, None], [None, 14,
                                                                                                        'Собрать Компоновку Низа Колонны-1 далее КНК-1: коннектор + сдвоенный обратный клапан + насадка-промывочная Ø 38,1мм',
                                                                                                        None, None,
                                                                                                        None, None,
                                                                                                        None, None,
                                                                                                        None, None,
                                                                                                        'Мастер ГНКТ'],
            [None, 15,
             'Произвести монтаж 4-х секционного превентора БП 80-70.00.00.000 (700атм) и инжектора на устье скважины согласно "Схемы №6 обвязки устья скважин I, II, III категории опасности возникновения ГНВП после проведения гидроразрыва пласта и работы на скважинах ППД с оборудованием койлтюбинговых установок на месторождениях ООО "Башнефть-Добыча" от 02.04.2019г. Произвести обвязку установки ГНКТ, насосно-компрессорного агрегата, желобной циркуляционной системы.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 16,
                                                                              'Внимание: Все требования ПБ и ОТ должны быть доведены до сведения работников, персонал должен быть проинформирован о начале проведения опрессовок. Все опрессовки производить согласно инструкции опрессовки ПВО и инструкции опрессовки нагнетательной и выкидной линии перед производством работ на скважине с Колтюбинговыми установками.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, 17,
                                                                                                     'При отрицательной температуре окружающей среды, нагреть до 50ºC и прокачать по ГНКТ солевой раствор в объеме ГНКТ для предотвращения замерзания раствора внутри г/трубы (получения ледяной пробки).',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 18,
             'При закрытой центральной задвижке фонтанной арматуры опрессовать ГНКТ и все нагнетательные линии на 250атм. Опрессовать ПВО, обратные клапана и выкидную линию от устья скважины до желобной ёмкости (надёжно закрепить, оборудовать дроссельными задвижками) опрессовать на 105атм с выдержкой 30мин. Результат опрессовки ПВО зафиксировать в вахтовом журнале и составить акт опрессовки ПВО. Установить на малом и большом затрубе технологический манометр. Провести УТЗ и инструктаж. Опрессовку проводить в присутствии представителя ПФС, мастера, бурильщика, машиниста подъемника и представителя супервайзерской службы. \nЗаявку на представителя ПФЧ подавать за 24 часа телефонограммой. По окончании опрессовоки ПВО, получить разрешения от представителя ПФС.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 'СПО промывочной КНК-1', None, None, None, None, None, None, None, None, None, None], [None, 19,
                                                                                                          'Открыв скважину и записав число оборотов задвижки – зафиксировать дату и время. Спустить КНК-1 в скважину с периодическими прокачками рабочей жидкостью (тех.вода 1,02г/см3)  с проверкой веса на подъём через каждые 300м спуска до глубины 1081м.',
                                                                                                          None, None,
                                                                                                          None, None,
                                                                                                          None, None,
                                                                                                          None, None,
                                                                                                          'Мастер ГНКТ'],
            [None, 20,
             'ВНИМАНИЕ: при получении посадки в НКТ в процессе спуска и наличии разгрузки на промывочный инструмент более 500кг (уведомить Заказчика – составить АКТ на посадку). Приподнять КНК-1 на 20м выше этой глубины.Произвести вывод НКА на рабочий режим, восстановить устойчивую циркуляцию промывочной жидкости (тех.вода 1,02г/см3) , продолжить спуск до гл.1081м с постоянным контролем промывочной жидкости в обратной ёмкости на наличие мех. примесей. Скорость спуска при промывке НКТ не более 5м/мин. Контрольная проверка веса через каждые 100м промывки.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 21,
                                                                              'На гл.1081м  произвести вывод НКА на рабочий режим, восстановить устойчивую циркуляцию промывочной жидкости (тех.вода 1,02г/см3), при необходимости произвести запуск и вывод на режим МАК, получить стабильную круговую циркуляцию азотированной смеси. Промывка в течении 60мин с контролем на мех.примеси в обратной ёмкости.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, None], [None, None,
                                                                                            'ВНИМАНИЕ: В процессе промывки скважины - параметры азотированной промывочной смеси могут изменяться (от 80 до 200л/мин по жидкости (тех.вода 1,02г/см3) и от 8 до 20м3/мин по азоту) в зависимости от качества выноса посторонних частиц с забоя - данный процесс находиться под постоянным контролем у мастера по сложным работам ГНКТ.',
                                                                                            None, None, None, None,
                                                                                            None, None, None, None,
                                                                                            None], [None, 22,
                                                                                                    'Произвести допуск КНК-1 с промывкой до "Муфты ГРП №5" на гл.1216,05-1216,95м.\nСкорость спуска при промывке не более 5м/мин, проверка веса на подъём через каждые 30м.',
                                                                                                    None, None, None,
                                                                                                    None, None, None,
                                                                                                    None, None,
                                                                                                    'Мастер ГНКТ'],
            [None, 23,
             'При промывке, в случае выноса большого объёма проппанта из пласта (или в случае поглощения промывочной жидкости) поинтервально через каждые 10м (или через каждые 2м) производить прокачку и  сопровождение гелевой пачки объёмом 0,5-3м3 со скоростью 10 м/мин до гл.1081м',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 24,
                                                                              'При слабой циркуляции или аномальном поглощении (более 5м3/ч) промывочной жидкости (тех.вода 1,02г/см3)  в процессе промывки, уведомить Заказчика, приподнять КНК-1 до гл.1081м восстановить стабильную круговой циркуляции жидкости (тех.вода 1,02г/см3). Допустить КНК-1 с циркуляцией (с контролем выхода на мех.примесей в смеси в обратной ёмкости) и продолжить промывку.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, 25,
                                                                                                     'ВНИМАНИЕ: в процессе всего периода проведения работ на скважине при отсутствии проходки и получении жёсткой посадки с разгрузкой более 500кг сверх собственного веса на данной глубине, по согласованию с Заказчиком произвести ОБСЛЕДОВАНИЕ ТЕКУЩЕГО ЗАБОЯ спуском торцевой печати на ГНКТ (Dпечати -согласовать с Заказчиком). Получить отпечаток разгрузкой на ГНКТ в 1000кг. Поднять печать из скважины. Дальнейшие работы по результатам обследования печати.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 26,
             'При отсутствии проходки и получения жесткой посадки, дальнейшие работы по согласованию с Заказчиком.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ представитель Заказчика'], [None, 27,
                                                                                                      'При достижении гл.1216,05м произвести промывку в следующем порядке:\n- прокачать гелевую пачку в объеме 2-3м3;\n- промыть скважину в течении 120 минут до выхода чистой, без посторонних примесей, промывочной жидкости (тех.вода 1,02г/см3). Составить акт.',
                                                                                                      None, None, None,
                                                                                                      None, None, None,
                                                                                                      None, None,
                                                                                                      'Мастер ГНКТ'],
            [None, 28,
             'Поднять КНК-1 на ГНКТ из скважины, закрыв скважину и записав число оборотов задвижки – зафиксировать дату и время. Демонтировать превентор, лубрикатор, КНК-1.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ представитель Заказчика'],
            [None, 'Спуск фрезеровочной КНК-2. Фрезерование муфт ГРП (фрак-портов)', None, None, None, None, None, None,
             None, None, None, None], [None, 29,
                                       'Собрать фрезеровочную Компоновку Низа Колонны-2, далее КНК-2: наружный коннектор Ø 54мм + обратный клапан створчатого типа 54мм + гидравлический разъединитель 57мм + ВЗД Ø 54-55мм + торцевой фрез Ø 68мм. Постоянно после сборки компоновки, проверять работоспособность ВЗД перед спуском в скважину на устье. Произвести замеры составных частей КНК с записью в журнале. Произвести монтаж лубрикатора и инжектора на устье скважины. Произвести необходимые опрессовки.',
                                       None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 30,
                                                                                                        'Открыв скважину и записав число оборотов задвижки – зафиксировать дату и время. Спустить КНК-2 в скважину с периодическими прокачками рабочей жидкостью (тех.вода 1,02г/см3)  с проверкой веса на подъём через каждые 300м спуска до глубины 1107м. Убедиться в наличии свободного прохода по лифту НКТ.',
                                                                                                        None, None,
                                                                                                        None, None,
                                                                                                        None, None,
                                                                                                        None, None,
                                                                                                        'Мастер ГНКТ'],
            [None, 31,
             'При получении посадки в НКТ и отсутствии прохода КНК-2 до гл.1107м, приподнять КНК-2 на 20м выше глубины посадки. Вывести НКА на рабочий режим в соответствии с рабочими параметрами ВЗД. Произвести проработку (проходного сечения НКТ) места посадки до получения свободного прохода в НКТ с составлением АКТа.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 32,
                                                                              'При свободном и беспрепятственном прохождении КНК-2 на г/трубе в НКТ до гл.1107м, продолжить доспуск КНК-2 с минимальной подачей  ВЗД до "Муфты ГРП №5" до получения посадки на гл.1216,05м. Установить метку на г/трубе.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, 33,
                                                                                                     'После соприкосновения с "Муфтой ГРП №5" приподнять КНК-2 на 10м выше. Проверить вес ГНКТ и давление циркуляции - эти значения будут ориентиром во время работы в случае заклинивания ВЗД и закупорки насадки. Вывести НКА на рабочий режим в соответствии с рабочими параметрами ВЗД.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 34,
             'Внимание: рабочее давление на устье в процессе разбуривания не должно превышать 100атм. Если циркуляционное давление выше 250атм, произвести закачку понизителя трения в концентрации 3-5л/1м3.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 35,
                                                                              'Допустить КНК-2 с циркуляцией, и с гл.1216,05м произвести фрезерование посадочного седла "МГРП №5" до гл.1216,95м до снижения рабочего давления и получения провала. Следить за устьевым давлением и постоянно контролировать выходящую из скважины жидкость на наличие мех.примесей.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, 36,
                                                                                                     'ВНИМАНИЕ: при слабой циркуляции или аномальном поглощении (более 5м3/ч) промывочной жидкости (тех.вода 1,02г/см3)  в процессе фрезерования, уведомить Заказчика, приподнять КНК-2 до гл.1081м восстановить стабильную циркуляцию и допустить КНК-2 до МГРП продолжить работы по фрезерованию.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 37,
             'После окончания фрезерования "МГРП №5" (1216,05-1216,95м) и получения прохода КНК-2 ниже глубины 1216,95м и возвращение веса к нормальным значениям (снижения рабочего давления и получения прохода ГНКТ), при необходимости прокачать на циркуляцию по г/трубе вязкую пачку в объеме 1м3. Проработать интервал "МГРП №5" три раза с выходом 5 метров ниже и выше. Минимизировать нахождение фрезы за интервалом разбуривания.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 38,
                                                                              'После окончания проработки интервала "МГРП №5", произвести допуск КНК-2 на г/трубе с циркуляцией до следующей "Муфты ГРП №4" (на гл.1265,13м); уведомить Заказчика, составить АКТ на посадку. Произвести работы по фрезерованию "МГРП №4-№2" до согласно вышеописанной технологии (п.31-37).',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, 39,
                                                                                                     'Внимание: при отсутствии проходки вследствии предполагаемого износа фреза, произвести смену вооружения: поднять фрез.КНК, заменить фрез, спустить фрез.КНК, продолжить работы по фрезерованию седел муфт ГРП.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 40,
             'Внимание: при отсутствии свободного и беспрепятственного прохода КНК-2 до следующей "Муфты ГРП №4 (№3.....№2)" по согласованию с Заказчиком, произвести  промежутучную промывку на промывочной КНК-1 до "Муфты ГРП №4 (№3.....№2)", выполнить п.41-43',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None,
                                                                              'По согласованию с Заказчиком, проведение процедуры промежуточной промывки:\n СПО промывочной КНК-1, промывка до МГРП - выполнение п.41-43',
                                                                              None, None, None, None, None, None, None,
                                                                              None, None, None], [None, 41,
                                                                                                  'Поднять КНК-2 на г/трубе из скважины. Закрыть коренную задвижку. Демонтировать инжектор, лубрикатор, КНК-2 (ВЗД с т/ф). Собрать КНК-1 (насадка промывочная Ø38.1мм + сдвоенный обратный клапан). Произвести монтаж лубрикатора и инжектора на устье скважины.Произвести необходимые опрессовки. Открыть скважину. Спустить КНК-1 в скважину с периодическими прокачками рабочей жидкостью (тех.вода 1,02г/см3) с проверкой веса на подъём через каждые 500м спуска до гл.1081м. Вывести НКА на рабочий режим промывки и получить стабильную круговую циркуляцию промывочной жидкости (тех.вода 1,02г/см3) произвести запуск азотного комплекса, вывести его на рабочий режим.Дождаться выхода пузыря азота. Получить стабильную круговуюциркуляцию азотированной смеси. Доспустить КНК-1 с циркуляцией на азотированной смеси до глубины непрохода КНК-2 и произвести промывку скважины до "Муфты ГРП №4 (№3.....№2)" до получения жесткой посадки.',
                                                                                                  None, None, None,
                                                                                                  None, None, None,
                                                                                                  None, None,
                                                                                                  'Мастер ГНКТ'],
            [None, 42,
             'При достижении "Муфты ГРП №4 (№3.....№2)" произвести промывку:\n- прокачать на циркуляцию по г/трубе вязкую пачку в V=2-3м3;\n- произвести промывку в течении не менее 2 часов, до чистой, без посторонних мех. примесей промывочной жидкости (тех.вода 1,02г/см3).\nСоставить акт на нормализацию в присутствии представителя Заказчика.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ представитель заказчика'], [None, 43,
                                                                                                      'Поднять КНК-1 на ГНКТ из скважины. Закрыть коренную задвижку. Сменить промывочную КНК-1 на фрезировочную КНК-2. Продолжить работы по фрезерованию МГРП.',
                                                                                                      None, None, None,
                                                                                                      None, None, None,
                                                                                                      None, None,
                                                                                                      'Мастер ГНКТ'],
            [None, 'Подъем фрезеровочной КНК-2', None, None, None, None, None, None, None, None, None, None], [None,
                                                                                                               'ВНИМАНИЕ БУРИЛЬЩИК! П О С Т О Я Н Н О !!! При подъеме ВЗД после фрезерования седел и шаров МГРП, во избежание заклинивания и получения прихвата ГНКТ (от возможного попадания остатков частиц шара или седла после разбуривания ) остановить г/трубу не доходя 50м до воронки и прокачать малый затруб тех.жидкостью (тех.вода 1,02г/см3) в объеме не менее 2х объемов НКТ (9,6м3).',
                                                                                                               None,
                                                                                                               None,
                                                                                                               None,
                                                                                                               None,
                                                                                                               None,
                                                                                                               None,
                                                                                                               None,
                                                                                                               None,
                                                                                                               None,
                                                                                                               None],
            [None, 44,
             'После окончания проработки "МГРП №2 от забоя" поднять КНК-2 до гл.1081м.\nПроизвести тех.отстой в течении 2ух часов для замера Ризб на тех.воде. Пересчитать забойное давление и необходимый удельный вес жидкости глушения. По доп.согласованию с Заказчиком, произвести СПО пром.КНК-1 с целью глушения скважины -  выполнение п.47-57.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 45,
                                                                              'После тех.отстоя произвести подъем КНК-2 на г/трубе из скважины соблюдая скорости безопасного СПО. Закрыть коренную задвижку.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, 46,
                                                                                                     'Демонтировать превентор, лубрикатор, КНК-2 (ВЗД с т/ф). Обрезать 1 метр ГНКТ после СПО фрезеровочной КНК.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 'Выполнение п.47-57 по доп. согласованию с Заказчиком.', None, None, None, None, None, None, None,
             None, None, None],
            [None, 'Спуск промывочной КНК-1', None, None, None, None, None, None, None, None, None, None], [None, 47,
                                                                                                            'Собрать промывочную КНК-1: коннектор + сдвоенный обратный клапан + насадка промывочная Ø 38,1мм. Произвести монтаж лубрикатора и инжектора на устье скважины. Произвести необходимые опрессовки.',
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            None, None,
                                                                                                            'Мастер ГНКТ'],
            [None, 48,
             'Открыв скважину и записав число оборотов задвижки – зафиксировать дату и время. Спустить КНК-1 в скважину до гл.1081м с ПЕРИОДИЧЕСКОЙ прокачкой рабочей жидкостью (тех.вода 1,02г/см3) и проверкой веса на подъём. Убедится в наличии свободного прохода КНК-1 по НКТ.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 49,
                                                                              'Произвести запуск и вывести Азотный комплекс и НКА на рабочий режим. Получить стабильную круговую циркуляцию азотированной смеси, промывка в течении 60мин с контролем на мех.примеси в обратной ёмкости.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, None,
                                                                                                     'Расчетные параметры циркуляции: по жидкости (тех.вода 1,02г/см3) 120л/мин; 10м3/мин по азоту.\nВ процессе промывки скважины, параметры азотированной промывочной смеси могут изменяться (от 80 до 200л/мин по жидкости и от 8 до 20м3/мин по азоту) в зависимости от качества выноса посторонних частиц с забоя. данный процесс находится под постоянным контролем у ст.мастера ГНКТ.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 50,
             'Произвести допуск КНК-1 с промывкой на азотированной смеси до текущего забоя на гл.1459м (при отсутствии проходки согласовать достигнутый забой с Заказчиком)',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 51,
                                                                              'При необходимости, при промывке производить сопровождение вымытой пачки со скоростью 2-3м/мин до глубины 1081м. Промывку производить до выхода чистой тех. жидкости (тех.вода 1,02г/см3) и только после этого продолжать промывку.',
                                                                              None, None, None, None, None, None, None,
                                                                              None, 'Мастер ГНКТ'], [None, 52,
                                                                                                     'При достижении глубины 1459м (или согласованного забоя) произвести промывку в следующем порядке:\n- прокачать гелевую пачку в объеме 2-3м3;\n- промыть скважину в течении 2 часов до выхода чистой, без посторонних примесей, промывочной жидкости (тех.вода 1,02г/см3).Составить Акт на промывку в присутствии представителя Заказчика.',
                                                                                                     None, None, None,
                                                                                                     None, None, None,
                                                                                                     None, None,
                                                                                                     'Мастер ГНКТ'],
            [None, 'По согласованию с Заказчиком, подтверждение нормализованного забоя', None, None, None, None, None,
             None, None, None, None, None], [None, 53,
                                             'Приподнять КНК-1 на ГНКТ не прекращая циркуляции до гл.1081м. Убедиться в отсутствии мех. примесей в промывочной жидкости (тех.вода 1,02г/см3) , остановить подачу жидкости НКА и ПАУ.',
                                             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 54, 'Произвести тех.отстой скважины для оседания твёрдых частиц в течении 2х часов.', None, None,
             None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 55,
                                                                  'После технологического отстоя допустить КНК-1 на г/трубе в скважину «без циркуляции» до гл.1459м, забой должен соответствовать ранее нормализованному. Составить АКТ с представителем Заказчика. При отсутствии ранее нормализованного забоя по согл. с Заказчиком, провести работы по нормализации забоя.',
                                                                  None, None, None, None, None, None, None, None,
                                                                  'Мастер ГНКТ представитель Заказчика'],
            [None, 'Подъем промывочной КНК-1', None, None, None, None, None, None, None, None, None, None], [None, 56,
                                                                                                             'Произвести подъем с замещением скважинной жидкости на раствор глушения, удельного веса по согласованию с Заказчиком, рассчитанного по замеру Ризб после 2-х часов отстоя и удел.веса рабочей жидкости в скважин, но не менее удельного веса расчитанного для пластового давления указанного в настоящем плане работ 1,23г/см3 (при Рпл=95атм).  До завоза раствора, скважину разряжать. Перед замещением КНК установить в интервале нижнего фрак-порта.\nПрокачать на циркуляцию жидкость глушения в объеме не менее 7,4м3 (трубного пространства)  с одновременным подъемом ГНКТ (с протяжкой ГНКТ перевести хвостовик). В процессе перевода соблюдать равенство объемов закаченной и отобранной из скважины жидкости, т.е. не допускать режима фонтанирования (поглощения).',
                                                                                                             None, None,
                                                                                                             None, None,
                                                                                                             None, None,
                                                                                                             None, None,
                                                                                                             'Мастер ГНКТ представитель Заказчика'],
            [None, 57,
             'Извлечь КНК-1 на ГНКТ из скважины. Закрыть скважину записав и сверив число оборотов задвижки – зафиксировать дату и время.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ представитель Заказчика'],
            [None, 'ДЕМОНТАЖ И ОСВОБОЖДЕНИЕ ТЕРРИТОРИИ', None, None, None, None, None, None, None, None, None, None],
            [None, 58, 'После закрытия задвижки - отдуть г/трубу азотом.', None, None, None, None, None, None, None,
             None, 'Мастер ГНКТ'], [None, 59,
                                    'Произвести демонтаж превентора и инжектора, установки ГНКТ. Очистить желобные ёмкости от проппанта в мешки – приготовить к вывозу. Составить Акт на количество вымытого проппанта. Произвести демонтаж рабочих линий, рабочей площадки.\nВнимание: произвести вывоз отработанной технологической жидкости и мешки с вымытым проппантом на пункт(ы) утилизации, согласованный с Заказчиком.',
                                    None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 60, 'Сдать скважину представителю Заказчика Составить АКТ.', None, None, None, None, None, None,
             None, None, 'Мастер ГНКТ'],
            [None, 'Контроль выхода малого затруба', None, None, None, None, None, None, None, None, None, None],
            [None, 61,
             'Во время промывки - выход малого затруба постоянно должен находиться под контролем. На желобной ёмкости постоянно осуществляется наблюдение за наличием проппанта и мех. примесей на выходной линии. \nПеред началом промывки – необходимо отрегулировать штуцерный монифольд так, как это необходимо – уровень промывочной жидкости в циркуляционной ёмкости не должен уменьшаться. Уровень жидкости должен находиться под постоянным наблюдением, чтобы избежать потери жидкости в пласт. Во время промывки уровень жидкости должен немного увеличиваться или оставаться неизменным.',
             None, None, None, None, None, None, None, None, 'Мастер ГНКТ'],
            [None, 'Действия при приватах ГНКТ.', None, None, None, None, None, None, None, None, None, None],
            [None, 62,
             'ВНИМАНИЕ: При наличии посадок КНК - спуск производить с остановками для промежуточных промывок. В случае прихвата ГНКТ в скважине - проинформировсть ответственного представителя Заказчика и руководство ГНКТ ООО "ВЕТЕРАН". Дальнейшие действия производить в присутствии представителя Заказчика с составлением АКТа согласно "Плана-Схемы действий при прихватах ГНКТ" ТЕХНОЛОГИЧЕСКОЙ ИНСТРУКЦИИ ОАО «Башнефть добыча»',
             None, None, None, None, None, None, None, None,
             'Мастер ГНКТ, предст.Заказчика Мастер по сложным работам ГНКТ'],
            [None, 'Использование хим. реагентов в процессе работ', None, None, None, None, None, None, None, None,
             None, None], [None, 63,
                           'а) Во время промывки возможен резкий вынос большого объёма проппанта из пласта, что может привести к потере циркуляции и последующему прихвату ГНКТ, данную ситуацию можно проследить, при этом вес ГНКТ резко понизится, а циркуляционное давление начнёт повышаться, в данном случае необходимо приостановить спуск ГНКТ, произвести промывку с добавлением понизителя трения гидравлического давления (дозировка до 3-5л /1м3 в зависимости от применяемого вида) до стабилизации рабочего давления, после чего продолжить промывку.\nб) В случае поглащения промывочной жидкости (тех.вода 1,02г/см3) в процессе промывки, после взятия каждой пачки проппанта производить прокачку загеленной жидкости (вязких пачек) в объеме 2-4м3 с сопровождением пачек в НКТ до гл.стингера с последующей промывкой до полного выноса проппанта на желобную ёмкость.\nв) При наличии посадок КНК, спуск производить с остановками для промежуточных промывок.\nг) В случае использования мембранной азотной установки, для уменьшения коррозионного влияния кислорода на ГНКТ, приготовить промывочную жидкость с добавлением ингибитора коррозии в расчете 120 л на 25м3 жидкости (тех.вода 1,02г/см3).\nд) При выходе густого высоковязкого геля (во избежании закупорки циркуляционной системы) использовать диструктор - лимонную кислоту в жидком виде.',
                           None, None, None, None, None, None, None, None, 'Мастер ГНКТ'], [None, 64,
                                                                                            'После закрытия задвижки, приготовить и прокачать по г/трубе по циркуляции на желобную ёмкость пачку – ингибитора коррозии в объёме 40л, с целью предотвращнения коррозийных отложений в г/трубе.Предположительный расход хим.реагентов на скважину: 1) Понизитель трения Лубритал - 30л (концентрация 1л/м3); 2) Загуститель ВГ-4 - 20л (для загеливания тех.жидкости и прокачки вязких пачек концентрация 5кг/м3)',
                                                                                            None, None, None, None,
                                                                                            None, None, None, None,
                                                                                            'Мастер ГНКТ']]
        for row in gnkt_work_list:
            krs_begin_gnkt.append(row)

        # for row in range(1, len(krs_begin_gnkt) + 1):  # Добавлением работ
        #     # print(row, len(schema_well_list[row-1]), schema_well_list[row-1][15])
        #     for col in range(1, 48):
        #         cell = ws4.cell(row=row, column=col)
        #
        #         cell.value = krs_begin_gnkt[row - 1][col - 1]
        #         ws4.cell(row=row, column=col).font = Font(name='Arial', size=11, bold=False)
        #         ws4.cell(row=row, column=col).alignment = Alignment(wrap_text=True, horizontal = 'center',
        #                                                                            vertical = 'center')
        #         if cell.value != None and row > 24:
        #             cell.border = border
        return krs_begin_gnkt

    def date_dmy(self, date_str):
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        # print(date_obj)
        # print(date_str)

        if isinstance(date_obj, datetime):
            return date_obj.strftime('%d.%m.%Y')
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            print(f' даь {date_obj}')
        return date_obj.strftime('%d.%m.%Y')

    def insert_ports_data(self, ports_data):

        ports_list = [
            [None, None, None, None, None, None, 'Интервалы установки фрак-портов  (муфт ГРП)', None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None,
             None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None,
             None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None,
             None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None,
             None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],
            [None, 'Цель работ', None, None, None, None, None, None,
             f'СПО промывочной КНК-1 с промывкой до МГРП №5. СПО фрезеровочной КНК-2: фрезерование МГРП №5-№2.'
             f' Тех.отстой , замер Ризб. По доп.согласованию с Заказчиком, СПО промывочной КНК-1 до '
             f'текущего забоя (МГРП №1).',
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None]
        ]
        port_len = len(ports_data)
        col_port = int(36 / port_len)
        for index_row, row in enumerate(ports_list):

            # dict_ports[f'Муфта №{index + 1}'] = {'кровля': port[0], 'подошва': port[1], 'шар': ball, 'седло': saddle,
            #                                      'тип': type_saddles}
            col = 45
            n = 3
            m = 0
            merge_port = {}
            for index, port in enumerate(ports_data):
                if index_row == 1:
                    ports_list[index_row][col - n - 2] = port


                elif index_row == 2:
                    ports_list[index_row][col - n - 2] = ports_data[port]['тип']
                elif index_row == 3:
                    ports_list[index_row][col - n - 2] = f'{ports_data[port]["подошва"]}м'
                    ports_list[index_row][col - n - 1] = 'Ø седла'
                    ports_list[index_row][col - n] = 'Ø шара'
                elif index_row == 4:
                    ports_list[index_row][col - n - 2] = f'{ports_data[port]["кровля"]}-'
                    ports_list[index_row][col - n - 1] = f'{ports_data[port]["седло"]}'
                    ports_list[index_row][col - n] = f'{ports_data[port]["шар"]}мм'
                # print(col - col_port - n)
                merge_port[182 + m] = (col - n - 1, 25, col - n + 1, 25)
                merge_port[182 + m + 1] = (col - n - 1, 26, col - n + 1, 26)
                n += col_port
                m += 2

        print(f'merge {merge_port}')
        return ports_list, merge_port

    def work_with_port(self, plast_work: str, dict_perforation: dict):
        ports_tuple = sorted(list(dict_perforation[plast_work]['интервал']), key=lambda x: x[0], reverse=True)
        dict_ports = {}

        manufacturer_list = ['НТЦ ЗЭРС', 'Зенит', 'Барбус']

        manufacturer, ok = QInputDialog.getItem(None, 'Выбор подрядчика по хвостовику',
                                                'Введите подрядчика по хвостовику',
                                                manufacturer_list, 0, False)
        if manufacturer == 'НТЦ ЗЭРС':
            type_column_list = ["ФПЗН.102", "ФПЗН1.114"]
            type_column, ok = QInputDialog.getItem(None, 'Выбор типа колонны', 'Введите тип колонны',
                                                   type_column_list, 1, False)


        elif manufacturer == 'Зенит':
            type_column = ["ФПЗН1.114"]
            type_saddles_list = ['1.952"', '2,022"', '2,092"', '2,162"', '114/58А', '2,322"',
                                 '2,402"', '2,487"', '2,577"', '2,667"', '2,757"', '2,547"']


        elif manufacturer == 'Барбус':
            type_column = ["гидравлич"]

        for index, port in enumerate(ports_tuple):
            if type_column == "ФПЗН.102" and manufacturer == 'НТЦ ЗЭРС':
                type_saddles_list = ['102/70', '102/67', '102/64', '102/61', '102/58', '102/55', '102/52', '102/49',
                                     '102/47', '102/45']

            elif type_column == "ФПЗН1.114" and manufacturer == 'НТЦ ЗЭРС':
                type_saddles_list = ['114/70А', '114/67А', '114/64А', '114/61А', '114/58А', '114/55А', '114/52А',
                                     '114/49А', '114/47А', '114/45А']
            elif type_column == "ФПЗН1.114" and manufacturer == 'Зенит':
                type_saddles_list = ['1.952"', '2,022"', '2,092"', '2,162"', '114/58А', '2,322"',
                                     '2,402"', '2,487"', '2,577"', '2,667"', '2,757"', '2,547"']
            elif type_column == "ФПЗН1.114" and manufacturer == 'Барбус':
                type_saddles_list = ['51,36t20', '54,00t20', '56,65t20', '59,80t20',
                                     '62,95t20', '66,10t20']
            type_saddles, ok = QInputDialog.getItem(None, 'Выбор типа порта ',
                                                    f'Введите тип порта {manufacturer} №{index + 1}',
                                                    type_saddles_list, 0, False)
            # print(dict_saddles[manufacturer])
            ball = dict_saddles[manufacturer][type_column][type_saddles].ball
            saddle = dict_saddles[manufacturer][type_column][type_saddles].saddle
            dict_ports[f'Муфта №{index + 1}'] = {'кровля': port[0], 'подошва': port[1], 'шар': ball, 'седло': saddle,
                                                 'тип': type_saddles}

        return dict_ports


if __name__ == '__main__':
    app = QApplication([])
    window = Work_with_gnkt()
    window.show()
    app.exec_()
