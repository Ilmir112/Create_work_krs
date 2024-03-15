from datetime import datetime

from PyQt5.QtWidgets import QInputDialog, QMainWindow, QMessageBox
from category_correct import CategoryWindow
from data_correct import DataWindow
from perforation_correct import PerforationCorrect
from work_py.leakage_column import LeakageWindow


class ProtectedIsDigit():
    def __init__(self, default_value=None, name=None):
        self._value = default_value
        self._name = name

    def __get__(self, instance, owner):
        if not instance:
            # print(f'значение {self._name} ра3вно {self._value}')
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if 'уст' in str(value).lower():
            self._value = 0
        elif isinstance(value, str):
            try:
                float_value = float(value.replace(",", "").replace(".", ""))  # Пробуем преобразовать строку в число
                self._value = float_value
            except ValueError:
                self._value = None  # Если не удалось преобразовать в число, сохраняем None
        elif isinstance(value, (int, float)):
            self._value = float(value)  # Преобразуем целое число в число с плавающей точкой
        else:
            print(f'Ошибка: Недопустимое значение {value}')


class ProtectedIsNonNone():
    def __init__(self, default_value=None, name=None):
        self._value = default_value
        self._name = name

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value is not None and not str(value).replace(",", "").replace(".", "").isdigit():
            instance.__dict__[self._name] = value

        else:
            print(f'Ошибка: {value} - не корректное строковое значение')
            raise ValueError("Значение должно быть строкой")


class FindIndexPZ(QMainWindow):
    def __init__(self, ws):
        super().__init__()
        self.readPZ(ws)
        self.data_window = None
        self.perforation_correct_window2 = None

    def readPZ(self, ws):
        from open_pz import CreatePZ

        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            ws.row_dimensions[row_ind].hidden = False

            if 'Категория скважины' in row:
                CreatePZ.cat_well_min = ProtectedIsDigit(row_ind + 1)  # индекс начала категории

            elif 'План-заказ' in row:

                CreatePZ.cat_well_max = ProtectedIsDigit(row_ind - 1)
                CreatePZ.data_well_min = ProtectedIsDigit(row_ind + 1)


            elif any(['Ожидаемые показатели после' in str(col) for col in row]):
                CreatePZ.data_x_min = ProtectedIsDigit(row_ind)
                # print(f' индекс Ожидаемые показатели {CreatePZ.data_x_min}')
            elif '11. Эксплуатационные горизонты и интервалы перфорации:' in row:
                CreatePZ.data_pvr_min = ProtectedIsDigit(row_ind)
            elif 'Оборудование скважины ' in row:
                CreatePZ.data_fond_min = ProtectedIsDigit(row_ind)


            elif any(['IX. Мероприятия по предотвращению' in str(col) for col in row]) or \
                    any(['IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in str(col) for col in
                         row]):
                CreatePZ.data_well_max = ProtectedIsDigit(row_ind)

            elif 'НКТ' == str(row[1]).upper():
                CreatePZ.pipes_ind = ProtectedIsDigit(row_ind + 1)


            elif 'ШТАНГИ' == str(row[1]).upper():
                CreatePZ.sucker_rod_ind = ProtectedIsDigit(row_ind + 1)


            elif 'ХI Планируемый объём работ:' in row or 'ХI. Планируемый объём работ:' \
                    in row or 'ХIII Планируемый объём работ:' in row \
                    or 'ХI Планируемый объём работ:' in row or 'Порядок работы' in row:
                CreatePZ.data_x_max = ProtectedIsDigit(row_ind)


            elif 'II. История эксплуатации скважины' in row:
                CreatePZ.data_pvr_max = ProtectedIsDigit(row_ind)

            elif 'III. Состояние скважины к началу ремонта ' in row:
                CreatePZ.condition_of_wells = ProtectedIsDigit(row_ind)
        try:
            check = CreatePZ.cat_well_min._value
        except:
            CreatePZ.cat_well_min = ProtectedIsDigit(QInputDialog.getInt(
                self, 'индекс начала копирования', 'Программа не смогла определить строку начала копирования',
                0, 0, 800)[0])
        try:
            check = CreatePZ.cat_well_max._value

        except:
            CreatePZ.cat_well_max = ProtectedIsDigit(QInputDialog.getInt(self, 'индекс начала копирования',
                                                                         'Программа не смогла определить строку начала копирования',
                                                                         0, 0, 800)[0])
        try:
            check = CreatePZ.sucker_rod_ind._value

        except:
            CreatePZ.sucker_rod_ind = ProtectedIsDigit(QInputDialog.getInt(self, 'индекс начала строки со штангами',
                                                                           'Программа не смогла найти строку со штангами',
                                                                           0, 0, 800)[0])
        try:
            check = CreatePZ.data_well_max._value

        except:
            CreatePZ.data_well_max = ProtectedIsDigit(QInputDialog.getInt(self, 'индекс окончания копирования',
                                                                          'Программа не смогла определить строку окончания копирования',
                                                                          0, 0, 800)[0])
        try:
            check = CreatePZ.data_x_max._value
        except:
            CreatePZ.data_x_max, _ = ProtectedIsDigit(
                QInputDialog.getInt(self, 'индекс окончания копирования ожидаемых показателей',
                                    'Программа не смогла определить строку окончания копирования'
                                    ' ожидаемых показателей',
                                    0, 0, 800)[0])
        try:
            check = CreatePZ.condition_of_wells._value
        except:
            CreatePZ.condition_of_wells = ProtectedIsDigit(
                QInputDialog.getInt(self, 'индекс копирования',
                                    'Программа не смогла определить строку n\ III. '
                                    'Состояние скважины к началу ремонта ',
                                    0, 0, 800)[0])
        try:
            check = CreatePZ.data_x_min._value
        except:
            CreatePZ.data_x_min = ProtectedIsDigit(
                QInputDialog.getInt(self, 'индекс начала копирования ожидаемых показателей',
                                    'Программа не смогла определить строку начала копирования'
                                    ' ожидаемых показателей',
                                    0, 0, 800)[0])
        try:
            check = CreatePZ.data_well_min._value
        except:
            CreatePZ.data_well_min = ProtectedIsDigit(
                QInputDialog.getInt(self, 'индекс начала строки после план заказ',
                                    'Программа не смогла найти начала строки после план заказ',
                                    0, 0, 800)[0])
        try:
            check = CreatePZ.data_pvr_max._value

        except:
            CreatePZ.data_pvr_max = ProtectedIsDigit(
                QInputDialog.getInt(self, 'индекс начала строки после план заказ',
                                    'Программа не смогла найти "II. История эксплуатации скважины"',
                                    0, 0, 800)[0])

        try:
            check = CreatePZ.pipes_ind._value

        except:
            CreatePZ.pipes_ind = ProtectedIsDigit(QInputDialog.getInt(self, 'индекс начала строки с НКТ',
                                                                      'Программа не смогла найти строку с НКТ',
                                                                      0, 0, 800)[0])
        try:
            check = CreatePZ.data_pvr_min._value
        except:
            CreatePZ.data_pvr_min = ProtectedIsDigit(QInputDialog.getInt(self, 'индекс начала начала ПВР',
                                                                         'Программа не смогла найти индекс начала ПВР',
                                                                         0, 0, 800)[0])
        try:
            check = CreatePZ.data_fond_min._value
        except:
            CreatePZ.data_fond_min = ProtectedIsDigit(
                QInputDialog.getInt(self, 'индекс начала строки с таблицей фондовыго оборудования',
                                    'Программа не смогла найти строку с таблицей фондового оборудования',
                                    0, 0, 800)[0])

    def check_str_None(self, string):
        # print(str(string).replace(' ', '') == '-')
        if isinstance(string, int) is True or isinstance(string, float) is True:
            return string
        elif str(string).replace(' ', '') == '-' or 'отсут' in str(string) or \
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
            for i in str(string):
                i.replace(',', '.')
                if i in '0123456789,.x':
                    b = str(b) + i
            return float(b)

    def definition_is_None(self, data, row, col, step, m=12):
        try:

            data = data._value
            while data is None or step == m:
                data = self.ws.cell(row=row, column=col + step).value

                step += 1

            return ProtectedIsNonNone(data)
        except:

            while data is None:
                data = self.ws.cell(row=row, column=col + step).value

                if step == m:
                    break
                step += 1

            return data


class WellNkt(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)

        self.read_well(ws, CreatePZ.pipes_ind._value, CreatePZ.condition_of_wells._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        try:
            a_plan = 0
            CreatePZ.nkt_mistake = False
            for row in range(begin_index, cancel_index):  # словарь  количества НКТ и метраж

                if ws.cell(row=row, column=3).value == 'План' or str(
                        ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                    a_plan = row
            if a_plan == 0:
                a_plan = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                                'Программа не могла определить начала строку с ПЗ НКТ - план')
            # print(f'индекс a_plan {a_plan}')
            for row in range(begin_index, cancel_index + 1):
                # print(str(ws.cell(row=row, column=4).value))
                key = str(ws.cell(row=row, column=4).value)
                if key != str(None) and key != '-' and "Диам" not in key:
                    value = ws.cell(row=row, column=7).value
                    if value:
                        if not key is None and row < a_plan:
                            CreatePZ.dict_nkt[key] = CreatePZ.dict_nkt.get(key, 0) + round(float(value), 1)
                        elif not key is None and row >= a_plan:
                            CreatePZ.dict_nkt_po[key] = CreatePZ.dict_nkt_po.get(key, 0) + round(float(value), 1)
                    # print(f'индекс a_plan {CreatePZ.dict_nkt}')
                # CreatePZ.shoe_nkt = float(sum(CreatePZ.dict_nkt.values()))
        except:
            CreatePZ.nkt_mistake = True
            mes = QMessageBox.warning(self, 'Ошибка', 'Программа не смогла определить диаметры и длину НКТ')


class WellSucker_rod(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ
        super().__init__(ws)

        self.read_well(ws, CreatePZ.sucker_rod_ind._value, CreatePZ.pipes_ind._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ
        try:
            CreatePZ.sucker_mistake = False
            b_plan = 0
            if CreatePZ.sucker_rod_ind._value != 0:
                for row in range(begin_index, cancel_index):  # словарь  количества штанг и метраж
                    if ws.cell(row=row, column=3).value == 'План' or str(
                            ws.cell(row=row, column=3).value).lower() == 'после ремонта' \
                            or str(
                        ws.cell(row=row, column=3).value).lower() == 'до ремонта':
                        b_plan = row

                if b_plan == 0:
                    b_plan = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                                    'Программа не могла определить начала строку с ПЗ штанги - план')
                # print(f'б {b_plan}')

                for row in range(begin_index, cancel_index - 1):

                    key = str(ws.cell(row=row, column=4).value).replace(' ', '')
                    value = ws.cell(row=row, column=7).value
                    if key != str(None) and key != '-' and key != '':
                        # print(key, value)
                        if key != None and row < b_plan:
                            CreatePZ.dict_sucker_rod[key] = CreatePZ.dict_sucker_rod.get(key, 0) + int(value + 1)
                        if key != None and row >= b_plan:
                            CreatePZ.dict_sucker_rod_po[key] = CreatePZ.dict_sucker_rod_po.get(key, 0) + int(value)
        except:
            CreatePZ.sucker_mistake = True
            mes = QMessageBox.warning(self, 'Ошибка', 'Программа не смогла определить диаметры и длину штанг')


class WellFond_data(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.read_well(ws, CreatePZ.data_fond_min._value, CreatePZ.condition_of_wells._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        CreatePZ.old_index = 1
        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            for col, cell in enumerate(row):
                value = cell.value
                if value:
                    if 'карта спуска' in str(value).lower():
                        col_plan = col
                    if 'до ремонта' in str(value).lower() and row_index < 6 + begin_index:
                        col_do = col

                    if 'Пакер' in str(value) and 'типоразмер' in str(row[col + 2].value):
                        try:
                            CreatePZ.paker_do["do"] = self.check_str_None(row[col_plan].value)[0]
                            CreatePZ.paker2_do["do"] = self.check_str_None(row[col_plan].value)[1]
                        except:
                            CreatePZ.paker_do["do"] = row[col_do].value

                        try:
                            CreatePZ.paker_do["posle"] = self.check_str_None(row[col_plan].value)[0]
                            CreatePZ.paker2_do["posle"] = self.check_str_None(row[col_plan].value)[1]
                        except:
                            CreatePZ.paker_do["posle"] = row[col_plan].value

                    elif value == 'Насос' and row[col + 2].value == 'типоразмер':
                        if row[col_do].value:
                            if ('НВ' in str(row[col_do].value).upper() or 'ШГН' in str(row[col_do].value).upper() \
                                or 'НН' in str(row[col_do].value).upper()) or 'RHAM' in str(row[col_do].value).upper():
                                CreatePZ.dict_pump_SHGN["do"] = row[col_do].value
                            if ('ЭЦН' in str(row[col_do].value).upper() or 'ВНН' in str(row[col_do].value).upper()):
                                CreatePZ.dict_pump_ECN["do"] = row[col_do].value

                        if row[col_plan].value:
                            if ('НВ' in str(row[col_plan].value).upper() or 'ШГН' in str(
                                    row[col_plan].value).upper() \
                                or 'НН' in str(row[col_plan].value).upper()) \
                                    or 'RHAM' in str(row[col_plan].value).upper():
                                CreatePZ.dict_pump_SHGN["posle"] = row[col_plan].value

                            if ('ЭЦН' in str(row[col_plan].value).upper() or 'ВНН' in str(
                                    row[col_plan].value).upper()):
                                CreatePZ.dict_pump_ECN["posle"] = row[col_plan].value

                        if CreatePZ.dict_pump_ECN["do"] != 0:
                            CreatePZ.dict_pump_ECN_h["do"] = ws.cell(row=row_index + 4, column=col_do + 1).value
                        if CreatePZ.dict_pump_SHGN["do"] != 0:
                            CreatePZ.dict_pump_SHGN_h["do"] = ws.cell(row=row_index + 4, column=col_do + 1).value
                        if CreatePZ.dict_pump_ECN["posle"] != 0:
                            CreatePZ.dict_pump_ECN_h["posle"] = ws.cell(row=row_index + 4,
                                                                        column=col_plan + 1).value
                        if CreatePZ.dict_pump_SHGN["posle"] != 0:
                            CreatePZ.dict_pump_SHGN_h["posle"] = ws.cell(row=row_index + 4,
                                                                         column=col_plan + 1).value

                    elif value == 'Н посадки, м':
                        try:
                            if CreatePZ.paker_do["do"] != 0:
                                CreatePZ.depth_fond_paker_do["do"] = self.check_str_None(row[col_do].value)[0]
                                CreatePZ.depth_fond_paker2_do["do"] = self.check_str_None(row[col_do].value)[1]
                        except:
                            if CreatePZ.paker_do["do"] != 0:
                                CreatePZ.depth_fond_paker_do["do"] = row[col_do].value
                        try:
                            if CreatePZ.paker_do["posle"] != 0:
                                CreatePZ.depth_fond_paker_do["posle"] = self.check_str_None(row[col_plan].value)[0]
                                CreatePZ.depth_fond_paker2_do["posle"] = self.check_str_None(row[col_plan].value)[1]
                        except:
                            if CreatePZ.paker_do["posle"] != 0:
                                CreatePZ.depth_fond_paker_do["posle"] = row[col_plan].value


class WellHistory_data(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.leakage_window = None
        self.ws = ws
        self.read_well(self.ws, CreatePZ.data_pvr_max._value, CreatePZ.data_fond_min._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ
        CreatePZ.max_expected_pressure = ProtectedIsNonNone('не корректно')
        CreatePZ.max_admissible_pressure = ProtectedIsNonNone('не корректно')

        # print(begin_index, cancel_index)
        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            for col, cell in enumerate(row):
                value = cell.value
                if value:

                    if 'нэк' in str(value).lower() or 'негерм' in str(
                            value).lower() or 'нарушение э' in str(
                        value).lower() or \
                            'нарушение г' in str(value).lower():
                        CreatePZ.leakiness_Count += 1
                        CreatePZ.leakiness = True
                    if ('авар' in str(
                            value).lower() or 'расхаж' in str(
                        value).lower() or 'лар' in str(value).lower()) \
                            and 'акт о расследовании аварии прилагается' not in str(value).lower():
                        CreatePZ.emergency_well = True
                        CreatePZ.emergency_count += 1
                    if 'сужен' in str(value).lower() or 'не проход' in str(value).lower():
                        CreatePZ.problem_with_ek = True

                    if 'Начало бурения' in str(value):
                        CreatePZ.date_drilling_run = row[col + 2].value

                    elif 'Конец бурения' == value:
                        CreatePZ.date_drilling_cancel = row[col + 2].value

                        CreatePZ.date_drilling_cancel = self.definition_is_None(
                            CreatePZ.date_drilling_cancel, row_index + begin_index, col + 1, 1)

                    elif 'Максимально ожидаемое давление на устье' == value:
                        CreatePZ.max_expected_pressure = ProtectedIsDigit(row[col + 1].value)
                        CreatePZ.max_expected_pressure = self.definition_is_None(
                            CreatePZ.max_expected_pressure, row_index + begin_index, col + 1, 1)

                    elif 'Максимально допустимое давление'.lower() in str(value).lower():
                        CreatePZ.max_admissible_pressure = ProtectedIsDigit(row[col + 1].value)
                        CreatePZ.max_admissible_pressure = self.definition_is_None(
                            CreatePZ.max_admissible_pressure, row_index + begin_index, col + 1, 1)

        if CreatePZ.leakiness == True:
            leakiness_quest = QMessageBox.question(self, 'нарушение колонны',
                                                   'Программа определела что в скважине'
                                                   f'есть нарушение - {CreatePZ.leakiness_Count}, верно ли?')
            if leakiness_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.leakiness = True
                if self.leakage_window is None:
                    self.leakage_window = LeakageWindow()
                    self.leakage_window.setWindowTitle("Геофизические исследования")
                    self.leakage_window.setGeometry(200, 400, 300, 400)
                    self.leakage_window.show()

                    CreatePZ.pause_app(self)
                    CreatePZ.dict_leakiness = self.leakage_window.addWork()
                    # print(f'словарь нарушений {CreatePZ.dict_leakiness}')
                    CreatePZ.pause = True
                    self.leakage_window = None  # Discard reference.


                else:
                    self.leakage_window.close()  # Close window.
                    self.leakage_window = None  # Discard reference.


            else:
                CreatePZ.leakiness = False


class WellCondition(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.ws = ws

        self.read_well(ws, CreatePZ.condition_of_wells._value, CreatePZ.data_well_max._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        CreatePZ.static_level = ProtectedIsNonNone('не корректно')
        CreatePZ.dinamic_level = ProtectedIsNonNone('не корректно')

        CreatePZ.dinamic_level = ProtectedIsDigit(0)
        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            for col, cell in enumerate(row):
                value = cell.value

                if 'нэк' in str(
                        value).lower() or 'негерм' in str(value).lower() or 'нарушение э' in str(
                    value).lower() or 'нарушение г' in str(value).lower():
                    CreatePZ.leakiness_Count += 1
                    CreatePZ.leakiness = True
                if ('авар' in str(value).lower() or 'расхаж' in str(value).lower() or 'лар' in str(value)) \
                        and 'акт о расследовании аварии прилагается' not in str(value):
                    CreatePZ.emergency_well = True
                    CreatePZ.emergency_count += 1
                if value:
                    if "Hст " in str(value):
                        if '/' in str(row[col + 1].value):
                            CreatePZ.static_level = ProtectedIsDigit(row[col + 1].value.split('/')[0])
                        else:
                            CreatePZ.static_level = ProtectedIsDigit(row[col + 1].value)
                    if "грп" in str(value).lower():
                        CreatePZ.grpPlan = True

                    if "Ндин " in str(value):
                        CreatePZ.dinamic_level = ProtectedIsDigit(row[col + 1].value)
                    if "% воды " in str(value):
                        CreatePZ.proc_water = str(row[col + 1].value).strip().replace('%', '')
                        CreatePZ.proc_water = self.definition_is_None(CreatePZ.proc_water, row_index, col + 1, 1)
                    if 'Vжг' in str(value):
                        try:
                            well_volume_in_PZ = str(row[col + 1].value).replace(',', '.')
                            # print(f'строка {well_volume_in_PZ}')
                            # well_volume_in_PZ = self.definition_is_None(well_volume_in_PZ, row_index, col + 1, 1)
                            CreatePZ.well_volume_in_PZ.append(round(float(well_volume_in_PZ), 1))
                        except:
                            well_volume_in_PZ, _ = QInputDialog.getDouble(None, 'Объем глушения',
                                                                          'ВВедите объем глушения согласно ПЗ', 50, 1,
                                                                          70)
                            CreatePZ.well_volume_in_PZ.append(well_volume_in_PZ)

        if CreatePZ.grpPlan:
            grpPlan_quest = QMessageBox.question(self, 'Подготовка к ГРП', 'Программа определела что в скважине'
                                                                           f'планируется ГРП, верно ли?')
            if grpPlan_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.grpPlan = True
            else:
                CreatePZ.grpPlan = False


class Well_expected_pick_up(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.ws = ws
        self.read_well(ws, CreatePZ.data_x_min._value, CreatePZ.data_x_max._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            # print(row_index)
            for col, cell in enumerate(row[0:15]):
                # print(row_index)
                value = cell.value
                if value:

                    if 'прием' in str(value).lower() or 'qж' in str(value).lower():
                        CreatePZ.expected_Q = row[col + 1].value
                      # print(CreatePZ.expected_Q)
                        CreatePZ.expected_Q = self.definition_is_None(CreatePZ.expected_Q, row_index, col + 1, 1)
                        print(f'после {CreatePZ.expected_Q}')
                    if 'зак' in str(value).lower() or 'давл' in str(value).lower() or 'p' in str(value).lower():
                        CreatePZ.expected_P = row[col + 1].value
                        CreatePZ.expected_P = self.definition_is_None(CreatePZ.expected_P, row_index, col + 1, 1)

                    if 'qж' in str(value).lower():
                        CreatePZ.Qwater = str(row[col + 1].value).strip().replace(' ', '').replace('м3/сут', '')
                        CreatePZ.Qwater = self.definition_is_None(CreatePZ.Qwater, row_index, col + 1, 1)

                    if 'qн' in str(value).lower():
                        CreatePZ.Qoil = str(row[col + 1].value).replace(' ', '').replace('т/сут', '')
                        CreatePZ.Qoil = self.definition_is_None(CreatePZ.Qoil, row_index, col + 1, 1)
                    if 'воды' in str(value).lower():
                        proc_water = str(row[col + 1].value).replace(' ', '').replace('%', '')
                        proc_water = int(float(proc_water)) if float(proc_water) > 1 else round(float(proc_water) * 100,
                                                                                                0)
                        CreatePZ.proc_water = self.definition_is_None(proc_water, row_index, col + 1, 1)

            try:
                CreatePZ.expected_pick_up[CreatePZ.expected_Q] = CreatePZ.expected_P
            except:
                print('Ошибка в определении ожидаемых показателей')


class Well_data(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.ws = ws
        self.read_well(self.ws, CreatePZ.cat_well_max._value, CreatePZ.data_pvr_min._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        CreatePZ.well_area = ProtectedIsNonNone('не корректно')
        CreatePZ.well_number = ProtectedIsNonNone('не корректно')
        CreatePZ.inv_number = ProtectedIsNonNone('не корректно')
        CreatePZ.cdng = ProtectedIsNonNone('не корректно')
        CreatePZ.bottomhole_drill = ProtectedIsNonNone('не корректно')
        CreatePZ.bottomhole_artificial = ProtectedIsNonNone('не корректно')
        CreatePZ.max_angle = ProtectedIsNonNone('не корректно')
        CreatePZ.max_angle_H = ProtectedIsNonNone('не корректно')
        CreatePZ.stol_rotora = ProtectedIsNonNone('не корректно')
        CreatePZ.level_cement_direction = ProtectedIsNonNone('не корректно')
        CreatePZ.column_direction_diametr = ProtectedIsNonNone('отсут')
        CreatePZ.column_direction_wall_thickness = ProtectedIsNonNone('отсут')
        CreatePZ.column_direction_lenght = ProtectedIsNonNone('отсут')
        CreatePZ.level_cement_conductor = ProtectedIsNonNone('отсут')
        CreatePZ.column_conductor_wall_thickness = ProtectedIsNonNone('отсут')
        CreatePZ.column_conductor_lenght = ProtectedIsNonNone('отсут')
        CreatePZ.column_diametr = ProtectedIsNonNone('не корректно')
        CreatePZ.column_wall_thickness = ProtectedIsNonNone('не корректно')
        CreatePZ.shoe_column = ProtectedIsNonNone('не корректно')
        CreatePZ.level_cement_column = ProtectedIsNonNone('не корректно')
        CreatePZ.pressuar_mkp = ProtectedIsNonNone('не корректно')
        CreatePZ.column_additional_diametr = ProtectedIsNonNone('не корректно')
        CreatePZ.column_additional_wall_thickness = ProtectedIsNonNone('не корректно')
        CreatePZ.head_column_additional = ProtectedIsNonNone('не корректно')
        CreatePZ.shoe_column_additional = ProtectedIsNonNone('не корректно')

        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index

            for col, cell in enumerate(row):
                value = cell.value
                if value:
                    if 'площадь' in str(value):  # определение номера скважины
                        CreatePZ.well_number = ProtectedIsDigit(row[col - 1].value)
                        CreatePZ.well_area = ProtectedIsNonNone(row[col + 1].value)
                    elif 'месторождение ' in str(value):  # определение номера скважины
                        CreatePZ.well_oilfield = ProtectedIsNonNone(row[col + 2].value)
                    elif 'Инв. №' in str(value):
                        CreatePZ.inv_number = ProtectedIsNonNone(row[col + 1].value)
                    elif 'цех' == value:
                        CreatePZ.cdng = ProtectedIsDigit(row[col + 1].value)
                        # print(f' ЦДНГ {CreatePZ.cdng._value}')
                    elif 'пробуренный забой' in str(value).lower():
                        CreatePZ.bottomhole_drill = ProtectedIsDigit(row[col + 2].value)
                        CreatePZ.bottomhole_drill = FindIndexPZ.definition_is_None(self, CreatePZ.bottomhole_drill,
                                                                                   row_index, col, 2)

                        CreatePZ.bottomhole_artificial = ProtectedIsDigit(row[col + 4].value)
                        print(f'пробуренный забой {CreatePZ.bottomhole_artificial}')
                        CreatePZ.bottomhole_artificial = \
                            FindIndexPZ.definition_is_None(self, CreatePZ.bottomhole_artificial, row_index, col, 5)
                        print(f'пробуренный забой {CreatePZ.bottomhole_artificial}')

                    elif 'зенитный угол' in str(value).lower():
                        CreatePZ.max_angle = ProtectedIsDigit(row[col + 4].value)
                        for index, col1 in enumerate(row):
                            if 'на глубине' in str(col1.value):
                                CreatePZ.max_angle_H = ProtectedIsDigit(row[index + 1].value)

                    elif 'текущий забой' in str(value).lower() and len(value) < 15:
                        CreatePZ.current_bottom = row[col + 2].value
                        CreatePZ.current_bottom = \
                            FindIndexPZ.definition_is_None(self, CreatePZ.current_bottom, row_index, col, 2)

                        CreatePZ.bottom = CreatePZ.current_bottom
                    elif '10. Расстояние от стола ротора до среза муфты э/колонны ' in str(value):
                        CreatePZ.stol_rotora = ProtectedIsDigit(row[col + 4].value)

                    elif 'Направление' in str(value) and 'Шахтное направление' not in str(value) and \
                            ws.cell(row=row_index + 1, column=col + 1).value != None and \
                            self.check_str_None(row[col + 3].value) != '0':
                        CreatePZ.column_direction_True = True
                        if CreatePZ.column_direction_True:
                            for col1, cell in enumerate(row):
                                if 'Уровень цемента' in str(cell.value):
                                    if 'уст' in str(row[col1 + 2].value).lower():
                                        CreatePZ.level_cement_direction = ProtectedIsDigit(0)
                                    else:
                                        CreatePZ.level_cement_direction = ProtectedIsDigit(
                                            str(row[col1 + 2].value.split('-')[0]).replace(" ", ""))
                        else:
                            CreatePZ.level_cement_direction = ProtectedIsNonNone('отсут')
                        try:
                            column_direction_data = row[col + 3].value.split('(мм),')
                            try:
                                CreatePZ.column_direction_diametr = ProtectedIsDigit(column_direction_data[0])
                            except:
                                CreatePZ.column_direction_diametr = ProtectedIsNonNone('не корректно')

                            try:
                                CreatePZ.column_direction_wall_thickness = ProtectedIsDigit(
                                    column_direction_data[1].replace(' ', ''))
                            except:
                                CreatePZ.column_direction_wall_thickness = ProtectedIsNonNone('не корректно')
                            try:
                                try:
                                    CreatePZ.column_direction_lenght = ProtectedIsDigit(
                                        column_direction_data[2].split('-')[1].replace('(м)', '').replace(" ", ""))
                                except:
                                    CreatePZ.column_direction_lenght = ProtectedIsDigit(
                                        column_direction_data[2].replace('(м)', '').replace(" ", ""))

                            except:
                                CreatePZ.column_direction_lenght = ProtectedIsNonNone('не корректно')
                        except:
                            CreatePZ.column_direction_diametr = ProtectedIsNonNone('не корректно')
                            CreatePZ.column_direction_wall_thickness = ProtectedIsNonNone('не корректно')
                            CreatePZ.column_direction_lenght = ProtectedIsNonNone('не корректно')

                    elif 'Кондуктор' in str(value) and \
                            self.check_str_None(row[col + 3].value) != '0':

                        for col1, cell in enumerate(row):
                            if 'Уровень цемента' in str(cell.value):

                                try:
                                    if 'уст' in str(row[col1 + 2].value).lower():
                                        CreatePZ.level_cement_conductor = ProtectedIsDigit(0)
                                    else:
                                        CreatePZ.level_cement_conductor = ProtectedIsDigit(
                                            str(row[col1 + 2].value.split('-')[0]).replace(' ', ''))
                                except:
                                    CreatePZ.level_cement_conductor = ProtectedIsNonNone('не корректно')
                        try:
                            column_conductor_data = str(row[col + 3].value).split('(мм),')
                            try:
                                CreatePZ.column_conductor_diametr = ProtectedIsDigit(column_conductor_data[0].strip())
                            except:
                                CreatePZ.column_conductor_diametr = ProtectedIsNonNone('не корректно')

                            try:
                                CreatePZ.column_conductor_wall_thickness = \
                                    ProtectedIsDigit(column_conductor_data[1].strip())
                            except:
                                CreatePZ.column_conductor_wall_thickness = ProtectedIsNonNone('не корректно')
                            try:
                                try:
                                    CreatePZ.column_conductor_lenght = ProtectedIsDigit(
                                        column_conductor_data[2].split('-')[1].replace('(м)', '').strip())
                                except:
                                    CreatePZ.column_conductor_lenght = ProtectedIsDigit(
                                        str(column_conductor_data[2].replace('(м)', '')).strip())
                            except:
                                CreatePZ.column_conductor_lenght = ProtectedIsNonNone('не корректно')

                        except:
                            CreatePZ.column_conductor_diametr = ProtectedIsNonNone('не корректно')
                            CreatePZ.column_conductor_wall_thickness = ProtectedIsNonNone('не корректно')
                            CreatePZ.column_conductor_lenght = ProtectedIsNonNone('не корректно')
                    elif str(
                            value) == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':

                        try:
                            data_main_production_string = str(ws.cell(row=row_index + 1, column=col + 1).value).split(
                                '(мм),', )
                            try:
                                CreatePZ.column_diametr = ProtectedIsDigit(
                                    float(str(data_main_production_string[0]).replace(',', '.')))
                            except:
                                CreatePZ.column_diametr = ProtectedIsNonNone('не корректно')
                            try:
                                CreatePZ.column_wall_thickness = ProtectedIsDigit(
                                    float(str(data_main_production_string[1]).replace(',', '.')))
                            except:
                                CreatePZ.column_wall_thickness = ProtectedIsNonNone('не корректно')
                            try:
                                if len(data_main_production_string[-1].split('-')) == 2:

                                    CreatePZ.shoe_column = ProtectedIsDigit(
                                        self.check_str_None(data_main_production_string[-1].split('-')[-1]))
                                else:
                                    CreatePZ.shoe_column = ProtectedIsDigit(
                                        self.check_str_None(data_main_production_string[-1]))
                            except:
                                CreatePZ.shoe_column = ProtectedIsNonNone('не корректно')
                        except ValueError:
                            CreatePZ.column_diametr = ProtectedIsNonNone('не корректно')
                            CreatePZ.column_wall_thickness = ProtectedIsNonNone('не корректно')
                            CreatePZ.shoe_column = ProtectedIsNonNone('не корректно')

                    elif 'Уровень цемента за колонной' in str(value):
                        CreatePZ.level_cement_column = ProtectedIsDigit(row[col + 3].value)
                        CreatePZ.level_cement_column = self.definition_is_None(CreatePZ.level_cement_column, row_index,
                                                                               col, 1)
                    elif 'Рмкп ( э/к и' in str(cell):
                        CreatePZ.pressuar_mkp = ProtectedIsNonNone(row[col + 2].value)
                    elif 'онструкция хвостовика' in str(value):

                        data_column_additional = self.check_str_None(ws.cell(row=row_index + 2, column=col + 2).value)
                        # print(f'доп колона {data_column_additional.strip(), self.check_str_None(data_column_additional.strip())}')
                        if data_column_additional != '0':
                            CreatePZ.column_additional = True
                        if CreatePZ.column_additional is True:
                            try:
                                CreatePZ.head_column_additional = ProtectedIsDigit(data_column_additional[0])
                            except:
                                CreatePZ.head_column_additional = ProtectedIsNonNone('не корректно')
                            try:
                                CreatePZ.shoe_column_additional = ProtectedIsDigit(data_column_additional[1])
                            except:
                                CreatePZ.shoe_column_additional = ProtectedIsNonNone('не корректно')

                            try:
                                try:
                                    data_add_column = self.check_str_None(
                                        ws.cell(row=row_index + 2, column=col + 4).value)
                                    # print(f' доп колонна {data_add_column}')
                                    CreatePZ.column_additional_diametr = ProtectedIsDigit(data_add_column[0])

                                except:
                                    CreatePZ.column_additional_diametr = ProtectedIsDigit(
                                        self.check_str_None(ws.cell(row=row_index + 2, column=col + 4).value))

                                try:
                                    data_add_column = self.check_str_None(
                                        ws.cell(row=row_index + 2, column=col + 4).value)
                                    CreatePZ.column_additional_wall_thickness = ProtectedIsDigit(data_add_column[1])
                                except:

                                    CreatePZ.column_additional_wall_thickness = ProtectedIsDigit(
                                        self.check_str_None(ws.cell(row=row_index + 2, column=col + 6).value))

                            except:
                                CreatePZ.column_additional_wall_thickness = ProtectedIsNonNone('не корректно')
                                CreatePZ.column_additional_diametr = ProtectedIsNonNone('не корректно')
                        else:
                            CreatePZ.column_additional_diametr = ProtectedIsNonNone('отсут')
                            CreatePZ.column_additional_wall_thickness = ProtectedIsNonNone('отсут')
                            CreatePZ.head_column_additional = ProtectedIsNonNone('отсут')
                            CreatePZ.shoe_column_additional = ProtectedIsNonNone('отсут')

        if self.data_window is None:
            self.data_window = DataWindow(self)
            self.data_window.setWindowTitle("Сверка данных")
            self.data_window.setGeometry(200, 400, 300, 400)

            self.data_window.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            self.data_window = None

        CreatePZ.nkt_diam = 73 if CreatePZ.column_diametr._value > 110 else 60
        CreatePZ.nkt_template = 59.6 if CreatePZ.column_diametr._value > 110 else 47.9

        if CreatePZ.column_additional:
            if CreatePZ.current_bottom > CreatePZ.shoe_column_additional._value:
                CreatePZ.open_trunk_well = True
            else:
                CreatePZ.open_trunk_well = False
        else:
            if CreatePZ.current_bottom > CreatePZ.shoe_column._value:
                CreatePZ.open_trunk_well = True
            else:
                CreatePZ.open_trunk_well = False


class Well_perforation(FindIndexPZ):
    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.ws = ws
        self.read_well(self.ws, CreatePZ.data_pvr_min._value, CreatePZ.data_pvr_max._value + 1)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ
        from krs import is_number, calculationFluidWork

        CreatePZ.old_version = True
        col_old_open_index = 0
        bokov_stvol = False
        osnov_stvol = False
        for row in ws.iter_rows(min_row=begin_index + 1, max_row=cancel_index + 2, values_only=True):
            # print(row)
            for col_index, column in enumerate(row):
                if 'оризонт'.lower() in str(column).lower() or 'пласт/'.lower() in str(column).lower():
                    col_plast_index = col_index - 1
                    print(f'пласт {col_plast_index}')
                if 'по вертикали'.lower() in str(column).lower():
                    col_vert_index = col_index - 1
                    print(f'вер {col_index}')
                if 'кровля'.lower() in str(column).lower():
                    col_roof_index = col_index - 1
                    # print(f'кров {col_index}')
                if 'подошва'.lower() in str(column).lower():
                    # print(f'подо {col_index}')
                    col_sole_index = col_index - 1
                if 'вскрытия'.lower() in str(column).lower():
                    # print(f'вскр {col_index}')
                    col_open_index = col_index - 1
                if 'отключ'.lower() in str(column).lower():
                    # print(f'октл {col_index}')
                    col_close_index = col_index - 1
                if 'удлине'.lower() in str(column).lower():
                    # print(f'удл {col_index}')
                    col_udlin_index = col_index - 1
                if 'Рпл'.lower() in str(column).lower():
                    # print(f'Рпл {col_index}')
                    col_pressuar_index = col_index - 1
                if 'замера' in str(column).lower():
                    # print(f'заме {col_index}')
                    col_date_pressuar_index = col_index - 1
                if 'вскрыт'.lower() in str(column).lower() and 'откл'.lower() in str(column).lower():
                    CreatePZ.old_version = True
                    col_old_open_index = col_index - 1
                if "сновной" in str(column).lower():
                    osnov_stvol = True
                if "боков" in str(column).lower():
                    bokov_stvol = True

        if osnov_stvol is True and bokov_stvol is True:
            mes = QMessageBox.warning(self, 'ОШИБКА', 'Ошибка в определении рабочий интервалов перфорации')
            begin_index = QInputDialog.getInt(self, 'Индекс начала', 'ВВедите индекс начала рабочих интервалов ПВР',
                                              0, 0, 300)[0] - 3

            cancel_index = QInputDialog.getInt(self, 'Индекс начала',
                                               'ВВедите индекс окончания рабочих интервалов ПВР', 0, 0, 300)[0] - 2

        perforations_intervals = []
        for row_index, row in enumerate(
                ws.iter_rows(min_row=begin_index + 3, max_row=cancel_index + 2)):
            lst = []

            if str(row[col_roof_index + 1].value).replace('.', '').replace(',', '').isdigit():
                if row[1].value != None:
                    plast = row[1].value
                    lst.append(plast)
                else:
                    lst.append(plast)

                for col in row[2:13]:

                    lst.append(col.value)

            if all([str(i).strip() == 'None' or i is None for i in lst]) is False:
                perforations_intervals.append(lst)
        print(perforations_intervals)
        for ind, row in enumerate(perforations_intervals):
            plast = row[col_plast_index]
            print(f'пласт {plast}')
            if plast is None:
                plast = perforations_intervals[ind - 1][col_plast_index]
            print(f'пластs {plast}')

            if any(['проект' in str((i)).lower() or 'не пер' in str((i)).lower() for i in row]) is False and all(
                    [str(i).strip() is None for i in row]) is False and is_number(row[col_roof_index]) is True \
                    and is_number(row[col_sole_index]) is True:
                # print(f'5 {row}')

                if is_number(str(row[col_vert_index]).replace(',', '.')) is True:
                    CreatePZ.dict_perforation.setdefault(plast,
                                                         {}).setdefault('вертикаль',
                                                                        set()).add(float(
                        str(row[col_vert_index]).replace(',', '.')))
                if any(['фильтр' in str(i).lower() for i in row]):
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', True)
                else:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                roof_int = round(float(str(row[col_roof_index]).replace(',', '.')), 1)
                sole_int = round(float(str(row[col_sole_index]).replace(',', '.')), 1)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('интервал', set()).add((roof_int, sole_int))
                CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('интервал', set()).add(
                    (roof_int, sole_int))
                # for interval in list(CreatePZ.dict_perforation[plast]["интервал"]):
                # print(interval)

                # print(f' эни {(interval[0],(roof_int, sole_int), interval[1])}, {interval[0] < roof_int < interval[1] or interval[0] < sole_int < interval[1]}')
                if any([interval[0] < roof_int < interval[1] or interval[0] < sole_int < interval[1] for interval in
                        list(CreatePZ.dict_perforation[plast]['интервал'])]):
                    # print(f'интервалы {CreatePZ.dict_perforation[plast]["интервал"]}')
                    for perf_int in [
                        sorted(list(CreatePZ.dict_perforation[plast]['интервал']), key=lambda x: x[0], reverse=False),
                        sorted(list(CreatePZ.dict_perforation[plast]['интервал']), key=lambda x: x[0], reverse=True)]:
                        for interval in sorted(perf_int):
                            # print(f'{interval[0], interval[1]},проверяемый {roof_int, sole_int}')
                            # print(interval[0] < roof_int < interval[1], interval[0] < sole_int < interval[1] )
                            if interval[0] < roof_int < interval[1] is False and interval[0] < sole_int < interval[
                                1] is False:
                                # print(f'удаление1 {roof_int, sole_int}, добавление{interval[0], sole_int}')
                                CreatePZ.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation[plast]['интервал'].add((roof_int, round(interval[1])))
                                CreatePZ.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].add(
                                    (roof_int, round(interval[1], 1)))

                            elif interval[0] < roof_int < interval[1] is False and interval[0] < sole_int < interval[1]:
                                # print(f'удаление2 {roof_int, sole_int}, добавление{interval[0], sole_int}')
                                CreatePZ.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation[plast]['интервал'].add((round(interval[0], 1), sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].add(
                                    (round(interval[0], 1), sole_int))

                            elif interval[0] < roof_int < interval[1] and interval[0] < sole_int < interval[1] is False:
                                # print(f'удаление3 {roof_int, sole_int}, добавление{roof_int, round(interval[1],1)}')
                                CreatePZ.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation[plast]['интервал'].add((roof_int, round(interval[1], 1)))
                                CreatePZ.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].add(
                                    (roof_int, round(interval[1], 1)))

                            elif interval[0] < roof_int < interval[1] and interval[0] < sole_int < interval[1]:
                                # print(f'удаление {roof_int, sole_int}')
                                CreatePZ.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                CreatePZ.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))

                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('вскрытие', set()).add(row[col_open_index])

                if col_old_open_index != col_open_index:
                    if row[col_close_index] is None or row[col_close_index] == '-':
                        CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
                        CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', False)
                    else:
                        CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', True)
                        CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', True)
                else:
                    if isinstance(row[col_old_open_index], datetime):
                        CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
                        CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', False)
                    else:
                        CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', True)
                        CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', True)

                zhgs = 1.01
                if str(row[col_pressuar_index]).replace(',', '').replace('.', '').isdigit() and row[col_vert_index]:
                    data_p = float(str(row[col_pressuar_index]).replace(',', '.'))
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('давление',
                                                                               set()).add(round(data_p, 1))
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     set()).add(round(data_p, 1))
                    zhgs = calculationFluidWork(float(row[col_vert_index]), float(data_p))
                else:
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     set()).add('0')
                if zhgs:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(zhgs)
                if row[col_date_pressuar_index]:
                    CreatePZ.dict_perforation.setdefault(
                        plast, {}).setdefault('замер', set()).add(row[col_date_pressuar_index])

            elif any([str((i)).lower() == 'проект' for i in row]) is True and all(
                    [str(i).strip() is None for i in row]) == False and is_number(row[col_roof_index]) is True \
                    and is_number(
                float(
                    str(row[col_roof_index]).replace(',', '.'))) is True: # Определение проектных интервалов перфорации
                roof_int = round(float(str(row[col_roof_index]).replace(',', '.')), 1)
                sole_int = round(float(str(row[col_sole_index]).replace(',', '.')), 1)
                print(roof_int, sole_int)
                if row[col_vert_index] != None:
                    CreatePZ.dict_perforation_project.setdefault(
                        plast, {}).setdefault('вертикаль', set()).add(round(float(row[col_vert_index]), 1))
                CreatePZ.dict_perforation_project.setdefault(
                    plast, {}).setdefault('интервал', set()).add((roof_int, sole_int))

                if row[col_pressuar_index] != None:
                    # print(f'давление {row[col_pressuar_index]}')
                    CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('давление', set()).add(
                        round(float(row[col_pressuar_index]), 1))
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(
                    calculationFluidWork(row[col_vert_index], row[col_pressuar_index]))

        if len(CreatePZ.dict_perforation_project) != 0:
            CreatePZ.plast_project = list(CreatePZ.dict_perforation_project.keys())

        if self.perforation_correct_window2 is None:
            self.perforation_correct_window2 = PerforationCorrect(self)
            self.perforation_correct_window2.setWindowTitle("Сверка данных перфорации")
            self.perforation_correct_window2.setGeometry(200, 400, 100, 400)

            self.perforation_correct_window2.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
            self.perforation_correct_window2 = None
            CreatePZ.definition_plast_work(self)
        else:
            self.perforation_correct_window2.close()
            self.perforation_correct_window2 = None

        if len(CreatePZ.dict_perforation_project) != 0:
            CreatePZ.plast_project = list(CreatePZ.dict_perforation_project.keys())


class Well_Category(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super(Well_Category, self).__init__(ws)
        self.read_well(ws, CreatePZ.cat_well_min._value, CreatePZ.data_well_min._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ
        print(f'индекс катего {begin_index, cancel_index}')
        for row in range(begin_index, cancel_index):
            for col in range(1, 13):
                cell = ws.cell(row=row, column=col).value
                if cell:

                    if 'по Pпл' in str(cell):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            # print(col)
                            if str(col) in ['атм'] and ws.cell(row=row, column=column - 2).value:
                                CreatePZ.cat_P_1.append(ws.cell(row=row, column=column - 2).value)
                              # print(CreatePZ.cat_P_P)
                                CreatePZ.cat_P_P.append(ws.cell(row=row, column=column - 1).value)

                    elif 'по H2S' in str(cell) and 'по H2S' not in str(
                            ws.cell(row=row - 1, column=2).value):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            # print(col)
                            if str(col) in ['%', 'мг/л', 'мг/дм3', 'мг/м3'] and \
                                    ws.cell(row=row, column=column - 2).value:
                                CreatePZ.cat_H2S_list.append(ws.cell(row=row, column=column - 2).value)

                    elif 'газовому фактору' in str(cell):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            if str(col) in ['м3/т']:
                                CreatePZ.cat_gaz_f_pr.append(ws.cell(row=row, column=column - 2).value)


                    elif 'мг/л' in str(cell) or 'мг/дм3' in str(cell):
                        cell2 = ws.cell(row=row, column=col - 1).value
                        if cell2:
                            CreatePZ.H2S_mg.append(float(self.check_str_None(cell2)))
                    elif 'м3/т' in str(cell):
                        cell2 = ws.cell(row=row, column=col - 1).value
                        if cell2:
                            CreatePZ.gaz_f_pr.append(round(float(self.check_str_None(cell2)), 1))
                    elif '%' in str(cell):
                        cell2 = ws.cell(row=row, column=col - 1).value
                        print(f'проц {cell2}')
                        CreatePZ.H2S_pr.append(float(str(self.check_str_None(cell2)).replace(',', '.')))

                    elif str(cell) in 'мг/м3':
                        cell2 = ws.cell(row=row, column=col - 1).value
                        if cell2:
                            CreatePZ.H2S_mg_m3.append(float(str(self.check_str_None(cell2)).replace(',', '.')) / 1000)

        if self.data_window is None:
            self.data_window = CategoryWindow(self)
            self.data_window.setWindowTitle("Сверка данных")
            self.data_window.setGeometry(200, 200, 200, 200)
            self.data_window.show()
            CreatePZ.pause_app(self)
            CreatePZ.pause = True
        else:
            self.data_window.close()
            self.data_window = None

        if len(CreatePZ.H2S_pr) == 0:
            mes = QMessageBox.warning(self, 'Ошибка', 'Программа не смогла найти данные по содержания '
                                                      'сероводорода в процентах')
            H2S_pr, _ = QInputDialog.getDouble(self, 'сероводород в процентах',
                                               'Введите значение серовородода в процентах', 0, 0, 100, 5)

            CreatePZ.H2S_pr.append(H2S_pr)

# wb = load_workbook('Копия 358 ПНЛГ  (Толбазинское 358) ПНЛГ на Дпаш.xlsx', data_only=True)
# name_list = wb.sheetnames
# old_index = 1
# ws = wb.active
#
# # Создаем экземпляр класса FindIndexPZ
# find_index = FindIndexPZ(ws)
# find_index.readPZ(ws)
# # Получаем значение атрибута cat_well_min
# cat_well_min = find_index.cat_well_min
# cat_well_max = find_index.cat_well_max
#
# d = Well_Category(ws)
# d.read_well(cat_well_min, cat_well_max)
# data_pvr_min = find_index.data_pvr_min
# data_pvr_max = find_index.data_pvr_max
# data_fond_min = find_index.data_fond_min
# sucker_rod_ind = find_index.sucker_rod_ind
# pipes_ind = find_index.pipes_ind
# condition_of_wells = find_index.condition_of_wells
# data_well_max = find_index.data_well_max
# data_x_max = find_index.data_x_max
# a = Well_expected_pick_up()
#
# a.read_well(data_well_max, data_x_max)
# # Используем значение атрибута cat_well_min
#
# print(a.proc_water, a.Qwater, a.Qoil)
