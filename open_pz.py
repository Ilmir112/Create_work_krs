from zipfile import ZipFile

from PIL import Image
import block_name
import plan
import krs

from datetime import datetime, time
from openpyxl import Workbook, load_workbook
from PyQt5 import QtCore
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QDialog
from openpyxl.drawing.image import Image
from openpyxl.drawing.spreadsheet_drawing import AbsoluteAnchor
from openpyxl.drawing.xdr import XDRPoint2D, XDRPositiveSize2D
from openpyxl.utils.units import pixels_to_EMU, cm_to_EMU

from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment

from cdng import events_gnvp, itog_1, events_gnvp_gnkt


class CreatePZ:
    gipsInWell = False
    grpPlan = False
    nktOpressTrue = False
    bottomhole_drill = 0
    open_trunk_well = False
    normOfTime = 0
    lift_ecn_can = False
    pause = True
    curator = '0'
    lift_ecn_can_addition = False
    column_passability = False
    column_additional_passability = False
    template_depth = 0
    nkt_diam = 73
    b_plan = 0
    expected_Q = 0
    expected_P = 0
    plast_select = ''
    dict_perforation = {}
    dict_perforation_project = {}
    itog_ind_min = 0
    kat_pvo = 2
    gaz_f_pr = []
    paker_layout = 0
    paker_diam_dict = {
        82: (88, 92),
        88: (92.1, 97),
        92: (97.1, 102),
        100: (102.1, 109),
        104: (109, 115),
        112: (118, 120),
        114: (120.1, 121.9),
        116: (122, 123.9),
        118: (124, 127.9),
        122: (128, 133),
        136: (144, 148),
        142: (148.1, 154),
        145: (154.1, 164),
        158: (166, 176),
        182: (190.6, 203.6),
        204: (215, 221)
    }
    column_additional_diametr = 0
    column_additional_wall_thickness = 0
    shoe_column_additional = 0
    column_diametr = 0
    column_wall_thickness = 0
    shoe_column = 0
    bottomhole_artificial = 0
    max_expected_pressure = 0
    head_column_additional = 0
    leakiness_Count = 0
    expected_pick_up = {}
    current_bottom = 0
    fluid_work = 0
    static_level = 0
    dinamic_level = 0
    work_perforations_approved = False
    dict_leakiness = {}
    leakiness = False
    emergency_well = False
    emergency_count = 0

    work_perforations = []
    work_perforations_dict = {}
    paker_do = {"do": 0, "posle": 0}
    column_additional = False
    well_number = None
    well_area = None
    values = []
    H_F_paker_do = {"do": 0, "posle": 0}
    paker2_do = {"do": 0, "posle": 0}
    H_F_paker2_do = {"do": 0, "posle": 0}
    perforation_roof = 50000
    perforation_sole = 0
    dict_pump_SHGN = {"do": '0', "posle": '0'}
    dict_pump_ECN = {"do": '0', "posle": '0'}
    dict_pump_SHGN_h = {"do": '0', "posle": '0'}
    dict_pump_ECN_h = {"do": '0', "posle": '0'}
    dict_pump = {"do": '0', "posle": '0'}
    leakiness_interval = []
    dict_pump_h = {"do": 0, "posle": 0}
    ins_ind = 0
    len_razdel_1 = 0
    cat_P_1 = []
    countAcid = 0
    swabTypeComboIndex = 1
    swabTrueEditType = 1
    data_x_max = 0
    drilling_interval = []
    max_angle = 0
    pakerTwoSKO = False
    privyazkaSKO = 0
    H2S_pr = []
    cat_H2S_list = []
    H2S_mg = []
    lift_key = 0
    max_admissible_pressure = 0
    region = ''
    dict_nkt = {}
    dict_nkt_po = {}
    data_well_max = 0
    data_pvr_max = 0
    dict_sucker_rod = {}
    dict_sucker_rod_po = {}
    row_expected = []
    rowHeights = []
    plast_project = []
    plast_work = []
    plast_all = []
    condition_of_wells = 0
    cat_well_min = []
    bvo = False
    old_version = False
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    image_list = []

    def __init__(self, dict_perforation_project, work_perforations_dict, ins_ind_border, wb, ws, parent=None):
        super().__init__(parent)
        # self.lift_ecn_can_addition = lift_ecn_can_addition
        self.dict_perforation_project = dict_perforation_project
        self.work_perforations_dict = work_perforations_dict
        self.ins_ind_border = ins_ind_border
        self.wb = wb
        self.ws = ws

    def open_excel_file(self, fname, work_plan):
        from data_correct import DataWindow
        CreatePZ.work_plan = work_plan
        global wb, ws
        wb = load_workbook(fname, data_only=True)
        name_list = wb.sheetnames
        # print(name_list)
        old_index = 1
        ws = wb.active
        for sheet in name_list:
            if sheet in wb.sheetnames and sheet != 'наряд-заказ КРС':
                wb.remove(wb[sheet])
        # print(wb.sheetnames)

        # zip = ZipFile(fname)
        # zip.extractall()

        # Копирование изображения
        # drawings = ws.drawings
        for img in ws._images:
            #     # Получение изображения и его координат
            #     # print(img.anchor)
            #     p2e = pixels_to_EMU
            #     h, w = img.height, img.width
            #
            #
            #
            #     # position = XDRPoint2D(p2e(), p2e())
            #     print(img.anchor)
            #     # print(f'size image {img.height} w-{img.width} ')
            #     # size = XDRPositiveSize2D(p2e(w*3), p2e(h))
            #     # img.anchor = AbsoluteAnchor(pos = position, ext = size)
            #
            #     # img.width = 200
            #     # img.height = 180
            #
            CreatePZ.image_list.append(img)

        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            ws.row_dimensions[row_ind].hidden = False
            if 'Категория скважины' in row:
                CreatePZ.cat_well_min.append(row_ind + 1)  # индекс начала категории

            elif 'План-заказ' in row or 'ПЛАН РАБОТ' in row:
                ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'
                CreatePZ.cat_well_max = row_ind - 1
                data_well_min = row_ind + 1


            elif any(['IX. Мероприятия по предотвращению' in str(col) for col in row]):
                CreatePZ.data_well_max = row_ind

            elif 'X. Ожидаемые показатели после ремонта:' in row:
                CreatePZ.data_x_min = row_ind


            elif 'ШТАНГИ' in row:
                sucker_rod = True
                sucker_rod_ind = row_ind
                # sucker_rod_ind = self.sucker_rod_ind

            elif 'НКТ' in row:
                pipes_ind = row_ind
                # pipes_ind = self.pipes_ind

            elif 'ХI Планируемый объём работ:' in row or 'ХI. Планируемый объём работ:' in row or 'ХIII Планируемый объём работ:' in row \
                    or 'ХI Планируемый объём работ:' in row:
                CreatePZ.data_x_max = row_ind

            elif 'II. История эксплуатации скважины' in row:
                data_pvr_max = row_ind

            elif 'III. Состояние скважины к началу ремонта ' in row:
                CreatePZ.condition_of_wells = row_ind

            for col, value in enumerate(row):
                if not value is None and col <= 12:
                    if 'площадь' == value:  # определение номера скважины
                        CreatePZ.well_number = row[col - 1]
                        CreatePZ.well_area = row[col + 1]
                    elif '11. Эксплуатационные горизонты и интервалы перфорации:' == value:
                        data_pvr_min = row_ind + 2
                    elif 'к ГРП' in str(value):
                        CreatePZ.grpPlan = True
                    elif '7. Пробуренный забой' == value:
                        index_bottomhole = row_ind
                        CreatePZ.bottomhole_drill = row[col + 2]
                        n = 1
                        while CreatePZ.bottomhole_drill is None:
                            CreatePZ.bottomhole_drill = row[col + 2 + n]
                            n += 1
                            CreatePZ.bottomhole_drill = row[col + 2 + n]
                        CreatePZ.bottomhole_artificial = row[col + 5]
                        n = 1
                        while CreatePZ.bottomhole_artificial is None:
                            CreatePZ.bottomhole_artificial = row[col + 5 + n]
                            n += 1
                            CreatePZ.bottomhole_artificial = float(row[col + 5 + n])
                    elif 'текущий забой ' == str(
                            value).lower():  # and any(['способ' in str(column).lower() for column in row]) == True:
                        CreatePZ.current_bottom = row[col + 2]
                        n = 2
                        while CreatePZ.current_bottom is None or n == 6:
                            # print(n)
                            CreatePZ.current_bottom = row[col + n]
                            n += 1



                    elif 'месторождение ' == value:
                        CreatePZ.oilfield = row[col + 2]

                    elif value == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':  # Определение данных по колонне
                        data_main_production_string = (ws.cell(row=row_ind + 2, column=col + 1).value).split('(мм),', )
                        try:
                            if len(data_main_production_string) == 3:
                                CreatePZ.column_diametr = float(data_main_production_string[0])
                                CreatePZ.column_wall_thickness = float(data_main_production_string[1])
                                if len(data_main_production_string[-1].split('-')) == 2:

                                    CreatePZ.shoe_column = CreatePZ.without_b(
                                        data_main_production_string[-1].split('-')[-1])
                                elif len(data_main_production_string[-1].split('(м)')) == 2:
                                    CreatePZ.shoe_column = CreatePZ.without_b(data_main_production_string[-1])
                        except ValueError:
                            pass


                    elif 'гипс' in str(value).lower() or 'гидратн' in str(value).lower():
                        CreatePZ.gipsInWell = True

                    elif '9. Максимальный зенитный угол' == value:
                        CreatePZ.max_angle = row[col + 1]
                        n = 1
                        while CreatePZ.max_angle is None:
                            CreatePZ.max_angle = row[col + n]
                            n += 1

                    elif 'по H2S' in row and ('мг/л' in row or 'мг/дм3' in row):
                        if value == 'мг/л' or 'мг/дм3':
                            if CreatePZ.if_None(row[col - 1]) == 'отсут':
                                CreatePZ.H2S_mg.append(0)
                            else:
                                CreatePZ.H2S_mg.append(row[col - 1])
                    elif '%' in row:

                        if value == '%':
                            # print(row_ind)
                            if CreatePZ.if_None(row[col - 1]) == 'отсут':
                                CreatePZ.H2S_pr.append(0)
                            else:
                                CreatePZ.H2S_pr.append(row[col - 1])

                        # print(f'H2s % {CreatePZ.H2S_pr}')
                    elif 'по H2S' in row and ('мг/м3' in row):

                        if len(CreatePZ.H2S_mg) == 0 and 'мг/м3' == value:
                            if CreatePZ.if_None(row[col - 1]) != 'отсут':
                                CreatePZ.H2S_mg.append(float(row[col - 1] / 1000))


                    elif '9. Максимальный зенитный угол' in row and value == 'на глубине':
                        try:
                            CreatePZ.max_h_angle = row[col + 1]
                        except:
                            CreatePZ.max_h_angle, ok = QInputDialog.getint(self, 'Глубина максимального угла',
                                                                           'Введите глубину максимального зетного угла: ',
                                                                           500, 1, 4000)
                    elif 'цех' == value:
                        cdng = row[col + 1]
                        CreatePZ.cdng = cdng
                        # print(f' ЦДНГ {CreatePZ.cdng}')
                    elif 'плотн.воды' == value:
                        try:
                            CreatePZ.water_cut = float(row[col - 1])  # обводненность
                        except:
                            CreatePZ.water_cut, ok = QInputDialog.getInt(self, 'Обводненность',
                                                                         'Введите обводненность скважинной продукции',
                                                                         100,
                                                                         0, 100)
                    elif value == 'м3/т':
                        CreatePZ.gaz_f_pr.append(row[col - 1])


                    elif '6. Конструкция хвостовика' in str(value):
                        column_add_index = row_ind + 3
                        CreatePZ.data_column_additional = ws.cell(row=row_ind + 3, column=col + 2).value

                        if CreatePZ.if_None(CreatePZ.data_column_additional) != 'отсут':
                            CreatePZ.column_additional = True
                            print(f' в скважине дополнительная колонны {CreatePZ.data_column_additional}')

                        # print(CreatePZ.column_additional)
                        if CreatePZ.column_additional == True:
                            try:
                                CreatePZ.head_column_additional = float(CreatePZ.data_column_additional.split('-')[0])
                            except:
                                CreatePZ.head_column_additional, ok = QInputDialog.getInt(self, 'голова доп колонны',
                                                                                          'введите глубину головы доп колонны',
                                                                                          600, 0, 3500)
                            try:
                                CreatePZ.shoe_column_additional = float(CreatePZ.data_column_additional.split('-')[1])
                                print(f'доп колонна {CreatePZ.shoe_column_additional}')
                            except:
                                CreatePZ.shoe_column_additional, ok = QInputDialog.getInt(self, ',башмак доп колонны',
                                                                                          'введите глубину башмак доп колонны',
                                                                                          600, 0, 3500)
                            try:
                                if ws.cell(row=row_ind + 3, column=col + 4).value.split('x') == 2:
                                    CreatePZ.column_additional_diametr = CreatePZ.without_b(
                                        ws.cell(row=row_ind + 3, column=col + 4).value.split('x')[0])
                                    CreatePZ.column_additional_wall_thickness = CreatePZ.without_b(
                                        ws.cell(row=row_ind + 3, column=col + 4).value.split('x')[1])
                            except:
                                pass
                            try:
                                CreatePZ.column_additional_diametr = float(
                                    CreatePZ.without_b(ws.cell(row=row_ind + 3, column=col + 4).value))
                                print(f' диаметр доп колонны {CreatePZ.column_additional_diametr}')
                            except:
                                CreatePZ.column_additional_diametr, ok = QInputDialog.getDouble(self,
                                                                                                ',диаметр доп колонны',
                                                                                                'введите внешний диаметр доп колонны',
                                                                                                102, 50, 170)
                            try:
                                CreatePZ.column_additional_wall_thickness = float(
                                    CreatePZ.without_b(ws.cell(row=row_ind + 3, column=col + 6).value))
                                if CreatePZ.column_additional_wall_thickness == '0':
                                    CreatePZ.column_additional_wall_thickness, ok = QInputDialog.getDouble(self,
                                                                                                           ',толщина стенки доп колонны',
                                                                                                           'введите толщину стенки доп колонны',
                                                                                                           6.5, 3, 11,
                                                                                                           1)

                                print(f'толщина стенки доп колонны {CreatePZ.column_additional_wall_thickness} ')
                            except:
                                CreatePZ.column_additional_wall_thickness, ok = QInputDialog.getDouble(self,
                                                                                                       ',толщина стенки доп колонны',
                                                                                                       'введите толщину стенки доп колонны',
                                                                                                       6.5, 3, 11, 1)
                        if float(CreatePZ.column_additional_diametr) >= 170:
                            CreatePZ.column_additional_diametr, ok = QInputDialog.getDouble(self,
                                                                                            ',диаметр доп колонны',
                                                                                            'введите внешний диаметр доп колонны',
                                                                                            114, 70, 220, 1)
                            CreatePZ.column_additional_wall_thickness, ok = QInputDialog.getDouble(self,
                                                                                                   ',толщина стенки доп колонны',
                                                                                                   'введите толщину стенки доп колонны',
                                                                                                   6.4, 4, 12, 1)

                    elif 'Дата вскрытия/отключения' == value:
                        CreatePZ.old_version = True
                        old_index = 0

                    elif 'Максимально ожидаемое давление на устье' == value:
                        CreatePZ.max_expected_pressure = row[col + 1]
                        n = 1
                        while CreatePZ.max_expected_pressure is None:
                            CreatePZ.max_expected_pressure = row[col + n]
                            n += 1


                    elif 'Максимально допустимое давление опрессовки э/колонны' == value or 'Максимально допустимое давление на э/колонну' == value:
                        CreatePZ.max_admissible_pressure = row[col + 1]
                        n = 1
                        while CreatePZ.max_admissible_pressure is None:
                            CreatePZ.max_admissible_pressure = row[col + n]
                            n += 1

                    elif 'Пакер' in str(value) and 'типоразмер' in str(row[col + 2]):
                        try:
                            CreatePZ.paker_do["do"] = (row[col + 4]).split('/')[0]
                            CreatePZ.paker2_do["do"] = (row[col + 4]).split('/')[1]
                        except:
                            CreatePZ.paker_do["do"] = CreatePZ.if_None(row[col + 4])
                            n = 1
                            while CreatePZ.paker_do["do"] is None:
                                CreatePZ.max_admissible_pressure = row[col + 4 + n]
                                n += 1
                        try:
                            CreatePZ.paker_do["posle"] = CreatePZ.paker_do["posle"].split('/')[0]
                            CreatePZ.paker2_do["posle"] = CreatePZ.paker_do["posle"].split('/')[1]
                        except:
                            CreatePZ.paker_do["posle"] = CreatePZ.if_None(row[col + 8 + old_index])
                            n = 0
                            while CreatePZ.paker_do["posle"] is None:
                                CreatePZ.CreatePZ.paker_do["posle"] = row[col + 8 + old_index + n]
                                n += 1

                    elif value == 'Насос' and row[col + 2] == 'типоразмер':
                        if CreatePZ.if_None(row[col + 4]) != 'отсут':
                            if ('НВ' in str(row[col + 4]).upper() or 'ШГН' in str(row[col + 4]).upper() \
                                    or 'НН' in str(row[col + 4]).upper()):
                                CreatePZ.dict_pump_SHGN["do"] = row[col + 4]
                                n = 0
                                while CreatePZ.dict_pump_SHGN["do"] is None:
                                    CreatePZ.dict_pump_SHGN["do"] = row[col + 4 + n]
                                    n += 1

                            if ('ЭЦН' in str(row[col + 4]).upper() or 'ВНН' in str(row[col + 4]).upper()):
                                CreatePZ.dict_pump_ECN["do"] = row[col + 4]
                                n = 0
                                while CreatePZ.dict_pump_ECN["do"] is None:
                                    CreatePZ.dict_pump_ECN["do"] = row[col + 4 + n]
                                    n += 1

                        if CreatePZ.if_None(row[col + 8 + old_index]) != 'отсут':

                            if ('НВ' in str(row[col + 8 + old_index]).upper() or 'ШГН' in str(
                                    row[col + 8 + old_index]).upper() \
                                    or 'НН' in str(row[col + 8 + old_index]).upper()):
                                CreatePZ.dict_pump_SHGN["posle"] = row[col + 8 + old_index]
                                n = 0
                                while CreatePZ.dict_pump_SHGN["posle"] is None or n == 12:
                                    CreatePZ.dict_pump_SHGN["posle"] = row[col + 8 + old_index + n]
                                    n += 1
                            if ('ЭЦН' in str(row[col + 8 + old_index]).upper() or 'ВНН' in str(
                                    row[col + 8 + old_index]).upper()):
                                CreatePZ.dict_pump_ECN["posle"] = row[col + 8 + old_index]
                                n = 0
                                while CreatePZ.dict_pump_ECN["posle"] is None or n == 12:
                                    CreatePZ.dict_pump_ECN["posle"] = row[col + 8 + old_index + n]
                                    n += 1

                        # print(f' ячейка {ws.cell(row=row_ind + 5, column=col + 3).value}')

                        if ws.cell(row=row_ind + 5, column=col + 3).value == 'Нсп, м':
                            if CreatePZ.dict_pump_ECN["do"] != '0':
                                # print(f' Спуск ЭЦН ТРУ {CreatePZ.if_None(CreatePZ.dict_pump_ECN["do"])}')
                                CreatePZ.dict_pump_ECN_h["do"] = ws.cell(row=row_ind + 5, column=col + 5).value

                            if CreatePZ.dict_pump_SHGN["do"] != '0':
                                CreatePZ.dict_pump_SHGN_h["do"] = ws.cell(row=row_ind + 5, column=col + 5).value
                            if CreatePZ.dict_pump_ECN["posle"] != '0':
                                CreatePZ.dict_pump_ECN_h["posle"] = ws.cell(row=row_ind + 5,
                                                                            column=col + 9 + old_index).value
                            if CreatePZ.dict_pump_SHGN["posle"] != '0':
                                CreatePZ.dict_pump_SHGN_h["posle"] = ws.cell(row=row_ind + 5,
                                                                             column=col + 9 + old_index).value

                    elif value == 'Н посадки, м':
                        try:
                            if CreatePZ.paker_do["do"] != '0':
                                print(CreatePZ.without_b(row[col + 2]))
                                CreatePZ.H_F_paker_do["do"] = CreatePZ.without_b(row[col + 2])[0]
                                CreatePZ.H_F_paker2_do["do"] = CreatePZ.without_b(row[col + 2])[1]
                        except:
                            if CreatePZ.paker_do["do"] != '0':
                                CreatePZ.H_F_paker_do["do"] = CreatePZ.without_b(row[col + 2])
                        try:
                            if CreatePZ.paker_do["posle"] != '0':
                                CreatePZ.H_F_paker_do["posle"] = CreatePZ.without_b(row[col + 6 + old_index])[0]
                                CreatePZ.H_F_paker2_do["posle"] = CreatePZ.without_b(row[col + 6 + old_index])[1]
                        except:
                            if CreatePZ.paker_do["posle"] != '0':
                                CreatePZ.H_F_paker_do["posle"] = CreatePZ.without_b(row[col + 6 + old_index])

                    elif " Нст " in str(value):
                        CreatePZ.static_level = row[col + 1]
                    elif " Ндин " in str(value):
                        CreatePZ.dinamic_level = row[col + 1]
        # вызов окна для проверки корректности данных
        if self.data_window is None:
            self.data_window = DataWindow(self)
            self.data_window.setWindowTitle("Сверка данных")
            self.data_window.setGeometry(200, 400, 300, 400)

            self.data_window.show()
        CreatePZ.pause_app(self)
        CreatePZ.pause = True

        if CreatePZ.condition_of_wells == 0:
            CreatePZ.condition_of_wells, ok = QInputDialog.getInt(self, 'индекс Окончания копирования',
                                                                  'Программа не смогла определить строку n\ III. Состояние скважины к началу ремонта ',
                                                                  0, 0, 800)

        if len(CreatePZ.cat_well_min) == 0:
            cat_well_min, ok = QInputDialog.getInt(self, 'индекс начала копирования',
                                                   'Программа не смогла определить строку начала копирования',
                                                   0, 0, 800)
            CreatePZ.cat_well_min.append(cat_well_min)
        if CreatePZ.data_x_max == 0:
            CreatePZ.data_x_max, ok = QInputDialog.getInt(self, 'индекс окончания копирования',
                                                          'Программа не смогла определить строку окончания копирования',
                                                          0, 0, 800)

        if str(CreatePZ.well_number) in ['1436', '756', '1235', '2517', '2529', '655', '2525', '751',
                                         '1371', '1293', '1420', '296', '321', '351', '186', '815', '135', '226', '377',
                                         '249']:
            QMessageBox.warning(self, 'Канатные технологии', f'Скважина согласована на канатные технологии')

        if CreatePZ.grpPlan:
            grpPlan_quest = QMessageBox.question(self, 'Подготовка к ГРП', 'Программа определела что в скважине'
                                                                           f'планируется ГРП, верно ли?')
            if grpPlan_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.grpPlan = True
            else:
                CreatePZ.grpPlan = False
        print(CreatePZ.dict_pump_ECN, CreatePZ.dict_pump_SHGN, CreatePZ.dict_pump_ECN_h, CreatePZ.H_F_paker_do)
        print()
        # Определение наличия по скважине нарушений
        for row in range(data_pvr_max, CreatePZ.data_well_max):
            for col in range(1, 13):
                value = str(ws.cell(row=row, column=col).value)
                if 'нэк' in str(
                        value).lower() or 'негерм' in value.lower() or 'нарушение э' in value.lower() or 'нарушение г' in value.lower():
                    CreatePZ.leakiness_Count += 1
                    CreatePZ.leakiness = True
                if (
                        'авар' in value.lower() or 'не проход' in value.lower() or 'расхаж' in value.lower() or 'лар' in value) \
                        and 'акт о расследовании аварии прилагается' not in value:
                    CreatePZ.emergency_well = True
                    CreatePZ.emergency_count += 1

        if CreatePZ.leakiness == True:
            leakiness_quest = QMessageBox.question(self, 'нарушение колонны', 'Программа определела что в скважине'
                                                                              f'есть нарушение - {CreatePZ.leakiness_Count}, верно ли?')
            if leakiness_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.leakiness = True
                krs.get_leakiness(self)

            else:
                CreatePZ.leakiness = False

        if CreatePZ.emergency_well == True:
            emergency_quest = QMessageBox.question(self, 'Аварийные работы ', 'Программа определела что в скважине'
                                                                              f'авария - {CreatePZ.emergency_count}, верно ли?')
            if emergency_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.emergency_well = True
            else:
                CreatePZ.emergency_well = False

        if CreatePZ.gipsInWell == True:
            gips_true_quest = QMessageBox.question(self, 'Гипсовые отложения',
                                                   'Программа определела что скважина осложнена гипсовыми отложениями '
                                                   'и требуется предварительно определить забой на НКТ, верно ли это?')

            if gips_true_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.gipsInWell = True
            else:
                CreatePZ.gipsInWell = False

        curator_list = ['ОР', 'ГТМ', 'ГРР', 'ГО', 'ВНС']
        curator = ['ГТМ'
                   if (CreatePZ.dict_pump_SHGN["posle"] != '0' and CreatePZ.dict_pump_ECN["posle"] == '0')
                      or (CreatePZ.dict_pump_SHGN["posle"] == '0' and CreatePZ.dict_pump_ECN["posle"] != '0')
                      or (CreatePZ.dict_pump_SHGN["posle"] != '0' and CreatePZ.dict_pump_ECN["posle"] != '0')
                   else 'ОР'][0]

        CreatePZ.region = block_name.region(cdng)

        CreatePZ.curator, ok = QInputDialog.getItem(self, 'Выбор кураторов ремонта', 'Введите сектор кураторов региона',
                                                    curator_list, curator_list.index(curator), False)
        print(f'куратор {CreatePZ.curator, CreatePZ.if_None(CreatePZ.dict_pump["posle"])}')
        if CreatePZ.column_additional == False and float(CreatePZ.shoe_column) < float(CreatePZ.current_bottom):
            CreatePZ.open_trunk_well = True
        elif CreatePZ.column_additional == True and float(CreatePZ.shoe_column_additional) < float(
                CreatePZ.current_bottom):
            CreatePZ.open_trunk_well = True

        print(f' ГРП - {CreatePZ.grpPlan}')
        print(f' глубина насоса ШГН {CreatePZ.dict_pump_SHGN_h}')
        print(f' насоса {CreatePZ.dict_pump_SHGN}')
        print(f'пакер {CreatePZ.paker_do}')
        print(f'глубина пакер {CreatePZ.H_F_paker_do}')
        print(f' диам колонны {CreatePZ.column_diametr}')
        print(f' гипс в скважине {CreatePZ.gipsInWell}')
        print(
            f'{CreatePZ.column_additional == False},{("ЭЦН" in str(CreatePZ.dict_pump["posle"]).upper() or "ВНН" in str(CreatePZ.dict_pump["posle"][0]).upper())}')
        print(f'Pdd {str(CreatePZ.dict_pump["posle"]).upper()}')
        if CreatePZ.column_additional == False and CreatePZ.dict_pump_ECN["posle"] != '0':
            print(
                f'{CreatePZ.column_additional == False},{("ЭЦН" in str(CreatePZ.dict_pump["posle"]).upper(), "ВНН" in str(CreatePZ.dict_pump["posle"]).upper())}')

            CreatePZ.lift_ecn_can = True
        elif CreatePZ.column_additional == True:
            if CreatePZ.dict_pump_ECN["posle"] != '0' and float(
                    CreatePZ.dict_pump_ECN_h["posle"]) < CreatePZ.head_column_additional:
                CreatePZ.lift_ecn_can = True

            elif CreatePZ.dict_pump_ECN["posle"] != '0' and \
                    float(CreatePZ.dict_pump_ECN_h["posle"]) > CreatePZ.head_column_additional:

                CreatePZ.lift_ecn_can_addition = True
            # print(f' ЭЦН длина" {CreatePZ.lift_ecn_can, CreatePZ.lift_ecn_can_addition, "ЭЦН" in str(CreatePZ.dict_pump["posle"][0]).upper()}')

        # print(f'fh {len(CreatePZ.H2S_mg)}')
        for row in range(CreatePZ.cat_well_min[0], CreatePZ.cat_well_max + 1):
            if 'по Pпл' == ws.cell(row=row, column=2).value:
                for column in range(1, 13):
                    col = ws.cell(row=row, column=column).value

                    if str(col) in ['1', '2', '3']:
                        CreatePZ.cat_P_1.append(int(col))
            if 'по H2S' == ws.cell(row=row, column=2).value and 'по H2S' != ws.cell(row=row - 1, column=2).value:
                for column in range(1, 13):
                    col = ws.cell(row=row, column=column).value
                    if str(col) in ['1', '2', '3']:
                        CreatePZ.cat_H2S_list.append(int(col))

            if '1' in CreatePZ.cat_H2S_list or '2' in CreatePZ.cat_H2S_list:
                if len(CreatePZ.H2S_mg) == 0:

                    H2S_mg = QInputDialog.getDouble(self, 'Сероводород',
                                                    'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                    H2S_mg_true_quest = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
                    CreatePZ.H2S_mg.append(H2S_mg)
                    while H2S_mg_true_quest == QMessageBox.StandardButton.Yes:
                        H2S_mg = QInputDialog.getDouble(self, 'Сероводород',
                                                        'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                        H2S_mg_true_quest = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
                        CreatePZ.H2S_mg.append(H2S_mg)
                if len(CreatePZ.H2S_pr) == 0:

                    H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                                    'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                    H2S_pr_true_quest = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
                    CreatePZ.H2S_mg.append(H2S_pr)
                    while H2S_pr_true_quest == QMessageBox.StandardButton.Yes:
                        H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                                        'Введите содержание сероводорода в мг/л', 50, 0, 1000, 2)
                        H2S_pr_true_quest = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
                        CreatePZ.H2S_mg.append(H2S_pr)
        if CreatePZ.curator == 'ОР':
            try:
                # print(CreatePZ.data_x_min, CreatePZ.data_x_max)
                # expected_list = []
                for row in range(CreatePZ.data_x_min + 2, CreatePZ.data_x_max + 1):
                    for col in range(1, 12):
                        if 'прием' in str(ws.cell(row=row, column=col).value).strip().lower() or 'q' in str(
                                ws.cell(row=row, column=col).value).strip().lower():
                            Qpr = ws.cell(row=row, column=col + 1).value
                            # print(f' приемис {Qpr}')
                            n = 1
                            while Qpr is None:
                                ws.cell(row=row, column=col + n).value
                                n += 1
                                Qpr = ws.cell(row=row, column=col + n).value
                            # print(f'после {Qpr}')


                        elif 'зак' in str(ws.cell(row=row, column=col).value).strip().lower() or 'давл' in str(
                                ws.cell(row=row, column=col).value).strip().lower() or 'P' in str(
                            ws.cell(row=row, column=col).value).strip().lower():
                            Pzak = ws.cell(row=row, column=col + 1).value
                            n = 1
                            # while Pzak is None:
                            #     n += 1
                            #     Pzak = ws.cell(row=row, column=col + n).value
                            #     print(f'pзака {Pzak}')

                CreatePZ.expected_P = Pzak
                CreatePZ.expected_Q = Qpr
                CreatePZ.expected_pick_up[Qpr] = Pzak
                # print(f' ожидаемые показатели {CreatePZ.expected_pick_up}')

            except:
                print('ошибка при определении плановых показателей')
                expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                     f'Ожидаемая приемистость по пласту ',
                                                     100, 0,
                                                     1600)
                expected_P, ok = QInputDialog.getInt(self, f'Ожидаемое Давление закачки',
                                                     f'Ожидаемое Давление закачки по пласту ',
                                                     100, 0,
                                                     250)
                CreatePZ.expected_pick_up[expected_Q] = expected_P
                print(f' Ожидаемые {CreatePZ.expected_pick_up}')
        # print(f' индекс нкт {pipes_ind + 1, CreatePZ.condition_of_wells}')

        for row in range(pipes_ind + 1, CreatePZ.condition_of_wells):  # словарь  количества НКТ и метраж
            if ws.cell(row=row, column=3).value == 'План' or str(
                    ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                CreatePZ.a_plan = row
        try:
            CreatePZ.a_plan == 0
        except:
            CreatePZ.a_plan, ok = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                                         'Программа не могла определить начала строку с ПЗ НКТ - план')
        # print(f'индекс {CreatePZ.a_plan}')
        for row in range(pipes_ind + 1, CreatePZ.condition_of_wells + 1):
            key = ws.cell(row=row, column=4).value
            value = CreatePZ.without_b(ws.cell(row=row, column=7).value)
            if not key is None and row < CreatePZ.a_plan:
                CreatePZ.dict_nkt[key] = CreatePZ.dict_nkt.get(key, 0) + float(value)
            elif not key is None and row >= CreatePZ.a_plan:
                CreatePZ.dict_nkt_po[key] = CreatePZ.dict_nkt_po.get(key, 0) + float(value)

        try:
            CreatePZ.shoe_nkt = float(sum(CreatePZ.dict_nkt.values()))
            CreatePZ.shoe_nkt > CreatePZ.bottomhole_artificial
        except:
            print('НКТ ниже забоя')
        # print(f' индекс штанг{sucker_rod_ind, pipes_ind}')
        try:
            for row in range(sucker_rod_ind, pipes_ind - 1):
                if ws.cell(row=row, column=3).value == 'План' or str(
                        ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                    CreatePZ.b_plan = row
                    # print(f'b_plan {CreatePZ.b_plan}')
            if CreatePZ.b_plan == 0:
                CreatePZ.b_plan, ok = QInputDialog.getDouble(self, 'Индекс плановго НКТ',
                                                             'Программа не могла определить начала строку с ПЗ штанги - план')

            for row in range(sucker_rod_ind + 1, pipes_ind - 1):

                key = ws.cell(row=row, column=4).value
                value = ws.cell(row=row, column=7).value
                if CreatePZ.if_None(key) != 'отсут' and row < CreatePZ.b_plan:

                    CreatePZ.dict_sucker_rod[key] = CreatePZ.dict_sucker_rod.get(key, 0) + int(
                        CreatePZ.without_b(value + 1))
                elif CreatePZ.if_None(key) != 'отсут' and row >= CreatePZ.b_plan:
                    CreatePZ.dict_sucker_rod_po[key] = CreatePZ.dict_sucker_rod_po.get(key, 0) + int(
                        CreatePZ.without_b(value))
                # self.dict_sucker_rod = dict_sucker_rod
                # self.dict_sucker_rod_po = dict_sucker_rod_po
            print(f' штанги на спуск {CreatePZ.dict_sucker_rod_po}')
        except:
            print('штанги отсутствуют')
        perforations_intervals = []

        print(f' индекс ПВР{data_pvr_min + 2, data_pvr_max + 1}')
        for row in range(data_pvr_min, data_pvr_max + 2):  # Сортировка интервала перфорации
            lst = []
            if isinstance(ws.cell(row=row, column=3).value, int) or isinstance(ws.cell(row=row, column=3).value, float):
                for i in range(2, 13):
                    lst.append(ws.cell(row=row, column=i).value)

                # print(ws.cell(row=row, column=6).value)
                if CreatePZ.old_version == True and isinstance(ws.cell(row=row, column=6).value, datetime) == True:
                    lst.insert(5, None)
                elif CreatePZ.old_version == True and isinstance(ws.cell(row=row, column=6).value,
                                                                 datetime) == False and not ws.cell(row=row,
                                                                                                    column=5).value is None:
                    lst.insert(5, 'отключен')
                if all([str(i).strip() == 'None' or i is None for i in lst]) == False:
                    perforations_intervals.append(lst)

        for ind, row in enumerate(perforations_intervals):
            print(row)
            krovlya_perf = float(row[2])

            print(f'кровля ПВР {krovlya_perf}')
            plast = row[0]
            if plast is None:
                plast = perforations_intervals[ind - 1][0]
                # print(f' после {plast}')
                perforations_intervals[ind][0] = perforations_intervals[ind - 1][0]

            # print(row, any([str((i)).lower() == 'проект' for i in row]), all([str(i).strip() is None for i in row]) == False)
            if any(['проект' in str((i)).lower() or 'не пер' in str((i)).lower() for i in row]) == False and all(
                    [str(i).strip() is None for i in row]) == False and krs.is_number(row[2]) == True \
                    and krs.is_number(float(row[3])) == True:
                # print(f'5 {row}')

                if krs.is_number(row[1]) == True:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('вертикаль', set()).add(row[1])

                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', 0)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('интервал', set()).add(
                    (round(float(row[2]), 1), round(float(row[3]), 1)))


                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('вскрытие', set()).add(row[4])
                # print(f'отключе {isinstance(row[5], datetime) == True, old_index} ggg {isinstance(row[6], datetime) == True, CreatePZ.old_version, old_index}')
                if row[5] is None or row[5] == '-':
                    print(f'отключение {plast, row[5], row[5] != "-"}')
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
                else:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', True)

                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('удлинение', set()).add(row[8])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('давление', set()).add(row[9])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('замер', set()).add(row[10])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(
                    krs.calculationFluidWork(row[1], row[9]))



            elif any([str((i)).lower() == 'проект' for i in row]) == True and all(
                    [str(i).strip() is None for i in row]) == False and krs.is_number(row[2]) == True \
                    and krs.is_number(float(row[2])) == True:  # Определение проектных интервалов перфорации

                self.dict_perforation_project.setdefault(plast, {}).setdefault('вертикаль', set()).add(row[1])
                self.dict_perforation_project.setdefault(plast, {}).setdefault('интервал', set()).add(
                    (round(float(row[2]), 1), round(float(row[3]), 1)))
                self.dict_perforation_project.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                self.dict_perforation_project.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                self.dict_perforation_project.setdefault(plast, {}).setdefault('удлинение', set()).add(
                    row[8])
                self.dict_perforation_project.setdefault(plast, {}).setdefault('давление', set()).add(
                    row[9])
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(
                    krs.calculationFluidWork(row[1], row[9]))


            # print(f'проект{CreatePZ.dict_perforation_project[plast]}')
        print(f'раб{CreatePZ.dict_perforation}')
        CreatePZ.definition_plast_work(self)
        CreatePZ.dict_perforation_project = self.dict_perforation_project
        if len(CreatePZ.dict_perforation_project) != 0:
            CreatePZ.plast_project = list(CreatePZ.dict_perforation_project.keys())
        print(f'работающие пласты {CreatePZ.plast_work}')

        if float(CreatePZ.column_diametr) < 110:
            CreatePZ.nkt_diam = 60
            print(f'диаметр НКТ {CreatePZ.nkt_diam}')
        # Определение работающих интервалов перфорации и заполнения в словарь

        if len(CreatePZ.plast_work) == 0:
            perf_true_quest = QMessageBox.question(self, 'Программа',
                                                   'Программа определили,что в скважине интервалов перфорации нет, верно ли?')
            if perf_true_quest == QMessageBox.StandardButton.Yes:
                for plast in CreatePZ.plast_all:
                    CreatePZ.dict_perforation[plast]['отключение'] = True
                    CreatePZ.dict_perforation[plast]['отрайбировано'] = False
                    CreatePZ.dict_perforation[plast]['Прошаблонировано'] = False

            else:
                plast_work = set()
                CreatePZ.current_bottom, ok = QInputDialog.getDouble(self, 'Необходимый забой',
                                                                     'Введите забой до которого нужно нормализовать')
                for plast, value in CreatePZ.dict_perforation.items():
                    for interval in value['интервал']:

                        perf_work_quest = QMessageBox.question(self, 'Добавление работающих интервалов перфорации',
                                                               f'Является ли данный интервал {CreatePZ.dict_perforation[plast]["интервал"]} работающим?')
                        if perf_work_quest == QMessageBox.StandardButton.No:
                            CreatePZ.dict_perforation[plast]['отключение'] = True
                        else:
                            plast_work.add(plast)
                            CreatePZ.dict_perforation[plast]['отключение'] = False

                CreatePZ.plast_work = list(plast_work)
                print(f'все интервалы {CreatePZ.plast_all}')
                print(f'раб интервалы {CreatePZ.plast_work}')
        try:
            for j in range(CreatePZ.data_x_min, CreatePZ.data_x_max):  # Ожидаемые показатели после ремонта
                lst = []
                for i in range(0, 12):
                    lst.append(ws.cell(row=j + 1, column=i + 1).value)
                CreatePZ.row_expected.append(lst)
        except:
            pass
        if '1' in CreatePZ.cat_P_1 or '1' in CreatePZ.cat_H2S_list or 1 in CreatePZ.cat_P_1 or 1 in CreatePZ.cat_H2S_list:
            CreatePZ.bvo = True
        print(f'БВО {CreatePZ.bvo}')
        print(CreatePZ.cat_P_1, CreatePZ.cat_H2S_list)

        plan.delete_rows_pz(self, ws)

        razdel_1 = block_name.razdel_1(self)

        for i in range(1, len(razdel_1)):  # Добавлением подписантов на вверху
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = razdel_1[i - 1][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
            ws.merge_cells(start_row=i, start_column=8, end_row=i, end_column=13)
        CreatePZ.ins_ind = 0

        # list_block = [cat_well_min,  CreatePZ.data_well_max]

        # head = plan.head_ind(cat_well_min, CreatePZ.data_well_max + 1)
        #
        # plan.copy._row(ws, ws2, CreatePZ.ins_ind, head)
        CreatePZ.ins_ind += CreatePZ.data_well_max - CreatePZ.cat_well_min[0] + 19
        # print(f' индекс вставки ГНВП{CreatePZ.ins_ind}')
        dict_events_gnvp = {}
        dict_events_gnvp['krs'] = events_gnvp()
        dict_events_gnvp['gnkt_opz'] = events_gnvp_gnkt()

        for i in range(CreatePZ.ins_ind, CreatePZ.ins_ind + len(dict_events_gnvp[work_plan]) - 1):
            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)

            if i == (CreatePZ.ins_ind + 13 or i == CreatePZ.ins_ind + 28) and work_plan == 'krs':

                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                               vertical='center')
                ws.cell(row=i, column=2).font = Font(name='Arial', size=13, bold=True)
                ws.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]
            elif i == CreatePZ.ins_ind + 11 and work_plan == 'gnkt_opz':
                # print(work_plan)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                               vertical='center')
                ws.cell(row=i, column=2).font = Font(name='Arial', size=11, bold=True)
                ws.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]
            else:
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                               vertical='top')
                ws.cell(row=i, column=2).font = Font(name='Arial', size=12)

                ws.cell(row=i, column=2).value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]
        ins_gnvp = CreatePZ.ins_ind
        CreatePZ.ins_ind += len(dict_events_gnvp[work_plan]) - 1

        ws.row_dimensions[2].height = 30
        ws.row_dimensions[6].height = 30

        # data_main_production_string = ws.cell(row=int(ind_data_main_production_string[1:])+1, column=int(ind_data_main_production_string[0])+2).value
        CreatePZ.insert_gnvp(ws, work_plan, ins_gnvp)

        # print(CreatePZ.row_expected)
        if len(CreatePZ.row_expected) != 0:
            for i in range(1, len(CreatePZ.row_expected) + 1):  # Добавление  показатели после ремонта
                ws.row_dimensions[CreatePZ.ins_ind + i - 1].height = None
                for j in range(1, 12):
                    if i == 1:
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).alignment = Alignment(wrap_text=False,
                                                                                          horizontal='center',
                                                                                          vertical='center')
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).value = CreatePZ.row_expected[i - 1][j - 1]
                    else:
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).font = Font(name='Arial', size=13, bold=True)
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).alignment = Alignment(wrap_text=False,
                                                                                          horizontal='left',
                                                                                          vertical='center')
                        ws.cell(row=i + CreatePZ.ins_ind, column=j).value = CreatePZ.row_expected[i - 1][j - 1]
            ws.merge_cells(start_column=2, start_row=CreatePZ.ins_ind + 1, end_column=12, end_row=CreatePZ.ins_ind + 1)
            CreatePZ.ins_ind += len(CreatePZ.row_expected)

        self.ins_ind_border = CreatePZ.ins_ind
        # wb.save(f"{CreatePZ.well_number}  1 {CreatePZ.well_area} {CreatePZ.cat_P_1}.xlsx")

        self.ws = ws
        self.wb = wb

        # wb.save(f'{CreatePZ.well_number} {CreatePZ.well_area} {work_plan}.xlsx')
        return self.ws

    def addItog(self, ws, ins_ind):
        print(ins_ind, self.table_widget.rowCount() - ins_ind + 1)
        ws.delete_rows(ins_ind, self.table_widget.rowCount() - ins_ind + 1)
        for i in range(ins_ind, len(itog_1(self)) + ins_ind):  # Добавлением итогов
            if i < ins_ind + 6:
                for j in range(1, 13):
                    ws.cell(row=i, column=j).value = itog_1(self)[i - ins_ind][j - 1]
                    if j != 1:
                        ws.cell(row=i, column=j).border = CreatePZ.thin_border
                        ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=11)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                               vertical='center')
            else:
                for j in range(1, 13):
                    ws.row_dimensions[i].height = 50

                    ws.cell(row=i, column=j).value = itog_1(self)[i - ins_ind][j - 1]
                    ws.cell(row=i, column=j).border = CreatePZ.thin_border
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                    ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                   vertical='center')

                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                ws.cell(row=i + ins_ind, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                         vertical='center')

        ins_ind += len(itog_1(self)) + 2

        curator_sel = block_name.curator_sel(self, CreatePZ.curator, CreatePZ.region)
        curator_ved_sel = block_name.curator_sel(self, CreatePZ.curator, CreatePZ.region)
        podp_down = block_name.pop_down(self, CreatePZ.region, curator_sel)
        for i in range(1 + ins_ind, 1 + ins_ind + len(podp_down)):  # Добавлением подписантов внизу
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = podp_down[i - 1 - ins_ind][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            if i in [1 + ins_ind + 7, 1 + ins_ind + 8, 1 + ins_ind + 9,
                     1 + ins_ind + 10, 1 + ins_ind + 11,
                     1 + ins_ind + 12, 1 + ins_ind + 13, 1 + ins_ind + 14]:
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=6)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, vertical='bottom', horizontal='left')
                ws.row_dimensions[i - 1].height = 30

                if i == 1 + ins_ind + 11:
                    ws.row_dimensions[i].height = 55
        ins_ind += len(podp_down)

    def insert_gnvp(ws, work_plan, ins_gnvp):
        rowHeights_gnvp = [30, 115.0, 155.5, 110.25, 36.0, 52.25, 36.25, 36.0, 45.25, 36.25, 165.75, 38.5, 30.25,
                           30.5,
                           18.0, 36, 281.75, 115.75, 65.0, 55.75, 33.0, 33.0, 30.25, 47.0, 57.25, 45.75, 33.75, 33.75,
                           350.25,
                           31.0, 51.75, 51.25, 87.25]
        rowHeights_gnvp_opz = [30, 95.0, 145.5, 25, 25.0, 52.25, 25.25, 20.0, 140.25, 36.25, 36.75, 20.5, 20.25, 20.5,
                               110.0, 60.5, 46.75, 36.75, 36.0, 36.75, 48.0, 36.0, 38.25]
        dict_rowHeights = {}
        dict_rowHeights['krs'] = rowHeights_gnvp
        dict_rowHeights['gnkt_opz'] = rowHeights_gnvp_opz
        # CreatePZ.rowHeights = CreatePZ.rowHeights + dict_rowHeights[work_plan]

        colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]
        # print(f' f {len(dict_rowHeights[work_plan])}')
        # print(f' индекс вставки высоты {ins_gnvp-2}')
        for index_row, row in enumerate(ws.iter_rows()):  # Копирование высоты строки
            if index_row + ins_gnvp <= len(dict_rowHeights[work_plan]) + ins_gnvp:
                ws.row_dimensions[index_row + ins_gnvp - 2].height = dict_rowHeights[work_plan][index_row - 1]
            for col_ind, col in enumerate(row):
                if col_ind <= 12:
                    ws.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind]
                else:
                    break

    def is_valid_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def if_None(value):
        if isinstance(value, datetime):
            return value
        elif value is None or 'отс' in str(value).lower() or value == '-' or value == 0:
            return 'отсут'
        else:
            return value

    def without_b(a):
        if isinstance(a, int) == True or isinstance(a, float) == True:
            return a
        elif a == '-' or a == 'отсутствует' or a == 'отсутв' or a == 'отсут' or a is None:
            return '0'

        elif len(a.split('/')) == 2:

            lst = []
            for i in a.split('/'):
                b = ''
                for j in i:
                    if j in '0123456789.x':
                        b = str(b) + j
                    elif j == ',':
                        b = str(b) + '.'

                lst.append(float(b))

            return lst
        elif len(a.split('-')) == 2:
            lst = []
            for i in a.split('-'):
                # print(i)
                lst.append(float(i.replace(',', '.').strip()))
            return lst[0]
        else:
            b = 0
            for i in a:
                i.replace(',', '.')
                if i in '0123456789,.x':
                    b = str(b) + i
                # print(b)

            return float(b)

    def definition_plast_work(self):
        # Определение работающих пластов
        plast_work = set()
        CreatePZ.perforation_roof = CreatePZ.current_bottom
        CreatePZ.perforation_roof_all = CreatePZ.current_bottom

        for plast, value in CreatePZ.dict_perforation.items():
            for interval in value['интервал']:
                print(f' интервалы ПВР {plast, interval[0], CreatePZ.dict_perforation[plast]["отключение"]}')
                print(CreatePZ.perforation_roof >= interval[0])
                if CreatePZ.current_bottom >= interval[0] and CreatePZ.dict_perforation[plast]["отключение"] == False:
                    plast_work.add(plast)

                if CreatePZ.dict_perforation[plast]['отключение'] == False:
                    if CreatePZ.perforation_roof >= interval[0]:
                        CreatePZ.perforation_roof = interval[0]
                        CreatePZ.dict_perforation[plast]["кровля"] = CreatePZ.perforation_roof
                    if CreatePZ.perforation_sole <= interval[1]:
                        CreatePZ.perforation_sole = interval[1]
                        CreatePZ.dict_perforation[plast]["подошва"] = CreatePZ.perforation_sole
                    if CreatePZ.perforation_roof_all >= interval[0]:
                        CreatePZ.perforation_roof_all = interval[0]
        print(CreatePZ.dict_perforation)
        CreatePZ.plast_all = list(CreatePZ.dict_perforation.keys())
        CreatePZ.plast_work = list(plast_work)
        print(f' раб {CreatePZ.plast_work}')
        # print(f' работ {CreatePZ.plast_work}')
        # print(f' все пласты {CreatePZ.plast_all}')

    def pause_app(self):
        while CreatePZ.pause == True:
            QtCore.QCoreApplication.instance().processEvents()

    def count_row_height(ws, ws2, work_list, merged_cells_dict, ind_ins):
        from openpyxl.utils.cell import range_boundaries, get_column_letter
        boundaries_dict = {}

        text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 90: (301, 400), 110: (401, 500),
                           130: (501, 600), 150: (601, 700), 170: (701, 800), 190: (801, 900), 210: (901, 1500)}
        for ind, _range in enumerate(ws.merged_cells.ranges):
            boundaries_dict[ind] = range_boundaries(str(_range))

        rowHeights1 = [ws.row_dimensions[i].height for i in range(ws.max_row)]
        colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]
        for i, row_data in enumerate(work_list):

            for column, data in enumerate(row_data):
                if column == 2:
                    if not data is None:
                        text = data
                        for key, value in text_width_dict.items():
                            if value[0] <= len(text) <= value[1]:
                                ws2.row_dimensions[i + 1].height = int(key)

        for i in range(1, len(work_list) + 1):  # Добавлением работ
            for j in range(1, 13):
                # print(ws2.cell(row=i, column=j).value)
                cell = ws2.cell(row=i, column=j)

                if cell and str(cell) != str(work_list[i - 1][j - 1]):
                    # print(work_list[i - 1][j - 1])
                    cell.value = work_list[i - 1][j - 1]
                    if i >= ind_ins:

                        if j != 1:
                            cell.border = CreatePZ.thin_border
                        if j == 11:
                            cell.font = Font(name='Arial', size=11, bold=False)
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
                                or 'порядок работы' in str(cell.value).lower() \
                                or 'ВСЕ ТЕХНОЛОГИЧЕСКИЕ ОПЕРАЦИИ' in str(cell.value).upper() \
                                or 'за 48 часов до спуска' in str(cell.value).upper():
                            print('есть жирный')
                            ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
        for row, col in merged_cells_dict.items():
            if len(col) != 2:
                # print(row)
                ws2.merge_cells(start_row=row + 1, start_column=3, end_row=row + 1, end_column=10)
        for key, value in boundaries_dict.items():
            # print(value)
            ws2.merge_cells(start_column=value[0], start_row=value[1],
                            end_column=value[2], end_row=value[3])

        head = plan.head_ind(0, ind_ins)
        plan.copy_true_ws(ws, ws2, head)

        # print(f'высота строк работ {ins_ind}')
        print(f'высота строк работ {len(rowHeights1)}')
        for index_row, row in enumerate(ws2.iter_rows()):  # Копирование высоты строки
            try:
                if index_row < ind_ins:
                    ws2.row_dimensions[index_row].height = rowHeights1[index_row]
            except:
                pass
            if index_row == 2:
                for col_ind, col in enumerate(row):
                    if col_ind <= 12:
                        ws2.column_dimensions[get_column_letter(col_ind + 1)].width = colWidth[col_ind]
        ws2.column_dimensions[get_column_letter(11)].width = 20
        ws2.column_dimensions[get_column_letter(12)].width = 20
        ws2.column_dimensions[get_column_letter(6)].width = 25

        # Копирование изображения
        for image in CreatePZ.image_list:
            ws2.add_image(image)
        return 'Высота изменена'

        # ws2.unmerge_cells(start_column=2, start_row=self.ins_ind, end_column=12, end_row=self.ins_ind)
