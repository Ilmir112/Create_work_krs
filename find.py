from datetime import datetime

from PyQt5.QtWidgets import QInputDialog, QMainWindow
from openpyxl import load_workbook


class ProtectedIsDigit(property):
    def __init__(self, default_value=None, name=None):
        self._value = default_value
        self._name = name

    def __get__(self, instance, owner):
        if not instance:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if value is not None and str(value).replace(",", "").replace(".", "").isdigit():
            instance.__dict__[self._name] = float(str(value).replace(" ", "").replace(",", "."))
        else:
            print(f'Ошибка: {value} - не корректное числовое значение')
            raise ValueError("Значение должно быть числовое")


class ProtectedIsNonNone(property):
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
        if isinstance(string, int) is True or isinstance(string, float) is True:
            return string
        elif string == '-' or string == 'отсутствует' or string == 'отсутв' or string == 'отсут' or string is None:
            return None
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
            # print(data._value, row, col, step, m)
            while data._value is None or step == m:
                data = ProtectedIsDigit(self.ws.cell(row=row, column=col + step).value)
                step += 1
            return data
        except:
            # print(data, row, col, step, m)
            while data is None or step == m:
                data = ProtectedIsDigit(self.ws.cell(row=row, column=col + step).value)
                step += 1
            return data


class Well_Category(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super(Well_Category, self).__init__(ws)

        self.read_well(ws, CreatePZ.cat_well_min._value, CreatePZ.data_well_min._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        for row in range(begin_index, cancel_index):
            for col in range(1, 13):
                cell = ws.cell(row=row, column=col).value
                if cell:

                    if 'по Pпл' in str(cell):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            # print(col)
                            if str(col) in ['1', '2', '3']:
                                CreatePZ.cat_P_1.append(int(col))
                    elif 'по H2S' in str(cell) and 'по H2S' not in str(
                            ws.cell(row=row - 1, column=2).value):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            if str(col) in ['1', '2', '3']:
                                CreatePZ.cat_H2S_list.append(int(col))
                    elif 'газовому фактору' in str(cell):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            if str(col) in ['1', '2', '3']:
                                CreatePZ.cat_gaz_f_pr.append(int(col))
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
                        if cell2:
                            CreatePZ.H2S_pr.append(float(str(self.check_str_None(cell2)).replace(',', '.')))

                    elif str(cell) in 'мг/м3':
                        cell2 = ws.cell(row=row, column=col - 1).value
                        if cell2:
                            CreatePZ.H2S_mg_m3.append(float(str(self.check_str_None(cell2)).replace(',', '.')) / 1000)
        # print(f'H2S {CreatePZ.H2S_pr, CreatePZ.H2S_mg}')
        if CreatePZ.cat_H2S_list[0] in [1, 2]:
            if len(CreatePZ.H2S_mg) == 0:
                H2S_mg = float(QInputDialog.getDouble(self, 'Сероводород',
                                                      'Введите содержание сероводорода в мг/л', 50, 0,
                                                      1000, 2)[0])
                CreatePZ.H2S_mg.append(H2S_mg)

            if len(CreatePZ.H2S_pr) == 0:
                H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                                'Введите содержание сероводорода в мг/л', 50, 0, 1000,
                                                2)
                CreatePZ.H2S_mg.append(H2S_pr)


class Well_data(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.ws = ws

        self.read_well(self.ws, CreatePZ.cat_well_max._value, CreatePZ.data_pvr_min._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

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

                        CreatePZ.bottomhole_artificial = ProtectedIsDigit(row[col + 2].value)
                        CreatePZ.bottomhole_artificial = \
                            FindIndexPZ.definition_is_None(self, CreatePZ.bottomhole_drill, row_index, col, 5)

                    elif 'зенитный угол' in str(value).lower():
                        CreatePZ.max_angle = ProtectedIsDigit(row[col + 4].value)
                        for index, col1 in enumerate(row):
                            if 'на глубине' in str(col1.value):
                                CreatePZ.max_angle_H = ProtectedIsDigit(row[index + 1])

                    elif 'текущий забой' in str(value).lower() and len(value) < 15:
                        CreatePZ.current_bottom = row[col + 2].value
                        CreatePZ.current_bottom = \
                            FindIndexPZ.definition_is_None(self, CreatePZ.current_bottom, row_index, col, 2)

                        CreatePZ.bottom = CreatePZ.current_bottom
                    elif '10. Расстояние от стола ротора до среза муфты э/колонны ' in str(value):
                        CreatePZ.stol_rotora = ProtectedIsDigit(row[col + 4].value)

                    elif 'Направление' in str(value) and 'Шахтное направление' not in str(value) and \
                            ws.cell(row=row_index + 1, column=col + 1).value != None:
                        CreatePZ.column_direction_True = True

                        for col1, cell in enumerate(row):
                            if 'Уровень цемента' in str(cell.value):
                                CreatePZ.level_cement_direction = ProtectedIsDigit(
                                    str(row[col1 + 2].value.split('-')[0]).replace(" ", ""))
                        try:
                            column_direction_data = row[col + 3].value.split('(мм),')
                            try:
                                CreatePZ.column_direction_diametr = ProtectedIsDigit(column_direction_data[0])

                            except:
                                CreatePZ.column_direction_diametr = 'не корректно'

                            try:
                                CreatePZ.column_direction_wall_thickness = ProtectedIsDigit(column_direction_data[0])
                            except:
                                CreatePZ.column_direction_wall_thickness = 'не корректно'
                            try:
                                CreatePZ.column_direction_lenght = ProtectedIsDigit(
                                    column_direction_data[2].split('-')[1].replace('(м)', '').replace(" ", ""))

                            except:
                                CreatePZ.column_direction_lenght = 'не корректно'
                        except:
                            CreatePZ.column_direction_diametr = 'не корректно'
                            CreatePZ.column_direction_wall_thickness = 'не корректно'
                            CreatePZ.column_direction_lenght = 'не корректно'

                    elif 'Кондуктор' in str(value) and \
                            row[col + 3].value not in ['-', '(мм), (мм), -(м)', None]:

                        for col1, cell in enumerate(row):
                            if 'Уровень цемента' in str(cell.value):
                                CreatePZ.level_cement_conductor = ProtectedIsDigit(
                                    str(row[col1 + 2].value.split('-')[0]).replace(' ', ''))

                        try:

                            column_conductor_data = str(row[col + 3].value).split('(мм),', )

                            try:
                                CreatePZ.column_conductor_diametr = ProtectedIsDigit(column_conductor_data[0])
                            except:
                                CreatePZ.column_conductor_diametr = 'не корректно'

                            try:
                                CreatePZ.column_conductor_wall_thickness = \
                                    ProtectedIsDigit(float(column_conductor_data[1]))
                            except:
                                CreatePZ.column_conductor_wall_thickness = 'не корректно'
                            try:
                                CreatePZ.column_conductor_lenght = ProtectedIsDigit(
                                    column_conductor_data[2].split('-')[1].replace('(м)', ''))
                            except:
                                CreatePZ.column_conductor_lenght = 'не корректно'

                        except:
                            CreatePZ.column_conductor_diametr = 'не корректно'
                            CreatePZ.column_conductor_wall_thickness = 'не корректно'
                            CreatePZ.column_conductor_lenght = 'не корректно'
                    elif str(
                            value) == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':

                        try:
                            data_main_production_string = str(ws.cell(row=row_index + 1, column=col + 1).value).split(
                                '(мм),', )
                            try:
                                CreatePZ.column_diametr = ProtectedIsDigit(float(data_main_production_string[0]))
                            except:
                                CreatePZ.column_diametr = 'не корректно'
                            try:
                                CreatePZ.column_wall_thickness = ProtectedIsDigit(float(data_main_production_string[1]))
                            except:
                                CreatePZ.column_wall_thickness = 'не корректно'
                            try:
                                if len(data_main_production_string[-1].split('-')) == 2:

                                    CreatePZ.shoe_column = ProtectedIsDigit(
                                        self.check_str_None(data_main_production_string[-1].split('-')[-1]))
                                else:
                                    CreatePZ.shoe_column = ProtectedIsDigit(
                                        self.check_str_None(data_main_production_string[-1]))
                            except:
                                CreatePZ.shoe_column = 'не корректно'
                        except ValueError:
                            CreatePZ.column_diametr = 'не корректно'
                            CreatePZ.column_wall_thickness = 'не корректно'
                            CreatePZ.shoe_column = 'не корректно'

                    elif 'Уровень цемента за колонной' in str(value):
                        CreatePZ.level_cement_column = ProtectedIsDigit(row[col + 1])
                        CreatePZ.level_cement_column = self.definition_is_None(CreatePZ.level_cement_column, row_index,
                                                                               col, 1)
                    elif 'Рмкп ( э/к и' in str(cell):
                        CreatePZ.pressuar_mkp = ProtectedIsNonNone(row[col + 2].value)
                    elif '6. Конструкция хвостовика' in str(value):

                        data_column_additional = self.check_str_None(ws.cell(row=row_index + 2, column=col + 2).value)
                        # print(f'доп колонна {self.check_str_None(ws.cell(row=row_index + 2, column=col + 2).value)}')
                        if data_column_additional != None:
                            CreatePZ.column_additional = True

                        if CreatePZ.column_additional is True:

                            try:
                                CreatePZ.head_column_additional = ProtectedIsDigit(data_column_additional[0])
                            except:
                                CreatePZ.head_column_additional = 'не корректно'
                            try:
                                CreatePZ.shoe_column_additional = ProtectedIsDigit(data_column_additional[1])
                            except:
                                CreatePZ.shoe_column_additional = 'не корректно'

                            try:
                                try:
                                    data_add_column = self.check_str_None(
                                        ws.cell(row=row_index + 2, column=col + 4).value)
                                    # print(f' доп колонна {data_add_column}')
                                    CreatePZ.column_additional_diametr = ProtectedIsDigit(data_add_column[0])
                                    CreatePZ.column_additional_wall_thickness = ProtectedIsDigit(data_add_column[1])
                                except:
                                    CreatePZ.column_additional_diametr = ProtectedIsDigit(
                                        self.check_str_None(ws.cell(row=row_index + 2, column=col + 4).value))
                                    CreatePZ.column_additional_wall_thickness = ProtectedIsDigit(
                                        self.check_str_None(ws.cell(row=row_index + 2, column=col + 6).value))

                            except:
                                CreatePZ.column_additional_diametr = 'не корректно'
                        else:
                            CreatePZ.column_additional_diametr = ProtectedIsNonNone('отсут')
                            CreatePZ.column_additional_wall_thickness = ProtectedIsNonNone('отсут')
                            CreatePZ.head_column_additional = ProtectedIsNonNone('отсут')
                            CreatePZ.shoe_column_additional = ProtectedIsNonNone('отсут')
                            # try:
                            #     CreatePZ.column_additional_diametr = \
                            #         ProtectedIsDigit(float(ws.cell(row=row + 3, column=col + 4).value))
                            #     # print(f' диаметр доп колонны {CreatePZ.column_additional_diametr}')
                            # except:
                            #     CreatePZ.column_additional_diametr = 'не корректно'
                            # try:
                            #     CreatePZ.column_additional_wall_thickness = \
                            #         ProtectedIsDigit(float(ws.cell(row=row + 3, column=col + 6).value))
                            # except:
                            #     CreatePZ.column_additional_wall_thickness = 'не корретно'


class Well_perforation(FindIndexPZ):
    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.ws = ws
        self.read_well(self.ws, CreatePZ.data_pvr_min._value, CreatePZ.data_pvr_max._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ
        from krs import is_number, calculationFluidWork

        CreatePZ.old_version = True

        for row in ws.iter_rows(min_row=begin_index - 2, max_row=begin_index + 2, values_only=True):
            if any(['вскрытия' in str(cell) for cell in row]) and any(['отключения' in str(cell) for cell in row]):
                CreatePZ.old_version = False
        # print(begin_index, cancel_index)
        perforations_intervals = []
        for row_index, row in enumerate(
                ws.iter_rows(min_row=begin_index + 3, max_row=cancel_index)):  # Сортировка интервала перфорации
            lst = []
            # print(row[3].value)
            if str(row[3].value).replace('.', '').replace(',', '').isdigit():
                for col in row[1:13]:
                    cell = col.value
                    lst.append(cell)

                # print(ws.cell(row=row, column=6).value)
                if CreatePZ.old_version is True and isinstance(ws.cell(row=row_index, column=6).value,
                                                               datetime) is True:
                    lst.insert(5, None)
                elif CreatePZ.old_version is True and isinstance(ws.cell(row=row_index, column=6).value,
                                                                 datetime) is False and not ws.cell(row=row_index,
                                                                                                    column=5).value is None:
                    lst.insert(5, 'отключен')
                # print(lst)
                if all([str(i).strip() == 'None' or i is None for i in lst]) is False:
                    perforations_intervals.append(lst)

        for ind, row in enumerate(sorted(perforations_intervals, key=lambda x: float(x[2]))):
            plast = row[0]
            if plast is None:
                plast = perforations_intervals[ind - 1][0]
                perforations_intervals[ind][0] = perforations_intervals[ind - 1][0]
            if any(['проект' in str((i)).lower() or 'не пер' in str((i)).lower() for i in row]) is False and all(
                    [str(i).strip() is None for i in row]) is False and is_number(row[2]) is True \
                    and is_number(float(str(row[3]))) is True:
                # print(f'5 {row}')

                if is_number(str(row[1]).replace(',', '.')) is True:
                    CreatePZ.dict_perforation.setdefault(plast,
                                                         {}).setdefault('вертикаль',
                                                                        set()).add(float(str(row[1]).replace(',', '.')))
                if any(['фильтр' in str(i).lower() for i in row]):
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', True)
                else:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                roof_int = round(float(str(row[2]).replace(',', '.')), 1)
                sole_int = round(float(str(row[3]).replace(',', '.')), 1)
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

                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('вскрытие', set()).add(row[4])
                # print(f'отключе {isinstance(row[5], datetime) == True, old_index} ggg {isinstance(row[6], datetime) == True, CreatePZ.old_version, old_index}')
                if row[5] is None or row[5] == '-':
                    # print(f'отключение {plast, row[5], row[5] != "-"}')
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', False)

                else:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отключение', True)
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', True)

                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                if row[8] != None:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('удлинение', set()).add(row[8])

                zhgs = 1.01
                if str(row[9]).replace(',', '').replace('.', '').isdigit() and row[1]:
                    data_p = float(str(row[9]).replace(',', '.'))
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('давление',
                                                                               set()).add(round(data_p, 1))
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     set()).add(round(data_p, 1))
                    zhgs = calculationFluidWork(float(row[1]), float(data_p))
                else:
                    CreatePZ.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     set()).add('0')
                if zhgs:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(zhgs)
                if row[10]:
                    CreatePZ.dict_perforation.setdefault(plast, {}).setdefault('замер', set()).add(row[10])

            elif any([str((i)).lower() == 'проект' for i in row]) is True and all(
                    [str(i).strip() is None for i in row]) == False and is_number(row[2]) is True \
                    and is_number(
                float(str(row[2]).replace(',', '.'))) is True:  # Определение проектных интервалов перфорации
                if row[1] != None:
                    CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('вертикаль',
                                                                                       set()).add(
                        round(float(row[1]), 1))
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('интервал', set()).add(
                    (round(float(str(row[2]).replace(',', '.')), 1), round(float(str(row[3]).replace(',', '.')), 1)))
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                if row[8] != None:
                    CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('удлинение', set()).add(
                        round(float(row[8]), 1))
                if row[9] != None:
                    # print(f'давление {row[9]}')
                    CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('давление', set()).add(
                        round(float(row[9]), 1))
                CreatePZ.dict_perforation_project.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(
                    calculationFluidWork(row[1], row[9]))

        if len(CreatePZ.dict_perforation_project) != 0:
            CreatePZ.plast_project = list(CreatePZ.dict_perforation_project.keys())


class WellHistory_data(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.ws = ws

        self.read_well(self.ws, CreatePZ.data_pvr_max._value, CreatePZ.data_fond_min._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        # print(begin_index, cancel_index)
        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            for col, cell in enumerate(row):
                value = cell.value
                if value:

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

                    elif 'Максимально допустимое давление опрессовки э/колонны' == value \
                            or 'Максимально допустимое давление на э/колонну' == value:
                        CreatePZ.max_admissible_pressure = ProtectedIsDigit(row[col + 1].value)
                        CreatePZ.max_admissible_pressure = self.definition_is_None(
                            CreatePZ.max_admissible_pressure, row_index + begin_index, col + 1, 1)


class WellFond_data(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.read_well(ws, CreatePZ.data_fond_min._value, CreatePZ.condition_of_wells._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        # print(begin_index, cancel_index)
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
                        # print([ind.value for ind in row])
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
                                CreatePZ.H_F_paker_do["do"] = self.check_str_None(row[col_do].value)[0]
                                CreatePZ.H_F_paker2_do["do"] = self.check_str_None(row[col_do].value)[1]
                        except:
                            if CreatePZ.paker_do["do"] != 0:
                                CreatePZ.H_F_paker_do["do"] = row[col_do].value
                        try:
                            if CreatePZ.paker_do["posle"] != 0:
                                CreatePZ.H_F_paker_do["posle"] = self.check_str_None(row[col_plan].value)[0]
                                CreatePZ.H_F_paker2_do["posle"] = self.check_str_None(row[col_plan].value)[1]
                        except:
                            if CreatePZ.paker_do["posle"] != 0:
                                CreatePZ.H_F_paker_do["posle"] = row[col_plan].value


class WellNkt(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)

        self.read_well(ws, CreatePZ.pipes_ind._value, CreatePZ.condition_of_wells._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        a_plan = 0

        for row in range(begin_index, cancel_index):  # словарь  количества НКТ и метраж

            if ws.cell(row=row, column=3).value == 'План' or str(
                    ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                a_plan = row
        if a_plan == 0:
            a_plan = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                            'Программа не могла определить начала строку с ПЗ НКТ - план')
        # print(f'индекс a_plan {a_plan}')
        for row in range(begin_index, cancel_index):
            # print(str(ws.cell(row=row, column=4).value))
            key = str(ws.cell(row=row, column=4).value)
            if key != str(None) and key != '-' and "Диам" not in key:
                value = ws.cell(row=row, column=7).value
                if not key is None and row < a_plan:
                    CreatePZ.dict_nkt[key] = CreatePZ.dict_nkt.get(key, 0) + round(float(value), 1)
                elif not key is None and row >= a_plan:
                    CreatePZ.dict_nkt_po[key] = CreatePZ.dict_nkt_po.get(key, 0) + round(float(value), 1)
                # print(f'индекс a_plan {CreatePZ.dict_nkt}')
            # CreatePZ.shoe_nkt = float(sum(CreatePZ.dict_nkt.values()))


class WellSucker_rod(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ
        super().__init__(ws)

        self.read_well(ws, CreatePZ.sucker_rod_ind._value, CreatePZ.pipes_ind._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        if CreatePZ.sucker_rod_ind._value != 0:
            for row in range(begin_index, cancel_index):  # словарь  количества штанг и метраж
                if ws.cell(row=row, column=3).value == 'План' or str(
                        ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                    b_plan = row

            if b_plan == 0:
                b_plan = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                                'Программа не могла определить начала строку с ПЗ штанги - план')
            print(f'б {b_plan}')

            for row in range(begin_index, cancel_index - 1):

                key = str(ws.cell(row=row, column=4).value).replace(' ', '')
                value = ws.cell(row=row, column=7).value
                if key != str(None) and key != '-' and key != '':
                    # print(key, value)
                    if key != None and row < b_plan:
                        CreatePZ.dict_sucker_rod[key] = CreatePZ.dict_sucker_rod.get(key, 0) + int(value + 1)
                    if key != None and row >= b_plan:
                        CreatePZ.dict_sucker_rod_po[key] = CreatePZ.dict_sucker_rod_po.get(key, 0) + int(value)


class WellCondition(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.ws = ws

        self.read_well(ws, CreatePZ.condition_of_wells._value, CreatePZ.data_well_max._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            for col, cell in enumerate(row):
                value = cell.value
                if value:
                    if "Hст " in str(value):
                        CreatePZ.static_level = ProtectedIsDigit(row[col + 1].value)
                    if "грп" in str(value).lower():
                        CreatePZ.grpPlan = True

                    if "Ндин " in str(value):
                        CreatePZ.dinamic_level = ProtectedIsDigit(row[col + 1].value)
                    if "% воды " in str(value):
                        CreatePZ.proc_water = row[col + 1].value
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


class Well_expected_pick_up(FindIndexPZ):

    def __init__(self, ws):
        from open_pz import CreatePZ

        super().__init__(ws)
        self.read_well(ws, CreatePZ.data_x_min._value, CreatePZ.data_well_max._value)

    def read_well(self, ws, begin_index, cancel_index):
        from open_pz import CreatePZ

        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            for col, cell in enumerate(row):
                value = cell.value
                if value:

                    if 'прием' in str(value).lower() or 'qж' in str(value).lower():
                        CreatePZ.expected_Q = row[col + 1].value
                        CreatePZ.expected_Q = self.definition_is_None(CreatePZ.expected_Q, row_index, col +1, 1)
                    if 'зак' in str(value).lower() or 'давл' in str(value).lower() or 'p' in str(value).lower():
                        CreatePZ.expected_P = row[col + 1].value
                        CreatePZ.expected_P = self.definition_is_None(CreatePZ.expected_Q, row_index, col + 1, 1)

                    if 'qж' in str(value).lower():
                        CreatePZ.Qwater = row[col + 1].value
                        CreatePZ.Qwater = self.definition_is_None(CreatePZ.Qwater, row_index, col+1, 1)

                    if 'qн' in str(value).lower():
                        CreatePZ.Qoil = row[col + 1].value
                        CreatePZ.Qoil = self.definition_is_None(CreatePZ.Qoil, row_index, col+1, 1)
                    elif 'воды' in str(value).lower():
                        CreatePZ.proc_water = row[col + 1].value
                        CreatePZ.proc_water = self.definition_is_None(CreatePZ.proc_water, row_index, col+1, 1)

            try:
                CreatePZ.expected_pick_up[CreatePZ.expected_Q] = CreatePZ.expected_P
            except:
                print('Ошибка в определении ожидаемых показателей')

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
