import datetime

from PyQt5.QtWidgets import QInputDialog
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

import block_name
import plan
from block_name import razdel_1
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

from krs import volume_vn_nkt


class Work_with_gnkt():

    def __init__(self):
        from open_pz import CreatePZ
        super(CreatePZ).__init__()
        self.create_excel_file = None

    def create_excel_file(self, ws):
        from open_pz import CreatePZ
        wb4 = Workbook()
        ws2 = wb4.get_sheet_by_name('Sheet')
        ws2.title = "Титульник"

        ws3 = wb4.create_sheet(title="Схема")


        head = plan.head_ind(CreatePZ.cat_well_min, CreatePZ.cat_well_max + 1)
        plan.copy_true_ws(ws, ws2, head)

        create_title = Work_with_gnkt.create_title_list(self, ws2)
        schema_well = Work_with_gnkt.schema_well(self, ws3)
        wb4.save(f"{CreatePZ.well_number} {CreatePZ.well_area} {CreatePZ.cat_P_1} категории.xlsx")
        print('файл сохранен')

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
            [None, None, '№ скважины:', f'{CreatePZ.well_number}', 'куст:', 11682, 'Месторождение:', None, None,
             CreatePZ.well_oilfield, None, None],
            [None, None, 'инв. №:', CreatePZ.inv_number, None, None, None, None, 'Площадь: ', CreatePZ.well_area, None,
             1],
            [None, None, None, None, None, None, None, None, None, None, None, None]]

        razdel = razdel_1(self, self.region)
        for row in razdel:  # Добавлением работ
            title_list.append(row)

        for row in [[None, 'Дата', None, None, '05.05.2023г.', None, None, None, None, None, None]]:
            title_list.insert(-1, row)
        # print(title_list)
        index_insert = 11
        ws2.cell(row=1, column=2).alignment = Alignment(wrap_text=False, horizontal='left',
                                                        vertical='center')
        ws2.column_dimensions[get_column_letter(1)].width = 15
        ws2.column_dimensions[get_column_letter(2)].width = 15
        for row in range(len(title_list)):  # Добавлением работ
            if row not in range(8, 13):
                ws2.row_dimensions[row].height = 30
            for col in range(1, 12):
                ws2.column_dimensions[get_column_letter(col)].width = 10
                cell = ws2.cell(row=row + index_insert, column=col)
                # print(f' Х {title_list[i ][col - 1]}')
                if title_list[row - 1][col - 1] != None:
                    cell.value = str(title_list[row - 1][col - 1])
                ws2.cell(row=row + index_insert, column=col).font = Font(name='Arial', size=11, bold=False)
                ws2.cell(row=row + index_insert, column=col).alignment = Alignment(wrap_text=False, horizontal='left',
                                                                                   vertical='center')
                if 'ПЛАН РАБОТ' in str(title_list[row - 1][col - 1]):
                    ws2.merge_cells(start_row=row + index_insert, start_column=2, end_row=row + index_insert,
                                    end_column=12)
                    ws2.cell(row=row + index_insert, column=col).font = Font(name='Arial', size=13, bold=False)
                    ws2.cell(row=row + index_insert, column=col).alignment = Alignment(wrap_text=False,
                                                                                       horizontal='center',
                                                                                       vertical='center')

            ws2.print_area = f'B1:L{44}'
            ws2.page_setup.fitToPage = True
            ws2.page_setup.fitToHeight = False
            ws2.page_setup.fitToWidth = True
            ws2.print_options.horizontalCentered = True
            # зададим размер листа
            ws2.page_setup.paperSize = ws2.PAPERSIZE_A4

    def schema_well(self, ws3):
        from open_pz import CreatePZ
        boundaries_dict = {0: (13, 13, 14, 14), 1: (43, 12, 45, 12), 2: (40, 16, 42, 16), 3: (7, 19, 12, 19),
                           4: (17, 21, 18, 21), 5: (19, 21, 20, 21), 6: (13, 10, 30, 10), 7: (15, 15, 16, 15),
                           8: (1, 1, 49, 2), 9: (46, 19, 48, 19), 10: (27, 15, 28, 15), 11: (29, 15, 30, 15),
                           12: (40, 11, 42, 11), 13: (33, 5, 48, 5), 14: (23, 15, 26, 15), 15: (13, 16, 14, 16),
                           16: (15, 16, 16, 16), 17: (9, 34, 48, 34), 18: (19, 19, 20, 19), 19: (27, 16, 28, 16),
                           20: (29, 19, 30, 19), 21: (13, 18, 14, 18), 22: (40, 13, 42, 13), 23: (11, 25, 13, 25),
                           24: (45, 26, 47, 26), 25: (27, 18, 28, 18), 26: (13, 17, 14, 17), 27: (15, 17, 16, 17),
                           28: (17, 17, 18, 17), 29: (32, 8, 39, 8), 30: (40, 15, 42, 15), 31: (19, 20, 20, 20),
                           32: (21, 20, 22, 20), 33: (21, 14, 22, 14), 34: (13, 19, 14, 19), 35: (26, 26, 28, 26),
                           36: (11, 13, 12, 13), 37: (43, 7, 48, 7), 38: (37, 3, 48, 3), 39: (7, 6, 12, 11), 40:
                               (27, 22, 28, 22), 41: (19, 22, 20, 22), 42: (32, 18, 39, 18), 43: (21, 22, 22, 22),
                           44: (46, 23, 48, 23), 45: (7, 18, 12, 18), 46: (18, 26, 20, 26), 47: (43, 8, 48, 8),
                           48: (13, 7, 30, 7), 49: (46, 15, 48, 15), 50: (43, 14, 45, 14), 51: (40, 18, 42, 18),
                           52: (17, 23, 18, 23), 53: (43, 10, 48, 10), 54: (29, 14, 30, 14), 55: (34, 26, 36, 26),
                           56: (40, 8, 42, 8), 57: (29, 23, 30, 23), 58: (43, 13, 45, 13), 59: (7, 20, 12, 20),
                           60: (15, 13, 16, 14), 61: (40, 17, 42, 17), 62: (17, 13, 18, 14), 63: (43, 9, 48, 9),
                           64: (13, 8, 30, 8), 65: (27, 13, 30, 13), 66: (34, 25, 36, 25), 67: (13, 21, 14, 21),
                           68: (15, 21, 16, 21), 69: (40, 10, 42, 10), 70: (17, 15, 18, 15), 71: (43, 15, 45, 15),
                           72: (32, 12, 39, 12), 73: (7, 22, 12, 22), 74: (40, 19, 42, 19), 75: (32, 21, 39, 21),
                           76: (46, 17, 48, 17), 77: (21, 18, 22, 18), 78: (46, 22, 48, 22), 79: (7, 12, 12, 12),
                           80: (40, 9, 42, 9), 81: (7, 21, 12, 21), 82: (10, 5, 30, 5), 83: (32, 7, 39, 7),
                           84: (23, 16, 26, 16), 85: (7, 23, 12, 23), 86: (13, 9, 30, 9), 87: (46, 12, 48, 12),
                           88: (21, 19, 22, 19), 89: (43, 16, 45, 16), 90: (2, 34, 8, 34), 91: (32, 22, 45, 22),
                           92: (27, 17, 28, 17), 93: (45, 25, 47, 25), 94: (22, 3, 26, 3), 95: (29, 17, 30, 17),
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
                           136: (11, 26, 13, 26), 137: (23, 21, 26, 21), 138: (18, 25, 20, 25), 139: (32, 13, 39, 13),
                           140: (40, 20, 42, 20), 141: (19, 15, 22, 15), 142: (17, 16, 18, 16), 143: (29, 16, 30, 16),
                           144: (15, 18, 16, 18), 145: (10, 37, 11, 37), 146: (17, 18, 18, 18), 147: (19, 18, 20, 18),
                           148: (29, 18, 30, 18), 149: (7, 15, 12, 15), 150: (40, 12, 42, 12), 151: (13, 6, 30, 6),
                           152: (13, 20, 14, 20), 153: (19, 16, 22, 16), 154: (30, 3, 36, 3), 155: (32, 10, 39, 10),
                           156: (40, 14, 42, 14), 157: (17, 19, 18, 19), 158: (19, 23, 26, 23), 159: (7, 24, 48, 24),
                           160: (32, 6, 39, 6), 161: (13, 22, 14, 22), 162: (27, 20, 28, 20), 163: (7, 16, 12, 16),
                           164: (29, 20, 30, 20), 165: (19, 17, 22, 17), 166: (17, 22, 18, 22), 167: (32, 20, 39, 20),
                           168: (32, 14, 39, 14), 169: (11, 14, 12, 14), 170: (23, 20, 26, 20), 171: (29, 22, 30, 22),
                           172: (46, 13, 48, 13), 173: (43, 20, 45, 20), 174: (32, 17, 39, 17), 175: (23, 22, 26, 22),
                           176: (7, 17, 12, 17), 177: (32, 19, 39, 19), 178: (27, 14, 28, 14), 179: (26, 25, 28, 25),
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

        colWidth = [2.28515625, 13.0, 4.5703125, 13.0, 13.0, 13.0, 5.7109375, 13.0, 13.0, 13.0, 4.7109375, 13.0,
                    5.140625, 13.0, 13.0, 13.0, 13.0, 13.0, 4.7109375, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                    13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0, 13.0,
                    13.0, 13.0, 5.42578125, None]
        plast_work = CreatePZ.plast_work[0]
        # print(plast_work,  list(CreatePZ.dict_perforation[plast_work]))
        pressuar = list(CreatePZ.dict_perforation[plast_work]['давление'])[0]
        zamer = list(CreatePZ.dict_perforation[plast_work]['замер'])[0]
        vertikal = min(list(CreatePZ.dict_perforation[plast_work]['вертикаль']))
        zhgs = list(CreatePZ.dict_perforation[plast_work]['рабочая жидкость'])[0]
        koef_anomal = round(float(pressuar) * 101325 / (float(vertikal) * 9.81 * 1000), 1)
        nkt = int(list(CreatePZ.dict_nkt.keys())[0])
        lenght_nkt = sum(list(map(int, CreatePZ.dict_nkt.values())))

        bottom_first_port = max(map(lambda x: x[0], [interval for interval in CreatePZ.dict_perforation[plast_work]]))

        arm_grp, ok = QInputDialog.getInT(None, 'Арматура ГРП',
                                                     'ВВедите номер Арматуры ГРП', 16, 0, 500)

        gnkt_lenght =QInputDialog.getInT(None, 'Длина ГНКТ',
                                                     'ВВедите длину ГНКТ', 1500, 500, 10000)



        schema_well_list = [
            ['СХЕМА СКВАЖИНЫ', None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None, None,
             '№ скважины:', None, None, None, None, None, None, None, CreatePZ.well_number, None, None, None, None, None, None,
             None, 'Месторождение:', None, None, None, None, None, None, CreatePZ.well_oilfield, None, None, None, None,
             None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None],

            [None, None, None, None, None, None, None, None, None,
             'Данные о размерности НКТ о конструкции скважины',
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None,
             'Дополнительная информация', None, None, None, None, None, None, None, None, None, None, None, None, None, None],
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
             'Пластовое давление', None, None, None, None, None, None, None, pressuar, None, None, zamer, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             'тройник 80х70-80х70 В60-В60',
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             'Содержание H2S', None, None, None, None, None, None, None, round(CreatePZ.H2S_mg[0],5), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None,
             f'ФА  ГРП ГУ 180х35-89 К1ХЛ № {arm_grp}',
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             'Газовый фактор', None, None, None, None, None, None, None, CreatePZ.gaz_f_pr[0], None, None, None, None, None, None, None],
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
             None, None, 6.21, None, None, 'на глубине', None, None, '1310', None],

            [None, None, None, None, None, None,
             'Стол ротора', None, None, None, CreatePZ.stol_rotora, None, None, None, None, None,
             None, None, 'от', None, 'до', None, None, None, None, None, 'п.м./л', None, 'м3', None, None,
             'Жидкость глушения', None, None, None, None, None, None, None, zhgs, None, None, 'в объеме', None, None,
             28.9, None],
            [None, None, None, None, None, None, 'Направление', None, None, None, None, None,
             CreatePZ.column_direction_diametr, None, CreatePZ.column_direction_wall_thickness, None,
             CreatePZ.column_direction_diametr - 2 * CreatePZ.column_direction_wall_thickness, None,
             CreatePZ.column_direction_lenght, None, None, None, CreatePZ.level_cement_direction, None, None,
             None, None, None, None, None, None, 'Ожидаемый дебит',
             None, None, None, None, None, None, None, CreatePZ.Qwater, None, None, CreatePZ.Qoil, None, None,
             CreatePZ.proc_water, None],
            [None, None, None, None, None, None, 'Кондуктор', None, None, None, None, None,
             CreatePZ.column_conductorn_diametr, None, CreatePZ.column_conductor_wall_thickness, None,
             CreatePZ.column_conductorn_diametr - 2 * CreatePZ.column_conductor_wall_thickness,
             None, CreatePZ.column_conductor_lenght, None, None, None, CreatePZ.level_cement_conductor,
             None, None, None, None, None, None, None, None,
             'Начало / окончание бурения', None, None, None, None, None, None, None,
             CreatePZ.date_drilling_run, None, None, CreatePZ.date_drilling_cancel, None, None, None,
             None],
            [None, None, None, None, None, None, 'Экспл. колонна', None, None, None, None, None,
             CreatePZ.column_diametr, None, CreatePZ.column_wall_thickness, None,
             CreatePZ.column_diametr - 2 * CreatePZ.column_wall_thickness, None, CreatePZ.shoe_column, None, None,
             None, CreatePZ.level_cement_column, None, None, None, 20.550703400000007, None, 22.757643438126006,
             None, None, 'Р в межколонном пространстве', None, None, None, None, None, None, None,
             0, None, None, None, CreatePZ.pressuar_mkp, None, None, None],
            [None, None, None, None, None, None, "Хвостовик  ''НТЦ ''ЗЭРС''", None, None, None, None,
             None, CreatePZ.column_additional_diametr, None,
             CreatePZ.column_additional_wall_thickness, None,
             CreatePZ.column_additional_diametr - 2 * CreatePZ.column_additional_wall_thickness, None,
             CreatePZ.head_column_additional, None, CreatePZ.shoe_column_additional, None, 'не цементиров.', None,
             None, None, 7.4013018499999985,
             None, 2.6034819387559995, None, None, 'Давление опрессовки МКП', None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, f'Подвеска НКТ {nkt}мм', None, None, None, None, None, nkt, None, 6.5,
             None, nkt - 2 * 6.5, None, 0, None, lenght_nkt, None, lenght_nkt, None, None, None,
             volume_vn_nkt(CreatePZ.dict_nkt), None, volume_vn_nkt(CreatePZ.dict_nkt) + 0.47, None, None,
             'Давление опрессовки ЭК ', None, None, None, None,
             None, None, None, CreatePZ.max_expected_pressure, None, None, datetime.datetime(2023, 3, 1, 0, 0),
             None, None, 'гермет.', None],
            [None, None, None, None, None, None, 'Гидроякорь ', None, None, None, None, None, 122, None, None, None, 71,
             None, lenght_nkt, None, lenght_nkt + 1, None, 0.5, None, None, None, None, None, None, None,
             None, 'Макс. допустимое Р опр-ки ЭК', None, None, None, None, None, None, None,
             CreatePZ.max_admissible_pressure, None, None, None,
             None, None, None, None],
            [None, None, None, None, None, None, 'Патрубок 1 шт.', None, None, None, None, None, nkt, None, 6.5, None,
             74.2, None, lenght_nkt - 5.6, None, lenght_nkt - 2.6, None, 3, None, None, None, None,
             None, None, None, None, 'Макс. ожидаемое Р на устье скв.', None, None, None, None, None, None, None, 92.8,
             None, None, None, None, None, None, None],
            [None, None, None, None, None, None, f'стингер {CreatePZ.paker_do["do"]}', None, None, None, None, None,
             None, None,
             None, None, 71, None, lenght_nkt - 2.6, None, lenght_nkt, None, 2.6, None, None, None, None,
             None, None, None, None, 'Текущий забой до ГРП ', None, None, None, None, None, None, None, None, None,
             None, None, None, None, CreatePZ.current_bottom, None],
            [None, None, None, None, None, None, 'ГНКТ', None, None, None, None, None, 38.1, None, 3.96, None, 30.18,
             None, gnkt_lenght, None, None, None, None, None, None, None, round(30.2 ** 2 *3.14/4000, 1), None,
             round(30.2 ** 2 *3.14/4000 *gnkt_lenght/1000, 1), None,
             None, 'Искусственный забой  (МГРП №1 с актив.шаром 30мм)', None, None, None, None, None, None, None, None,
             None, None, None, None, None, bottom_first_port, None],
            [None, None, None, None, None, None, 'Интервалы установки фрак-портов  (муфт ГРП)', None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, 5, None, None, None, None, None, None, 4, None,
             None, None, None, None, None, None, 3, None, None, None, None, None, None, None, 2, None, None, None, None,
             None, None, None, None, None, None, 1, None, None],
            [None, None, None, None, None, None, None, None, None, None, '114/58А', None, None, None, None, None, None,
             '114/52А', None, None, None, None, None, None, None, '114/49А', None, None, None, None, None, None, None,
             '114/47А', None, None, None, None, None, None, None, None, None, None, 'ФПЗН1.114', None, None],
            [None, None, None, None, None, None, None, None, None, None, 1216.95, 'Ø  седла', 'Ø  шара', None, None,
             None, None, 1266.03, 'Ø  седла', 'Ø  шара', None, None, None, None, None, 1326.54, 'Ø  седла', 'Ø  шара',
             None, None, None, None, None, 1387.13, 'Ø  седла', 'Ø  шара', None, None, None, None, None, None, None,
             None, 1460.25, 'Ø  седла', 'Ø  шара', None],
            [None, None, None, None, None, None, None, None, None, None, 1216.05, 55.55, 58.17, None, None, None, None,
             1265.1299999999999, 49.8, 52.43, None, None, None, None, None, 1325.6399999999999, 47.2, 49.71, None, None,
             None, None, None, 1386.23, 45.06, 47.07, None, None, None, None, None, None, None, None, 1459.15, 30, 32],
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

        for row in range(1, len(schema_well_list) + 1):  # Добавлением работ
            print(row, len(schema_well_list[row-1]), schema_well_list[row-1][15])
            for col in range(1, 48):
                cell = ws3.cell(row=row, column=col)

                cell.value = schema_well_list[row - 1][col - 1]
                ws3.cell(row=row, column=col).font = Font(name='Arial', size=11, bold=False)
                ws3.cell(row=row, column=col).alignment = Alignment( horizontal='center',
                                                                                   vertical='center')

        for key, value in boundaries_dict.items():
            ws3.merge_cells(start_column=value[0], start_row=value[1],
                            end_column=value[2], end_row=value[3])

        for index_row, row in enumerate(ws3.iter_rows()):  # Копирование высоты строки
            ws3.row_dimensions[index_row].height = rowHeights1[index_row]
            if row == 8:
                for col_ind, col in enumerate(row):

                    ws3.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind]