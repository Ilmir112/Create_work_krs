
import block_name
import main
import plan
import krs

from PIL import Image
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QDialog, QMainWindow
from openpyxl_image_loader import SheetImageLoader
from openpyxl.drawing.image import Image
from openpyxl.utils.cell import get_column_letter
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
from collections import namedtuple

from cdng import events_gnvp, itog_1, events_gnvp_gnkt
from find import ProtectedIsDigit, ProtectedIsNonNone
from work_py.gnkt_frez import Work_with_gnkt
from find import FindIndexPZ, Well_perforation, Well_Category, Well_data, \
    WellNkt, WellFond_data, WellCondition, WellHistory_data, WellSucker_rod, Well_expected_pick_up


class CreatePZ(QMainWindow):
    column_direction_lenght = ProtectedIsDigit()
    Qoil = 0
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
    column_direction_True = False
    expected_Q = 0
    expected_P = 0
    plast_select = ''
    dict_perforation = {}
    dict_perforation_project = {}
    itog_ind_min = 0
    kat_pvo = 2
    gaz_f_pr = []
    paker_diametr = 0
    cat_gaz_f_pr = []
    paker_layout = 0

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
    dict_perforation_short = {}

    leakiness = False
    emergency_well = False
    emergency_count = 0
    skm_interval = []
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
    number_dp = ''
    len_razdel_1 = 0
    count_template = 0
    well_volume_in_PZ = []
    cat_P_1 = []
    costumer = 'ОАО "Башнефть"'
    contractor = 'ООО "Ойл-Сервис'
    dict_contractor = {'ООО "Ойл-Сервис':
        {
            'Дата ПВО': '15.10.2021г'
        }
    }
    countAcid = 0

    swabTypeComboIndex = 1
    swabTrueEditType = 1
    data_x_max = 0
    drilling_interval = []
    max_angle = 0
    data_x_min = 0
    pakerTwoSKO = False
    privyazkaSKO = 0
    H2S_pr = []
    pipes_ind = 0
    sucker_rod_ind = 0
    cat_H2S_list = []
    H2S_mg = []
    H2S_mg_m3 = []
    lift_key = 0
    dict_category = {}
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

    cat_P_P = []
    well_oilfield = 0
    template_depth_addition = 0
    condition_of_wells = 0

    well_volume_in_PZ = []
    bvo = False
    old_version = True
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    image_list = []
    problem_with_ek = False
    problem_with_ek_depth = 10000
    problem_with_ek_diametr = 220

    def __init__(self, wb, ws, data_window, perforation_correct_window2, parent=None):
        super(CreatePZ, self).__init__()
        # self.lift_ecn_can_addition = lift_ecn_can_addition
        self.wb = wb
        self.ws = ws
        self.data_window = data_window
        self.perforation_correct_window2 = perforation_correct_window2

    def open_excel_file(self, ws, work_plan):

        from data_correct import DataWindow
        from find import FindIndexPZ
        from category_correct import CategoryWindow

        CreatePZ.work_plan = work_plan
        CreatePZ.dict_category = CategoryWindow.dict_category

        # Запуск основного класса и всех дочерних классов в одной строке
        window = [cls(ws) for cls in FindIndexPZ.__subclasses__()]
        # CreatePZ.cat_P_1 = list(map(int, [
        #     CreatePZ.dict_category[plast]['по давлению'].category for plast in CreatePZ.plast_work if
        #     CreatePZ.dict_category.get(plast) and CreatePZ.dict_category[plast]['отключение'] == 'рабочий'
        # ]))
        #
        # CreatePZ.cat_P_1_plan = list(map(int, [
        #     CreatePZ.dict_category[plast]['по давлению'].category for plast in CreatePZ.plast_work if
        #     CreatePZ.dict_category.get(plast) and CreatePZ.dict_category[plast]['отключение'] == 'планируемый'
        # ]))
        #
        # CreatePZ.cat_H2S_list = list(map(int,
        #                                  [CreatePZ.dict_category[plast]['по сероводороду'].category for plast in
        #                                   CreatePZ.plast_work if
        #     CreatePZ.dict_category.get(plast) and CreatePZ.dict_category[plast]['отключение'] == 'рабочий']))
        #
        # CreatePZ.cat_H2S_list_plan = list(map(int,
        #                                  [CreatePZ.dict_category[plast]['по сероводороду'].category for plast in
        #                                   CreatePZ.plast_work if
        #                                   CreatePZ.dict_category.get(plast) and
        #                                   CreatePZ.dict_category[plast]['отключение'] == 'планируемый']))
        #
        # CreatePZ.cat_gaz_f_pr = list(map(int,
        #                                  [CreatePZ.dict_category[plast]['по газовому фактору'].category for plast in
        #                                   CreatePZ.plast_work if
        #     CreatePZ.dict_category.get(plast) and CreatePZ.dict_category[plast]['отключение'] == 'рабочий']))
        #
        # CreatePZ.H2S_pr = list(map(float,
        #                                  [CreatePZ.dict_category[plast]['по сероводороду'].data_procent for plast in
        #                                   CreatePZ.plast_work if
        #     CreatePZ.dict_category.get(plast) and CreatePZ.dict_category[plast]['отключение'] == 'рабочий']))
        #
        # CreatePZ.H2S_mg = list(map(float,
        #                            [CreatePZ.dict_category[plast]['по сероводороду'].data_mg_l for plast in
        #                             CreatePZ.plast_work if
        #     CreatePZ.dict_category.get(plast) and CreatePZ.dict_category[plast]['отключение'] == 'рабочий']))

        for row_ind, row in enumerate(ws.iter_rows(values_only=True)):
            ws.row_dimensions[row_ind].hidden = False

            if any(['ПЛАН РАБОТ' in str(col) for col in row]):
                CreatePZ.number_dp, ok = QInputDialog.getText(None, 'Номер дополнительного плана работ',
                                                              'Введите номер дополнительного плана работ')
                ws.cell(row=row_ind + 1, column=2).value = f'ДОПОЛНИТЕЛЬНЫЙ ПЛАН РАБОТ № {CreatePZ.number_dp}'
                print(f'номер доп плана {CreatePZ.number_dp}')

            if 'План-заказ' in row:
                ws.cell(row=row_ind + 1, column=2).value = 'ПЛАН РАБОТ'

            for col, value in enumerate(row):
                if not value is None and col <= 12:
                    if 'гипс' in str(value).lower() or 'гидратн' in str(value).lower():
                        CreatePZ.gipsInWell = True


        CreatePZ.region = block_name.region(CreatePZ.cdng._value)
        thread = main.ExcelWorker()

        CreatePZ.without_damping = thread.check_well_existence(
            CreatePZ.well_number._value, CreatePZ.well_area._value, CreatePZ.region)



        if CreatePZ.leakiness == True:
            leakiness_quest = QMessageBox.question(self, 'нарушение колонны',
                                                   'Программа определела что в скважине'
                                                   f'есть нарушение - {CreatePZ.leakiness_Count}, верно ли?')
            if leakiness_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.leakiness = True
                krs.get_leakiness(self)

            else:
                CreatePZ.leakiness = False

        if CreatePZ.emergency_well == True:
            emergency_quest = QMessageBox.question(self, 'Аварийные работы ',
                                                   'Программа определела что в скважине'
                                                   f'авария - {CreatePZ.emergency_count}, верно ли?')
            if emergency_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.emergency_well = True
            else:
                CreatePZ.emergency_well = False
        if CreatePZ.problem_with_ek == True:
            problem_with_ek_quest = QMessageBox.question(self, 'ВНИМАНИЕ НЕПРОХОД ',
                                                   'Программа определела что в скважине '
                                                   f'ссужение в ЭК -, верно ли?')
            if problem_with_ek_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.problem_with_ek = True
                CreatePZ.problem_with_ek_depth, ok = QInputDialog.getInt(None, 'Глубина сужения',
                                                        "ВВедите глубину сужения", 0, 0, int(CreatePZ.current_bottom))
                CreatePZ.problem_with_ek_diametr, ok = QInputDialog.getInt(None, 'диаметр внутренний сужения',
                                                        "ВВедите внутренний диаметр сужения", 0, 0,
                                                                int(CreatePZ.current_bottom))
            else:
                CreatePZ.problem_with_ek = False

        if CreatePZ.gipsInWell == True:
            gips_true_quest = QMessageBox.question(self, 'Гипсовые отложения',
                                                   'Программа определела что скважина осложнена гипсовыми отложениями '
                                                   'и требуется предварительно определить забой на НКТ, верно ли это?')

            if gips_true_quest == QMessageBox.StandardButton.Yes:
                CreatePZ.gipsInWell = True
            else:
                CreatePZ.gipsInWell = False

        # Копирование изображения
        image_loader = SheetImageLoader(ws)

        for row in range(1, CreatePZ.data_well_max._value):
            for col in range(1, 12):
                try:
                    image = image_loader.get(f'{get_column_letter(col)}{row}')
                    image.save(f'imageFiles/image_work/image{get_column_letter(col)}{row}.png')
                    image_size = image.size
                    image_path = f'imageFiles/image_work/image{get_column_letter(col)}{row}.png'

                    coord = f'{get_column_letter(col)}{row + 17 - CreatePZ.cat_well_min}'

                    CreatePZ.image_list.append((image_path, coord, image_size))

                except:
                    pass


        for j in range(CreatePZ.data_x_min._value, CreatePZ.data_x_max._value):  # Ожидаемые показатели после ремонта
            lst = []
            for i in range(0, 12):
                lst.append(ws.cell(row=j + 1, column=i + 1).value)
            CreatePZ.row_expected.append(lst)



        if CreatePZ.work_plan != 'gnkt_frez':
            # print(f'план работ {CreatePZ.work_plan}')
            plan.delete_rows_pz(self, ws)
            razdel_1 = block_name.razdel_1(self, CreatePZ.region)

            for i in range(1, len(razdel_1)):  # Добавлением подписантов на вверху
                for j in range(1, 13):
                    ws.cell(row=i, column=j).value = razdel_1[i - 1][j - 1]
                    ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=7)
                ws.merge_cells(start_row=i, start_column=8, end_row=i, end_column=13)
            CreatePZ.ins_ind = 0

            CreatePZ.ins_ind += CreatePZ.data_well_max._value - CreatePZ.cat_well_min._value + 19
            # print(f' индекс вставки ГНВП{CreatePZ.ins_ind}')
            dict_events_gnvp = {}
            dict_events_gnvp['krs'] = events_gnvp()
            dict_events_gnvp['gnkt_opz'] = events_gnvp_gnkt()
            dict_events_gnvp['dop_plan'] = events_gnvp()
            # if work_plan != 'dop_plan':
            text_width_dict = {20: (0, 100), 30: (101, 200), 40: (201, 300), 60: (301, 400), 70: (401, 500),
                               90: (501, 600), 110: (601, 700), 120: (701, 800), 130: (801, 900),
                               150: (901, 1500), 270: (1500, 2300)}

            for i in range(CreatePZ.ins_ind, CreatePZ.ins_ind + len(dict_events_gnvp[work_plan]) - 1):
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=12)
                data = ws.cell(row=i, column=2)
                data.value = dict_events_gnvp[work_plan][i - CreatePZ.ins_ind][1]

                if 'Мероприятия' in str(data.value) or \
                        'Меры по предупреждению' in str(data.value) or \
                        "о недопустимости нецелевого расхода" in str(data.value):
                    data.alignment = Alignment(wrap_text=True, horizontal='center',
                                               vertical='center')
                    data.font = Font(name='Arial', size=13, bold=True)

                else:
                    data.alignment = Alignment(wrap_text=True, horizontal='left',
                                               vertical='top')
                    data.font = Font(name='Arial', size=12)

                # print(f'ГНВП -{data.value , len(data.value), len(dict_events_gnvp[work_plan])}')
                if not data.value is None:
                    text = data.value
                    for key, value in text_width_dict.items():
                        if value[0] <= len(text) <= value[1]:
                            ws.row_dimensions[i].height = int(key)

            ins_gnvp = CreatePZ.ins_ind
            CreatePZ.ins_ind += len(dict_events_gnvp[work_plan]) - 1

            ws.row_dimensions[2].height = 30
            ws.row_dimensions[6].height = 30

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
                ws.merge_cells(start_column=2, start_row=CreatePZ.ins_ind + 1, end_column=12,
                               end_row=CreatePZ.ins_ind + 1)
                CreatePZ.ins_ind += len(CreatePZ.row_expected)

                self.ins_ind_border = CreatePZ.ins_ind
                # wb.save(f"{CreatePZ.well_number}  1 {CreatePZ.well_area} {CreatePZ.cat_P_1}.xlsx")

            # wb.save(f'{CreatePZ.well_number} {CreatePZ.well_area} {work_plan}.xlsx')
            return ws

    def addItog(self, ws, ins_ind, work_plan):

        ws.delete_rows(ins_ind, self.table_widget.rowCount() - ins_ind + 1)
        if work_plan != 'gnkt_frez':
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
        print(f'куратор {curator_sel, CreatePZ.curator}')
        podp_down = block_name.pop_down(self, CreatePZ.region, curator_sel)

        for i in range(1 + ins_ind, 1 + ins_ind + len(podp_down)):  # Добавлением подписантов внизу
            for j in range(1, 13):
                ws.cell(row=i, column=j).value = podp_down[i - 1 - ins_ind][j - 1]
                ws.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=False)
            if i in [1 + ins_ind + 7, 1 + ins_ind + 8, 1 + ins_ind + 9,
                     1 + ins_ind + 10, 1 + ins_ind + 11,
                     1 + ins_ind + 12, 1 + ins_ind + 13, 1 + ins_ind + 14]:
                ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=6)
                ws.cell(row=i, column=2).alignment = Alignment(wrap_text=False, vertical='bottom', horizontal='left')
                ws.row_dimensions[i - 1].height = 30

                if i == 1 + ins_ind + 11:
                    ws.row_dimensions[i].height = 55
        ins_ind += len(podp_down)

    def is_valid_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def if_None(value):
        if isinstance(value, datetime):
            return value
        elif value is None or 'отс' in str(value).lower() or str(value).replace(' ', '') == '-' \
                or value == 0 or str(value).replace(' ', '') == '':
            return 'отсут'
        else:
            return value

    def definition_plast_work(self):
        # Определение работающих пластов
        plast_work = set()
        perforation_roof = CreatePZ.current_bottom
        perforation_sole = 0

        for plast, value in CreatePZ.dict_perforation.items():
            for interval in value['интервал']:
                # print(f' интервалы ПВР {plast, interval[0], CreatePZ.dict_perforation[plast]["отключение"]}')
                # print(CreatePZ.perforation_roof >= interval[0])
                if CreatePZ.current_bottom >= interval[0] and CreatePZ.dict_perforation[plast]["отключение"] is False:
                    plast_work.add(plast)

                if CreatePZ.dict_perforation[plast]["отключение"] is False:
                    roof = min(list(map(lambda x: x[0], list(CreatePZ.dict_perforation[plast]['интервал']))))
                    sole = max(list(map(lambda x: x[1], list(CreatePZ.dict_perforation[plast]['интервал']))))
                    CreatePZ.dict_perforation[plast]["кровля"] = roof
                    CreatePZ.dict_perforation[plast]["подошва"] = sole
                    if perforation_roof >= roof:
                        perforation_roof = roof
                    if perforation_sole < sole:
                        perforation_sole = sole

                else:

                    CreatePZ.dict_perforation[plast]["кровля"] = \
                        min(list(map(lambda x: x[0], list(CreatePZ.dict_perforation[plast]['интервал']))))
                    CreatePZ.dict_perforation[plast]["подошва"] = \
                        max(list(map(lambda x: x[1], list(CreatePZ.dict_perforation[plast]['интервал']))))

        CreatePZ.perforation_roof = perforation_roof
        CreatePZ.perforation_sole = perforation_sole
        # print(CreatePZ.dict_perforation)
        CreatePZ.plast_all = list(CreatePZ.dict_perforation.keys())
        CreatePZ.plast_work = list(plast_work)



    def pause_app(self):
        while CreatePZ.pause == True:
            QtCore.QCoreApplication.instance().processEvents()

    def count_row_height(ws, ws2, work_list, merged_cells_dict, ind_ins):
        from openpyxl.utils.cell import range_boundaries, get_column_letter

        boundaries_dict = {}

        text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 95: (301, 400), 110: (401, 500),
                           130: (501, 600), 150: (601, 700), 170: (701, 800), 190: (801, 900), 210: (901, 1500)}
        for ind, _range in enumerate(ws.merged_cells.ranges):
            boundaries_dict[ind] = range_boundaries(str(_range))

        rowHeights1 = [ws.row_dimensions[i].height for i in range(ws.max_row)]
        colWidth = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]
        # print(colWidth)
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
                cell = ws2.cell(row=i, column=j)
                if cell and str(cell) != str(work_list[i - 1][j - 1]):
                    if str(work_list[i - 1][j - 1]).replace('.', '').isdigit() and \
                            str(work_list[i - 1][j - 1]).count('.') != 2:
                        cell.value = str(work_list[i - 1][j - 1]).replace('.', ',')
                        # print(f'цифры {cell.value}')
                    else:
                        cell.value = work_list[i - 1][j - 1]
                    if i >= ind_ins:
                        if j != 1:
                            cell.border = CreatePZ.thin_border
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
        for row, col in merged_cells_dict.items():
            if len(col) != 2:
                # print(row)
                ws2.merge_cells(start_row=row + 1, start_column=3, end_row=row + 1, end_column=10)
        for key, value in boundaries_dict.items():
            # print(value)
            ws2.merge_cells(start_column=value[0], start_row=value[1],
                            end_column=value[2], end_row=value[3])

        head = plan.head_ind(0, ind_ins)
        # print(f'head - {head}')

        plan.copy_true_ws(ws, ws2, head)

        # вставка сохраненных изображение по координатам ячеек
        if CreatePZ.image_list:
            for img in CreatePZ.image_list:
                logo = Image(img[0])
                logo.width, logo.height = img[2][0] * 0.48, img[2][1] * 0.72
                ws2.add_image(logo, img[1])

        # print(f'высота строк работ {ins_ind}')
        # print(f'высота строк работ {len(rowHeights1)}')
        for index_row, row in enumerate(ws2.iter_rows()):  # Копирование высоты строки
            if all([col is None for col in row]):
                ws2.row_dimensions[index_row].hidden = True
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

        ws2.column_dimensions[get_column_letter(6)].width = 18

        return 'Высота изменена'

#
