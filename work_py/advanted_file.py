import base64
from datetime import datetime
from io import BytesIO

from PyQt5.QtWidgets import QMessageBox

import plan
import data_list

from openpyxl.styles import Font, Alignment

def skm_interval(self, template):
    sgm_true = False
    if template in ['СГМ ЭК', 'СГМ открытый ствол' 'СГМ в основной колонне',
                                         'СГМ в доп колонне + открытый ствол',
                                         'СГМ в доп колонне']:
        sgm_true = True

    interval_raid = []
    if self.data_well.paker_before["after"] != 0:
        interval_raid.append([float(self.data_well.depth_fond_paker_before["after"]) - 20,
             float(self.data_well.depth_fond_paker_before["after"]) + 20])

    if self.data_well.paker_second_before["after"]:
        interval_raid.append([float(self.data_well.depth_fond_paker_second_before["after"]) - 20,
             float(self.data_well.depth_fond_paker_second_before["after"]) + 20])

    if self.data_well.dict_leakiness:
        for nek in list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()):
            if int(float(nek.split('-')[1])) + 20 < self.data_well.skm_depth:
                interval_raid.append([int(float(nek.split('-')[0])) - 90, int(float(nek.split('-')[1])) + 20])
            else:
                interval_raid.append([int(float(nek.split('-')[0])) - 90, self.data_well.skm_depth])
    asd = self.data_well.skm_depth
    perforating_intervals = []
    for plast in self.data_well.plast_all:
        for interval in self.data_well.dict_perforation[plast]['интервал']:
            if interval[1] <= self.data_well.skm_depth:
                interval_raid.append([interval[0] - 90, interval[1] - 2])
                if self.data_well.skm_depth >= interval[1] + 20:
                    if [interval[1] + 2, interval[1] + 20] not in interval_raid:
                        interval_raid.append([interval[1] + 2, interval[1] + 20])
                else:
                    if [interval[1] + 2, self.data_well.skm_depth] not in interval_raid:
                        interval_raid.append([interval[1] + 2, self.data_well.skm_depth])
                perforating_intervals.append(interval)

    if self.data_well.plast_project:
        for plast in self.data_well.dict_perforation_project:
            for interval in self.data_well.dict_perforation_project[plast]['интервал']:
                if interval[1] + 20 < self.data_well.skm_depth:
                    interval_raid.append([interval[0] - 70, interval[1] + 20])
    if perforating_intervals:
        interval_raid = remove_overlapping_intervals(self, perforating_intervals, interval_raid)

    merged_segments = merge_overlapping_intervals(interval_raid)
    
    merged_segments_new = []

    for interval in merged_segments:

        if template in ['ПСШ ЭК', 'ПСШ без хвоста', 'ПСШ открытый ствол', 'СГМ ЭК', 'СГМ открытый ствол']:
            if self.data_well.skm_depth >= interval[1] > interval[0]:
                merged_segments_new.append(interval)
            elif interval[1] >= self.data_well.skm_depth >= interval[0] and interval[1] > interval[0]:
                merged_segments_new.append([interval[0], self.data_well.skm_depth])

        elif template in ['ПСШ СКМ в доп колонне c хвостом', 'ПСШ СКМ в доп колонне без хвоста',
                          'ПСШ СКМ в доп колонне + открытый ствол',
                                         'СГМ в доп колонне + открытый ствол',
                                         'СГМ в доп колонне'] and self.data_well.skm_depth >= interval[1]:

            if float(self.data_well.head_column_additional.get_value) < interval[0] < interval[1] and float(
                    self.data_well.head_column_additional.get_value) <= interval[1] <= self.data_well.skm_depth:
                # print(f'1 {interval, merged_segments}')
                merged_segments_new.append(interval)

            elif (interval[0] < float(self.data_well.head_column_additional.get_value) < interval[1] 
                  and interval[1] >= self.data_well.skm_depth >= interval[0] and interval[1] > interval[0]):
                # print(f'2 {interval, merged_segments}')

                merged_segments_new.append((self.data_well.head_column_additional.get_value + 2, self.data_well.skm_depth))
            elif (interval[0] < float(self.data_well.head_column_additional.get_value) <
                  interval[1] <= self.data_well.skm_depth and interval[1] > interval[0]):

                merged_segments_new.append((self.data_well.head_column_additional.get_value + 2, interval[1]))
                # print(f'3 {interval, merged_segments}')

        elif template in ['ПСШ Доп колонна СКМ в основной колонне', 'СГМ в основной колонне']:
            if (interval[0] < float(self.data_well.head_column_additional.get_value) and
                    interval[1] < float(self.data_well.head_column_additional.get_value) and 
                    self.data_well.skm_depth >= interval[1] > interval[0]):
                merged_segments_new.append(interval)

            elif (interval[0] < float(self.data_well.head_column_additional.get_value) < interval[1] and
                  interval[1] >= self.data_well.skm_depth >= interval[0] and interval[1] > interval[0]):
                # merged_segments.remove(interval)
                merged_segments_new.append((interval[0], self.data_well.skm_depth))

    return merged_segments_new


# Функция исключения из интервалов скреперования интервалов ПВР
def remove_overlapping_intervals(self, perforating_intervals, skm_interval=None):
    skipping_intervals = []
    if skm_interval is None:
        # print(f' перфорация_ {perforating_intervals}')

        if self.data_well.paker_before["after"] != 0:
            if self.data_well.skm_depth > self.data_well.depth_fond_paker_before["after"] + 20:
                skipping_intervals.append(
                    [float(self.data_well.depth_fond_paker_before["after"]) - 70,
                     float(self.data_well.depth_fond_paker_before["after"]) + 20])
                # print(f'1 {skipping_intervals}')
            elif self.data_well.skm_depth > self.data_well.depth_fond_paker_before["after"]:
                skipping_intervals.append(
                    [float(self.data_well.depth_fond_paker_before["after"]) - 20, self.data_well.skm_depth])
                # print(f'2 {skipping_intervals}')

        if self.data_well.dict_leakiness:
            for nek in list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()):
                if int(float(nek.split('-')[1])) + 20 < self.data_well.skm_depth:
                    skipping_intervals.append([int(float(nek.split('-')[0])) - 90, int(float(nek.split('-')[1])) + 20])
                else:
                    skipping_intervals.append([int(float(nek.split('-')[0])) - 90,
                                               self.data_well.skm_depth])
        # print(f'глубина СКМ {self.data_well.skm_depth, skipping_intervals}')
        perforating_intervals = sorted(perforating_intervals, key=lambda x: x[0])
    skipping_intervals.extend(skm_interval)
    # for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
    #
    #     if pvr[1] + 20 < self.data_well.skm_depth:
    #         skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
    #         if self.data_well.skm_depth >= pvr[1] + 20:
    #             if [pvr[1] + 2, pvr[1] + 20] not in skipping_intervals:
    #                 skipping_intervals.append([pvr[1] + 2, pvr[1] + 20])
    #         else:
    #             if [pvr[1] + 2, self.data_well.skm_depth] not in skipping_intervals:
    #                 skipping_intervals.append([pvr[1] + 2, self.data_well.skm_depth])

    skipping_intervals = merge_overlapping_intervals(sorted(skipping_intervals, key=lambda x: x[0]))
    skipping_intervals_new = []
    for skm in sorted(skipping_intervals, key=lambda x: x[0]):
        krovly_skm = int(skm[0])
        pod_skm = int(skm[1])

        skm_range = list(range(krovly_skm, pod_skm))
        for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
            # print(int(pvr[0]) in skm_range, skm_range[0], int(pvr[0]))
            if int(pvr[0]) in skm_range and int(pvr[1]) in skm_range and skm_range[0] + 1 <= int(pvr[0]):
                if skm_range[0] + 1 < int(pvr[0]) - 2:
                    skipping_intervals_new.append((skm_range[0] + 1, int(pvr[0] - 2)))
                    skm_range = skm_range[skm_range.index(int(pvr[1])):]
                else:
                    skm_range = skm_range[skm_range.index(int(pvr[1]+1)):]
            else:
                skipping_intervals_new.append(skm)

    skipping_intervals_new.append((skm_range[0], pod_skm))
    return skipping_intervals_new


def raiding_interval(data_well, ryber_key):
    interval_raid = []
    crt = 0
    for plast in data_well.plast_all:

        if data_well.dict_perforation[plast]['отрайбировано'] is False and \
                data_well.dict_perforation[plast]['кровля'] <= data_well.current_bottom:

            for interval in data_well.dict_perforation[plast]['интервал']:
                if data_well.current_bottom > float(interval[1]) > float(interval[0]):
                    if (data_well.column_additional is False or 
                            (data_well.column_additional and data_well.head_column_additional.get_value 
                             > data_well.current_bottom)):

                        if float(interval[1]) + 20 <= data_well.current_bottom and \
                                data_well.shoe_column.get_value >= float(interval[1]) + 20:
                            crt = [float(interval[0]) - 20, float(interval[1]) + 20]
                        elif float(interval[1]) + 20 >= data_well.shoe_column.get_value > data_well.current_bottom:
                            crt = [float(interval[0]) - 20, data_well.shoe_column.get_value]
                        elif float(interval[1]) + 20 >= data_well.shoe_column.get_value and \
                                data_well.shoe_column.get_value <= data_well.current_bottom:
                            crt = [float(interval[0]) - 20, data_well.current_bottom]
                        elif float(interval[1]) + 20 < data_well.shoe_column.get_value and \
                                float(interval[1] + 20) > data_well.current_bottom:
                            crt = [float(interval[0]) - 20, data_well.current_bottom]
                    else:
                        if float(interval[1]) + 20 <= data_well.current_bottom and \
                                data_well.shoe_column_additional.get_value >= float(interval[1]) + 20:
                            crt = [float(interval[0]) - 20, float(interval[1]) + 20]
                        elif float(interval[1]) + 20 >= data_well.shoe_column_additional.get_value:
                            crt = [float(interval[0]) - 20, data_well.shoe_column.get_value]
                        elif float(interval[1]) + 20 < data_well.shoe_column_additional.get_value and \
                                float(interval[1] + 20) > data_well.current_bottom:
                            crt = [float(interval[0]) - 20, data_well.current_bottom]
                if crt != 0 and crt not in interval_raid:
                    interval_raid.append(crt)

    if len(data_well.drilling_interval) != 0:
        for interval in data_well.drilling_interval:
            if float(interval[1]) + 20 <= data_well.current_bottom and interval[0] < interval[1]:
                interval_raid.append((float(interval[0]) - 20, float(interval[1]) + 20))
            elif float(interval[1]) + 20 > data_well.current_bottom and interval[0] < interval[1]:
                interval_raid.append((float(interval[0]) - 20, data_well.current_bottom))

    if len(data_well.dict_leakiness) != 0:

        for nek in list(data_well.dict_leakiness['НЭК']['интервал'].keys()):
            if data_well.dict_leakiness['НЭК']['интервал'][nek]['отрайбировано'] is False:

                if float(nek.split('-')[1]) + 30 <= data_well.current_bottom and float(
                        nek.split('-')[0]) + 30 <= data_well.current_bottom:
                    crt = (float(nek.split('-')[0]) - 30, float(nek.split('-')[1]) + 30)
                else:
                    crt = (float(nek.split('-')[0]) - 30, data_well.current_bottom)
                interval_raid.append(crt)

    merged_segments = merge_overlapping_intervals(interval_raid)
    merged_segments_new = []
    if ryber_key == 'райбер в ЭК' and data_well.column_additional:
        for interval in merged_segments:
            if interval[0] < data_well.head_column_additional.get_value and interval[0] < interval[1]:
                merged_segments_new.append(interval)

    elif ryber_key == 'райбер в ДП' and data_well.column_additional:
        for interval in merged_segments:
            if interval[1] > data_well.head_column_additional.get_value and interval[0] < interval[1]:
                merged_segments_new.append(interval)
    else:
        for interval in merged_segments:
            if interval[0] < interval[1]:
                merged_segments_new = merged_segments
    return merged_segments_new


def change_true_raid(self, interval_raid):
    if self.data_well.dict_leakiness:
        for nek in list(self.data_well.dict_leakiness['НЭК']['интервал'].keys()):
            for interval in interval_raid:
                # print(interval[0], list(nek)[0], interval[1])
                if interval[0] <= float(nek.split('-')[0]) <= interval[1]:
                    self.data_well.dict_leakiness['НЭК']['интервал'][nek]['отрайбировано'] = True
    if self.data_well.plast_all:
        for plast in self.data_well.plast_all:
            for _ in list((self.data_well.dict_perforation[plast]['интервал'])):
                for interval in interval_raid:
                    if interval[0] <= list(interval)[0] <= interval[1]:
                        self.data_well.dict_perforation[plast]['отрайбировано'] = True


def merge_overlapping_intervals(intervals):
    merged = []
    intervals = sorted(intervals, key=lambda x: x[0])
    for interval in intervals:
        if interval[0] < interval[1]:
            if not merged or interval[0] > merged[-1][1]:
                merged.append(interval)
            else:
                if interval[0] < interval[1]:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    # print(f'интервалы СКМ {merged}')

    return merged


def raid(string):
    if len(string) == 1:
        return f'{int(float(string[0][0]))} - {int(float(string[0][1]))}'
    if len(string) == 0:
        return 'разбуренного цем моста'
    elif len(string) > 1:
        interval = ''
        for i in list(string):
            interval += f'{int(float(i[0]))} - {int(float(i[1]))}, '

    return interval[:-2]


def definition_plast_work(self):
    from work_py.alone_oreration import calculation_fluid_work
    # Определение работающих пластов
    plast_work = set()
    perforation_roof = 5000
    perforation_sole = 0

    for plast, value in self.data_well.dict_perforation.items():
        for _ in value['интервал']:

            if self.data_well.dict_perforation[plast]["отключение"] is False:
                plast_work.add(plast)
            roof = min(list(map(lambda x: float(x[0]), list(self.data_well.dict_perforation[plast]['интервал']))))
            sole = max(list(map(lambda x: float(x[1]), list(self.data_well.dict_perforation[plast]['интервал']))))
            self.data_well.dict_perforation[plast]["кровля"] = roof
            self.data_well.dict_perforation[plast]["подошва"] = sole
            if self.data_well.dict_perforation[plast]["отключение"] is False:

                if perforation_roof >= roof and self.data_well.current_bottom > roof:
                    perforation_roof = roof
                if perforation_sole < sole < self.data_well.current_bottom:
                    perforation_sole = sole
        zhgs = 1.01
        if "вертикаль" in list(self.data_well.dict_perforation[plast].keys()):

            vertical = min(filter(lambda x: type(x) in [float, int], self.data_well.dict_perforation[plast]["вертикаль"]))

            self.data_well.dict_perforation[plast]['давление'].append(0)
            pressure = float(max(filter(lambda x: type(x) in [float, int], self.data_well.dict_perforation[plast]['давление'])))

            if vertical and pressure:
                zhgs = calculation_fluid_work(self.data_well, vertical,pressure)
                self.data_well.dict_perforation.setdefault(plast, {}).setdefault('рабочая жидкость',
                                                                                         []).append(zhgs)
            else:

                self.data_well.dict_perforation.setdefault(plast, {}).setdefault('рабочая жидкость',
                                                                                         []).append(zhgs)

    self.data_well.perforation_roof = perforation_roof
    self.data_well.perforation_sole = perforation_sole
    self.data_well.dict_perforation = dict(
        sorted(self.data_well.dict_perforation.items(), key=lambda item: (not item[1]['отключение'],
                                                                     item[0])))
    self.data_well.plast_all = list(self.data_well.dict_perforation.keys())
    self.data_well.plast_work = list(plast_work)
    self.data_well.plast_all = list(self.data_well.dict_perforation.keys())
    data_list.plast_work = self.data_well.plast_work
    if len(self.data_well.dict_perforation_project) != 0:
        self.data_well.plast_project = list(self.data_well.dict_perforation_project.keys())




def count_row_height(self, wb2, ws, ws2, work_list, merged_cells_dict, ind_ins):
    from openpyxl.utils.cell import range_boundaries, get_column_letter
    from PIL import Image

    boundaries_dict = {}

    text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 95: (301, 400), 110: (401, 500),
                       150: (501, 600), 170: (601, 700), 190: (701, 800), 230: (801, 1000), 270: (1000, 1500)}

    for ind, _range in enumerate(ws.merged_cells.ranges):
        boundaries_dict[ind] = range_boundaries(str(_range))

    row_heights1 = [ws.row_dimensions[i].height for i in range(ws.max_row)]
    col_width = [ws.column_dimensions[get_column_letter(i + 1)].width for i in range(0, 13)] + [None]
    # print(col_width)
    for i, row_data in enumerate(work_list):
        for column, data in enumerate(row_data):
            if column == 2:
                if data is not None:
                    text = data
                    for key, value in text_width_dict.items():
                        if value[0] <= len(text) <= value[1]:
                            ws2.row_dimensions[i + 1].height = int(key)

    head = plan.head_ind(0, ind_ins)

    plan.copy_true_ws(self.data_well, ws, ws2, head)
    boundaries_dict_index = 1000
    stop_str = 1500
    for i in range(1, len(work_list) + 1):  # Добавлением работ
        if 'Наименование работ' in work_list[i - 1][2]:
            boundaries_dict_index = i + 1

        if 'код площади' in work_list[i - 1]:
            for j in range(1, 13):
                cell = ws2.cell(row=i, column=j)
                cell.number_format = 'General'
                cell.value = str(work_list[i - 1][j - 1])
        elif 'по H2S' in work_list[i - 1]:
            for j in range(1, 13):
                cell = ws2.cell(row=i, column=j)
                cell.number_format = 'General'
                cell.value = str(work_list[i - 1][j - 1])
        elif 'ИТОГО:' in work_list[i - 1]:
            stop_str = i

        for j in range(1, 13):
            cell = ws2.cell(row=i, column=j)
            if cell and str(cell) != str(work_list[i - 1][j - 1]):
                # print(work_list[i - 1][j - 1])
                cell.value = is_num(work_list[i - 1][j - 1])
                if i >= ind_ins:
                    if abs(i - ind_ins) > 1 and stop_str > i:
                        if self.work_plan in ['dop_plan', 'dop_plan_in_base']:
                            if 'Ранее проведенные работ' not in str(ws2[F"C{i}"].value):
                                ws2[F"B{i}"].value = f'=COUNTA($C${ind_ins + 3}:C{i})'
                        else:
                            ws2[F"B{i}"].value = f'=COUNTA($C${ind_ins + 2}:C{i})'
                    if j != 1:
                        cell.border = data_list.thin_border
                    if j == 11:
                        cell.font = Font(name='Arial', size=11, bold=False)
                    # if j == 12:
                    #     cell.value = work_list[i - 1][j - 1]
                    else:
                        cell.font = Font(name='Arial', size=13, bold=False)
                    if work_list[i - 1][4]:
                        ws2.cell(row=i-1, column=2).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
                        ws2.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
                    else:
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
                            or 'за 48 часов до спуска'.upper() in str(cell.value).upper() \
                            or 'Требования безопасности'.upper() in str(cell.value).upper() \
                            or 'Контроль воздушной среды проводится'.upper() in str(cell.value).upper() \
                            or 'ТЕХНОЛОГИЧЕСКИЕ ПРОЦЕССЫ'.upper() in str(cell.value).upper() \
                            or 'Требования безопасности при выполнении работ'.upper() in str(cell.value).upper() \
                            or 'за 48 часов до спуска'.upper() in str(cell.value).upper() \
                            or 'за 48 часов до спуска'.upper() in str(cell.value).upper() \
                            or 'за 48 часов до спуска'.upper() in str(cell.value).upper() \
                            or 'РИР' in str(cell.value).upper() \
                            or 'При отсутствии избыточного давления' in str(cell.value):
                        # print('есть жирный')
                        ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                    elif 'порядок работы' in str(cell.value).lower() or \
                            'наименование работ' in str(cell.value).lower():
                        ws2.cell(row=i, column=j).font = Font(name='Arial', size=13, bold=True)
                        ws2.cell(row=i, column=j).alignment = Alignment(wrap_text=True, horizontal='center',
                                                                        vertical='center')
    # print(merged_cells_dict)
    for row, col in merged_cells_dict.items():
        if len(col) != 2:
            # print(row)
            ws2.merge_cells(start_row=row + 1, start_column=3, end_row=row + 1, end_column=10)

    for key, value in boundaries_dict.items():

        if value[1] <= boundaries_dict_index-3:
            ws2.merge_cells(start_column=value[0], start_row=value[1],
                            end_column=value[2], end_row=value[3])


    if self.data_well.image_data:
        for image_info in self.data_well.image_data:
            coord = image_info["coord"]
            width = image_info["width"]
            height = image_info["height"]
            image_base64 = image_info["data"]

            try:
                # Декодирование из Base64 и создание изображения:
                decoded_image_data = base64.b64decode(image_base64)

                # Создаем объект PIL Image из декодированных данных
                image = Image.open(BytesIO(decoded_image_data))

                # Проверка размеров изображения:
                print(f"Размеры изображения: {image.size}")

                self.insert_image(ws2, image, coord, width * 0.72, height * 0.48)

            except ValueError as e:
                print(f"Ошибка при вставке изображения: {type(e).__name__}\n\n{str(e)}")

    for index_row, row in enumerate(ws2.iter_rows()):  # Копирование высоты строки
        if all([col is None for col in row]):
            ws2.row_dimensions[index_row].hidden = True
        try:
            if index_row < ind_ins:
                ws2.row_dimensions[index_row].height = row_heights1[index_row]
        except:
            pass
        if index_row == 2:
            for col_ind, col in enumerate(row):
                if col_ind <= 12:
                    ws2.column_dimensions[get_column_letter(col_ind + 1)].width = col_width[col_ind]
    ws2.column_dimensions[get_column_letter(11)].width = 20
    ws2.column_dimensions[get_column_letter(12)].width = 20

    ws2.column_dimensions[get_column_letter(6)].width = 18

    return 'Высота изменена'


def is_num(num):
    try:
        if isinstance(num, datetime):
            return num.strftime('%d.%m.%Y')
        elif str(round(float(num), 6))[-1] != 0:
            return round(float(num), 6)
        elif str(round(float(num), 5))[-1] != 0:
            return round(float(num), 5)
        elif str(round(float(num), 4))[-1] != 0:
            return round(float(num), 4)
        elif str(round(float(num), 3))[-1] != 0:
            return round(float(num), 3)
        elif str(round(float(num), 2))[-1] != 0:
            return round(float(num), 2)
        elif str(round(float(num), 1))[-1] != 0:
            return round(float(num), 1)
        elif str(round(float(num), 0))[-1] != 0:
            return int(float(num))
    except:
        return num