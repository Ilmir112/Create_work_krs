import json
from collections import namedtuple
from datetime import datetime

import data_list
from data_base.config_base import connection_to_database, WorkDatabaseWell
from find import FindIndexPZ
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QTabWidget, QInputDialog, QMessageBox

from main import MyMainWindow
from data_list import contractor, ProtectedIsDigit
from work_py.advanted_file import definition_plast_work


class TabPageUnion(QWidget):
    def __init__(self, data_well: FindIndexPZ):
        super().__init__()

        self.validator_float = QDoubleValidator(0.0, 8000.0, 2)
        self.validator_int = QIntValidator(0, 8000)
        self.data_well = data_well

    def paker_diameter_select(self, depth_landing):
        paker_diam_dict = {
            82: (84, 92),
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
        paker_diameter = 0
        try:
            if self.data_well.column_additional is False or (
                    self.data_well.column_additional is True and int(depth_landing) <= self.data_well.head_column_additional.get_value):
                diam_internal_ek = self.data_well.column_diameter.get_value - 2 * self.data_well.column_wall_thickness.get_value
            else:
                diam_internal_ek = self.data_well.column_additional_diameter.get_value - \
                                   2 * self.data_well.column_additional_wall_thickness.get_value

            for diam, diam_internal_paker in paker_diam_dict.items():
                if diam_internal_paker[0] <= diam_internal_ek <= diam_internal_paker[1]:
                    paker_diameter = diam
                    break
        except Exception as e:
            print('ошибка проверки диаметра пакера')

        return paker_diameter

    def insert_data_dop_plan(self, result, paragraph_row):
        self.data_well.plast_project = []
        self.data_well.dict_perforation_project = {}
        self.data_well.data_list = []
        self.data_well.gips_in_well = False
        self.data_well.drilling_interval = []
        self.data_well.for_paker_list = False
        self.data_well.grp_plan = False
        self.data_well.angle_data = []
        self.data_well.nkt_opress_true = False
        self.data_well.bvo = False
        self.data_well.stabilizator_need = False
        self.data_well.current_bottom_second = 0

        paragraph_row = paragraph_row - 1

        if len(result) <= paragraph_row:
            QMessageBox.warning(self, 'Ошибка', f'В плане работ только {len(result)} пунктов')
            return

        self.data_well.current_bottom = result[paragraph_row][1]

        self.data_well.dict_perforation = json.loads(result[paragraph_row][2])

        self.data_well.plast_all = json.loads(result[paragraph_row][3])
        self.data_well.plast_work = json.loads(result[paragraph_row][4])
        self.data_well.dict_leakiness = json.loads(result[paragraph_row][5])
        self.data_well.leakiness = False
        self.data_well.leakiness_interval = []
        if self.data_well.dict_leakiness:
            self.data_well.leakiness = True
            self.data_well.leakiness_interval = list(self.data_well.dict_leakiness['НЭК'].keys())

        if result[paragraph_row][6] == 'true':
            self.data_well.column_additional = True
        else:
            self.data_well.column_additional = False

        self.data_well.fluid_work = result[paragraph_row][7]

        self.data_well.category_pressure = result[paragraph_row][8]
        self.data_well.category_h2s = result[paragraph_row][9]
        self.data_well.category_gas_factor = result[paragraph_row][10]
        self.data_well.category_pvo = 2
        if str(self.data_well.category_pressure) == '1' or str(self.data_well.category_h2s) == '1' \
                or self.data_well.category_gas_factor == '1':
            self.data_well.category_pvo = 1
        try:
            self.data_well.template_depth, self.data_well.template_length, \
            self.data_well.template_depth_addition, self.data_well.template_length_addition = \
                json.loads(result[paragraph_row][11])
        except Exception:
            self.data_well.template_depth = result[paragraph_row][11]
        self.data_well.skm_interval = json.loads(result[paragraph_row][12])

        self.data_well.problem_with_ek_depth = result[paragraph_row][13]
        self.data_well.problem_with_ek_diameter = result[paragraph_row][14]
        try:
            self.data_well.head_column = ProtectedIsDigit(result[paragraph_row][16])
        except Exception:
            print('отсутствуют данные по голове хвостовика')
        self.data_well.dict_perforation_short = json.loads(result[paragraph_row][2])

        try:
            self.data_well.ribbing_interval = json.loads(result[paragraph_row][15])
        except Exception:
            print('отсутствуют данные по интервалам райбирования')

        definition_plast_work(self)
        return True

    @staticmethod
    def check_if_none(value):
        if isinstance(value, datetime):
            return value
        elif value is None or 'отс' in str(value).lower() or str(value).replace(' ', '') == '-' \
                or value == 0 or str(value).replace(' ', '') == '':
            return 'отсут'
        else:
            return value


class TabWidgetUnion(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class WindowUnion(MyMainWindow):
    def __init__(self, data_well: FindIndexPZ):
        super().__init__()
        self.data_well = data_well

    def select_nkt_grp(self):

        if self.data_well.column_additional is False or\
                (self.data_well.column_additional is True and self.data_well.current_bottom >=
                 self.data_well.head_column_additional.get_value):
            return f'НКТ{self.data_well.nkt_diam}мм'
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value < 110:
            return f'НКТ60мм L- {round(self.data_well.current_bottom - self.data_well.head_column_additional.get_value + 20, 0)}'
        elif self.data_well.column_additional is True and self.data_well.column_additional_diameter.get_value > 110:
            return f'НКТ{self.data_well.nkt_diam}мм со снятыми фасками L- ' \
                   f'{round(self.data_well.current_bottom - self.data_well.head_column_additional.get_value + 20, 0)}'

    @staticmethod
    def read_excel_in_base(number_well, area_well, work_plan, type_kr):
        db = connection_to_database(data_list.DB_WELL_DATA)
        data_well_base = WorkDatabaseWell(db)

        data_well = data_well_base.read_excel_in_base(number_well, area_well, work_plan, type_kr)

        try:
            dict_well = json.loads(data_well[len(data_well) - 1][0])
            data = dict_well['data']
            rowHeights = dict_well['rowHeights']
            if 'colWidth' in list(dict_well.keys()):
                col_width = dict_well['colWidth']
            elif 'col_width' in list(dict_well.keys()):
                col_width = dict_well['col_width']
            boundaries_dict = dict_well['merged_cells']

        except Exception as e:
            QMessageBox.warning(None, 'Ошибка', f'Введены не все параметры {type(e).__name__}\n\n{str(e)}')
            return

        return data, rowHeights, col_width, boundaries_dict

    def definition_open_trunk_well(self):
        self.data_well.nkt_diam = 73 if self.data_well.column_diameter.get_value > 110 else 60
        self.data_well.nkt_template = 59.6 if self.data_well.column_diameter.get_value > 110 else 47.9

        if self.data_well.column_additional:
            if self.data_well.current_bottom > self.data_well.shoe_column_additional.get_value:
                self.data_well.open_trunk_well = True
            else:
                self.data_well.open_trunk_well = False
        else:
            if self.data_well.current_bottom > self.data_well.shoe_column.get_value:
                self.data_well.open_trunk_well = True
            else:
                self.data_well.open_trunk_well = False
    def extraction_data(self, table_name, paragraph_row=0):
        date_table = table_name.split(' ')[-1]
        well_number = table_name.split(' ')[0]
        well_area = table_name.split(' ')[1]
        type_kr = table_name.split(' ')[-4].replace('None', 'null')
        contractor = data_list.contractor
        work_plan = table_name.split(' ')[-3]

        db = connection_to_database(data_list.DB_WELL_DATA)
        data_well_base = WorkDatabaseWell(db, self.data_well)

        result_table = data_well_base.extraction_data(str(well_number), well_area, type_kr,
                                                      work_plan, date_table, contractor)

        if result_table is None:
            QMessageBox.warning(self, 'Ошибка',
                                f'В базе данных скв {well_number} {well_area} отсутствует данные, '
                                f'используйте excel вариант плана работ')
            return None

        if result_table[0]:
            result = json.loads(result_table[0])
            from data_base.work_with_base import insert_data_well_dop_plan
            insert_data_well_dop_plan(self, result_table[1])

            self.data_well.type_kr = result_table[2]
            if result_table[3]:
                dict_data_well = json.loads(result_table[3])
                # self.data_well.dict_category
                pressure = namedtuple("pressure", "category data_pressure")
                Data_h2s = namedtuple("Data_h2s", "category data_percent data_mg_l poglot")
                Data_gaz = namedtuple("Data_gaz", "category data")
                self.data_well.dict_category = {}

                for plast, plast_data in dict_data_well.items():
                    self.data_well.dict_category.setdefault(plast, {}).setdefault(
                        'по давлению',
                        pressure(*dict_data_well[plast]['по давлению']))
                    self.data_well.dict_category.setdefault(plast, {}).setdefault(
                        'по сероводороду', Data_h2s(*dict_data_well[plast]['по сероводороду']))
                    self.data_well.dict_category.setdefault(plast, {}).setdefault(
                        'по газовому фактору', Data_gaz(*dict_data_well[plast]['по газовому фактору']))

                    self.data_well.dict_category.setdefault(plast, {}).setdefault(
                        'отключение', dict_data_well[plast]['отключение'])

            if self.data_well.work_plan in ['dop_plan', 'dop_plan_in_base']:
                data = self.insert_data_dop_plan(result, paragraph_row)
                if data is None:
                    return None
            elif self.data_well.work_plan == 'plan_change':
                data = self.insert_data_plan(result)
                if data is None:
                    return None
            data_list.data_well_is_True = True

        else:
            data_list.data_in_base = False
            QMessageBox.warning(self, 'Проверка наличия таблицы в базе данных',
                                f"Таблицы '{table_name}' нет в базе данных.")

        return True

    def insert_data_plan(self, result):
        self.data_well.data_list = []
        self.data_well.gips_in_well = False
        self.data_well.drilling_interval = []
        self.data_well.for_paker_list = False
        self.data_well.grp_plan = False
        self.data_well.angle_data = []
        self.data_well.nkt_opress_true = False
        self.data_well.plast_project = []
        self.data_well.drilling_interval = []
        self.data_well.dict_perforation_project = {}
        self.data_well.bvo = False
        self.data_well.fluid = float(result[0][7][:4].replace('г', ''))
        self.data_well.stabilizator_need = False
        self.data_well.current_bottom_second = 0

        for ind, row in enumerate(result):
            if ind == 1:
                self.data_well.bottom = row[1]
                self.data_well.category_pressure_second = row[8]
                self.data_well.category_h2s_second = row[9]
                self.data_well.gaz_factor_pr_second = row[10]

                self.data_well.plast_work_short = json.dumps(row[3], ensure_ascii=False)

            data_list = []
            for index, data in enumerate(row):
                if index == 6:
                    if data == 'false' or data == 0 or data == '0':
                        data = False
                    else:
                        data = True
                data_list.append(data)
            self.data_well.data_list.append(data_list)
        self.data_well.current_bottom = result[ind][1]
        self.data_well.dict_perforation = json.loads(result[ind][2])

        self.data_well.plast_all = json.loads(result[ind][3])
        self.data_well.plast_work = json.loads(result[ind][4])
        self.data_well.dict_leakiness = json.loads(result[ind][5])
        self.data_well.leakiness = False
        self.data_well.leakiness_interval = []
        if self.data_well.dict_leakiness:
            self.data_well.leakiness = True
            self.data_well.leakiness_interval = list(self.data_well.dict_leakiness['НЭК'].keys())

        self.data_well.dict_perforation_short = json.loads(result[ind][2])

        self.data_well.category_pressure = result[ind][8]
        self.data_well.category_h2s = result[ind][9]
        self.data_well.category_gas_factor = result[ind][10]
        if str(result[ind][8]) == '1' or str(result[ind][9]) == '1' or str(result[ind][10]) or '1':
            self.data_well.bvo = True

        definition_plast_work(self)
        return True

    def calculate_angle(self, max_depth_pvr, angle_data):
        tuple_angle = ()
        for depth, angle, _ in angle_data:
            if abs(float(depth) - float(max_depth_pvr)) < 10:
                tuple_angle = depth, angle, f'Зенитный угол на глубине {depth}м равен {angle}гр'

        return tuple_angle

    def calc_work_fluid(self, fluid_work_insert):
        self.data_well.fluid = float(fluid_work_insert)
        self.data_well.fluid_short = fluid_work_insert

        category_h2s_list = [
            self.data_well.dict_category[plast]['по сероводороду'].category
            for plast in list(
                self.data_well.dict_category.keys()) if self.data_well.dict_category[plast]['отключение'] == 'рабочий']

        if 2 in category_h2s_list or 1 in category_h2s_list:
            expenditure_h2s_list = []
            if self.data_well.plast_work:
                try:
                    for _ in self.data_well.plast_work:
                        poglot = [self.data_well.dict_category[plast]['по сероводороду'].poglot for plast in
                                  list(self.data_well.dict_category.keys())
                                  if self.data_well.dict_category[plast]['по сероводороду'].category in [1, 2]][
                            0]
                        expenditure_h2s_list.append(poglot)
                except ValueError:
                    pass
            else:
                expenditure_h2s, _ = QInputDialog.getDouble(self, 'Расчет поглотителя',
                                                            'Отсутствуют рабочие пласты, нужно ввести '
                                                            'необходимый расчет поглотителя', 0.01, 0, 10, 2)

            expenditure_h2s = round(max(expenditure_h2s_list), 3)
            fluid_work = f'{fluid_work_insert}г/см3 с добавлением поглотителя сероводорода ' \
                         f'{self.data_well.type_absorbent} из ' \
                         f'расчета {expenditure_h2s}л/м3 либо аналог '
            fluid_work_short = f'{fluid_work_insert}г/см3 c ' \
                               f'{self.data_well.type_absorbent} - {expenditure_h2s}л/м3 '
        else:
            fluid_work = f'{fluid_work_insert}г/см3 '
            fluid_work_short = f'{fluid_work_insert}г/см3'

        return fluid_work, fluid_work_short

    def pvo_gno(self, kat_pvo):
        date_str = ''
        if 'Ойл' in contractor:
            date_str = 'от 07.03.2024г'
        elif 'РН' in contractor:
            date_str = ''
        # print(f' ПВО {kat_pvo}')
        pvo_2 = f'Установить ПВО по схеме №2 утвержденной главным инженером {contractor} {date_str} (тип плашечный ' \
                f'сдвоенный ПШП-2ФТ-152х21) и посадить пакер. ' \
                f'Спустить пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) и ' \
                f'линии манифольда до концевых ' \
                f'задвижек на Р-{self.data_well.max_admissible_pressure.get_value}атм на максимально ' \
                f'допустимое давление ' \
                f'опрессовки эксплуатационной колонны в течении ' \
                f'30мин), сорвать пакер. ' \


        pvo_1 = f'Установить ПВО по схеме №2 утвержденной главным инженером {contractor} {date_str} ' \
                f'(тип плашечный сдвоенный ПШП-2ФТ-160х21Г Крестовина КР160х21Г, ' \
                f'задвижка ЗМС 65х21 (3шт), Шарового крана 1КШ-73х21, авар. трубы (патрубок НКТ73х7-7-Е, ' \
                f' (при необходимости произвести монтаж переводника' \
                f' П178х168 или П168 х 146 или ' \
                f'П178 х 146 в зависимости от типоразмера крестовины и колонной головки). Спустить и посадить ' \
                f'пакер на глубину 10м. Опрессовать ПВО (трубные плашки превентора) на ' \
                f'Р-{self.data_well.max_admissible_pressure.get_value}атм ' \
                f'(на максимально допустимое давление опрессовки ' \
                f'эксплуатационной колонны в течении 30мин), сорвать и извлечь пакер. Опрессовать ' \
                f'выкидную линию после концевых задвижек на ' \
                f'Р - 50 кгс/см2 (5 МПа) - для противовыбросового оборудования, рассчитанного на' \
                f'давление до 210 кгс/см2 ((21 МПа)\n' \
                f'- Обеспечить обогрев превентора и СУП в зимнее время . \n Получить разрешение на ' \
                f'производство работ в ' \
                f'присутствии представителя ПФС'
        if kat_pvo == 1:
            return pvo_1, f'Монтаж ПВО по схеме №2 + ГидроПревентор'
        else:
            # print(pvo_2)
            return pvo_2, f'Монтаж ПВО по схеме №2'
