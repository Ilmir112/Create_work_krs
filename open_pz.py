import base64

import well_data
from datetime import datetime
from PyQt5.QtWidgets import QInputDialog, QMessageBox
from openpyxl_image_loader import SheetImageLoader
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Font, Alignment, Border, Side

from cdng import events_gnvp, add_itog, events_gnvp_gnkt
from data_base.config_base import connection_to_database, WorkDatabaseWell
from find import ProtectedIsNonNone
from main import MyMainWindow
from plan import delete_rows_pz
from block_name import region_select, razdel_1, curator_sel, pop_down
from work_py.dop_plan_py import DopPlanWindow
from work_py.check_in_pz import CustomMessageBox


class CreatePZ(MyMainWindow):
    def __init__(self, wb, ws,  parent=None):
        super(CreatePZ, self).__init__()

        self.wb = wb
        self.ws = ws



    def open_excel_file(self, ws, work_plan):
        from find import FindIndexPZ
        from work_py.leakage_column import LeakageWindow
        from category_correct import CategoryWindow

        from find import WellNkt, Well_perforation, WellCondition, WellHistory_data, Well_data, Well_Category, \
            WellFond_data, WellSucker_rod, Well_expected_pick_up, WellData


        well_data.work_plan = work_plan

        well_data.dict_category = CategoryWindow.dict_category
        # Запуск основного класса и всех дочерних классов в одной строке
        well_pz = FindIndexPZ(ws)

        well_data.region = region_select(well_data.cdng._value)

        WellData.read_well(self, ws, well_data.cat_well_max._value, well_data.data_pvr_min._value)
        well_data.region = region_select(well_data.cdng._value)

        date_str2 = datetime.strptime('2024-09-19', '%Y-%m-%d')

        if work_plan == 'dop_plan':
            number_list = list(map(str, range(1, 50)))
            well_data.number_dp, ok = QInputDialog.getItem(self, 'Номер дополнительного плана работ',
                                                           'Введите номер дополнительного плана работ',
                                                           number_list, 0, False)

            db = connection_to_database(well_data.DB_WELL_DATA)
            data_well_base = WorkDatabaseWell(db)

            data_well = data_well_base.check_in_database_well_data(well_data.well_number._value, well_data.well_area._value,
                                            f'ДП№{well_data.number_dp}')

            if data_well:

                date_str1 = datetime.strptime(f'{data_well[1]}', '%Y-%m-%d')
                if date_str1 > date_str2:

                    change_work_work_plan = QMessageBox.question(self,
                                                                 'Наличие в базе данных',
                                                                 'Проверка показала что данные по скважине есть в'
                                                                 ' базе данных, '
                                                                 'загрузить с базы?')

                    if change_work_work_plan == QMessageBox.StandardButton.Yes:
                        well_data.type_kr = data_well[2]
                        well_data.work_plan = 'dop_plan_in_base'
                        self.work_plan = 'dop_plan_in_base'
                        well_data.data_in_base = True
                        self.rir_window = DopPlanWindow(well_data.ins_ind, None, work_plan)
                        # self.rir_window.setGeometry(200, 400, 100, 200)
                        self.rir_window.show()
                        self.pause_app()
                        well_data.pause = True

                        return

        if well_data.data_well_is_True is False:
            WellNkt.read_well(self, ws, well_data.pipes_ind._value, well_data.condition_of_wells._value)
            if well_data.work_plan not in ['application_pvr', 'application_gis']:
                WellSucker_rod.read_well(self, ws, well_data.sucker_rod_ind._value, well_data.pipes_ind._value)
                WellFond_data.read_well(self, ws, well_data.data_fond_min._value, well_data.condition_of_wells._value)
            WellHistory_data.read_well(self, ws, well_data.data_pvr_max._value, well_data.data_fond_min._value)
            WellCondition.read_well(self, ws, well_data.condition_of_wells._value, well_data.data_well_max._value)

            Well_expected_pick_up.read_well(self, ws, well_data.data_x_min._value, well_data.data_x_max._value)
            Well_data.read_well(self, ws, well_data.cat_well_max._value, well_data.data_pvr_min._value)

            Well_perforation.read_well(self, ws, well_data.data_pvr_min._value, well_data.data_pvr_max._value + 1)
            Well_Category.read_well(self, ws, well_data.cat_well_min._value, well_data.data_well_min._value)
        if 'Ойл' in well_data.contractor:
            contractor = 'ОЙЛ'
        elif 'РН' in well_data.contractor:
            contractor = 'РН'

        if work_plan == 'plan_change':
            DopPlanWindow.extraction_data(self, str(well_data.well_number._value) + " " +
                                          well_data.well_area._value + " " + 'krs' + " " + contractor, 1)
            ws.delete_rows(well_data.plan_correct_index._value, ws.max_row)
            return ws

        if well_data.inv_number._value == 'не корректно' or well_data.inv_number is None:
            QMessageBox.warning(self, 'Инвентарный номер отсутствует',
                                'Необходимо уточнить наличие инвентарного номера')
            return

        if well_data.leakiness is True:
            if WellCondition.leakage_window is None:
                WellCondition.leakage_window = LeakageWindow()
                WellCondition.leakage_window.setWindowTitle("Геофизические исследования")
                # WellCondition.leakage_window.setGeometry(200, 400, 300, 400)
                WellCondition.leakage_window.show()

                self.pause_app()
                well_data.dict_leakiness = WellCondition.leakage_window.add_work()
                # print(f'словарь нарушений {well_data.dict_leakiness}')
                well_data.pause = True
                WellCondition.leakage_window = None  # Discard reference.

            else:
                well_data.leakiness = False

        if work_plan not in ['application_pvr', 'application_gis', 'gnkt_bopz', 'gnkt_opz', 'gnkt_after_grp',
                             'gnkt_frez']:
            if work_plan != 'plan_change':
                for row_ind, row in enumerate(ws.iter_rows(values_only=True, max_col=13)):
                    ws.row_dimensions[row_ind].hidden = False

                    if any(['ПЛАН РАБОТ' in str(col).upper() for col in row]) \
                            and work_plan == 'dop_plan':
                        ws.cell(row=row_ind + 1, column=2).value = f'ДОПОЛНИТЕЛЬНЫЙ ПЛАН РАБОТ № {well_data.number_dp}'


                    elif 'План-заказ' in row:
                        # print(row)

                        ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'

                    for col, value in enumerate(row):
                        if not value is None and col <= 12:
                            if 'гипс' in str(value).lower() or 'гидратн' in str(value).lower():
                                well_data.gipsInWell = True

                if well_data.emergency_well is True:
                    emergency_quest = QMessageBox.question(self, 'Аварийные работы ',
                                                           'Программа определила что в скважине'
                                                           f' авария - {well_data.emergency_count}, верно ли?')
                    if emergency_quest == QMessageBox.StandardButton.Yes:
                        well_data.emergency_well = True
                        well_data.emergency_bottom, ok = QInputDialog.getInt(self, 'Аварийный забой',
                                                                             'Введите глубину аварийного забоя',
                                                                             0, 0,
                                                                             int(well_data.bottomhole_artificial._value))
                    else:
                        well_data.emergency_well = False
                if well_data.problemWithEk is True:
                    problemWithEk_quest = QMessageBox.question(self, 'ВНИМАНИЕ НЕПРОХОД ',
                                                               f'Программа определила что в скважине '
                                                               f'ссужение в ЭК -, верно ли?')
                    if problemWithEk_quest == QMessageBox.StandardButton.Yes:
                        well_data.problemWithEk = True
                        well_data.problemWithEk_depth, ok = QInputDialog.getInt(self, 'Глубина сужения',
                                                                                "ВВедите глубину cсужения", 0, 0,
                                                                                int(well_data.current_bottom))
                        well_data.problemWithEk_diametr = QInputDialog.getInt(self, 'диаметр внутренний cсужения',
                                                                              "ВВедите внутренний диаметр cсужения", 0,
                                                                              0,
                                                                              int(well_data.current_bottom))[0]
                    else:
                        well_data.problemWithEk = ProtectedIsNonNone(False)

                if well_data.gipsInWell is True:
                    gips_true_quest = QMessageBox.question(self, 'Гипсовые отложения',
                                                           'Программа определила что скважина осложнена гипсовыми отложениями '
                                                           'и требуется предварительно определить забой на НКТ, верно ли это?')

                    if gips_true_quest == QMessageBox.StandardButton.Yes:
                        well_data.gipsInWell = True
                    else:
                        well_data.gipsInWell = False

            try:
                # Копирование изображения
                image_loader = SheetImageLoader(ws)
            except Exception as e:
                QMessageBox.warning(None, 'Ошибка', f'Ошибка в копировании изображений {e}')

            if len(well_data.check_data_in_pz) != 0:
                check_str = ''
                for ind, check_data in enumerate(well_data.check_data_in_pz):
                    if check_data not in check_str:
                        check_str += f'{ind + 1}. {check_data} \n'
                self.show_info_message(check_str)

            well_data.image_data = []
            for row in range(1, well_data.data_well_max._value):
                for col in range(1, 12):
                    try:
                        image = image_loader.get(f'{get_column_letter(col)}{row}')
                        image.save(
                            f'{well_data.path_image}imageFiles/image_work/image{get_column_letter(col)}{row}.png')
                        image_size = image.size
                        image_path = f'{well_data.path_image}imageFiles/image_work/image{get_column_letter(col)}{row}.png'

                        coord = f'{get_column_letter(col)}{row + 17 - well_data.cat_well_min._value}'

                        well_data.image_list.append((image_path, coord, image_size))
                        # Чтение изображения в байты
                        with open(image_path, "rb") as f:
                            image_bytes = f.read()
                        # Преобразование в Base64
                        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

                        # Создание словаря для изображения
                        image_info = {
                            "coord": coord,
                            "width": image_size[0],
                            "height": image_size[1],
                            "data": image_base64
                        }
                        # Сохранение Base64 данных в файл (для проверки)
                        with open("image_base64.txt", "w", encoding="utf-8") as f:
                            f.write(image_base64)
                        # Добавление информации в список
                        well_data.image_data.append(image_info)

                    except:
                        pass
            if work_plan != 'plan_change':
                for j in range(well_data.data_x_min._value,
                               well_data.data_x_max._value):  # Ожидаемые показатели после ремонта
                    lst = []
                    for i in range(0, 12):
                        lst.append(ws.cell(row=j + 1, column=i + 1).value)
                    well_data.row_expected.append(lst)

            if well_data.work_plan not in ['gnkt_frez', 'application_pvr',
                                           'application_gis', 'gnkt_after_grp', 'gnkt_opz', 'plan_change']:
                # print(f'план работ {well_data.work_plan}')
                delete_rows_pz(self, ws)
                razdel = razdel_1(self, well_data.region, well_data.contractor)

                for i in range(1, len(razdel)):  # Добавлением подписантов на вверху
                    for j in range(1, 13):
                        ws.cell(row=i, column=j).value = razdel[i - 1][j - 1]
                        ws.cell(row=i, column=j).font = Font(name='Arial Cyr', size=13, bold=True)
                    ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
                    ws.merge_cells(start_row=i, start_column=8, end_row=i, end_column=12)
                well_data.ins_ind = 0

                well_data.ins_ind += well_data.data_well_max._value - well_data.cat_well_min._value + 19
                # print(f' индекс вставки ГНВП{well_data.ins_ind}')
                dict_events_gnvp = {}
                dict_events_gnvp['krs'] = events_gnvp(well_data.contractor)
                dict_events_gnvp['gnkt_opz'] = events_gnvp_gnkt()
                dict_events_gnvp['gnkt_bopz'] = events_gnvp_gnkt()
                dict_events_gnvp['dop_plan'] = events_gnvp(well_data.contractor)
                dict_events_gnvp['normir_new'] = events_gnvp(well_data.contractor)
                # if work_plan != 'dop_plan':
                text_width_dict = {20: (0, 100), 30: (101, 200), 40: (201, 300), 60: (301, 400), 70: (401, 500),
                                   90: (501, 600), 110: (601, 700), 120: (701, 800), 130: (801, 900),
                                   150: (901, 1500), 270: (1500, 2300)}

                # Устанавливаем параметры границы
                red = 'FF0000'  # Красный цвет в формате HEX
                thin_border = Border(left=Side(style='thin', color=red),
                                     right=Side(style='thin', color=red),
                                     top=Side(style='thin', color=red),
                                     bottom=Side(style='thin', color=red))

                if work_plan != 'normir':
                    if 'Ойл' in well_data.contractor:
                        for i in range(well_data.ins_ind, well_data.ins_ind + len(dict_events_gnvp[work_plan])):
                            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                            data = ws.cell(row=i, column=2)
                            data.value = dict_events_gnvp[work_plan][i - well_data.ins_ind][1]

                            if 'Мероприятия' in str(data.value) or \
                                    'Меры по предупреждению' in str(data.value) or \
                                    ' ТЕХНОЛОГИЧЕСКИЕ ПРОЦЕССЫ' in str(data.value) or \
                                    'Признаки отравления сернистым водородом' in str(data.value) or \
                                    'Контроль воздушной среды проводится:' in str(data.value) or \
                                    'Требования безопасности при выполнении работ:' in str(data.value) or \
                                    'Меры по предупреждению' in str(data.value) or \
                                    'Меры по предупреждению' in str(data.value) or \
                                    'Меры по предупреждению' in str(data.value) or \
                                    "о недопустимости нецелевого расхода" in str(data.value):
                                data.alignment = Alignment(wrap_text=True, horizontal='center',
                                                           vertical='center')
                                data.fill = well_data.yellow_fill
                                data.font = Font(name='Arial Cyr', size=13, bold=True)

                            else:
                                data.alignment = Alignment(wrap_text=True, horizontal='left',
                                                           vertical='center')

                                data.font = Font(name='Arial Cyr', size=12)
                            if not data.value is None:
                                text = data.value
                                for key, value in text_width_dict.items():
                                    if value[0] <= len(text) <= value[1]:
                                        ws.row_dimensions[i].height = int(key)

                    elif 'РН' in well_data.contractor:
                        # Устанавливаем красный цвет для текста
                        red_font = Font(name='Arial Cyr', size=13, color='FF0000', bold=True)
                        for i in range(well_data.ins_ind, well_data.ins_ind + len(dict_events_gnvp[work_plan])):
                            for col in range(12):
                                data = ws.cell(row=i, column=col + 1)
                                data.border = thin_border
                                data.value = dict_events_gnvp[work_plan][i - well_data.ins_ind][col]

                                data_2 = ws.cell(row=i, column=3).value
                                data_1 = ws.cell(row=i, column=2).value
                                ws.cell(row=i, column=col + 1).font = Font(name='Arial Cyr', size=13, bold=False)

                            if 'IX.I. Мероприятия по предотвращению технологических аварий при ремонте скважин:' in str(
                                    data_1):
                                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                               vertical='center')

                                ws.cell(row=i, column=2).font = Font(name='Arial Cyr', size=13, bold=True)
                            elif 'При работе с вертлюгами обеспечить' in str(data_2) \
                                    or 'На основании приказа' in str(data_2) \
                                    or 'Согласно мероприятий по снижению а' in str(data_2) \
                                    or 'Во время нештатных ' in str(data_2) \
                                    or 'Для предотвращения падения ' in str(data_2) \
                                    or 'После герметизации устья' in str(data_2) \
                                    or 'При свинчивании и развинчивании' in str(data_2) \
                                    or 'Сборку фрезерующего, ' in str(data_2) \
                                    or 'При нулевых и отрицательных' in str(data_2):
                                ws.merge_cells(start_row=i, start_column=3, end_row=i, end_column=11)
                                ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                               vertical='center')
                                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                               vertical='center')
                                ws.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                                vertical='center')
                                ws.cell(row=i, column=3).font = Font(name='Arial Cyr', size=13, bold=True)
                                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                               vertical='center')
                            else:
                                ws.merge_cells(start_row=i, start_column=3, end_row=i, end_column=11)
                                ws.cell(row=i, column=3).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                               vertical='center')

                                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                               vertical='center')
                                ws.cell(row=i, column=12).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                                vertical='center')
                                ws.cell(row=i, column=3).font = Font(name='Arial Cyr', size=13, bold=False)

                            if 'ВЫ ДОЛЖНЫ ОТКАЗАТЬСЯ' in str(data_2):
                                ws.cell(row=i, column=3).font = red_font

                            if not data_2 is None:
                                text = data_2
                                for key, value in text_width_dict.items():
                                    text_lenght = len(text)
                                    if value[0] <= text_lenght <= value[1]:
                                        if '\n' in text:
                                            row_dimension_value = int(len(text) / 4 + text.count('\n') * 5)
                                            ws.row_dimensions[i].height = row_dimension_value
                                        else:
                                            row_dimension_value = int(len(text) / 4)
                                            ws.row_dimensions[i].height = int(len(text) / 4)

                    well_data.ins_ind += len(dict_events_gnvp[work_plan]) - 1

                    ws.row_dimensions[2].height = 30

                    if len(well_data.row_expected) != 0:
                        for i in range(1, len(well_data.row_expected) + 1):  # Добавление показатели после ремонта
                            ws.row_dimensions[well_data.ins_ind + i - 1].height = None
                            for j in range(1, 12):
                                if i == 1:
                                    ws.cell(row=i + well_data.ins_ind, column=j).font = Font(name='Arial Cyr', size=13,
                                                                                             bold=False)
                                    ws.cell(row=i + well_data.ins_ind, column=j).alignment = Alignment(wrap_text=False,
                                                                                                       horizontal='center',
                                                                                                       vertical='center')
                                    ws.cell(row=i + well_data.ins_ind, column=j).value = well_data.row_expected[i - 1][
                                        j - 1]
                                else:
                                    ws.cell(row=i + well_data.ins_ind, column=j).font = Font(name='Arial Cyr', size=13,
                                                                                             bold=False)
                                    ws.cell(row=i + well_data.ins_ind, column=j).alignment = Alignment(wrap_text=False,
                                                                                                       horizontal='left',
                                                                                                       vertical='center')
                                    ws.cell(row=i + well_data.ins_ind, column=j).value = well_data.row_expected[i - 1][
                                        j - 1]
                        ws.merge_cells(start_column=2, start_row=well_data.ins_ind + 1, end_column=12,
                                       end_row=well_data.ins_ind + 1)
                        well_data.ins_ind += len(well_data.row_expected)
                    if work_plan not in ['application_pvr', 'gnkt_frez', 'gnkt_after_grp', 'gnkt_opz', 'gnkt_bopz',
                                         'plan_change']:
                        work_list = [
                            [None, None, 'Порядок работы', None, None, None, None, None, None, None, None, None],
                            [None, 'п/п', 'Наименование работ', None, None, None, None, None, None, None,
                             'Ответственный',
                             'Нормы времени \n мин/час.']]

                        for i in range(1, len(work_list) + 1):  # Добавление  показатели после ремонта
                            for j in range(1, 13):
                                ws.cell(row=i + well_data.ins_ind, column=j).font = Font(name='Arial Cyr', size=13,
                                                                                         bold=True)
                                ws.cell(row=i + well_data.ins_ind, column=j).alignment = Alignment(wrap_text=False,
                                                                                                   horizontal='center',
                                                                                                   vertical='center')
                                ws.cell(row=i + well_data.ins_ind, column=j).value = work_list[i - 1][
                                    j - 1]
                            if i == 1:
                                ws.merge_cells(start_column=3, start_row=well_data.ins_ind + i, end_column=12,
                                               end_row=well_data.ins_ind + i)
                            elif i == 2:
                                ws.merge_cells(start_column=3, start_row=well_data.ins_ind + i, end_column=10,
                                               end_row=well_data.ins_ind + i)

                    self.ins_ind_border = well_data.ins_ind

            return ws

        elif work_plan in ['application_pvr']:
            for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
                for col_ind, col in enumerate(row):
                    if col_ind in [3, 2]:
                        if 'кровля' in str(col).lower():
                            type_pvr = ws.cell(row=row_ind, column=3).value
                            index_row_pvr_begin = row_ind + 1
                        if 'произвести контрольную' in str(col).lower():
                            index_row_pvr_cancel = row_ind
                            if index_row_pvr_begin < index_row_pvr_cancel:
                                well_data.index_row_pvr_list.append(
                                    (index_row_pvr_begin, index_row_pvr_cancel, type_pvr))
                                index_row_pvr_begin, index_row_pvr_cancel = 0, 0
            for pvr in well_data.index_row_pvr_list:
                for row in range(pvr[0], pvr[1]):
                    row_list = []
                    for col in range(2, 9):
                        row_list.append(str(ws.cell(row=row + 1, column=col + 1).value))
                    well_data.pvr_row.append(row_list)

            # print(f'Индексы ПВР {well_data.pvr_row}')

        elif work_plan in ['application_gis']:
            for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
                for col_ind, col in enumerate(row):
                    if col_ind in [3, 2]:
                        if ('задача ' in str(col).lower() or 'техкарт' in str(col).lower() or
                            'задаче №' in str(col).lower()) and \
                                'перфорация' not in str(col).lower() and 'привязка' not in str(col).lower() and \
                                'отбивка' not in str(col).lower():
                            type_pvr = ws.cell(row=row_ind + 1, column=3).value
                            well_data.gis_list.append(type_pvr)
        else:
            return ws

    @staticmethod
    def show_info_message(message):
        dialog = CustomMessageBox(message)
        dialog.exec_()  # Открываем диалоговое окно в модальном режиме

    def add_itog(self, ws, ins_ind, work_plan):
        if ws.merged_cells.ranges:
            merged_cells_copy = list(ws.merged_cells.ranges)  # Создаем копию множества объединенных ячеек
            for merged_cell in merged_cells_copy:
                if merged_cell.min_row > ins_ind + 5:
                    try:
                        ws.unmerge_cells(str(merged_cell))
                    except:
                        pass

        if work_plan not in ['gnkt_frez', 'application_pvr', 'gnkt_after_grp', 'gnkt_opz', 'gnkt_bopz']:
            itog_list = add_itog()
            for i in range(ins_ind, len(itog_list) + ins_ind):  # Добавлением итогов
                if i < ins_ind + 6:
                    for j in range(1, 13):
                        ws.cell(row=i, column=j).value = itog_list[i - ins_ind][j - 1]
                        if j != 1:
                            ws.cell(row=i, column=j).border = well_data.thin_border
                            ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)

                    ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=11)
                    ws.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                   vertical='center')
                else:
                    ws.row_dimensions[ins_ind + 6].height = 50
                    ws.row_dimensions[ins_ind + 8].height = 50
                    for j in range(1, 13):
                        ws.cell(row=i, column=j).value = itog_list[i - ins_ind][j - 1]
                        ws.cell(row=i, column=j).border = well_data.thin_border
                        ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                        ws.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='left',
                                                                       vertical='center')

                    ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                    ws.cell(row=i, column=j).alignment = Alignment(wrap_text=False, horizontal='left',
                                                                   vertical='center')

            ins_ind += len(add_itog()) + 2

        curator_s = curator_sel(well_data.curator, well_data.region)
        # print(f'куратор {curator_sel, well_data.curator}')
        podp_down = pop_down(self, well_data.region, curator_s)

        for i in range(1 + ins_ind, 1 + ins_ind + len(podp_down)):

            # Добавлением подписантов внизу
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = podp_down[i - 1 - ins_ind][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)

            if i in range(ins_ind + 7, 1 + ins_ind + 15):
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=6)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=False, vertical='center', horizontal='left')
            else:
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=False, vertical='center', horizontal='left')
        ws.row_dimensions[ins_ind + 7].height = 30
        ws.row_dimensions[ins_ind + 9].height = 25

        ins_ind += len(podp_down)
        aaa = ws.max_row

        ws.delete_rows(ins_ind, aaa - ins_ind)

    def is_valid_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

#