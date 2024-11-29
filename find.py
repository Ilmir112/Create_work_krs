import re
from io import BytesIO

import data_list
import base64
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from openpyxl.reader.excel import load_workbook
from openpyxl.utils import column_index_from_string
from openpyxl.workbook import Workbook
from openpyxl.utils.cell import get_column_letter
from openpyxl_image_loader import SheetImageLoader

from main import ExcelWorker, MyMainWindow, MyWindow

from plan import delete_rows_pz

from data_list import ProtectedIsDigit, ProtectedIsNonNone


class FindIndexPZ(MyMainWindow):
    wb_pvr = Workbook()

    def __init__(self, ws, work_plan, parent=None):
        super().__init__()

        self.perforation_sole = 5000
        self.number_dp = 0
        self.fluid_work = None
        self.nkt_template = None
        self.nkt_diam = None
        self.perforation_roof = 5000
        self.old_version = False
        self.region = None
        self.fluid = ''
        self.curator = None
        self.data_well_max = ProtectedIsDigit(0)
        self.plan_correct_index = ProtectedIsDigit(0)
        self.condition_of_wells = ProtectedIsDigit(0)
        self.plan_correct_index = ProtectedIsDigit(0)
        self.type_absorbent = ''
        self.sucker_rod_none = False
        self.fluid_work_short = '0.87г/см3'

        self.ws = ws
        self.wb = parent.wb

        self.category_h2s = 0
        self.category_gas_factor = 0

        self.thread_excel = None

        self.without_damping = False
        self.insert_index = 0
        self.bottom = 5000
        self.work_plan = work_plan
        self.row_expected = []
        self.column_direction_true = False
        self.category_h2s_list = []
        self.value_h2s_mg = []
        self.category_gaz_factor_percent = []
        self.gaz_factor_percent = []
        self.bur_rastvor = ''
        self.bottom_hole_drill = ProtectedIsNonNone('не корректно')
        self.bottom_hole_artificial = ProtectedIsNonNone(5000)
        self.max_angle = ProtectedIsNonNone('не корректно')
        self.well_number = ProtectedIsNonNone('не корректно')
        self.well_area = ProtectedIsNonNone('не корректно')
        self.max_angle_depth = ProtectedIsNonNone('не корректно')
        self.stol_rotor = ProtectedIsNonNone('не корректно')
        self.column_conductor_diameter = ProtectedIsNonNone('не корректно')
        self.column_conductor_wall_thickness = ProtectedIsNonNone('не корректно')
        self.column_conductor_length = ProtectedIsNonNone('не корректно')
        self.level_cement_direction = ProtectedIsNonNone('не корректно')
        self.column_direction_diameter = ProtectedIsNonNone('отсут')
        self.column_direction_wall_thickness = ProtectedIsNonNone('отсут')
        self.column_direction_length = ProtectedIsNonNone('отсут')
        self.level_cement_conductor = ProtectedIsNonNone('отсут')
        self.column_diameter = ProtectedIsNonNone('не корректно')
        self.column_wall_thickness = ProtectedIsNonNone('не корректно')
        self.shoe_column = ProtectedIsNonNone('не корректно')
        self.level_cement_column = ProtectedIsNonNone('не корректно')
        self.pressure_mkp = ProtectedIsNonNone('0')
        self.column_additional_diameter = ProtectedIsNonNone('не корректно')
        self.column_additional_wall_thickness = ProtectedIsNonNone('не корректно')
        self.head_column_additional = ProtectedIsNonNone('не корректно')
        self.shoe_column_additional = ProtectedIsNonNone('не корректно')
        self.interval_temp = ProtectedIsNonNone('не корректно')
        self.dict_sucker_rod = {}
        self.dict_sucker_rod_after = {}
        self.leakiness_count = 0
        self.emergency_count = 0

        self.date_drilling_cancel = ''
        self.date_drilling_run = ''
        self.date_commissioning = ''
        self.max_expected_pressure = ProtectedIsNonNone('не корректно')
        self.max_admissible_pressure = ProtectedIsNonNone('не корректно')
        self.result_pressure = ProtectedIsNonNone('не корректно')
        self.first_pressure = ProtectedIsNonNone('не корректно')
        self.static_level = ProtectedIsNonNone('не корректно')
        self.dinamic_level = ProtectedIsNonNone('не корректно')
        self.well_volume_in_pz = []
        self.pressure_mkp = ProtectedIsNonNone('не корректно')

        self.column_direction_true = False
        self.column_additional = False
        self.data_window = None
        self.perforation_correct_window2 = None
        self.for_paker_list = False
        self.grp_plan = False
        self.angle_data = []
        self.Qoil = 0
        self.Qwater = 0
        self.expected_pressure = 0
        self.appointment = ProtectedIsNonNone('')
        self.expected_Q = 0
        self.sucker_rod_ind = ProtectedIsDigit(0)
        self.percent_water = 0
        self.expected_pick_up = {}
        self.ribbing_interval = []
        self.drilling_interval = []
        self.nkt_opress_true = False
        self.stabilizator_need = False
        self.norm_of_time = 0
        self.leakiness = False
        self.pipes_ind = ProtectedIsDigit(0)
        self.data_x_min = ProtectedIsDigit(0)
        self.data_x_max = ProtectedIsDigit(0)
        self.data_pvr_min = ProtectedIsDigit(0)
        self.data_fond_min = ProtectedIsDigit(0)
        self.data_pvr_min = ProtectedIsDigit(0)
        self.pipes_ind = ProtectedIsDigit(0)
        self.data_pvr_max = ProtectedIsDigit(0)
        self.well_area = ProtectedIsNonNone("")
        self.well_oilfield = ProtectedIsNonNone("")
        self.inventory_number = ProtectedIsNonNone("")
        self.cdng = ProtectedIsNonNone("")
        self.paker_before = {"do": 0, "posle": 0}
        self.depth_fond_paker_before = {"do": 0, "posle": 0}
        self.paker_second_before = {"do": 0, "posle": 0}
        self.depth_fond_paker_second_before = {"do": 0, "posle": 0}
        self.dict_pump_shgn = {"do": 0, "posle": 0}
        self.dict_pump_ecn = {"do": 0, "posle": 0}
        self.dict_pump_shgn_depth = {"do": 0, "posle": 0}
        self.dict_pump_ecn_depth = {"do": 0, "posle": 0}
        self.dict_sucker_rod = {}
        self.gis_list = []
        self.pvr_row_list = []
        self.dict_nkt_before = {}
        self.dict_nkt_after = {}
        self.dict_sucker_rod_after = {}
        self.dict_pump = {"do": 0, "posle": 0}
        self.column_head_m = ''
        self.wellhead_fittings = ''
        self.groove_diameter = ''
        self.image_list = []
        self.image_data = []
        self.dict_leakiness = {}
        self.data_list = []
        self.open_trunk_well = False
        self.count_template = 0
        self.template_depth = 0
        self.leakiness_interval = []
        self.category_pressure_second = ''
        self.category_h2s_second = ''
        self.category_pressure_well = []
        self.gaz_factor_pr_second = ''
        self.current_bottom_second = 0
        self.current_bottom = 5000
        self.template_length = 0
        self.template_depth_addition = 0
        self.template_length_addition = 0

        self.type_kr = ''
        self.konte_true = False
        self.bvo = False
        self.category_pvo = 2

        self.problem_with_ek = False
        self.problem_with_ek_diameter = 220
        self.problem_with_ek_depth = 10000
        self.dict_perforation = {}
        self.dict_perforation_short = {}
        self.dict_perforation_project = {}
        self.category_pressure_list = []
        self.category_pressure = None
        self.skm_interval = []
        self.leakiness = False
        self.check_data_in_pz = []
        self.emergency_well = False
        self.problem_with_ek = False
        self.gips_in_well = False
        self.index_row_pvr_list = []
        self.plast_all = []

        self.value_h2s_percent = []
        self.value_h2s_mg = []
        self.value_h2s_mg_m3 = []
        self.dict_category = {}
        self.check_data_in_pz = []
        self.plast_project = []
        self.plast_work = []
        self.category_p_p = []
        self.image_data = []
        self.check_data_in_pz = []

        self.gis_list = []
        self.index_row_pvr_list = []
        self.data_x_max = ProtectedIsDigit(0)
        self.cat_well_min = ProtectedIsDigit(0)
        self.cat_well_max = ProtectedIsDigit(0)
        self.data_well_min = ProtectedIsDigit(0)
        self.data_x_min = ProtectedIsDigit(0)
        self.data_fond_min = ProtectedIsDigit(0)
        self.data_pvr_min = ProtectedIsDigit(0)
        self.well_volume_in_pz = []

        self.read_pz()

    def read_pz(self):
        cat_well_min = []
        image_loader = None
        try:
            # Копирование изображения
            image_loader = SheetImageLoader(self.ws)

        except Exception as e:
            QMessageBox.warning(None, 'Ошибка', f'Ошибка в копировании изображений {e}')

        for row_ind, row in enumerate(self.ws.iter_rows(values_only=True, max_row=300, max_col=20)):
            self.ws.row_dimensions[row_ind].hidden = False
            if self.cat_well_min.get_value != 0:
                if self.data_x_max.get_value < row_ind and image_loader:
                    self.work_with_img(image_loader, row_ind)

            if 'Категория скважины' in row:
                cat_well_min.append(row_ind + 1)
                self.cat_well_min = ProtectedIsDigit(min(cat_well_min))  # индекс начала категории

            elif any(['план-заказ' in str(col).lower() or 'план работ' in str(col).lower() for col in row]) \
                    and row_ind < 50:
                self.cat_well_max = ProtectedIsDigit(row_ind)
                self.data_well_min = ProtectedIsDigit(row_ind + 1)
            elif any(['стабилизатор' in str(col).lower() and 'желез' in str(col).lower() for col in row]):
                self.data_well.stabilizator_need = True

            elif any(['Ожидаемые показатели после' in str(col) for col in row]):
                self.data_x_min = ProtectedIsDigit(row_ind)
                # print(f' индекс Ожидаемые показатели {self.data_x_min}')
            elif '11. Эксплуатационные горизонты и интервалы перфорации:' in row:
                self.data_pvr_min = ProtectedIsDigit(row_ind)
            elif 'Оборудование скважины ' in row:
                self.data_fond_min = ProtectedIsDigit(row_ind)

            elif any(['VIII. Вид и категория ремонта, его шифр' in str(col) for col in row]):
                type_kr = self.ws.cell(row=row_ind + 2, column=1).value
                n = 1
                while type_kr is None and n != 8:
                    type_kr = self.ws.cell(row=row_ind + 2, column=1 + n).value
                    n += 1
                self.type_kr = type_kr

            elif any(['IX. Мероприятия по предотвращению' in str(col) for col in row]) or \
                    any(['IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in str(col) for col in
                         row]):

                self.data_well_max = ProtectedIsDigit(row_ind)

            elif 'НКТ' == str(row[1]).upper():
                self.pipes_ind = ProtectedIsDigit(row_ind + 1)

            elif 'ШТАНГИ' == str(row[1]).upper():
                self.sucker_rod_ind = ProtectedIsDigit(row_ind + 1)

            elif ('ХI Планируемый объём работ:' in row or
                  'ХI. Планируемый объём работ:' in row or 'ХIII Планируемый объём работ:' in row
                  or 'ХI Планируемый объём работ:' in row or 'Порядок работы' in row) \
                    and self.data_x_max.get_value == 0:
                self.data_x_max = ProtectedIsDigit(row_ind)
                break

            elif any(['II. История эксплуатации скважины' in str(col) for col in row]):
                self.data_pvr_max = ProtectedIsDigit(row_ind)

            elif 'III. Состояние скважины к началу ремонта ' in row:
                self.condition_of_wells = ProtectedIsDigit(row_ind)
            elif 'Герметизация , разгерметизация  устья  скважины' in row:
                self.plan_correct_index = ProtectedIsDigit(row_ind)

            for col, value in enumerate(row):
                if value is not None and col <= 12:
                    if 'сужен' in str(value).lower() or 'не проход' in str(value).lower() or \
                            'дорн' in str(value).lower() or 'пластырь' in str(value).lower():
                        self.problem_with_ek = True
                        self.problem_with_ek = True

                    if 'гипс' in str(value).lower() or 'гидратн' in str(value).lower():
                        self.gips_in_well = True

        if self.cat_well_max.get_value == 0:
            QMessageBox.warning(self, 'Ошибка', 'Не корректный файл excel, либо отсутствует строка с '
                                                'текстом ПЛАН-ЗАКАЗ или ПЛАН-РАБОТ')
            self.pause_app()
            return

        if self.cat_well_min.get_value == 0:
            QMessageBox.warning(self, 'индекс начала копирования',
                                'Программа не смогла определить строку начала копирования, нужно '
                                'добавить "Категория скважины" в ПЗ для определения начала копирования')
            self.pause_app()
            return
        if self.data_well_max.get_value == 0:
            QMessageBox.warning(self, 'индекс окончания копирования',
                                'Программа не смогла определить строку с IX. Мероприятия по предотвращению аварий '
                                'нужно добавить "IX. Мероприятия по предотвращению аварии" в ПЗ')
            self.pause_app()
            return
        if self.data_well_min.get_value == 0:
            QMessageBox.warning(self, 'индекс начала строки после план заказ',
                                'Программа не смогла найти начала строку с названием "План работ" или "план заказ"')
            self.pause_app()
            return

        if self.sucker_rod_none:
            if self.sucker_rod_ind.get_value == 0:
                sucker_mes = QMessageBox.question(self, 'ШТАНГИ', 'Программа определелила, что в скважине '
                                                                  'отсутствуют штанги, корректно ли это?')
                if sucker_mes == QMessageBox.StandardButton.Yes:
                    self.sucker_rod_ind = ProtectedIsDigit(0)
                else:
                    QMessageBox.information(self, 'ШТАНГИ', 'Нужно добавить "ШТАНГИ" в таблицу?')
                    self.pause_app()
                    return

        if self.data_x_max.get_value == 0:
            QMessageBox.warning(self, 'индекс окончания копирования ожидаемых показателей',
                                'Программа не смогла определить строку окончания копирования'
                                ' ожидаемых показателей "ХI Планируемый объём работ"')
            self.pause_app()
            return

        if self.data_x_min.get_value == 0:
            QMessageBox.warning(self, 'индекс начала копирования ожидаемых показателей',
                                'Программа не смогла определить строку начала копирования ожидаемых показателей')
            self.pause_app()
            return

        if self.data_pvr_max.get_value == 0:
            QMessageBox.warning(self, 'индекс историю',
                                'Программа не смогла найти "II. История эксплуатации скважины"')
            self.pause_app()
            return

        if self.pipes_ind.get_value == 0:
            QMessageBox.warning(self, 'индекс начала строки с НКТ',
                                'Программа не смогла найти строку с НКТ, необходимо проверить столбец В')
            self.pause_app()
            return
        if self.data_pvr_min.get_value == 0:
            QMessageBox.warning(self, 'индекс начала начала ПВР', 'Программа не смогла найти индекс начала ПВР')
            self.pause_app()
            return
        if self.data_fond_min.get_value == 0:
            QMessageBox.warning(self, 'индекс начала строки с таблицей фондовыго оборудования',
                                'Программа не смогла найти строку с таблицей фондового оборудования')
            self.pause_app()
            return
        if self.type_kr == '':
            QMessageBox.information(self, 'Вид ГТМ', 'Приложение не смогло найти тип КР, '
                                                     'необходимо внести вручную')
        if self.condition_of_wells.get_value == 0:
            QMessageBox.warning(
                self, 'индекс копирования',
                'Программа не смогла определить строку n\ III. Состояние скважины к началу ремонта ')
            self.pause_app()
            return
        if self.type_kr in ['', None]:
            self.check_data_in_pz.append('Не указан Вид и категория ремонта, его шифр\n')

        if self.work_plan != 'plan_change':
            self.row_expected = []
            for j in range(self.data_x_min.get_value,
                           self.data_x_max.get_value):  # Ожидаемые показатели после ремонта
                lst = []
                for i in range(0, 12):
                    lst.append(self.ws.cell(row=j + 1, column=i + 1).value)
                self.row_expected.append(lst)

    def work_with_img(self, image_loader, row):
        for col in range(1, 12):
            coord = f'{get_column_letter(col)}{row}'
            if image_loader.image_in(coord):
                # Загружаем изображение из текущей ячейки
                image_file = image_loader.get(coord)
                if image_file:
                    coord = f'{get_column_letter(col)}{row + 17 - self.cat_well_min.get_value}'

                    # Создаем байтовый поток
                    image_bytes = BytesIO()
                    # Сохраняем изображение в байтовом потоке
                    image_file.save(image_bytes, format='PNG')  # Замените 'PNG' на другой формат, если необходимо
                    image_bytes.seek(0)  # Возвращаемся в начало байтового потока
                    image_base64 = base64.b64encode(image_bytes.read()).decode("utf-8")

                    # Создание словаря для изображения
                    image_info = {
                        "coord": coord,
                        "width": image_file.width,
                        "height": image_file.height,
                        "data": image_base64
                    }

                    # Добавление информации в список
                    self.image_data.append(image_info)

    def check_str_none(self, string):

        try:
            if MyWindow.check_str_isdigit(str(string)) is True:
                if str(round(float(str(string).replace(',', '.')), 1))[-1] == "0":
                    return int(float(str(string).replace(',', '.')))
                else:
                    return round(float(str(string).replace(',', '.')), 4)
            elif str(string).replace(' ', '') == '-' or 'отсут' in str(string).lower() or \
                    str(string).strip() == '' or string is None:
                return '0'
            elif '(мм)' in string and '(м)' in string:
                return string
            elif len(str(string).split('/')) == 2:
                lst = []
                for i in str(string).split('/'):
                    b = ''
                    for j in i:
                        if j in '0123456789.x':
                            b = str(b) + j
                        elif j == ',':
                            b = str(b) + '.'
                    lst.append(float(b))
                return lst
            elif len(str(string).split('-')) == 2:
                lst = []
                for i in str(string).split('-'):
                    # print(i)
                    lst.append(float(i.replace(',', '.').strip()))
                return lst

            else:
                b = 0
                for i in str(string.strip()):
                    i.replace(',', '.')
                    if i in '0123456789,.x':
                        b = str(b) + i
                b = float(b)
                return b
        except Exception as e:
            QMessageBox.warning(self, 'Ошибка',
                                f'Ошибка в прочтении файла в строке {string} {e}, Проверьте excel файл')

    def definition_is_none(self, data, row, col, step, m=12):
        if data.__class__ == ProtectedIsNonNone:
            data = data.get_value
            while (data is None) and (step < m):
                data = self.ws.cell(row=row, column=col + step).value
                step += 1
            return ProtectedIsNonNone(data)
        elif data.__class__ == ProtectedIsDigit:
            data = data.get_value
            while (data is None) and (step < m):
                data = self.ws.cell(row=row, column=col + step).value
                step += 1
            return ProtectedIsDigit(data)
        else:
            while (data is None) and (step < m):
                data = self.ws.cell(row=row, column=col + step).value
                step += 1
            return data


class WellNkt(FindIndexPZ):
    def __init__(self):
        super().__init__()
        # self.read_well(self.ws, data_list.pipes_ind.get_value, data_list.condition_of_wells.get_value)

    def read_well(self, begin_index, cancel_index):
        dict_nkt = {}
        dict_nkt_po = {}

        a_plan = 0
        data_list.nkt_mistake = False
        for row in range(begin_index, cancel_index):  # словарь количества НКТ и метраж
            if 'план' in str(self.ws.cell(row=row, column=3).value).lower() or str(
                    self.ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                a_plan = row
        if a_plan == 0:
            QMessageBox.warning(self, 'Индекс планового НКТ',
                                'Программа не могла определить начала строку с ПЗ НКТ - план')
            self.pause_app()
            return

        for row in range(begin_index, cancel_index + 1):
            # print(str(self.ws.cell(row=row, column=4).value))
            key = str(self.ws.cell(row=row, column=4).value)
            if key != str(None) and key != '-' and "Диам" not in key:
                value = self.ws.cell(row=row, column=7).value
                if value:
                    if key is not None and row < a_plan:
                        dict_nkt[key] = dict_nkt.get(
                            key, 0) + round(self.check_str_none(value), 1)
                    elif key is not None and row >= a_plan:
                        dict_nkt_po[key] = dict_nkt_po.get(
                            key, 0) + round(self.check_str_none(value), 1)
                # print(f'индекс a_plan {dict_nkt}')
            # data_list.shoe_nkt = float(sum(dict_nkt.values()))
        # except Exception:
        #     data_list.nkt_mistake = True
        #     QMessageBox.warning(self, 'Ошибка', 'Программа не смогла определить диаметры и длину НКТ')
        self.dict_nkt_before = dict_nkt
        self.dict_nkt_after = dict_nkt_po


class WellSuckerRod(FindIndexPZ):
    def __init__(self):
        super().__init__()

    # self.read_well(self.ws, data_list.sucker_rod_ind.get_value, data_list.pipes_ind.get_value)

    def read_well(self, begin_index, cancel_index):
        self.dict_sucker_rod = {}
        self.dict_sucker_rod_after = {}

        # try:
        dict_sucker_rod = {}
        dict_sucker_rod_po = {}

        b_plan = 0
        if self.sucker_rod_ind.get_value != 0:
            for row in range(begin_index, cancel_index):  # словарь количества штанг и метраж
                if 'план' in str(self.ws.cell(row=row, column=3).value) or str(
                        self.ws.cell(row=row, column=3).value).lower() == 'план' \
                        or str(self.ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                    b_plan = row

            if b_plan == 0 and self.sucker_rod_none is True:
                sucker_rod_question = QMessageBox.question(self,
                                                           'отсутствие штанг',
                                                           'Программа определило что штанг в '
                                                           'скважине нет, корректно?')
                if sucker_rod_question == QMessageBox.StandardButton.Yes:
                    self.sucker_rod_none = False
                else:
                    self.sucker_rod_none = True

                if self.sucker_rod_none is True:
                    sucker_rod_question = QMessageBox.warning(self, 'Индекс планового НКТ',
                                                              'Программа не могла определить начала строку с ПЗ'
                                                              ' штанги - план')
                    self.pause_app()
                    return
            # print(f'б {b_plan}')

            for row in range(begin_index, cancel_index - 1):

                key = str(self.ws.cell(row=row, column=4).value).replace(' ', '')
                value = self.ws.cell(row=row, column=7).value
                if key != str(None) and key != '-' and key != '' and 'отсут' not in str(key).lower():
                    # print(key, value)
                    if key is not None and row < b_plan:
                        try:
                            dict_sucker_rod[key] = dict_sucker_rod.get(key, 0) + int(
                                float(str(value).replace(',', '.'))) + 1
                        except Exception:
                            QMessageBox.warning(self, 'Ошибка', 'Ошибка в определении длины штанг до ремонта, '
                                                                'скорректируйте план заказ')
                            self.pause_app()
                            break

                            return
                    if key is not None and row >= b_plan:
                        try:
                            dict_sucker_rod_po[key] = dict_sucker_rod_po.get(key, 0) + int(
                                float(str(value).replace(',', '.')))
                        except Exception:
                            QMessageBox.warning(self, 'Ошибка', 'Ошибка в определении длины штанг до ремонта, '
                                                                'скорректируйте план заказ')
                            self.pause_app()
                            break

                            return
        self.dict_sucker_rod = dict_sucker_rod
        self.dict_sucker_rod_after = dict_sucker_rod_po


class WellFondData(FindIndexPZ):

    def __init__(self):
        super().__init__()
        # self.read_well(self.ws, data_list.data_fond_min.get_value, data_list.condition_of_wells.get_value)

    def read_well(self, begin_index, cancel_index):

        paker_do = {"do": 0, "posle": 0}
        depth_fond_paker_do = {"do": 0, "posle": 0}
        paker2_do = {"do": 0, "posle": 0}
        depth_fond_paker2_do = {"do": 0, "posle": 0}
        dict_pump_shgn = {"do": '0', "posle": '0'}
        dict_pump_ecn = {"do": '0', "posle": '0'}
        dict_pump_shgn_h = {"do": '0', "posle": '0'}
        dict_pump_ecn_h = {"do": '0', "posle": '0'}
        dict_pump = {"do": '0', "posle": '0'}
        data_list.old_index = 1
        wellhead_fittings = ''
        column_head_m = ''
        groove_diameter = ''
        for row_index, row in enumerate(self.ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            for col, cell in enumerate(row):
                value = cell.value
                if value:
                    if 'карта спуска' in str(value).lower():
                        col_plan = col
                    if 'до ремонта' in str(value).lower() and row_index < 6 + begin_index:
                        col_do = col
                    if 'колонная головка' in str(value) and 'типоразмер' in str(row[col + 2].value):
                        column_head_m = row[col_do].value
                    if 'Арматура устьевая' in str(value) and 'типоразмер' in str(row[col + 2].value):
                        wellhead_fittings = row[col_do].value

                    if 'диаметр канавки' in str(value).lower():
                        groove_diameter = row[col_do].value
                        if groove_diameter is None:
                            groove_diameter = ''

                    if 'Пакер' in str(value) and 'типоразмер' in str(row[col + 2].value):
                        if '/' in str(row[col_do].value):
                            paker_do["do"] = str(row[col_do].value).split('/')[0]
                            paker2_do["do"] = str(row[col_do].value).split('/')[1]
                        else:
                            paker_do["do"] = row[col_do].value

                        if '/' in str(row[col_plan].value):
                            paker_do["posle"] = str(row[col_plan].value).split('/')[0]
                            paker2_do["posle"] = str(row[col_plan].value).split('/')[1]
                        else:
                            paker_do["posle"] = row[col_plan].value

                    elif value == 'Насос' and row[col + 2].value == 'типоразмер':
                        if row[col_do].value:
                            if ('ЭЦН' in str(row[col_do].value).upper() or 'ВНН' in str(row[col_do].value).upper()):
                                dict_pump_ecn["do"] = row[col_do].value
                                if '/' in str(row[col_do].value):
                                    dict_pump_ecn["do"] = [ecn for ecn in row[col_do].value.split('/')
                                                           if 'ЭЦН' in ecn or 'ВНН' in ecn][0]
                            elif ('НВ' in str(row[col_do].value).upper() or 'ШГН' in str(row[col_do].value).upper() or
                                  'НН' in str(row[col_do].value).upper()) or 'RH' in str(row[col_do].value).upper():
                                dict_pump_shgn["do"] = row[col_do].value
                                if '/' in str(row[col_do].value):
                                    dict_pump_shgn["do"] = [ecn for ecn in row[col_do].value.split('/')
                                                            if 'НВ' in ecn or 'НН' in ecn or
                                                            'ШГН' in ecn or 'RH' in ecn][0]

                                # print(dict_pump_ecn["do"])

                        if row[col_plan].value:
                            if ('ЭЦН' in str(row[col_plan].value).upper() or 'ВНН' in str(
                                    row[col_plan].value).upper()):
                                dict_pump_ecn["posle"] = row[col_plan].value
                                if '/' in str(row[col_plan].value):
                                    dict_pump_ecn["posle"] = [ecn for ecn in row[col_plan].value.split('/')
                                                              if 'ЭЦН' in ecn or 'ВНН' in ecn][0]

                            elif ('НВ' in str(row[col_plan].value).upper() or
                                  'ШГН' in str(row[col_plan].value).upper() or
                                  'НН' in str(row[col_plan].value).upper()) or \
                                    'RHAM' in str(row[col_plan].value).upper():
                                dict_pump_shgn["posle"] = row[col_plan].value
                                if '/' in str(row[col_plan].value):
                                    dict_pump_shgn["posle"] = [ecn for ecn in row[col_plan].value.split('/')
                                                               if 'НВ' in ecn or 'НН' in ecn or
                                                               'ШГН' in ecn or 'RHAM' in ecn][0]

                        if dict_pump_ecn["do"] != 0:
                            dict_pump_ecn_h["do"] = self.check_str_none(
                                self.ws.cell(row=row_index + 4,
                                             column=col_do + 1).value)
                            if '/' in str(self.ws.cell(row=row_index + 4, column=col_do + 1).value):
                                dict_pump_ecn_h["do"] = max(self.check_str_none(self.ws.cell(
                                    row=row_index + 4, column=col_do + 1).value))
                        if dict_pump_shgn["do"] != 0:

                            dict_pump_shgn_h["do"] = self.check_str_none(
                                self.ws.cell(row=row_index + 4,
                                             column=col_do + 1).value)
                            if '/' in str(self.ws.cell(row=row_index + 4, column=col_do + 1).value):
                                dict_pump_shgn_h["do"] = min(self.check_str_none(self.ws.cell(
                                    row=row_index + 4, column=col_do + 1).value))
                        if dict_pump_ecn["posle"] != 0:
                            dict_pump_ecn_h["posle"] = self.check_str_none(self.ws.cell(row=row_index + 4,
                                                                                        column=col_plan + 1).value)
                            if '/' in str(self.ws.cell(row=row_index + 4, column=col_plan + 1).value):
                                dict_pump_ecn_h["posle"] = max(
                                    self.check_str_none(self.ws.cell(row=row_index + 4,
                                                                     column=col_plan + 1).value))
                        if dict_pump_shgn["posle"] != 0:
                            dict_pump_shgn_h["posle"] = self.check_str_none(
                                self.ws.cell(row=row_index + 4,
                                             column=col_plan + 1).value)
                            if '/' in str(self.ws.cell(row=row_index + 4, column=col_plan + 1).value):
                                dict_pump_shgn_h["posle"] = min(
                                    self.check_str_none(self.ws.cell(row=row_index + 4,
                                                                     column=col_plan + 1).value))

                    elif value == 'Н посадки, м':
                        try:
                            if paker_do["do"] != 0:
                                depth_fond_paker_do["do"] = \
                                    self.check_str_none(row[col_do].value)[0]
                                depth_fond_paker2_do["do"] = \
                                    self.check_str_none(row[col_do].value)[1]
                        except Exception:
                            if paker_do["do"] != 0:
                                depth_fond_paker_do["do"] = row[col_do].value
                        try:
                            if paker_do["posle"] != 0:
                                depth_fond_paker_do["posle"] = \
                                    self.check_str_none(row[col_plan].value)[0]
                                depth_fond_paker2_do["posle"] = \
                                    self.check_str_none(row[col_plan].value)[1]
                        except Exception:
                            if paker_do["posle"] != 0:
                                depth_fond_paker_do["posle"] = row[col_plan].value

        if wellhead_fittings in [None, '']:
            self.check_data_in_pz.append('Не указан тип устьевой арматуры\n')
        if column_head_m in [None, '']:
            self.check_data_in_pz.append('Не указан тип Колонной головки или завод-изготовитель\n')
        if groove_diameter in [None, '']:
            self.check_data_in_pz.append(
                'Не указан Диаметр канавки устьевой арматуры или тип резьбы\n ')

        self.paker_before = paker_do
        self.depth_fond_paker_before = depth_fond_paker_do
        self.paker_second_before = paker2_do
        self.depth_fond_paker_second_before = depth_fond_paker2_do
        self.dict_pump_shgn = dict_pump_shgn
        self.dict_pump_ecn = dict_pump_ecn
        self.dict_pump_shgn_depth = dict_pump_shgn_h
        self.dict_pump_ecn_depth = dict_pump_ecn_h
        self.dict_pump = dict_pump
        self.column_head_m = column_head_m
        self.wellhead_fittings = wellhead_fittings
        self.groove_diameter = groove_diameter


class WellHistoryData(FindIndexPZ):

    def __init__(self):
        super().__init__()
        self.leakage_window = None

        # self.read_well(self.ws, data_list.data_pvr_max.get_value, data_list.data_fond_min.get_value)

    def read_well(self, begin_index, cancel_index):

        for row_index, row in enumerate(self.ws.iter_rows(min_row=begin_index, max_row=cancel_index, max_col=20)):
            for col, cell in enumerate(row):
                value = cell.value
                if value:
                    if 'нэк' in str(value).lower() or 'негерм' in str(
                            value).lower() or 'нарушение э' in str(
                        value).lower() or \
                            'нарушение г' in str(value).lower():
                        self.leakiness_count += 1

                    if ('авар' in str(
                            value).lower() or 'расхаж' in str(
                        value).lower() or 'лар' in str(value).lower()) \
                            and 'акт о расследовании аварии прилагается' not in str(value).lower():
                        self.emergency_well = True
                        self.emergency_well = True
                        self.emergency_count += 1
                        self.emergency_count += 1

                    if 'Начало бурения' in str(value):
                        # self.date_drilling_run = row[col + 2].value
                        self.date_drilling_run = row[col + 2].value

                    elif 'Конец бурения' == value:
                        self.date_drilling_cancel = row[col + 2].value
                        self.date_drilling_cancel = row[col + 2].value

                        self.date_drilling_cancel = \
                            self.definition_is_none(self.date_drilling_cancel,
                                                    row_index + begin_index, col + 1, 1)
                    elif 'Дата ввода в экспл' in str(value):
                        self.date_commissioning = row[col + 2].value
                        if type(self.date_commissioning) is datetime:
                            self.date_commissioning = self.date_commissioning.strftime(
                                '%d.%m.%Y')
                    elif 'ствол скважины' in str(row[col].value).lower() and 'буров' in str(row[col].value).lower():
                        self.bur_rastvor = row[col].value

                    elif 'Максимально ожидаемое давление на устье' == value:
                        self.max_expected_pressure = ProtectedIsDigit(row[col + 1].value)
                        self.max_expected_pressure = FindIndexPZ.definition_is_none(
                            self, self.max_expected_pressure, row_index + begin_index, col + 1, 1)
                    elif 'Результат предыдущей ' in str(value):
                        self.result_pressure = ProtectedIsDigit(row[col + 1].value)
                        self.result_pressure = self.definition_is_none(
                            self.result_pressure,
                            row_index + begin_index,
                            col + 1, 1)

                    elif 'Первоначальное давление опрессовки э/колонны' == value:
                        self.first_pressure = ProtectedIsDigit(row[col + 3].value)
                    elif 'максимально допустимое давление' in str(value).lower():
                        self.max_admissible_pressure = ProtectedIsDigit(row[col + 1].value)
                        self.max_admissible_pressure = \
                            self.definition_is_none(self.max_admissible_pressure, row_index + begin_index, col + 1, 1)
        if self.date_drilling_run == '':
            self.check_data_in_pz.append('не указано начало бурения\n')
        if self.date_drilling_cancel == '':
            self.check_data_in_pz.append('не указано окончание бурения\n')

        if self.date_commissioning == '':
            self.check_data_in_pz.append('не указано дата ввода\n')
        if self.max_expected_pressure == '':
            self.check_data_in_pz.append('не указано максимально ожидаемое давление на устье\n')
        if self.max_admissible_pressure == '':
            self.check_data_in_pz.append('не указано максимально допустимое давление на устье\n')


class WellCondition(FindIndexPZ):
    leakage_window = None

    def __init__(self):
        super().__init__()

        # self.read_well(self.ws, data_list.condition_of_wells.get_value, self.data_well.data_well_max.get_value)

    def read_well(self, begin_index, cancel_index):

        for row_index, row in enumerate(self.ws.iter_rows(min_row=begin_index, max_row=cancel_index, max_col=20)):
            row_index += begin_index
            for col, cell in enumerate(row):
                value = cell.value
                if value is not None:
                    if 'нэк' in str(value).lower() or 'негерм' in str(value).lower() or \
                            'нарушение э' in str(value).lower() or 'нарушение г' in str(value).lower():
                        self.leakiness_count += 1

                    if ('авар' in str(value).lower() or 'расхаж' in str(value).lower() or 'лар' in str(value)) \
                            and 'акт о расследовании аварии прилагается' not in str(value):
                        self.emergency_well = True
                        self.emergency_count += 1
                    if value:
                        if "Hст " in str(value):
                            if '/' in str(row[col + 1].value):
                                self.static_level = ProtectedIsDigit(row[col + 1].value.split('/')[0])
                            else:
                                self.static_level = ProtectedIsDigit(row[col + 1].value)
                        elif 'Рмкп ' in str(value):
                            self.pressure_mkp = ProtectedIsNonNone(row[col + 2].value)

                        elif "грп" in str(value).lower():
                            self.grp_plan = True

                        elif "Ндин " in str(value):
                            self.dinamic_level = ProtectedIsDigit(row[col + 1].value)
                        elif "% воды " in str(value):
                            self.percent_water = str(row[col + 1].value).strip().replace('%', '')
                            self.percent_water = FindIndexPZ.definition_is_none(
                                self, self.percent_water, row_index,
                                col + 1, 1)
                        elif 'Vжг' in str(value):
                            try:
                                well_volume_in_pz = str(row[col + 1].value).replace(',', '.')
                                # print(f'строка {well_volume_in_pz}')

                                self.well_volume_in_pz.append(round(float(well_volume_in_pz), 1))
                            except Exception:
                                well_volume_in_pz, _ = QInputDialog.getDouble(self, 'Объем глушения',
                                                                              'ВВедите объем глушения согласно ПЗ', 50,
                                                                              1, 70)
                                self.well_volume_in_pz.append(well_volume_in_pz)

        if self.static_level.get_value == 'не корректно':
            self.check_data_in_pz.append('не указано статический уровень')
        if self.pressure_mkp.get_value in [None, 'не корректно', '-', 'нет', 'отсут']:
            self.check_data_in_pz.append(
                'не указано наличие наличие устройство замера давления и наличие давления в МКП')

        if self.leakiness_count != 0:
            leakiness_quest = QMessageBox.question(self, 'нарушение колонны',
                                                   f'Программа определила что в скважине'
                                                   f' есть нарушение - {self.leakiness_count}, '
                                                   f'верно ли?')
            if leakiness_quest == QMessageBox.StandardButton.Yes:
                self.leakiness = True


class WellExpectedPickUp(FindIndexPZ):
    def __init__(self):
        super().__init__()
        # self.read_well(self.ws, self.data_well.data_x_min.get_value, self.data_well.data_x_max.get_value)

    def read_well(self, begin_index, cancel_index):

        for row_index, row in enumerate(self.ws.iter_rows(min_row=begin_index, max_row=cancel_index, max_col=20)):
            row_index += begin_index
            # print(row_index)
            for col, cell in enumerate(row[0:15]):
                # print(row_index)
                value = cell.value
                if value:

                    if 'прием' in str(value).lower() or 'qж' in str(value).lower():
                        self.expected_Q = row[col + 1].value

                        self.expected_Q = self.definition_is_none(self.expected_Q, row_index,
                                                                  col + 1, 1)

                    if 'зак' in str(value).lower() or 'давл' in str(value).lower() or 'p' in str(value).lower():
                        self.expected_pressure = row[col + 1].value
                        self.expected_pressure = self.definition_is_none(self.expected_pressure, row_index,
                                                                         col + 1, 1)

                    if 'qж' in str(value).lower():
                        self.Qwater = str(row[col + 1].value).strip().replace(' ', '').replace(
                            'м3/сут', '')
                        self.Qwater = self.definition_is_none(
                            self.Qwater,
                            row_index, col + 1, 1)

                    if 'qн' in str(value).lower():
                        self.Qoil = str(row[col + 1].value).replace(' ', '').replace('т/сут', '')
                        self.Qoil = self.definition_is_none(self.Qoil,
                                                            row_index, col + 1, 1)
                    if 'воды' in str(value).lower() and "%" in str(value).lower():
                        try:
                            proc_water = str(row[col + 1].value).replace(' ', '').replace('%', '')

                            proc_water = self.definition_is_none(proc_water, row_index, col + 1, 1)
                            self.percent_water = int(float(proc_water)) if float(
                                proc_water) > 1 else round(
                                float(proc_water) * 100,
                                0)
                        except Exception:
                            print(f'ошибка в определение')

            try:
                if self.expected_Q and self.expected_pressure:
                    self.expected_pick_up[self.expected_Q] = self.expected_pressure
            except Exception as e:
                print(f'Ошибка в определении ожидаемых показателей {e}')

        return self


class WellName(FindIndexPZ):
    def __init__(self):
        super().__init__(self, parent=None)
        # self.read_well(self.ws, self.cat_well_max.get_value, data_list.data_pvr_min.get_value)

    def read_well(self, begin_index, cancel_index):
        for row_index, row in enumerate(self.ws.iter_rows(min_row=begin_index, max_row=cancel_index, max_col=20)):
            row_index += begin_index

            for col, cell in enumerate(row):
                value = cell.value
                if value:
                    if 'площадь' in str(value):
                        self.well_number = ProtectedIsNonNone(str(row[col - 1].value))
                        self.well_area = ProtectedIsNonNone(str(row[col + 1].value).replace(" ", "_"))
                        # self.well_number = ProtectedIsNonNone(row[col - 1].value)
                        # self.well_area = ProtectedIsNonNone(row[col + 1].value)
                    elif 'месторождение ' in str(value):  # определение номера скважины
                        self.well_oilfield = ProtectedIsNonNone(row[col + 2].value)
                        # self.well_oilfield = ProtectedIsNonNone(row[col + 2].value)
                    elif 'Инв. №' in str(value):
                        self.inventory_number = ProtectedIsNonNone(row[col + 1].value)
                        # self.inventory_number = ProtectedIsNonNone(row[col + 1].value)
                    elif 'цех' == value:
                        self.cdng = ProtectedIsDigit(row[col + 1].value)
                        # self.cdng = ProtectedIsDigit(row[col + 1].value)
                    elif 'назначение' in str(value):
                        self.appointment = ProtectedIsNonNone(row[col + 2].value)
                        # well_data.appointment = ProtectedIsDigit(row[col + 1].value)
                        # print(f' ЦДНГ {self.cdng.get_value}')

        return self


class WellData(FindIndexPZ):

    def __init__(self):
        super().__init__()

        # self.read_well(self.ws, self.cat_well_max.get_value, data_list.data_pvr_min.get_value)

    def read_well(self, begin_index, cancel_index):
        for row_index, row in enumerate(self.ws.iter_rows(min_row=begin_index, max_row=cancel_index, max_col=20)):
            row_index += begin_index

            for col, cell in enumerate(row[:13]):
                value = cell.value
                if value:
                    if 'пробуренный забой' in str(value).lower():
                        self.bottom_hole_drill = ProtectedIsDigit(row[col + 2].value)
                        self.bottom_hole_drill = self.definition_is_none(
                            self.bottom_hole_drill,
                            row_index, col, 2)

                        self.bottom_hole_artificial = ProtectedIsDigit(row[col + 4].value)
                        # print(f'пробуренный забой {self.bottom_hole_artificial}')
                        self.bottom_hole_artificial = \
                            self.definition_is_none(self.bottom_hole_artificial,
                                                    row_index, col, 5)
                        # print(f'пробуренный забой {self.bottom_hole_artificial}')

                    elif 'интервалы темпа набора кривизны ' in str(value).lower():
                        self.interval_temp = ProtectedIsDigit(row[col + 2].value)
                        self.interval_temp = self.definition_is_none(
                            self.interval_temp, row_index, col + 2, 1)

                    elif 'зенитный угол' in str(value).lower():
                        self.max_angle = ProtectedIsDigit(row[col + 4].value)
                        for index, col1 in enumerate(row[:14]):
                            if 'на глубине' in str(col1.value):
                                self.max_angle_depth = ProtectedIsDigit(row[index + 1].value)
                            if index > 10:
                                break

                    elif 'текущий забой' in str(value).lower() and len(value) < 15:
                        self.current_bottom = row[col + 2].value
                        self.current_bottom = \
                            FindIndexPZ.definition_is_none(
                                self, self.current_bottom, row_index, col, 2)

                        self.bottom = self.current_bottom
                    elif '10. Расстояние от стола ротора до среза муфты э/колонны ' in str(value):
                        self.stol_rotor = FindIndexPZ.definition_is_none(
                            self, ProtectedIsDigit(row[col + 5].value), row_index, col + 1, 1)

                    elif 'Направление' in str(value) and 'Шахтное направление' not in str(value) and \
                            self.ws.cell(row=row_index + 1, column=col + 1).value is not None and \
                            self.check_str_none(row[col + 3].value) != '0':
                        self.column_direction_true = True
                        if self.column_direction_true:
                            cell = None
                            for col1, cell in enumerate(row):
                                if 'Уровень цемента' in str(cell.value):
                                    n = 1
                                    while row[col1 + n].value is None or n > 6:
                                        if 'уст' in str(row[col1 + 2].value).lower() or str(
                                                row[col1 + 2].value).isdigit():
                                            self.level_cement_direction = ProtectedIsDigit(0)
                                        else:
                                            if '-' in str(row[col1 + 2].value):
                                                self.level_cement_direction = ProtectedIsDigit(
                                                    str(row[col1 + 2].value.split('-')[0]).replace(" ", ""))
                                        n += 1
                        else:
                            self.level_cement_direction = ProtectedIsNonNone('отсут')
                        try:
                            column_direction_data = row[col + 3].value.split('(мм),')
                            try:
                                self.column_direction_diameter = ProtectedIsDigit(
                                    column_direction_data[0])
                            except Exception:
                                self.column_direction_diameter = ProtectedIsNonNone('не корректно')

                            try:
                                self.column_direction_wall_thickness = ProtectedIsDigit(
                                    column_direction_data[1].replace(' ', ''))
                            except Exception:
                                self.column_direction_wall_thickness = ProtectedIsNonNone(
                                    'не корректно')
                            try:
                                try:
                                    self.column_direction_length = ProtectedIsDigit(
                                        column_direction_data[2].split('-')[1].replace('(м)', '').replace(" ", ""))
                                except Exception:
                                    self.column_direction_length = ProtectedIsDigit(
                                        column_direction_data[2].replace('(м)', '').replace(" ", ""))

                            except Exception:
                                self.column_direction_length = ProtectedIsNonNone('не корректно')
                        except Exception:
                            self.column_direction_diameter = ProtectedIsNonNone('не корректно')
                            self.column_direction_wall_thickness = ProtectedIsNonNone('не корректно')
                            self.column_direction_length = ProtectedIsNonNone('не корректно')

                    elif 'Кондуктор' in str(value) and \
                            self.check_str_none(row[col + 3].value) != '0':
                        cell = None
                        for col1, cell in enumerate(row):
                            if 'Уровень цемента' in str(cell.value):
                                try:
                                    if 'уст' in str(row[col1 + 2].value).lower() or str(row[col1 + 2].value).isdigit():
                                        self.level_cement_conductor = ProtectedIsDigit(0)
                                    else:
                                        self.level_cement_conductor = ProtectedIsDigit(
                                            str(row[col1 + 2].value.split('-')[0]).replace(' ', ''))
                                except Exception:
                                    self.level_cement_conductor = ProtectedIsNonNone('не корректно')
                        try:
                            column_conductor_data = str(row[col + 3].value).split('(мм),')
                            try:
                                self.column_conductor_diameter = ProtectedIsDigit(
                                    column_conductor_data[0].strip())
                            except Exception:
                                self.column_conductor_diameter = ProtectedIsNonNone('не корректно')

                            try:
                                self.column_conductor_wall_thickness = \
                                    ProtectedIsDigit(column_conductor_data[1].strip())
                            except Exception:
                                self.column_conductor_wall_thickness = ProtectedIsNonNone(
                                    'не корректно')
                            try:
                                try:
                                    self.column_conductor_length = ProtectedIsDigit(
                                        column_conductor_data[2].split('-')[1].replace('(м)', '').strip())
                                except Exception:
                                    self.column_conductor_length = ProtectedIsDigit(
                                        str(column_conductor_data[2].replace('(м)', '')).strip())
                            except Exception:
                                self.column_conductor_length = ProtectedIsNonNone('не корректно')

                        except Exception:
                            self.column_conductor_diameter = ProtectedIsNonNone('не корректно')
                            self.column_conductor_wall_thickness = ProtectedIsNonNone('не корректно')
                            self.column_conductor_length = ProtectedIsNonNone('не корректно')
                    elif str(
                            value) == '4. Эксплуатационная колонна (диаметр(мм),' \
                                      ' толщина стенки(мм), глубина спуска(м))':

                        try:
                            data_main_production_string = str(
                                self.ws.cell(row=row_index + 1, column=col + 1).value).split(
                                '(мм),', )
                            try:
                                self.column_diameter = ProtectedIsDigit(
                                    float(str(data_main_production_string[0]).replace(',', '.')))
                            except Exception:
                                self.column_diameter = ProtectedIsNonNone('не корректно')
                            try:
                                self.column_wall_thickness = ProtectedIsDigit(
                                    float(str(data_main_production_string[1]).replace(',', '.')))
                            except Exception:
                                self.column_wall_thickness = ProtectedIsNonNone('не корректно')
                            try:
                                if len(data_main_production_string[-1].split('-')) == 2:

                                    self.shoe_column = ProtectedIsDigit(
                                        self.check_str_none(
                                            data_main_production_string[-1].strip().split('-')[
                                                -1]))

                                else:
                                    self.shoe_column = ProtectedIsDigit(
                                        self.check_str_none(data_main_production_string[-1]))
                            except Exception:
                                self.shoe_column = ProtectedIsNonNone('не корректно')
                        except ValueError:
                            self.column_diameter = ProtectedIsNonNone('не корректно')
                            self.column_wall_thickness = ProtectedIsNonNone('не корректно')
                            self.shoe_column = ProtectedIsNonNone('не корректно')

                    elif 'Уровень цемента за колонной' in str(value):
                        self.level_cement_column = ProtectedIsDigit(row[col + 3].value)
                        self.level_cement_column = self.definition_is_none(
                            self.level_cement_column, row_index, col, 1)

                    elif 'онструкция хвостовика' in str(value):

                        data_column_additional = self.check_str_none(self.ws.cell(row=row_index + 2,
                                                                                  column=col + 2).value)

                        if data_column_additional != '0':
                            self.column_additional = True
                        if self.column_additional is True:
                            try:
                                self.head_column_additional = ProtectedIsDigit(
                                    data_column_additional[0])
                            except Exception:
                                self.head_column_additional = ProtectedIsNonNone('не корректно')
                            try:
                                self.shoe_column_additional = ProtectedIsDigit(
                                    data_column_additional[1])
                            except Exception:
                                self.shoe_column_additional = ProtectedIsNonNone('не корректно')

                            try:
                                try:
                                    data_add_column = self.check_str_none(
                                        self.ws.cell(row=row_index + 2,
                                                     column=col + 4).value)
                                    # print(f' доп колонна {data_add_column}')
                                    self.column_additional_diameter = ProtectedIsDigit(
                                        data_add_column[0])

                                except Exception:
                                    self.column_additional_diameter = ProtectedIsDigit(
                                        self.check_str_none(
                                            self.ws.cell(row=row_index + 2,
                                                         column=col + 4).value))

                                try:
                                    data_add_column = self.check_str_none(
                                        self.ws.cell(row=row_index + 2,
                                                     column=col + 4).value)
                                    self.column_additional_wall_thickness = ProtectedIsDigit(
                                        data_add_column[1])
                                except Exception:

                                    self.column_additional_wall_thickness = ProtectedIsDigit(
                                        self.check_str_none(
                                            self.ws.cell(row=row_index + 2,
                                                         column=col + 6).value))

                            except Exception:
                                self.column_additional_wall_thickness = ProtectedIsNonNone(
                                    'не корректно')
                                self.column_additional_diameter = ProtectedIsNonNone('не корректно')
                        else:
                            self.column_additional_diameter = ProtectedIsNonNone('отсут')
                            self.column_additional_wall_thickness = ProtectedIsNonNone('отсут')
                            self.head_column_additional = ProtectedIsNonNone('отсут')
                            self.shoe_column_additional = ProtectedIsNonNone('отсут')

        if self.stol_rotor.get_value in ['не корректно', None, '']:
            self.check_data_in_pz.append('не указано Стол ротора \n')
        if self.max_angle.get_value in ['не корректно', None, '']:
            self.check_data_in_pz.append('не указано максимальный угол \n')
        if self.max_angle_depth.get_value in ['не корректно', None, '']:
            self.check_data_in_pz.append('не указано глубина максимального угла\n')
        if self.level_cement_column.get_value in ['не корректно', None, '']:
            self.check_data_in_pz.append('не указан уровень цемент за колонной\n')

        if self.max_angle.get_value > 45 or 'gnkt' in self.work_plan:
            angle_true_question = QMessageBox.question(self,
                                                       'Зенитный угол',
                                                       'Зенитный угол больше 45 градусов, '
                                                       'для корректной работы необходимо '
                                                       'загрузить данные инклинометрии. Загрузить?')
            if angle_true_question == QMessageBox.StandardButton.Yes:
                self.angle_data = WellData.read_angle_well()
                if self.angle_data is None:
                    self.pause_app()

        if type(self.column_diameter.get_value) in [float, int]:
            # if str(self.paker_before["do"]).lower() not in ['0', 0, '-', 'отсут', '', 'none', None]:
            #
            #     if '/' in str(self.depth_fond_paker_before["do"]):
            #         paker_diameter = TabPageSo.paker_diameter_select(
            #             self, str(self.depth_fond_paker_before["do"]).split('/')[0])
            #         if paker_diameter not in self.paker_before["do"]:
            #             self.check_data_in_pz.append(
            #                 f'Не корректно указан диаметр фондового пакера в карте спуска '
            #                 f'ремонта {str(self.paker_before["do"]).split("/")[0]} требуется пакер '
            #                 f'диаметром {paker_diameter}мм')
            #     else:
            #         if self.depth_fond_paker_before["do"] != 0:
            #             paker_diameter = TabPageSo.paker_diameter_select(self,
            #                                                              self.depth_fond_paker_before["do"])
            #             if str(paker_diameter) not in self.paker_before["do"]:
            #                 self.check_data_in_pz.append(
            #                     f'Не корректно указан диаметр фондового пакера в карте спуска '
            #                     f'ремонта {self.paker_before["do"]} требуется пакер '
            #                     f'диаметром {paker_diameter}мм')

            if self.dict_pump_ecn["do"] != '0' and self.dict_pump_shgn["do"] != '0':
                if self.paker_before["do"] in ['0', None, 0]:
                    self.check_data_in_pz.append(
                        f'В план заказе не указано посадка пакера при спущенной компоновке ОРД ')
            if self.dict_pump_ecn['posle'] != '0' and \
                    self.dict_pump_shgn['posle'] != '0':
                if self.paker_before["do"] in ['0', None, 0]:
                    self.check_data_in_pz.append(
                        f'В план заказе не указано посадка пакера при cпуске ОРД ')

        if str(self.well_number.get_value) in ['']:
            QMessageBox.warning(self, 'Канатные технологии', f'Скважина согласована на канатные технологии')
            self.konte_true = True

        if self.data_window is None:
            from data_correct import DataWindow
            self.data_window = DataWindow(self)
            self.data_window.setWindowTitle("Сверка данных")
            self.data_window.setGeometry(100, 100, 300, 400)

            self.data_window.show()
            self.pause_app()
            data_list.pause = True
            self.data_window = None

            if self.work_plan == 'krs':
                from data_base.config_base import connection_to_database
                from data_base.config_base import WorkDatabaseWell
                db = connection_to_database(data_list.DB_WELL_DATA)
                check_in_base = WorkDatabaseWell(db, self)
                tables_filter = check_in_base.get_tables_starting_with(self.well_number.get_value,
                                                                       self.well_area.get_value, 'ПР',
                                                                       self.type_kr.split(' ')[0])
                if tables_filter:
                    mes = QMessageBox.question(None, 'Наличие в базе',
                                               f'В базе имеется план работ по скважине:\n {" ".join(tables_filter)}. '
                                               f'При продолжении план пересохранится, продолжить?')
                    if mes == QMessageBox.StandardButton.No:
                        self.pause_app()
                        return

    @staticmethod
    def read_angle_well():
        fname = None
        while fname is None:
            fname, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Выберите файл', '.',
                                                             "Файлы Exсel (*.xlsx);;Файлы Exсel (*.xls)")
            # Загрузка файла Excel
            wb = load_workbook(fname)
            sheet_angle = wb.active
            angle_data = []
            depth_column = ''
            row_data = ''
            angle_column = ''
            curvature_column = ''
            for index_row, row in enumerate(sheet_angle.iter_rows(min_row=1, max_row=10, values_only=True)):
                for col, value in enumerate(row):
                    if value is not None:
                        if 'глубина' in str(value).lower() and col <= 7:
                            depth_column = col
                            row_data = index_row

                        elif ('Угол, гpад' in str(value) and col <= 7) or 'зенитный' in str(value).lower():
                            angle_column = col

                        elif 'кривизна' in str(value).lower() or 'гр./10' in str(value).lower():
                            curvature_column = col

            if depth_column == '' or row_data == '' or angle_column == '' or curvature_column == '':
                mes = QMessageBox.question(None, 'Ошибка', 'Файл не корректный, необходимо загрузить корректный файл')
                if mes == QMessageBox.StandardButton.No:
                    fname = 'без загрузки'
                else:
                    fname = None
        if fname not in ['без загрузки']:
            # Вставка данных в таблицу
            for index_row, row in enumerate(sheet_angle.iter_rows(min_row=row_data, values_only=True)):
                if str(row[depth_column]).replace(',', '').replace('.', '').isdigit():
                    angle_data.append((row[depth_column], row[angle_column], row[curvature_column]))
        else:
            return []
        return angle_data


class WellPerforation(FindIndexPZ):
    def __init__(self):
        super().__init__()

    def read_well(self, begin_index, cancel_index):
        from work_py.alone_oreration import is_number, calculation_fluid_work

        self.old_version = True
        col_old_open_index = 0
        bokov_stvol = False
        osnov_stvol = False
        col_plast_index = -1
        col_vert_index = 0
        col_roof_index = 0
        col_sole_index = 0
        col_open_index = 0
        col_close_index = 0
        col_udlin_index = 0
        col_pressure_index = 0
        col_date_pressure_index = 0

        if len(self.dict_perforation) == 0:
            for row in self.ws.iter_rows(min_row=begin_index + 1, max_row=begin_index + 3, values_only=True):
                # print(row)
                for col_index, column in enumerate(row[:14]):
                    if 'оризонт'.lower() in str(column).lower() or 'пласт/'.lower() in str(column).lower():
                        col_plast_index = col_index - 1

                    elif 'по вертикали'.lower() in str(column).lower():
                        col_vert_index = col_index - 1
                        # print(f'вер {col_index}')
                    elif 'кровля'.lower() in str(column).lower():
                        col_roof_index = col_index - 1
                        # print(f'кров {col_index}')
                    elif 'подошва'.lower() in str(column).lower():
                        # print(f'подо {col_index}')
                        col_sole_index = col_index - 1
                    elif 'вскрытия'.lower() in str(column).lower():
                        # print(f'вскр {col_index}')
                        col_open_index = col_index - 1
                    elif 'отключен'.lower() in str(column).lower() and col_index < 8:
                        # print(f'октл {col_index}')
                        col_close_index = col_index - 1
                    elif 'удлине'.lower() in str(column).lower():
                        # print(f'удл {col_index}')
                        col_udlin_index = col_index - 1
                    elif 'Рпл,атм'.lower() in str(column).lower().strip():
                        col_pressure_index = col_index - 1
                    elif 'замера' in str(column).lower():
                        col_date_pressure_index = col_index - 1
                    if 'вскрыт'.lower() in str(column).lower() and 'откл'.lower() in str(column).lower():
                        self.old_version = True
                        col_old_open_index = col_index - 1
                    if "сновной" in str(column).lower():
                        osnov_stvol = True
                    if "боков" in str(column).lower():
                        bokov_stvol = True
            column_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
            if col_date_pressure_index == 0:
                col_date_pressure_index = column_index_from_string(QInputDialog.getItem(
                    self, 'Ошибка', 'Программа не смогла определить колонку в таблице ПВР где указано в дата замера',
                    column_list, 11)[0]) - 2

            if col_pressure_index == 0:
                col_pressure_index = column_index_from_string(
                    QInputDialog.getItem(self, 'Ошибка', 'Программа не смогла определить колонку '
                                                         'в таблице ПВР где указано в Рпл',
                                         column_list, 10)[0]) - 2
            if col_udlin_index == 0:
                col_udlin_index = column_index_from_string(
                    QInputDialog.getItem(self, 'Ошибка', 'Программа не смогла определить колонку '
                                                         'в таблице ПВР где указано в удлинение',
                                         column_list, 9)[0]) - 2
            if col_close_index == 0:
                col_close_index = column_index_from_string(
                    QInputDialog.getItem(self, 'Ошибка', 'Программа не смогла определить колонку '
                                                         'в таблице ПВР где указано дата отключения',
                                         column_list, 6)[0]) - 2
            if col_open_index == 0:
                col_open_index = column_index_from_string(
                    QInputDialog.getItem(self, 'Ошибка', 'Программа не смогла определить колонку '
                                                         'в таблице ПВР где указано дата вскрытия',
                                         column_list, 5)[0]) - 2
            if col_sole_index == 0:
                col_sole_index = column_index_from_string(
                    QInputDialog.getItem(self, 'Ошибка', 'Программа не смогла определить колонку '
                                                         'в таблице ПВР где указано Подошва ИП',
                                         column_list, 4)[0]) - 2
            if col_roof_index == 0:
                col_roof_index = column_index_from_string(
                    QInputDialog.getItem(self, 'Ошибка', 'Программа не смогла определить колонку '
                                                         'в таблице ПВР где указано кровля ИП',
                                         column_list, 3)[0]) - 2
            if col_vert_index == 0:
                col_vert_index = column_index_from_string(
                    QInputDialog.getItem(self, 'Ошибка', 'Программа не смогла определить колонку '
                                                         'в таблице ПВР где указано вертикаль',
                                         column_list, 2)[0]) - 2
            if col_plast_index == -1:
                col_plast_index = column_index_from_string(
                    QInputDialog.getItem(self, 'Ошибка', 'Программа не смогла определить колонку '
                                                         'в таблице ПВР где указано пласт',
                                         column_list, 1)[0]) - 2

            if osnov_stvol is True and bokov_stvol is True:
                QMessageBox.warning(self, 'ОШИБКА', 'Ошибка в определении рабочий интервалов перфорации')
                begin_index = QInputDialog.getInt(self, 'Индекс начала', 'ВВедите индекс начала рабочих интервалов ПВР',
                                                  0, 0, 300)[0] - 3

                cancel_index = QInputDialog.getInt(self, 'Индекс начала',
                                                   'ВВедите индекс окончания рабочих интервалов ПВР', 0, 0, 300)[0] - 2

            perforations_intervals = []
            try:
                row_index = ''
                for row_index, row in enumerate(
                        self.ws.iter_rows(min_row=begin_index + 3, max_row=cancel_index + 2)):
                    lst = []

                    if str(row[col_roof_index + 1].value).replace('.', '').replace(',', '').isdigit():
                        if row[1].value is not None:
                            plast = row[1].value
                            lst.append(plast)
                        else:
                            lst.append(plast)

                        for col in row[2:13]:
                            lst.append(col.value)

                    if all([str(i).strip() == 'None' or i is None for i in lst]) is False:
                        perforations_intervals.append(lst)
            except Exception:
                QMessageBox.warning(self, 'ОШИБКА',
                                    F'Приложение не смогло определить индекс пласта в строке {row_index}')
                data_list.pause = True
                self.pause_app()

            for ind, row in enumerate(perforations_intervals):
                plast = row[col_plast_index].strip()
                # print(f'пласт {plast}')
                if plast is None:
                    plast = perforations_intervals[ind - 1][col_plast_index].strip()
                # print(f'пластs {plast}')

                if any(['проект' in str((i)).lower() or 'не пер' in str((i)).lower() for i in row]) is False and all(
                        [str(i).strip() is None for i in row]) is False and is_number(row[col_roof_index]) is True \
                        and is_number(row[col_sole_index]) is True:
                    # print(f'5 {row}')

                    if is_number(str(row[col_vert_index]).replace(',', '.')) is True:
                        self.dict_perforation.setdefault(
                            plast, {}).setdefault('вертикаль', []).append(
                            float(str(row[col_vert_index]).replace(',', '.')))
                    if any(['фильтр' in str(i).lower() for i in row]):
                        self.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', True)
                    else:
                        self.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
                    self.dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                    roof_int = round(float(str(row[col_roof_index]).replace(',', '.')), 1)
                    sole_int = round(float(str(row[col_sole_index]).replace(',', '.')), 1)
                    self.dict_perforation.setdefault(plast, {}).setdefault('интервал', []).append(
                        (roof_int, sole_int))
                    self.dict_perforation_short.setdefault(plast, {}).setdefault('интервал',
                                                                                 []).append(
                        (roof_int, sole_int))
                    # for interval in list(self.dict_perforation[plast]["интервал"]):
                    # print(interval)

                    self.dict_perforation.setdefault(plast, {}).setdefault('вскрытие', []).append(
                        row[col_open_index])

                    if col_old_open_index != col_open_index:
                        if row[col_close_index] is None or row[col_close_index] == '-':
                            self.dict_perforation.setdefault(plast, {}).setdefault('отключение',
                                                                                   False)
                            self.dict_perforation_short.setdefault(plast, {}).setdefault('отключение',
                                                                                         False)
                        else:
                            self.dict_perforation.setdefault(plast, {}).setdefault('отключение', True)
                            self.dict_perforation_short.setdefault(plast, {}).setdefault('отключение',
                                                                                         True)
                    else:

                        if isinstance(row[col_old_open_index], datetime):
                            self.dict_perforation.setdefault(plast, {}).setdefault('отключение',
                                                                                   False)
                            self.dict_perforation_short.setdefault(plast, {}).setdefault('отключение',
                                                                                         False)
                        else:
                            self.dict_perforation.setdefault(plast, {}).setdefault('отключение', True)
                            self.dict_perforation_short.setdefault(plast, {}).setdefault('отключение',
                                                                                         True)

                    if str(row[col_pressure_index]).replace(',', '').replace('.', '').isdigit() and row[col_vert_index]:
                        data_p = float(str(row[col_pressure_index]).replace(',', '.'))
                        self.dict_perforation.setdefault(plast, {}).setdefault('давление',
                                                                               []).append(
                            round(data_p, 1))
                        self.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     []).append(
                            round(data_p, 1))
                    else:
                        self.dict_perforation.setdefault(plast, {}).setdefault('давление',
                                                                               []).append(
                            round(0, 1))
                        self.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     []).append(
                            round(0, 1))

                    if row[col_date_pressure_index]:
                        self.dict_perforation.setdefault(
                            plast, {}).setdefault('замер', []).append(row[col_date_pressure_index])

                elif any([str((i)).lower() == 'проект' for i in row]) is True and all(
                        [str(i).strip() is None for i in row]) is False and is_number(row[col_roof_index]) is True \
                        and is_number(
                    float(
                        str(row[col_roof_index]).replace(',',
                                                         '.'))) is True:  # Определение проектных интервалов перфорации
                    roof_int = round(float(str(row[col_roof_index]).replace(',', '.')), 1)
                    sole_int = round(float(str(row[col_sole_index]).replace(',', '.')), 1)

                    if len(perforations_intervals) > ind + 1 and perforations_intervals[ind + 1][4] is None:
                        perforations_intervals[ind + 1][4] = 'проект'

                    if row[col_vert_index] is not None:
                        self.dict_perforation_project.setdefault(
                            plast, {}).setdefault('вертикаль', []).append(
                            round(float(str(row[col_vert_index]).replace(',', '.')), 1))
                        self.dict_perforation_project.setdefault(
                            plast, {}).setdefault('интервал', []).append((roof_int, sole_int))

                    if row[col_pressure_index] is not None:
                        self.dict_perforation_project.setdefault(plast, {}).setdefault('давление',
                                                                                       []).append(
                            round(self.check_str_none(row[col_pressure_index]), 1))
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('рабочая жидкость',
                                                                                   []).append(
                        calculation_fluid_work(self, row[col_vert_index], row[col_pressure_index]))

            # объединение интервалов перфорации если они пересекаются
            for plast, value in self.dict_perforation.items():
                intervals = value['интервал']
                merged_segments = list()
                for roof_int, sole_int in sorted(list(intervals), key=lambda x: x[0]):

                    if not merged_segments or roof_int > merged_segments[-1][1]:
                        merged_segments.append((roof_int, sole_int))
                    else:
                        merged_segments[-1] = [merged_segments[-1][0], max(sole_int, merged_segments[-1][1])]

                self.dict_perforation[plast]['интервал'] = merged_segments
        for plast in self.dict_perforation:
            if self.dict_perforation[plast]['отключение'] is False:
                try:
                    zamer = self.dict_perforation[plast]['замер'][0]
                    zamer = zamer.split(' ')
                    for string in zamer:
                        if string.count('.') == 2:
                            string = re.sub(r'[^.\d]', '', string)
                            zamer_str = datetime.strptime(string, '%d.%m.%Y').date()
                    date_now = datetime.now().date()

                    # Вычитаем даты, получая timedelta (разницу в днях)
                    difference = date_now - zamer_str

                    if self.category_pressure == 3:
                        if difference.days > 90:
                            self.check_data_in_pz.append(
                                f'замер по пласту {plast} не соответствует регламенту '
                                f'для скважин 3-й категории не более 3 месяцев до '
                                f'начала ремонта')
                    elif self.category_pressure == 2:
                        if difference.days > 30:
                            self.check_data_in_pz.append(
                                f'замер по пласту {plast} не соответствует регламенту '
                                f'для скважин 3-й категории не более 1 месяца до '
                                f'начала ремонта')
                    elif self.category_pressure == 1:
                        if difference.days > 3:
                            self.check_data_in_pz.append(
                                f'замер по пласту {plast} не соответствует регламенту '
                                f'для скважин 3-й категории не более 3 дней до '
                                f'начала ремонта')
                except Exception:
                    print('Ошибка добавления в информационное сообщение')

        if self.perforation_correct_window2 is None:
            from perforation_correct import PerforationCorrect
            self.perforation_correct_window2 = PerforationCorrect(self)
            self.perforation_correct_window2.setWindowTitle("Сверка данных перфорации")
            # self.perforation_correct_window2.setGeometry(200, 400, 100, 400)

            self.perforation_correct_window2.show()
            self.pause_app()
            data_list.pause = True
            self.perforation_correct_window2 = None
            # definition_plast_work(self)
        else:
            self.perforation_correct_window2.close()
            self.perforation_correct_window2 = None

        if len(self.dict_perforation_project) != 0:
            self.plast_project = list(self.dict_perforation_project.keys())


class WellCategory(FindIndexPZ):

    def read_well(self, begin_index, cancel_index):
        if data_list.data_in_base is False:
            try:
                for row in range(begin_index, cancel_index):
                    for col in range(1, 13):
                        cell = self.ws.cell(row=row, column=col).value
                        if cell:
                            if str(cell).strip() in ['атм'] and self.ws.cell(row=row, column=col - 2).value:
                                self.category_pressure_list.append(self.ws.cell(row=row, column=col - 2).value)
                                self.category_pressure_well.append(self.ws.cell(row=row, column=col - 1).value)

                            elif str(cell).strip() in ['%', 'мг/л', 'мг/дм3', 'мг/м3', 'мг/дм', 'мгдм3']:
                                if str(cell).strip() == '%':
                                    if self.ws.cell(row=row, column=col - 2).value is None:
                                        self.category_h2s_list.append(
                                            self.ws.cell(row=row - 1, column=col - 2).value)
                                    else:
                                        self.category_h2s_list.append(
                                            self.ws.cell(row=row, column=col - 2).value)
                                    if str(self.ws.cell(row=row, column=col - 1).value).strip() in ['', '-', '0',
                                                                                                    'None'] or \
                                            'отс' in str(self.ws.cell(row=row, column=col - 1).value).lower():
                                        self.value_h2s_percent.append(0)
                                        if self.ws.cell(row=row - 1, column=col - 2).value not in ['3', 3]:
                                            self.check_data_in_pz.append(
                                                'Не указано значение сероводорода в процентах')
                                    else:
                                        self.value_h2s_percent.append(
                                            float(str(self.ws.cell(row=row, column=col - 1).value).replace(',', '.')))
                                if str(cell).strip() in ['мг/л', 'мг/дм3', 'мг/дм', 'мгдм3']:
                                    if str(self.ws.cell(row=row, column=col - 1).value).strip() in ['', '-', '0',
                                                                                                    'None'] or \
                                            'отс' in str(self.ws.cell(row=row, column=col - 1).value).lower():
                                        self.value_h2s_mg.append(0)
                                        a = self.ws.cell(row=row, column=col - 2).value
                                        if self.ws.cell(row=row, column=col - 2).value not in ['3', 3]:
                                            self.check_data_in_pz.append(
                                                'Не указано значение сероводорода в мг/л')

                                    else:

                                        self.value_h2s_mg.append(
                                            float(str(self.ws.cell(row=row, column=col - 1).value).replace(',', '.')))

                                if str(cell).strip() in ['мг/м3'] and self.ws.cell(row=row - 1,
                                                                                   column=col - 1).value not in \
                                        ['мг/л', 'мг/дм3', 'мг/дм', 'мгдм3'] and \
                                        self.ws.cell(row=row + 1, column=col - 1).value not in \
                                        ['мг/л', 'мг/дм3', 'мг/дм', 'мгдм3']:
                                    if str(self.ws.cell(
                                            row=row, column=col - 1).value).strip() in ['', '-', '0', 'None'] or \
                                            'отс' in str(self.ws.cell(row=row, column=col - 1).value).lower():
                                        self.value_h2s_mg.append(0)

                                    else:
                                        self.value_h2s_mg.append(float(str(
                                            self.check_str_none(
                                                str(self.ws.cell(row=row,
                                                                 column=col - 1).value).replace(
                                                    ',', '.')))) / 1000)

                            elif str(cell).strip() == 'м3/т':

                                self.category_gaz_factor_percent.append(self.ws.cell(row=row, column=col - 2).value)
                                if 'отс' in str(self.ws.cell(row=row, column=col - 1).value) or \
                                        'None' in str(self.ws.cell(row=row, column=col - 1).value) or \
                                        '-' in str(self.ws.cell(row=row, column=col - 1).value):
                                    self.gaz_factor_percent.append(3)
                                else:
                                    self.gaz_factor_percent.append(float(
                                        str(self.ws.cell(row=row, column=col - 1).value).replace(',', '.')))
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Ошибка обработки данных по категориям {e}')

            if len(self.category_h2s_list) == 0:
                QMessageBox.warning(self, 'ОШИБКА', 'Приложение не смогла найти значение '
                                                    'сероводорода в процентах')
                data_list.pause = True
                self.pause_app()

            if self.data_window is None:
                from category_correct import CategoryWindow
                self.data_window = CategoryWindow(self)
                self.data_window.setWindowTitle("Сверка данных")
                # self.data_window.setGeometry(200, 200, 200, 200)
                self.data_window.show()
                self.pause_app()
                data_list.pause = True
            else:
                self.data_window.close()
                self.data_window = None

            if len(self.value_h2s_percent) == 0:
                QMessageBox.warning(self, 'Ошибка', 'Программа не смогла найти данные по содержания '
                                                    'сероводорода в процентах')
                h2s_pr, _ = QInputDialog.getDouble(self, 'сероводород в процентах',
                                                   'Введите значение серовородода в процентах', 0, 0, 100, 5)

                self.value_h2s_percent.append(h2s_pr)

            self.category_pressure = self.category_pressure_list[0]
            # print(f'категория по давлению {self.category_pressure}')
            self.category_h2s = self.category_h2s_list[0]
            self.category_gas_factor = self.category_gaz_factor_percent[0]

            self.thread_excel = ExcelWorker(self)

            self.without_damping, stop_app = self.thread_excel.check_well_existence(
                self.well_number.get_value, self.well_area.get_value,
                self.region)
            if stop_app:
                self.pause_app()

            try:
                category_pressure_well, categoty_h2s_well, categoty_gf, data = self.thread_excel.check_category(
                    self.well_number, self.well_area, self.region)

                if category_pressure_well:
                    if str(category_pressure_well) != str(self.category_pressure):
                        QMessageBox.warning(None, 'Некорректная категория давления',
                                            f'согласно классификатора от {data} категория скважина '
                                            f'по давлению {category_pressure_well} категории')
                        self.check_data_in_pz.append(
                            f'согласно классификатора от {data} категория скважины '
                            f'по давлению {category_pressure_well} категории\n')
                if categoty_h2s_well:
                    if str(self.category_h2s_list[0]) != str(self.category_h2s):
                        # print(str(self.category_h2s_list[0]), self.category_h2s)
                        #
                        QMessageBox.warning(None, 'Некорректная категория давления',
                                            f'согласно классификатора от {data} категория скважина '
                                            f'по сероводороду {categoty_h2s_well} категории')
                        self.check_data_in_pz.append(
                            f'согласно классификатора от {data} категория скважина '
                            f'по сероводороду {categoty_h2s_well} категории\n')

                if categoty_gf:
                    if str(categoty_gf) != str(self.category_gas_factor):
                        QMessageBox.warning(None, 'Некорректная категория давления',
                                            f'согласно классификатора от {data} категория скважина '
                                            f'по газовому фактору {categoty_gf} категории')
                        self.check_data_in_pz.append(f'согласно классификатора от {data} категория скважина '
                                                     f'по газовому фактору {categoty_gf} категории\n')
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка',
                                    f'Скважина не найдена в классификаторе \n {type(e).__name__}\n\n{str(e)}')

        if self.work_plan not in ['gnkt_frez', 'application_pvr',
                                  'application_gis', 'gnkt_after_grp', 'gnkt_opz', 'plan_change']:
            # print(f'план работ {self.work_plan}')
            delete_rows_pz(self, self.ws, self.cat_well_min, self.data_well_max, self.data_x_max)
            self.insert_index = self.data_well_max.get_value - self.cat_well_min.get_value + 19

        return self
