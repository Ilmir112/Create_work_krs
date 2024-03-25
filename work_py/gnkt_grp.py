from datetime import datetime

from PyQt5.QtWidgets import QInputDialog, QMainWindow, QTabWidget, QWidget, QTableWidget, QApplication
# from PyQt5.uic.properties import QtWidgets
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from PyQt5 import QtCore, QtWidgets

import well_data
from perforation_correct import PerforationCorrect

import block_name
import main
import plan
from block_name import razdel_1
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from open_pz import CreatePZ

from gnkt_data.gnkt_data import dict_saddles
from work_py.data_informations import dict_data_cdng, calc_pntzh


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

       
        super(QMainWindow, self).__init__()
        self.table_widget = table_widget
        self.table_title = table_title
        self.table_schema = table_schema

        self.dict_perforation = well_data.dict_perforation
        self.ws = ws
        self.work_plan = 'gnkt_after_grp'
        self.perforation_correct_window2 = None

        self.ws_title = Work_with_gnkt.wb_gnkt_frez.create_sheet(title="Титульник")
        self.ws_schema = Work_with_gnkt.wb_gnkt_frez.create_sheet(title="Схема")
        self.ws_work = Work_with_gnkt.wb_gnkt_frez.create_sheet(title="Ход работ")

        head = plan.head_ind(well_data.cat_well_min, well_data.cat_well_max + 1)
        # print(f'ff  {head}')p
        # print(self.ws)
        plan.copy_true_ws(self.ws, self.ws_title, head)

        create_title = self.create_title_list(self.ws_title)
        schema_well = self.schema_well(self.ws_schema)

        main.MyWindow.copy_pz(self, self.ws_title, table_title, self.work_plan, 13, 1)
        main.MyWindow.copy_pz(self, self.ws_schema, table_schema, self.work_plan, 47, 2)
        main.MyWindow.copy_pz(self, self.ws_work, table_widget, self.work_plan, 12, 3)
        work_well = self.work_gnkt_frez(self.ports_data, self.plast_work)
        main.MyWindow.populate_row(self, 0, work_well, table_widget)

        CreatePZ.addItog(self, self.ws_work, self.table_widget.rowCount() + 1, self.work_plan)
        # Work_with_gnkt.wb_gnkt_frez.save(f"{well_data.well_number} {well_data.well_area} {well_data.cat_P_1}
        # категории.xlsx")
        # print('файл сохранен')

    def count_row_height(self, ws2, work_list, sheet_name):
       
        from openpyxl.utils.cell import range_boundaries, get_column_letter

        colWidth = [2.85546875, 14.42578125, 16.140625, 22.85546875, 17.140625, 14.42578125, 13.0, 13.0, 17.0,
                     14.42578125, 13.0, 21, 12.140625, None]

        text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 110: (301, 400), 120: (401, 500),
                           130: (501, 600), 150: (601, 700), 170: (701, 800), 190: (801, 900), 230: (901, 1500)}

        boundaries_dict = {}

        for ind, _range in enumerate(ws2.merged_cells.ranges):
            boundaries_dict[ind] = range_boundaries(str(_range))

        for key, value in boundaries_dict.items():
            ws2.unmerge_cells(start_column=value[0], start_row=value[1],
                              end_column=value[2], end_row=value[3])
        ins_ind = 1


        for i in range(1, len(work_list) + 1):  # Добавлением работ
            if str(work_list[i-1][1]).isdigit() and i>39: # Нумерация
                work_list[i-1][1] = str(ins_ind)
                ins_ind += 1
            for j in range(1, 13):
                cell = ws2.cell(row=i, column=j)

                if cell and str(cell) != str(work_list[i - 1][j - 1]):
                    if str(work_list[i - 1][j - 1]).replace('.', '').isdigit() and \
                            str(work_list[i - 1][j - 1]).count('.') != 2:
                        cell.value = str(work_list[i - 1][j - 1]).replace('.', ',')
                        # print(f'цифры {cell.value}')
                    else:
                        cell.value = work_list[i - 1][j - 1]





        # print(merged_cells_dict)
        if sheet_name != 'Ход работ':
            for key, value in boundaries_dict.items():
                # print(value)
                ws2.merge_cells(start_column=value[0], start_row=value[1],
                                end_column=value[2], end_row=value[3])




        elif sheet_name == 'Ход работ':
            for i, row_data in enumerate(work_list):
                # print(f'gghhg {work_list[i][2]}')
                for column, data in enumerate(row_data):
                    if column == 2:
                        if not data is None:
                            text = data
                            for key, value in text_width_dict.items():
                                if value[0] <= len(text) <= value[1]:
                                    ws2.row_dimensions[i + 1].height = int(key)
                    elif column == 1:
                        if not data is None:
                            text = data
                            # print(text)
                            for key, value in text_width_dict.items():
                                if value[0] <= len(text) <= value[1]:
                                    ws2.row_dimensions[i + 1].height = int(key)
                    if column != 0:
                        ws2.cell(row=i + 1, column=column + 1).border = well_data.thin_border
                    if column == 1 or column == 11:
                        ws2.cell(row=i + 1, column=column + 1).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                                 vertical='center')
                        ws2.cell(row=i + 1, column=column + 1).font = Font(name='Arial', size=13, bold=False)
                    else:
                        ws2.cell(row=i + 1, column=column + 1).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                                     vertical='center')
                        ws2.cell(row=i + 1, column=column + 1).font = Font(name='Arial', size=13, bold=False)
                        if 'примечание' in str(ws2.cell(row=i + 1, column=column + 1).value).lower() or \
                            'внимание' in str(ws2.cell(row=i + 1, column=column + 1).value).lower() or \
                            'мероприятия' in str(ws2.cell(row=i + 1, column=column + 1).value).lower() or \
                            'порядок работ' in str(ws2.cell(row=i + 1, column=column + 1).value).lower() or \
                            'По доп.согласованию с Заказчиком' in str(ws2.cell(row=i + 1, column=column + 1).value).lower():
                            # print('есть жирный')
                            ws2.cell(row=i + 1, column=column + 1).font = Font(name='Arial', size=13, bold=True)

                if len(work_list[i][1]) > 5:
                    ws2.merge_cells(start_column=2, start_row= i + 1, end_column= 12, end_row=i + 1)
                    ws2.cell(row=i + 1, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
                    ws2.cell(row=i + 1, column=2).fill = PatternFill(start_color='C5D9F1', end_color='C5D9F1',
                                                                      fill_type='solid')
                    ws2.cell(row=i + 1, column=2).font = Font(name='Arial', size=13, bold=True)

                else:
                    ws2.merge_cells(start_column=3, start_row=i + 1, end_column=11, end_row=i + 1)
                    ws2.cell(row=i + 1, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                            vertical='center')




            for col in range(13):
                ws2.column_dimensions[get_column_letter(col + 1)].width = colWidth[col]

            ws2.print_area = f'B1:L{self.table_widget.rowCount() + 45}'
            ws2.page_setup.fitToPage = True
            ws2.page_setup.fitToHeight = False
            ws2.page_setup.fitToWidth = True
            ws2.print_options.horizontalCentered = True
            # зададим размер листа
            ws2.page_setup.paperSize = ws2.PAPERSIZE_A4
            # содержимое по ширине страницы
            ws2.sheet_properties.pageSetUpPr.fitToPage = True
            ws2.page_setup.fitToHeight = False

        for row_ind, row in enumerate(ws2.iter_rows(values_only=True)):
            for col, value in enumerate(row):
                if 'А.Р. Хасаншин' in str(value):
                    coordinate = f'{get_column_letter(col + 1)}{row_ind - 1}'
                    self.insert_image(ws2, 'imageFiles/Хасаншин.png', coordinate)
                elif 'Д.Д. Шамигулов' in str(value):
                    coordinate = f'{get_column_letter(col + 1)}{row_ind - 2}'
                    self.insert_image(ws2, 'imageFiles/Шамигулов.png', coordinate)
                elif 'Зуфаров' in str(value):
                    coordinate = f'{get_column_letter(col - 2)}{row_ind}'
                    self.insert_image(ws2, 'imageFiles/Зуфаров.png', coordinate)
                elif 'М.К.Алиев' in str(value):
                    coordinate = f'{get_column_letter(col - 1)}{row_ind - 2}'
                    self.insert_image(ws2, 'imageFiles/Алиев махир.png', coordinate)
                elif 'З.К. Алиев' in str(value):
                    coordinate = f'{get_column_letter(col - 1)}{row_ind - 2}'
                    self.insert_image(ws2, 'imageFiles/Алиев Заур.png', coordinate)
                    break
        print(f'{sheet_name} - вставлена')

    def save_to_gnkt(self):
       

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
            Work_with_gnkt.count_row_height(self, worksheet, work_list, sheet_name)

        ws6 = Work_with_gnkt.wb_gnkt_frez.create_sheet(title="СХЕМЫ КНК_44,45")
        main.MyWindow.insert_image(self, ws6, 'imageFiles/schema_well/СХЕМЫ КНК_44,45.png', 'A1', 550, 900)
        ws7 = Work_with_gnkt.wb_gnkt_frez.create_sheet(title="СХЕМЫ КНК_38,1")
        main.MyWindow.insert_image(self, ws7, 'imageFiles/schema_well/СХЕМЫ КНК_38,1.png', 'A1', 550, 900)

        # path = 'workiii'
        path = 'D:\Documents\Desktop\ГТМ'
        filenames = f"{well_data.well_number} {well_data.well_area} кат {well_data.cat_P_1} {self.work_plan}.xlsx"
        full_path = path + '/' + filenames
        # print(f'10 - {ws2.max_row}')
        # print(wb2.path)
        # print(f' кате {well_data.cat_P_1}')

        if well_data.bvo == True:
            ws5 = Work_with_gnkt.wb_gnkt_frez.create_sheet('Sheet1')
            ws5.title = "Схемы ПВО"
            ws5 = Work_with_gnkt.wb_gnkt_frez["Схемы ПВО"]
            Work_with_gnkt.wb_gnkt_frez.move_sheet(ws5, offset=-1)
            # schema_list = self.check_pvo_schema(ws5, ins_ind + 2)

        if Work_with_gnkt.wb_gnkt_frez:
            Work_with_gnkt.wb_gnkt_frez.remove(Work_with_gnkt.wb_gnkt_frez['Sheet'])

            main.MyWindow.saveFileDialog(self, Work_with_gnkt.wb_gnkt_frez, full_path)

            Work_with_gnkt.wb_gnkt_frez.close()
            print(f"Table data saved to Excel {full_path} {well_data.number_dp}")
        if self.wb:
            self.wb.close()

    def create_title_list(self, ws2):
       

        well_data.region = block_name.region(well_data.cdng)
        self.region = well_data.region

        title_list = [
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, 'ООО «Башнефть-Добыча»', None, None, None, None, None, None, None, None, None, None],
            [None, None, None, f'{well_data.cdng}', None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, 'ПЛАН РАБОТ НА СКВАЖИНЕ С ПОМОЩЬЮ УСТАНОВКИ С ГИБКОЙ ТРУБОЙ', None, None, None,
             None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, '№ скважины:', f'{well_data.well_number}', 'куст:', None, 'Месторождение:', None, None,
             well_data.well_oilfield, None, None],
            [None, None, 'инв. №:', well_data.inv_number, None, None, None, None, 'Площадь: ', well_data.well_area, None,
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
                                    end_column=11)
                    ws2.merge_cells(start_row=row -4 + index_insert, start_column=2, end_row=row -4 + index_insert,
                                    end_column=4)
                    ws2.cell(row=row + index_insert, column=col).font = Font(name='Arial', size=14, bold=True)
                    ws2.cell(row=row + index_insert, column=col).alignment = Alignment(wrap_text=False,
                                                                                       horizontal='center',
                                                                                       vertical='center')
                if 'СОГЛАСОВАНО:' in str(title_list[row - 1][col - 1]):
                    a = row + index_insert

            # for row in range(len(title_list)):  # Добавлением работ
            if a:
                if a > row:
                    # print(f'сссооссоссо {row + index_insert}')
                    ws2.merge_cells(start_row=row + index_insert, start_column=2, end_row=row + index_insert,
                                    end_column=6)
                    ws2.merge_cells(start_row=row + index_insert, start_column=8, end_row=row + index_insert,
                                    end_column=11)

        ws2.print_area = f'B1:K{44}'
        ws2.page_setup.fitToPage = True
        ws2.page_setup.fitToHeight = False
        ws2.page_setup.fitToWidth = True
        ws2.print_options.horizontalCentered = True
        # зададим размер листа
        ws2.page_setup.paperSize = ws2.PAPERSIZE_A4

    def schema_well(self, ws3):
        from krs import volume_vn_nkt, well_volume

        boundaries_dict = {}

        rowHeights1 = []

        colWidth = []

        self.plast_work = well_data.plast_all[0]
        plast_work = self.plast_work
        # print(self.plast_work, list(well_data.dict_perforation[plast_work]))
        self.pressuar = list(well_data.dict_perforation[plast_work]["давление"])[0]

        zamer = list(well_data.dict_perforation[plast_work]['замер'])[0]
        vertikal = min(map(float, list(well_data.dict_perforation[plast_work]["вертикаль"])))
        self.fluid = self.calc_fluid()
        zhgs = f'{self.fluid}г/см3'
        koef_anomal = round(float(self.pressuar) * 101325 / (float(vertikal) * 9.81 * 1000), 1)
        nkt = int(list(well_data.dict_nkt.keys())[0])
        if nkt == 73:
            nkt_widht = 5.5
        elif nkt == 89:
            nkt_widht = 6.5
        elif nkt == 60:
            nkt_widht = 5
        lenght_nkt = sum(list(map(int, well_data.dict_nkt.values())))



        arm_grp, ok = QInputDialog.getInt(None, 'Арматура ГРП',
                                          'ВВедите номер Арматуры ГРП', 16, 0, 500)

        gnkt_lenght, _ = QInputDialog.getInt(None, 'Длина ГНКТ',
                                             'ВВедите длину ГНКТ', 3500, 500, 10000)
        volume_vn_gnkt = round(30.2 ** 2 * 3.14 / (4 * 1000), 2)
        volume_gnkt = round(gnkt_lenght * volume_vn_gnkt / 1000, 1)

        well_volume_ek = well_volume(self, well_data.head_column_additional._value)
        well_volume_dp = well_volume(self, well_data.current_bottom) - well_volume_ek

        volume_pm_ek = round(3.14 * (well_data.column_diametr._value - 2 * well_data.column_wall_thickness._value) ** 2 / 4 / 1000, 2)
        volume_pm_dp = round(3.14 * (well_data.column_additional_diametr._value - 2 *
                                     well_data.column_additional_wall_thickness._value) ** 2 / 4 / 1000, 2)
        schema_well_list = [
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None],
            [None, 'СХЕМА СКВАЖИНЫ', None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Данные о размерности труб',
             None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Тип ПВО', None, None, '4-х секционный превентор БП 80-70.00.00.000 (700атм) К2', None, None, None, None,
             None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Тип ФА', None, None, 'АУШГН-146 / АУГРП 146*14', None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Тип КГ', None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, well_data.column_diametr._value, None, None,
             'Стол ротора', None, well_data.stol_rotora, 'Øнаруж мм', 'толщ, мм', 'Øвнут, мм', 'Интервал спуска, м',
             None, 'ВПЦ.\nДлина', 'Объем', None],
            [None, None, None, None, None, None, None, None, None, well_data.shoe_column._value, None, None,
             'Ø канавки', None, 211, None, None, None, None, None, None, 'л/п.м.', 'м3'],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Шахтное направление', None, None, f'-', None, None, f'-', f'-', f'-', None, None],
            [None, None, None, None, None, None, None, None, None,
             'НКТ 89мм', None, None, 'Направление', None, None,
             well_data.column_direction_diametr._value, well_data.column_direction_wall_thickness._value,
             round(well_data.column_direction_diametr._value - 2 *well_data.column_direction_wall_thickness._value,1),
             0, well_data.column_direction_lenght, well_data.level_cement_direction._value, None, None],
            [None, None, None, None, None, None, None, None, None, 2448, None, None,
             'Кондуктор', None, None,
             well_data.column_conductor_diametr._value, well_data.column_conductor_wall_thickness._value,
             round(well_data.column_conductor_diametr._value - 2 * well_data.column_conductor_wall_thickness._value, 1),
             0, well_data.column_conductor_lenght._value, well_data.level_cement_conductor._value, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Экспл. колонна', None, None,
             well_data.column_diametr._value, well_data.column_wall_thickness._value,
             round(well_data.column_diametr._value - 2* well_data.column_wall_thickness._value, 1),
             0, well_data.shoe_column,well_data.level_cement_direction, volume_pm_ek, well_volume_ek],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'доп.колонна', None, None,
             well_data.column_additional_diametr._value, well_data.column_additional_wall_thickness._value,
             round(well_data.column_additional_diametr._value - 2* well_data.column_additional_wall_thickness._value, 1),
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'колонна НКТ', None, None, nkt, nkt_widht, nkt -2 * nkt_widht, 0, lenght_nkt, None, 4.335917984, 10.605655388864],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             f'{well_data.paker_do["do"]}', None, None, None, None, 50,
             well_data.depth_fond_paker_do["do"], well_data.depth_fond_paker_do["do"] + 2, None,  None,  None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'воронка', None, None, nkt, nkt_widht , nkt -2 * nkt_widht, 0, lenght_nkt, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'ГНКТ', None, None, 38.1, 3.68, 30.74, gnkt_lenght, None, None, volume_vn_gnkt, volume_gnkt],

            [None, None, None, None, None, None, None, None, None, None, None, None, None,
             'Данные о забое', None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Тек. забой перед ГРП', None, None, None, None, None, None, None, None, well_data.current_bottom, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Текущий забой', None, None, None, None, None, None, None, None, well_data.current_bottom, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Искусственный забой  ', None, None, None, None, None, None, None, None, well_data.bottomhole_artificial._value, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Дополнительная информация', None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Категория скважины', None, None, None, None, 2, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, 'Содержание H2S',
             None, None, None, None, 28.37, None, None, None, None, None],
            [None, None, None, None, None, None, None, 2468, None, None, None, None,
             'Газовый фактор', None, None, None, None, 52.6, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Коэффициент аномальности', None, None, None, None, 0.7534098067523365, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Плотность жидкость глушения', None, None, None, None, 1.02, None, 'в объеме', None, 30.28, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Текущий дебит скважины', None, None, None, None, 0.4, None, 0.3, None, 0.02, None],
            [None, None, None, None, None, None, None, 2474, None, None, None, None,
             'Ожидаемый дебит скважины', None, None, None, None, 16.7, None, 7.3, None, 0.51, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Максимальный угол наклона', None, None, None, None, 1.75, None, 'на глубине', None, 1480, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Макс. набор кривизны более', None, None, None, None, 'вертикальная', None, 'на глубине', None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Дата начало / окончания бурения', None, None, None, None, datetime.datetime(1995, 8, 27, 0, 0),
             None, datetime.datetime(1996, 1, 21, 0, 0), None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Дата ввода в эксплуатацию', None, None, None, None, datetime.datetime(1998, 1, 6, 0, 0),
             None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Р в межколонном пространстве', None, None, None, None, 0, None, ' ', None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Первоначальное Р опр-ки ЭК', None, None, None, None, 150, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'Результат предыдущей опрес-и ЭК', None, None, None, None, 80, None,
             datetime.datetime(2018, 2, 6, 0, 0), None, 'гермет.', None],
            [None, None, None, None, None, None, None, None, 'Тек.забой', None, None, None,
             'Макс.допустимое Р опр-ки ЭК', None, None, None, None, 80, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, 2488.8, None, None, None,
             'Макс. ожидаемое Р на устье ', None, None, None, None, 70, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None,  None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],
           [None, None, None, None, None, None, None, None, None, None, None, None,
            'Данные о перфорации', None, None, None, None, None, None, None, None, None, None],
           [None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None],
           [None, None, None, None, None, None, None, None, None,
            'пакер', None, None, 'Пласт\nгоризонт', None, 'Глубина пласта по вертикали', None,
            'Интервал перфорации',
            None, None, None, 'Дата вскрытия/\nотключения', 'Р пл. атм \nДата замера', None],
           [None, None, None, None, None, None, None, None, None, 2446, None, None, None, None, None,
            None, 'от', None, 'до', None, None, None, None],
           [None, None, None, None, None, None, None, None, None, None, None, None,
            'Dпаш', None, 2467.68, None, 2468, None, 2474, None, datetime.datetime(1996, 2, 1, 0, 0),
            180, None],
           [None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, datetime.datetime(2018, 2, 3, 0, 0), None, None],
           [None, None, None, None, None, None, None, None, None, 'воронка', None, None, None,
            None, None, None, None, None, None, None, datetime.datetime(2019, 10, 5, 0, 0),
            datetime.datetime(2023, 4, 1, 0, 0), None],
           [None, None, None, None, None, None, None, None, None, 2448, None, None, None,
            None, None, None, None, None, None, None, 'июнь 2023г.', None, None]]



        # print(ports_list)
        for row in self.ports_list:
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
            if row < 23:
                ws3.cell(row=row, column=7).font = Font(name='Arial', size=11, bold=True, color='002060')
                ws3.cell(row=row, column=32).font = Font(name='Arial', size=11, bold=True, color='002060')

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

        ws3.cell(row=1, column=1).font = Font(name='Arial', size=18, bold=True)
        ws3.cell(row=3, column=14).font = Font(name='Arial', size=18, bold=True)
        ws3.cell(row=3, column=30).font = Font(name='Arial', size=18, bold=True)
        ws3.cell(row=3, column=22).font = Font(name='Arial', size=18, bold=True)
        ws3.cell(row=3, column=37).font = Font(name='Arial', size=18, bold=True)
        ws3.cell(row=24, column=7).font = Font(name='Arial', size=14, bold=True, color='002060')
        ws3.cell(row=34, column=1).font = Font(name='Arial', size=14, bold=True, color='002060')
        ws3.cell(row=34, column=9).font = Font(name='Arial', size=14, bold=True, color='002060')
        ws3.cell(row=5, column=10).font = Font(name='Arial', size=14, bold=False, color='002060', underline='single')
        ws3.cell(row=5, column=33).font = Font(name='Arial', size=14, bold=False, color='002060', underline='single')

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
      # print(Column_img)
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

    def work_gnkt_frez(self, ports_data, plast_work):
        pass

    def volume_dumping(self, ntk_true, first_muft):
        from krs import volume_pod_NKT, volume_jamming_well

        if ntk_true == True:
            volume = volume_pod_NKT(self) * 1.2
        else:
            volume = volume_jamming_well(self, first_muft) * 1.1
        return round(volume, 1)

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





    def calc_fluid(self):
       
        fluid_list = []
        try:

            fluid_p = 0.83
            for plast in well_data.plast_work:
                if float(list(well_data.dict_perforation[plast]['рабочая жидкость'])[0]) > fluid_p:
                    fluid_p = list(well_data.dict_perforation[plast]['рабочая жидкость'])[0]
            fluid_list.append(fluid_p)

            fluid_work_insert, ok = QInputDialog.getDouble(self, 'Рабочая жидкость',
                                                           'Введите расчетный удельный вес жидкости глушения в '
                                                           'конце жидкости',
                                                           max(fluid_list), 0.87, 2, 2)
        except:
            fluid_work_insert, ok = QInputDialog.getDouble(self, 'Рабочая жидкость',
                                                           'Введите удельный вес рабочей жидкости',
                                                           0, 0.87, 2, 2)
        return fluid_work_insert


if __name__ == '__main__':
    app = QApplication([])
    window = Work_with_gnkt()
    window.show()
    app.exec_()
