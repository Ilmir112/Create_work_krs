from datetime import datetime

from PyQt5.QtWidgets import QInputDialog, QMainWindow
from openpyxl import load_workbook

from krs import is_number, calculationFluidWork


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
            instance.__dict__[self._name] = value
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
        self.ws = ws
        self.cat_well_min = ProtectedIsDigit('не корректно',self)
        self.cat_well_max = ProtectedIsDigit(0)
        self.data_well_min = ProtectedIsDigit(0)
        self.data_well_max = ProtectedIsDigit(0)
        self.data_x_min = ProtectedIsDigit(0)
        self.data_pvr_max = ProtectedIsDigit(0)
        self.sucker_rod_ind = ProtectedIsDigit('не корректно', self)
        self.pipes_ind = ProtectedIsDigit(0)
        self.data_x_max = ProtectedIsDigit(0)
        self.condition_of_wells = ProtectedIsDigit(0)
        self.data_pvr_min = ProtectedIsDigit()
        self.data_fond_min = ProtectedIsDigit(0)
        self.readPZ(ws)

        # try:
        #     if self.cat_well_min._value == 0:
        #         self.cat_well_min, ok = QInputDialog.getInt(self, 'индекс начала копирования',
        #                                                     'Программа не смогла определить строку начала копирования',
        #                                                     0, 0, 800)
        # except:
        #     pass
        # try:
        #     if self.cat_well_max._value == 0:
        #         self.cat_well_max, ok = QInputDialog.getInt(self, 'индекс начала копирования',
        #                                                     'Программа не смогла определить строку начала копирования',
        #                                                     0, 0, 800)
        # except:
        #     pass
        # try:
        #     if self.data_well_max == 0:
        #         self.data_well_max, ok = QInputDialog.getInt(self, 'индекс окончания копирования',
        #                                                      'Программа не смогла определить строку окончания копирования',
        #                                                      0, 0, 800)
        #
        # except:
        #     pass
        # try:
        #     if self.data_x_max._value == 0:
        #         self.data_x_max, _ = QInputDialog.getInt(self, 'индекс окончания копирования ожидаемых показателей',
        #                                                  'Программа не смогла определить строку окончания копирования'
        #                                                  ' ожидаемых показателей',
        #                                                  0, 0, 800)
        # except:
        #     pass
        # try:
        #
        #     if self.data_x_min._value == 0:
        #         self.data_x_min, _ = QInputDialog.getInt(self, 'индекс начала копирования ожидаемых показателей',
        #                                               'Программа не смогла определить строку начала копирования'
        #                                               ' ожидаемых показателей',
        #                                               0, 0, 800)
        # except:
        #     pass
        # try:
        #
        #     if self.data_well_min._value == 0:
        #         self.data_well_min, ok = QInputDialog.getInt(self, 'индекс начала строки после план заказ',
        #                                                  'Программа не смогла найти начала строки после план заказ',
        #                                                  0, 0, 800)
        # except:
        #     pass
        # try:
        #     if self.data_pvr_max._value == 0:
        #         self.data_pvr_max, ok = QInputDialog.getInt(self, 'индекс начала строки после план заказ',
        #                                                 'Программа не смогла найти "II. История эксплуатации скважины"',
        #                                                 0, 0, 800)
        # except:
        #     pass
        #
        # try:
        #     if self.pipes_ind._value == 0:
        #         self.pipes_ind, ok = QInputDialog.getInt(self, 'индекс начала строки с НКТ',
        #                                              'Программа не смогла найти строку с НКТ',
        #                                              0, 0, 800)
        # except:
        #     pass
        # try:
        #     if self.data_pvr_min._value == 0:
        #         self.data_pvr_min, ok = QInputDialog.getInt(self, 'индекс начала начала ПВР',
        #                                                 'Программа не смогла найти индекс начала ПВР',
        #                                                 0, 0, 800)
        # except:
        #     pass
        # try:
        #
        #     if self.data_fond_min._value == 0:
        #         self.data_fond_min, ok = QInputDialog.getInt(self, 'индекс начала строки с таблицей фондовыго оборудования',
        #                                                  'Программа не смогла найти строку с таблицей фондового оборудования',
        #                                                  0, 0, 800)
        # except:
        #     pass

        print(
            f'cat_min {self.cat_well_min} max{self.cat_well_max} v {self.data_well_min} d {self.data_well_max} f {self.data_x_min}'
            f'd {self.data_pvr_max} fdf {self.sucker_rod_ind} fdswe {self.pipes_ind} asd {self.data_x_max} sdfef {self.condition_of_wells} '
            f'sdfasf {self.data_pvr_min} sdfwe {self.data_fond_min}')


    def readPZ(self, ws):

        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            ws.row_dimensions[row_ind].hidden = False

            if 'Категория скважины' in row:
                self.cat_well_min = row_ind + 1  # индекс начала категории

            elif 'План-заказ' in row:
                print(row)
                # ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'
                self.cat_well_max = row_ind - 1
                self.data_well_min = row_ind + 1
                print(f'строка {self.cat_well_max}')

            elif any(['Ожидаемые показатели после' in str(col) for col in row]):
                self.data_x_min = row_ind
                # print(f' индекс Ожидаемые показатели {self.data_x_min}')
            elif '11. Эксплуатационные горизонты и интервалы перфорации:' in row:
                self.data_pvr_min =row_ind
            elif 'Оборудование скважины ' in row:
                self.data_fond_min = row_ind


            elif any(['IX. Мероприятия по предотвращению' in str(col) for col in row]) or \
                    any(['IX. Мероприятия по предотвращению аварий, инцидентов и осложнений::' in str(col) for col in
                         row]):
                self.data_well_max = row_ind

            elif 'НКТ' == str(row[1]).upper():
                self.pipes_ind = row_ind+1
                print(f'ИНДЕК {self.pipes_ind}')

            elif 'ШТАНГИ' == str(row[1]).upper():
                self.sucker_rod_ind = row_ind+1
                print(f'ИНДЕК штанги{self.sucker_rod_ind}')

            elif 'ХI Планируемый объём работ:' in row or 'ХI. Планируемый объём работ:' in row or 'ХIII Планируемый объём работ:' in row \
                    or 'ХI Планируемый объём работ:' in row or 'Порядок работы' in row:
                self.data_x_max = row_ind


            elif 'II. История эксплуатации скважины' in row:
                self.data_pvr_max = row_ind

            elif 'III. Состояние скважины к началу ремонта ' in row:
                self.condition_of_wells = row_ind

    def definition_is_None(self, data, row, col, step, m = 12):
        print(data, row, col, step, m)
        while data is None or step == m:
            data = self.ws.cell(row=row, column=col + step).value
            step += 1
        return data



class Well_Category(FindIndexPZ):

    def __init__(self, ws):
        super(Well_Category, self).__init__(ws)


        self.cat_P_1 = []
        self.cat_H2S_list = []
        self.cat_gaz_f_pr = []
        self.H2S_mg = []
        self.H2S_pr = []
        self.gaz_f_pr = []
        print(f'gggg{self.cat_well_max}')
        self.read_well(ws, self.cat_well_min, self.data_well_min)

    def read_well(self, ws, begin_index, cancel_index):
        print(begin_index, cancel_index)
        for row in range(begin_index, cancel_index):
            for col in range(1, 13):
                cell = ws.cell(row=row, column=col).value
                if cell:
                    print(cell)
                    if 'по Pпл' in str(cell):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            # print(col)
                            if str(col) in ['1', '2', '3']:
                                self.cat_P_1.append(int(col))
                    elif 'по H2S' in str(cell) and 'по H2S' not in str(
                            ws.cell(row=row - 1, column=2).value):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            if str(col) in ['1', '2', '3']:
                                self.cat_H2S_list.append(int(col))
                    elif 'газовому фактору' in str(cell):
                        for column in range(1, 13):
                            col = ws.cell(row=row, column=column).value
                            if str(col) in ['1', '2', '3']:
                                self.cat_gaz_f_pr.append(int(col))
                    elif 'мг/л' in str(cell) or 'мг/дм3' in str(cell):

                        cell2 = ws.cell(row=row, column=col-1).value
                        if cell2:
                            self.H2S_mg.append(float(str(cell2).replace(',', '.')))
                    elif 'м3/т' in str(cell):
                        cell2 = ws.cell(row=row, column=col-1).value
                        if cell2:
                            self.gaz_f_pr.append(round(float(str(cell2).replace(',', '.')), 1))
                    elif '%' in str(cell):
                        cell2 = ws.cell(row=row, column=col - 1).value
                        if cell2:
                            print(f'jjj {cell2}')
                            self.H2S_pr.append(float(str(cell2).replace(',', '.')))

                    elif str(cell) in 'мг/м3':
                        cell2 = ws.cell(row=row, column=col - 1).value
                        if cell2:
                            self.H2S_mg_m3.append(float(str(cell2).replace(',', '.')) / 1000)
        print(f'H2S {self.H2S_pr, self.H2S_mg}')
        if self.cat_H2S_list[0] in [1, 2]:
            if len(self.H2S_mg) == 0:
                H2S_mg = float(QInputDialog.getDouble(self, 'Сероводород',
                                                      'Введите содержание сероводорода в мг/л', 50, 0,
                                                      1000, 2)[0])
                self.H2S_mg.append(H2S_mg)

            if len(self.H2S_pr) == 0:
                H2S_pr = QInputDialog.getDouble(self, 'Сероводород',
                                                'Введите содержание сероводорода в мг/л', 50, 0, 1000,
                                                2)
                self.H2S_mg.append(H2S_pr)

class Well_data(FindIndexPZ):
    
    def __init__(self, ws):
        super().__init__(ws)
        self.ws =ws
        self.well_well_number = ProtectedIsDigit('не корректно')
        self.well_area = ProtectedIsNonNone('не корректно')
        self.well_oilfield = ProtectedIsNonNone('не корректно')
        self.inv_number = ProtectedIsNonNone('не корректно')
        self.bottomhole_drill = ProtectedIsDigit('не корректно')
        self.bottomhole_artificial = ProtectedIsDigit('не корректно')
        self.current_bottom = ProtectedIsDigit('не корректно')
        self.bottom = self.current_bottom
        self.max_angle = ProtectedIsDigit('не корректно')
        self.max_angle_H = ProtectedIsDigit('не корректно')
        self.stol_rotora = ProtectedIsDigit('не корректно')
        self.column_direction_True = False
        self.column_direction_diametr = ProtectedIsDigit('не корректно')
        self.column_direction_wall_thickness = ProtectedIsDigit('не корректно')
        self.column_direction_lenght = ProtectedIsDigit('не корректно')
        self.column_conductor_diametr = ProtectedIsDigit('не корректно')
        self.column_conductor_wall_thickness = ProtectedIsDigit('не корректно')
        self.column_conductor_lenght = ProtectedIsDigit('не корректно')
        self.level_cement_direction = ProtectedIsDigit('не корректно')
        self.level_cement_conductor = ProtectedIsDigit('не корректно')
        self.column_diametr = ProtectedIsDigit('не корректно')
        self.column_wall_thickness = ProtectedIsDigit('не корректно')
        self.shoe_column = ProtectedIsDigit('не корректно')
        self.head_column_additional = ProtectedIsDigit('не корректно')
        self.shoe_column_additional = ProtectedIsDigit('не корректно')
        self.column_additional_diametr = ProtectedIsDigit('не корректно')
        self.column_additional_wall_thickness = ProtectedIsDigit('не корректно')
        self.cdng = ProtectedIsNonNone('не корректно')
        self.level_cement_column = 0
        self.column_additional = False
        self.read_well(self.ws, self.cat_well_max, self.data_pvr_min)


    def read_well(self, ws, begin_index, cancel_index):
        for row in range(begin_index, cancel_index + 1):
            for col in range(1, 13):
                cell = str(ws.cell(row=row, column=col).value)
                if cell:
                    if 'площадь' in cell:  # определение номера скважины
                        self.well_number = ws.cell(row=row, column=col-1).value
                        self.well_area = ws.cell(row=row, column=col+1).value
                    elif 'месторождение ' in cell:  # определение номера скважины
                        self.well_oilfield = ws.cell(row=row, column=col+2).value
                    elif 'Инв. №' in cell:
                        self.inv_number = ws.cell(row=row, column=col+1).value
                    elif 'цех' == cell:

                        self.cdng = str(ws.cell(row=row, column=col + 1).value)
                        # print(f' ЦДНГ {CreatePZ.cdng}')
                    elif 'пробуренный забой' in cell.lower():

                        self.bottomhole_drill = ws.cell(row=row, column=col+2).value
                        self.bottomhole_drill = FindIndexPZ.definition_is_None(self, self.bottomhole_drill, row, col, 2)

                        self.bottomhole_artificial = ws.cell(row=row, column=col + 5).value
                        self.bottomhole_artificial = \
                            FindIndexPZ.definition_is_None(self, self.bottomhole_drill, row, col, 5)

                    elif 'текущий забой' in cell.lower() and len(cell) < 15:
                        self.current_bottom = ws.cell(row=row, column=col + 2).value
                        self.current_bottom = \
                            FindIndexPZ.definition_is_None(self, self.bottomhole_drill, row, col, 2)

                        self.bottom = self.current_bottom
                    elif '10. Расстояние от стола ротора до среза муфты э/колонны ' in cell:
                        self.stol_rotora = ws.cell(row=row, column=col + 4).value

                    elif 'Направление' in cell and 'Шахтное направление' not in cell and \
                            ws.cell(row=row + 1, column=col + 4).value != 'отсут':
                        self.column_direction_True = True
                        for col in range(1, 13):
                            if 'Уровень цемента' in cell:
                                self.level_cement_direction = str(ws.cell(row=row, column=col+2).value).split('-')[0].replace(' ', '')

                        try:
                            column_direction_data = ws.cell(row=row + 1, column=col + 4).value.split('(мм),')

                            try:
                                self.column_direction_diametr = float(column_direction_data[0])
                            except:
                                self.column_direction_diametr = 'не корректно'

                            try:
                                self.column_direction_wall_thickness = float(column_direction_data[1])
                            except:
                                self.column_direction_wall_thickness = 'не корректно'
                            try:
                                self.column_direction_lenght = float(
                                    column_direction_data[2].split('-')[1].replace('(м)', ''))

                            except:
                                self.column_direction_lenght = 'не корректно'
                        except:
                            self.column_direction_diametr = 'не корректно'
                            self.column_direction_wall_thickness = 'не корректно'
                            self.column_direction_lenght = 'не корректно'
                    elif 'Кондуктор' in cell and \
                            ws.cell(row=row + 1, column=col + 4).value not in ['-', '(мм), (мм), -(м)', None]:
                        for col in range(1, 13):
                            if 'Уровень цемента' in cell:
                                self.level_cement_conductor = str(
                                    ws.cell(row=row, column=col+2).value).split('-')[0].replace(' ', '')

                        try:
                            column_conductor_data = (ws.cell(row=row + 1, column=col + 4).value).split('(мм),', )

                            try:
                                self.column_conductor_diametr = float(column_conductor_data[0])
                            except:
                                self.column_conductor_diametr = 'не корректно'
                            try:
                                self.column_conductor_wall_thickness = float(column_conductor_data[1])
                            except:
                                self.column_conductor_wall_thickness = 'не корректно'
                            try:

                                self.column_conductor_lenght = float(
                                    column_conductor_data[2].split('-')[1].replace('(м)', ''))
                            except:
                                self.column_conductor_lenght = 'не корректно'

                        except:
                            self.column_conductor_diametr = 'не корректно'
                            self.column_conductor_wall_thickness = 'не корректно'
                            self.column_conductor_lenght = 'не корректно'
                    elif cell == '4. Эксплуатационная колонна (диаметр(мм), толщина стенки(мм), глубина спуска(м))':
                        print(row,col, ws.cell(row=row + 1, column=col).value)
                        try:
                            data_main_production_string = (ws.cell(row=row + 1, column=col).value).split('(мм),', )
                            try:
                                self.column_diametr = float(data_main_production_string[0])
                            except:
                                self.column_diametr = 'не корректно'
                            try:
                                self.column_wall_thickness = float(data_main_production_string[1])
                            except:
                                self.column_wall_thickness =  'не корректно'
                            try:
                                if len(data_main_production_string[-1].split('-')) == 2:

                                    self.shoe_column = data_main_production_string[-1].split('-')[-1]
                                elif len(data_main_production_string[-1].split('(м)')) == 2:
                                    self.shoe_column = data_main_production_string[-1]
                            except:
                                self.shoe_column = 'не корректно'
                        except ValueError:
                            self.column_diametr = 'не корректно'
                            self.column_wall_thickness = 'не корректно'
                            self.shoe_column = 'не корректно'
                    elif 'Уровень цемента за колонной' in str(cell):
                        self.level_cement_column = str(ws.cell(row=row, column=col+2).value)
                        self.level_cement_column = self.definition_is_None(self.level_cement_column, row, col, 1)
                    elif 'Рмкп ( э/к и' in str(cell):
                        self.pressuar_mkp = str(ws.cell(row=row, column=col+2).value)
                    elif '6. Конструкция хвостовика' in str(cell):
                        self.data_column_additional = ws.cell(row=row + 2, column=col + 1).value
                        if self.data_column_additional:
                            self.column_additional = True

                        if self.column_additional is True:
                            try:
                                self.head_column_additional = float(self.data_column_additional.split('-')[0])
                            except:
                                self.head_column_additional = 'не корректно'
                            try:
                                self.shoe_column_additional = float(self.data_column_additional.split('-')[1])
                            except:
                                self.shoe_column_additional = 'не корректно'
                            try:
                                if ws.cell(row=row + 3, column=col + 4).value.split('x') == 2:
                                    self.column_additional_diametr = \
                                        ws.cell(row=row + 3, column=col + 4).value.split('x')[0]
                                    self.column_additional_wall_thickness = \
                                        ws.cell(row=row + 3, column=col + 4).value.split('x')[1]
                            except:
                                self.column_additional_diametr = 'не корректно'
                            try:
                                self.column_additional_diametr = float(ws.cell(row=row + 3, column=col + 4).value)
                                # print(f' диаметр доп колонны {self.column_additional_diametr}')
                            except:
                                self.column_additional_diametr = 'не корректно'
                            try:
                                self.column_additional_wall_thickness = float(
                                    ws.cell(row=row + 3, column=col + 6).value)
                            except:
                                self.column_additional_wall_thickness = 'не корретно'


class Well_perforation(FindIndexPZ):
    def __init__(self, ws):
        super().__init__(ws)
        self.ws =ws
        self.dict_perforation = {}
        self.dict_perforation_short = {}
        self.dict_perforation_project = {}
        self.read_well(self.ws, self.data_pvr_min, self.data_pvr_max)
        

    def read_well(self, ws, begin_index, cancel_index):
        self.old_version = True
        print()
        for row in ws.iter_rows(min_row=begin_index - 2, max_row=begin_index + 2, values_only=True):
            if any(['вскрытия' in str(cell) for cell in row]) and any(['отключения' in str(cell) for cell in row]):
                self.old_version = False
        print(begin_index, cancel_index)
        perforations_intervals = []
        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index+3, max_row=cancel_index)):  # Сортировка интервала перфорации
            lst = []
            # print(row[3].value)
            if str(row[3].value).replace('.', '').replace(',', '').isdigit():
                for col in row[1:13]:
                    cell = col.value
                    lst.append(cell)

                # print(ws.cell(row=row, column=6).value)
                if self.old_version is True and isinstance(ws.cell(row=row_index, column=6).value, datetime) is True:
                    lst.insert(5, None)
                elif self.old_version is True and isinstance(ws.cell(row=row_index, column=6).value,
                                                                 datetime) is False and not ws.cell(row=row_index,
                                                                                                    column=5).value is None:
                    lst.insert(5, 'отключен')
                # print(lst)
                if all([str(i).strip() == 'None' or i is None for i in lst]) is False:
                    perforations_intervals.append(lst)

        print(perforations_intervals)
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
                    self.dict_perforation.setdefault(plast,
                                                         {}).setdefault('вертикаль',
                                                                        set()).add(float(str(row[1]).replace(',', '.')))
                if any(['фильтр' in str(i).lower() for i in row]):
                    self.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', True)
                else:
                    self.dict_perforation.setdefault(plast, {}).setdefault('отрайбировано', False)
                self.dict_perforation.setdefault(plast, {}).setdefault('Прошаблонировано', False)
                roof_int = round(float(str(row[2]).replace(',', '.')), 1)
                sole_int = round(float(str(row[3]).replace(',', '.')), 1)
                self.dict_perforation.setdefault(plast, {}).setdefault('интервал', set()).add((roof_int, sole_int))
                self.dict_perforation_short.setdefault(plast, {}).setdefault('интервал', set()).add(
                    (roof_int, sole_int))
                # for interval in list(self.dict_perforation[plast]["интервал"]):
                # print(interval)
                # print(f' эни {(interval[0],(roof_int, sole_int), interval[1])}, {interval[0] < roof_int < interval[1] or interval[0] < sole_int < interval[1]}')
                if any([interval[0] < roof_int < interval[1] or interval[0] < sole_int < interval[1] for interval in
                        list(self.dict_perforation[plast]['интервал'])]):
                    # print(f'интервалы {self.dict_perforation[plast]["интервал"]}')
                    for perf_int in [
                        sorted(list(self.dict_perforation[plast]['интервал']), key=lambda x: x[0], reverse=False),
                        sorted(list(self.dict_perforation[plast]['интервал']), key=lambda x: x[0], reverse=True)]:
                        for interval in sorted(perf_int):
                            # print(f'{interval[0], interval[1]},проверяемый {roof_int, sole_int}')
                            # print(interval[0] < roof_int < interval[1], interval[0] < sole_int < interval[1] )
                            if interval[0] < roof_int < interval[1] is False and interval[0] < sole_int < interval[
                                1] is False:
                                # print(f'удаление1 {roof_int, sole_int}, добавление{interval[0], sole_int}')
                                self.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                self.dict_perforation[plast]['интервал'].add((roof_int, round(interval[1])))
                                self.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                self.dict_perforation_short[plast]['интервал'].add(
                                    (roof_int, round(interval[1], 1)))

                            elif interval[0] < roof_int < interval[1] is False and interval[0] < sole_int < interval[1]:
                                # print(f'удаление2 {roof_int, sole_int}, добавление{interval[0], sole_int}')
                                self.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                self.dict_perforation[plast]['интервал'].add((round(interval[0], 1), sole_int))
                                self.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                self.dict_perforation_short[plast]['интервал'].add(
                                    (round(interval[0], 1), sole_int))

                            elif interval[0] < roof_int < interval[1] and interval[0] < sole_int < interval[1] is False:
                                # print(f'удаление3 {roof_int, sole_int}, добавление{roof_int, round(interval[1],1)}')
                                self.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                self.dict_perforation[plast]['интервал'].add((roof_int, round(interval[1], 1)))
                                self.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))
                                self.dict_perforation_short[plast]['интервал'].add(
                                    (roof_int, round(interval[1], 1)))

                            elif interval[0] < roof_int < interval[1] and interval[0] < sole_int < interval[1]:
                                # print(f'удаление {roof_int, sole_int}')
                                self.dict_perforation[plast]['интервал'].discard((roof_int, sole_int))
                                self.dict_perforation_short[plast]['интервал'].discard((roof_int, sole_int))

                self.dict_perforation.setdefault(plast, {}).setdefault('вскрытие', set()).add(row[4])
                # print(f'отключе {isinstance(row[5], datetime) == True, old_index} ggg {isinstance(row[6], datetime) == True, self.old_version, old_index}')
                if row[5] is None or row[5] == '-':
                    # print(f'отключение {plast, row[5], row[5] != "-"}')
                    self.dict_perforation.setdefault(plast, {}).setdefault('отключение', False)
                    self.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', False)

                else:
                    self.dict_perforation.setdefault(plast, {}).setdefault('отключение', True)
                    self.dict_perforation_short.setdefault(plast, {}).setdefault('отключение', True)

                self.dict_perforation.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                self.dict_perforation.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                if row[8] != None:
                    self.dict_perforation.setdefault(plast, {}).setdefault('удлинение', set()).add(row[8])

                zhgs = 1.01
                if str(row[9]).replace(',', '').replace('.', '').isdigit() and row[1]:
                    data_p = float(str(row[9]).replace(',', '.'))
                    self.dict_perforation.setdefault(plast, {}).setdefault('давление',
                                                                               set()).add(round(data_p, 1))
                    self.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     set()).add(round(data_p, 1))
                    zhgs = calculationFluidWork(float(row[1]), float(data_p))
                else:
                    self.dict_perforation_short.setdefault(plast, {}).setdefault('давление',
                                                                                     set()).add('0')
                if zhgs:
                    self.dict_perforation.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(zhgs)
                if row[10]:
                    self.dict_perforation.setdefault(plast, {}).setdefault('замер', set()).add(row[10])

            elif any([str((i)).lower() == 'проект' for i in row]) is True and all(
                    [str(i).strip() is None for i in row]) == False and is_number(row[2]) is True \
                    and is_number(
                float(str(row[2]).replace(',', '.'))) is True:  # Определение проектных интервалов перфорации
                if row[1] != None:
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('вертикаль',
                                                                                       set()).add(
                        round(float(row[1]), 1))
                self.dict_perforation_project.setdefault(plast, {}).setdefault('интервал', set()).add(
                    (round(float(str(row[2]).replace(',', '.')), 1), round(float(str(row[3]).replace(',', '.')), 1)))
                self.dict_perforation_project.setdefault(plast, {}).setdefault('отв', set()).add(row[6])
                self.dict_perforation_project.setdefault(plast, {}).setdefault('заряд', set()).add(row[7])
                if row[8] != None:
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('удлинение', set()).add(
                        round(float(row[8]), 1))
                if row[9] != None:
                    # print(f'давление {row[9]}')
                    self.dict_perforation_project.setdefault(plast, {}).setdefault('давление', set()).add(
                        round(float(row[9]), 1))
                self.dict_perforation_project.setdefault(plast, {}).setdefault('рабочая жидкость', set()).add(
                    calculationFluidWork(row[1], row[9]))


        if len(self.dict_perforation_project) != 0:
            self.plast_project = list(self.dict_perforation_project.keys())


class WellHistory_data(FindIndexPZ):

    def __init__(self, ws):
        super().__init__(ws)
        self.ws = ws
        self.date_drilling_run = ProtectedIsNonNone('не корректно')
        self.date_drilling_cancel = ProtectedIsNonNone('не корректно')
        self.max_expected_pressure = ProtectedIsDigit('не корректно')
        self.max_admissible_pressure = ProtectedIsDigit('не корректно')
        self.read_well(self.ws, self.data_pvr_max, self.data_fond_min)


    def read_well(self, ws, begin_index, cancel_index):
        # print(begin_index, cancel_index)
        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):

            for col, cell in enumerate(row):
                value = cell.value
                if value:

                    if 'Начало бурения' in str(value):
                        self.date_drilling_run = str(row[col + 2].value)

                    elif 'Конец бурения' == value:
                        self.date_drilling_cancel = row[col + 2].value

                        self.date_drilling_cancel = self.definition_is_None(
                            self.date_drilling_cancel, row_index + begin_index, col + 1, 1)

                    elif 'Максимально ожидаемое давление на устье' == value:
                        self.max_expected_pressure = row[col + 1].value
                        self.max_expected_pressure = self.definition_is_None(
                            self.max_expected_pressure,  row_index+begin_index, col+1, 1)

                    elif 'Максимально допустимое давление опрессовки э/колонны' == value \
                            or 'Максимально допустимое давление на э/колонну' == value:
                        self.max_admissible_pressure = row[col + 1].value
                        self.max_admissible_pressure = self.definition_is_None(
                            self.max_admissible_pressure,  row_index + begin_index , col+1, 1)

class WellFond_data(FindIndexPZ):

    def __init__(self, ws):
        super().__init__(ws)
        self.paker_do = {'do': None, 'posle': None}
        self.paker2_do = {'do': None, 'posle': None}
        self.dict_pump_SHGN = {'do': None, 'posle': None}
        self.dict_pump_SHGN_h = {'do': None, 'posle': None}
        self.dict_pump_ECN = {'do': None, 'posle': None}
        self.dict_pump_ECN_h= {'do': None, 'posle': None}
        self.H_F_paker_do = {'do': None, 'posle': None}
        self.H_F_paker2_do = {'do': None, 'posle': None}

        try:
            if self.condition_of_wells._value == 0:
                self.condition_of_wells, ok = QInputDialog.getInt(self, 'индекс копирования',
                                                                  'Программа не смогла определить строку n\ III. '
                                                                  'Состояние скважины к началу ремонта ',
                                                                  0, 0, 800)
        except:
            pass
        self.read_well(ws, self.data_fond_min, self.condition_of_wells)





    def read_well(self, ws, begin_index, cancel_index):
        print(begin_index, cancel_index)
        self.old_index = 1
        for row in range(begin_index, cancel_index):
            cell = str(ws.cell(row=row, column=2).value)
            if cell:
                if cell.upper() == 'ШТАНГИ':
                    self.sucker_rod_ind = row
                if cell.upper() == 'НКТ':
                    self.pipes_ind = row

        print(f' нкт индекс {self.pipes_ind}')
        try:
            print(self.sucker_rod_ind._value == 'не корректно')
            if self.sucker_rod_ind._value == 'не корректно':
                self.sucker_rod_ind, ok = QInputDialog.getInt(self, 'индекс начала строки со штангами',
                                                          'Программа не смогла найти строку со штангами',
                                                          0, 0, 800)
                print(f'штанги {self.sucker_rod_ind}')
        except:
            pass

        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            for col, cell in enumerate(row):

                value = cell.value
                if value:
                    if 'карта спуска' in str(value).lower():
                        col_plan = col
                        print(f' колонна план {col_plan}')
                    if 'до ремонта' in str(value).lower() and row_index < 6 + begin_index:
                        col_do = col
                        print(f' колонна до ре { col_do}')

                    if 'Пакер' in str(value) and 'типоразмер' in str(row[col + 2].value):
                        try:
                            self.paker_do["do"] = str((row[col_plan])).value.split('/')[0]
                            self.paker2_do["do"] = str(row[col_plan]).value.split('/')[1]
                        except:
                            self.paker_do["do"] = row[col_plan].value


                        try:
                            self.paker_do["posle"] = self.paker_do["posle"].split('/')[0]
                            self.paker2_do["posle"] = self.paker_do["posle"].split('/')[1]
                        except:
                            self.paker_do["posle"] = row[col_plan].value
                            # self.paker_do["posle"] = self.definition_is_None(
                            #     self.paker_do["posle"], row_index, col_plan, 1)

                    elif value == 'Насос' and row[col + 2].value == 'типоразмер':
                        # print([ind.value for ind in row])
                        if row[col_do].value:
                            if ('НВ' in str(row[col_do].value).upper() or 'ШГН' in str(row[col_do].value).upper() \
                                    or 'НН' in str(row[col_do].value).upper()) or 'RHAM' in str(row[col_do].value).upper():
                                self.dict_pump_SHGN["do"] = row[col_do].value
                            if ('ЭЦН' in str(row[col_do].value).upper() or 'ВНН' in str(row[col_do].value).upper()):
                                self.dict_pump_ECN["do"] = row[col_do].value


                        if row[col_plan].value:
                            if ('НВ' in str(row[col_plan].value).upper() or 'ШГН' in str(
                                    row[col_plan].value).upper() \
                                    or 'НН' in str(row[col_plan].value).upper()) \
                                    or 'RHAM' in str(row[col_plan].value).upper():
                                self.dict_pump_SHGN["posle"] = row[col_plan].value

                            if ('ЭЦН' in str(row[col_plan].value).upper() or 'ВНН' in str(
                                    row[col_plan].value).upper()):
                                self.dict_pump_ECN["posle"] = row[col_plan].value

                        if ws.cell(row=row_index + 5, column=col + 3).value == 'Нсп, м':
                            if self.dict_pump_ECN["do"] != 0:
                                self.dict_pump_ECN_h["do"] = ws.cell(row= row_index + 5, column=col_do).value
                            if self.dict_pump_SHGN["do"] != 0:
                                self.dict_pump_SHGN_h["do"] = ws.cell(row=row_index + 5, column=col_do).value
                            if self.dict_pump_ECN["posle"] != 0:
                                self.dict_pump_ECN_h["posle"] = ws.cell(row=row_index + 5,
                                                                            column=col_plan).value
                            if self.dict_pump_SHGN["posle"] != 0:
                                self.dict_pump_SHGN_h["posle"] = ws.cell(row=row_index + 5,
                                                                             column=col_plan).value

                    elif value == 'Н посадки, м':
                        try:
                            if self.paker_do["do"] != 0:
                                self.H_F_paker_do["do"] = row[col_do].value
                                self.H_F_paker2_do["do"] = row[col_do].value
                        except:
                            if self.paker_do["do"] != 0:
                                self.H_F_paker_do["do"] = row[col_do].value
                        try:
                            if self.paker_do["posle"] != 0:
                                self.H_F_paker_do["posle"] = row[col_plan].value
                                self.H_F_paker2_do["posle"] = row[col_plan].value
                        except:
                            if self.paker_do["posle"] != 0:
                                self.H_F_paker_do["posle"] = row[col_plan].value

class WellNkt(FindIndexPZ):

    def __init__(self, ws):
        super().__init__(ws)

        self.dict_nkt = {}
        self.dict_nkt_po = {}
        print(self.sucker_rod_ind, self.pipes_ind)
        self.read_well(ws, self.sucker_rod_ind, self.pipes_ind)

    def read_well(self, ws, begin_index, cancel_index):
        a_plan  = 0
        print(begin_index, cancel_index)
        for row in range(begin_index, cancel_index):  # словарь  количества НКТ и метраж
            if ws.cell(row=row, column=3).value == 'План' or str(
                    ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                a_plan = row
        if a_plan == 0:
            a_plan, ok = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                                         'Программа не могла определить начала строку с ПЗ НКТ - план')
        # print(f'индекс a_plan {a_plan}')
        for row in range(begin_index, cancel_index):
            # print(str(ws.cell(row=row, column=4).value))
            key = str(ws.cell(row=row, column=4).value)
            if key != str(None) and key != '-' and "Диам" not in key:
                value = ws.cell(row=row, column=7).value
                if not key is None and row < a_plan:
                    self.dict_nkt[key] = self.dict_nkt.get(key, 0) + round(float(value), 1)
                elif not key is None and row >= a_plan:
                    self.dict_nkt_po[key] = self.dict_nkt_po.get(key, 0) + round(float(value), 1)
            # print(f'индекс a_plan {self.dict_nkt}')
        # self.shoe_nkt = float(sum(self.dict_nkt.values()))

class WellSucker_rod(FindIndexPZ):

    def __init__(self, ws):
        super().__init__(ws)
        self.dict_sucker_rod_po = {}
        self.dict_sucker_rod = {}
        self.read_well(ws, self.pipes_ind, self.condition_of_wells)

    def read_well(self, ws, begin_index, cancel_index):
        for row in range(begin_index, cancel_index):  # словарь  количества штанг и метраж
            if ws.cell(row=row, column=3).value == 'План' or str(
                    ws.cell(row=row, column=3).value).lower() == 'после ремонта':
                b_plan = row

        if b_plan == 0:
            b_plan, ok = QInputDialog.getDouble(self, 'Индекс планового НКТ',
                                                         'Программа не могла определить начала строку с ПЗ штанги - план')
        print(f'б {b_plan}')
        for row in range(begin_index, cancel_index-1):

            key = str(ws.cell(row=row, column=4).value).replace(' ', '')
            value = ws.cell(row=row, column=7).value
            if key != str(None) and key != '-' and key != '':
                print(key, value)
                if key != None and row < b_plan:
                    self.dict_sucker_rod[key] = self.dict_sucker_rod.get(key, 0) + int(value + 1)
                if key != None and row >= b_plan:
                    self.dict_sucker_rod_po[key] = self.dict_sucker_rod_po.get(key, 0) + int(value)

class WellCondition(FindIndexPZ):

    def __init__(self, ws):
        super().__init__(ws)

        self.proc_water = ProtectedIsDigit(100)

        self.static_level = ProtectedIsDigit(0)
        self.dinamic_level = ProtectedIsDigit(0)
        self.well_volume_in_PZ = []
        self.read_well(ws, self.condition_of_wells, self.data_well_max)
        self.grpPlan = False


    def read_well(self, ws, begin_index, cancel_index):

        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            for col, cell in enumerate(row):
                value = cell.value
                if value:
                    if "Hст " in str(value):
                        self.static_level = row[col + 1].value
                    if "грп" in str(value).lower():
                        self.grpPlan = True

                    if "Ндин " in str(value):
                        self.dinamic_level = row[col + 1].value
                    if "% воды " in str(value):
                        self.proc_water = row[col + 1].value
                        # self.proc_water =self.definition_is_None(self.proc_water, row_index, col + 1, 1)
                    if 'Vжг' in str(value):
                        try:
                            well_volume_in_PZ = str(row[col + 1].value).replace(',', '.')
                            # print(f'строка {well_volume_in_PZ}')
                            # well_volume_in_PZ = self.definition_is_None(well_volume_in_PZ, row_index, col + 1, 1)
                            self.well_volume_in_PZ.append(round(float(well_volume_in_PZ), 1))
                        except:
                            well_volume_in_PZ, _ = QInputDialog.getDouble(None, 'Объем глушения',
                                                                          'ВВедите объем глушения согласно ПЗ', 50, 1,
                                                                          70)
                            self.well_volume_in_PZ.append(well_volume_in_PZ)

class Well_expected_pick_up(FindIndexPZ):

    def __init__(self, ws):
        super().__init__(ws)

        self.expected_Q = ProtectedIsDigit(0)

        self.expected_P = ProtectedIsDigit(0)
        self.Qwater = ProtectedIsDigit(0)
        self.expected_pick_up = []
        self.Qoil = ProtectedIsDigit(0)
        self.read_well(ws, self.data_x_min, self.data_well_max)

    def read_well(self, ws, begin_index, cancel_index):

        for row_index, row in enumerate(ws.iter_rows(min_row=begin_index, max_row=cancel_index)):
            row_index += begin_index
            for col, cell in enumerate(row):
                value = cell.value
                if value:

                    if 'прием' in str(value).lower() or 'qж' in str(value).lower():
                        self.expected_Q = row[col +1].value
                        # self.expected_Q = self.definition_is_None(self.expected_Q, row_index, col +1, 1)
                    if 'зак' in str(value).lower() or 'давл' in str(value).lower() or 'p' in str(value).lower():
                        self.expected_P = row[col + 1].value
                        # self.expected_P = self.definition_is_None(self.expected_Q, row_index, col + 1, 1)

                    if 'qж' in str(value).lower():
                        self.Qwater = row[col + 1].value
                        # self.Qwater = self.definition_is_None(self.Qwater, row_index, col+1, 1)

                    if 'qн' in str(value).lower():
                        self.Qoil = row[col + 1].value
                        # self.Qoil = self.definition_is_None(self.Qoil, row_index, col+1, 1)
                    elif 'воды' in str(value).lower():
                        self.proc_water = row[col + 1].value
                        # self.proc_water = self.definition_is_None(self.proc_water, row_index, col+1, 1)

            try:
                self.expected_pick_up[self.expected_Q] = self.expected_P
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