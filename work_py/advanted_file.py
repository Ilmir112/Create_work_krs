import base64
from datetime import datetime
from io import BytesIO

from PyQt5.QtWidgets import QMessageBox

import plan
import data_list

from openpyxl.styles import Font, Alignment

def skm_interval(self, template):
    sgm_True = False
    if template in ['СГМ ЭК', 'СГМ открытый ствол' 'СГМ в основной колонне',
                                         'СГМ в доп колонне + открытый ствол',
                                         'СГМ в доп колонне']:
        sgm_True = True

    str_raid = []
    if self.dict_data_well["paker_do"]["posle"] != 0:
        str_raid.append(
            [float(self.dict_data_well["depth_fond_paker_do"]["posle"]) - 20,
             float(self.dict_data_well["depth_fond_paker_do"]["posle"]) + 20])

    if self.dict_data_well["dict_leakiness"]:
        a = self.dict_data_well["dict_leakiness"]
        for nek in list(self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()):
            if int(float(nek.split('-')[1])) + 20 < self.dict_data_well["current_bottom"]:
                str_raid.append([int(float(nek.split('-')[0])) - 90, int(float(nek.split('-')[1])) + 20])
            else:
                str_raid.append([int(float(nek.split('-')[0])) - 90,
                                 self.dict_data_well["current_bottom"] - 2])

    if all(
            [self.dict_data_well["dict_perforation"][plast]['отрайбировано'] is True for plast in self.dict_data_well["plast_all"]
             if self.dict_data_well["dict_perforation"][plast]['подошва'] < self.dict_data_well["current_bottom"]]) or sgm_True:
        str_raid = []

        perforating_intervals = []

        for plast in self.dict_data_well["plast_all"]:
            for interval in self.dict_data_well["dict_perforation"][plast]['интервал']:
                if interval[1] < self.dict_data_well["current_bottom"]:
                    perforating_intervals.append(list(interval))

        str_raid.extend(remove_overlapping_intervals(self, perforating_intervals))

    elif all([self.dict_data_well["dict_perforation"][plast]['отрайбировано'] is False for plast in self.dict_data_well["plast_all"]]):
        str_raid.append([self.dict_data_well["perforation_roof"] - 90, self.dict_data_well["skm_depth"]])
        if self.dict_data_well["dict_leakiness"]:
            for nek in list(self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()):
                # print(f' наруш {nek}')
                if float(nek.split('-')[1]) + 20 < self.dict_data_well["current_bottom"]:
                    str_raid.append([int(float(nek.split('-')[0])) - 90, int(float(nek.split('-')[1])) + 20])
                else:
                    str_raid.append([int(float(nek.split('-')[0])) - 90,
                                     self.dict_data_well["current_bottom"] - 2])


    if self.dict_data_well["plast_project"]:
        if any(
            [plast in self.dict_data_well['plast_all'] for plast in self.dict_data_well["plast_project"]]) is False:
            for plast in self.dict_data_well["dict_perforation_project"]:

                for interval in self.dict_data_well["dict_perforation_project"][plast]['интервал']:
                    if interval[1] < self.dict_data_well["current_bottom"]:
                        str_raid.append([interval[0] - 70, interval[1] + 20])
                    else:
                        str_raid.append([interval[0] - 70, self.dict_data_well["current_bottom"] - 2])

    # print(f'скреперо {str_raid}')
    merged_segments = merge_overlapping_intervals(str_raid)
    # print(f'скреперо после {merged_segments}')
    merged_segments_new = []

    for interval in merged_segments:

        if template in ['ПСШ ЭК', 'ПСШ без хвоста', 'ПСШ открытый ствол', 'СГМ ЭК', 'СГМ открытый ствол']:
            if self.dict_data_well["skm_depth"] >= interval[1] and interval[1] > interval[0]:
                merged_segments_new.append(interval)
            elif self.dict_data_well["skm_depth"] <= interval[1] and self.dict_data_well["skm_depth"] >= interval[0] and interval[1] > interval[
                0]:
                merged_segments_new.append([interval[0], self.dict_data_well["skm_depth"]])

        elif template in ['ПСШ СКМ в доп колонне c хвостом', 'ПСШ СКМ в доп колонне без хвоста',
                          'ПСШ СКМ в доп колонне + открытый ствол',
                                         'СГМ в доп колонне + открытый ствол',
                                         'СГМ в доп колонне'] and self.dict_data_well["skm_depth"] >= interval[1]:

            if interval[0] > float(self.dict_data_well["head_column_additional"]._value) and interval[1] >= float(
                    self.dict_data_well["head_column_additional"]._value) and self.dict_data_well["skm_depth"] >= interval[1] \
                    and interval[1] > interval[0]:
                # print(f'1 {interval, merged_segments}')
                merged_segments_new.append(interval)

            elif interval[0] < float(self.dict_data_well["head_column_additional"]._value) and interval[1] > float(
                    self.dict_data_well["head_column_additional"]._value) and self.dict_data_well["skm_depth"] <= interval[1] \
                    and self.dict_data_well["skm_depth"] >= interval[0] and interval[1] > interval[0]:
                # print(f'2 {interval, merged_segments}')

                merged_segments_new.append((self.dict_data_well["head_column_additional"]._value + 2, self.dict_data_well["skm_depth"]))
            elif interval[0] < float(self.dict_data_well["head_column_additional"]._value) and interval[1] > float(
                    self.dict_data_well["head_column_additional"]._value) and self.dict_data_well["skm_depth"] >= interval[1] and interval[1] > \
                    interval[0]:

                merged_segments_new.append((self.dict_data_well["head_column_additional"]._value + 2, interval[1]))
                # print(f'3 {interval, merged_segments}')

        elif template in ['ПСШ Доп колонна СКМ в основной колонне', 'СГМ в основной колонне']:
            if interval[0] < float(self.dict_data_well["head_column_additional"]._value) and interval[1] < float(
                    self.dict_data_well["head_column_additional"]._value) and self.dict_data_well["skm_depth"] >= interval[1] and interval[1] > \
                    interval[0]:
                merged_segments_new.append(interval)

            elif interval[0] < float(self.dict_data_well["head_column_additional"]._value) and interval[1] > float(
                    self.dict_data_well["head_column_additional"]._value) and self.dict_data_well["skm_depth"] <= interval[1] \
                    and self.dict_data_well["skm_depth"] >= interval[0] and interval[1] > interval[0]:
                # merged_segments.remove(interval)
                merged_segments_new.append((interval[0], self.dict_data_well["skm_depth"]))

    return merged_segments_new


# Функция исключения из интервалов скреперования интервалов ПВР
def remove_overlapping_intervals(self, perforating_intervals, skm_interval=None):
    if skm_interval is None:
        # print(f' перфорация_ {perforating_intervals}')
        skipping_intervals = []
        if self.dict_data_well["paker_do"]["posle"] != 0:
            if self.dict_data_well["skm_depth"] > self.dict_data_well["depth_fond_paker_do"]["posle"] + 20:
                skipping_intervals.append(
                    [float(self.dict_data_well["depth_fond_paker_do"]["posle"]) - 70,
                     float(self.dict_data_well["depth_fond_paker_do"]["posle"]) + 20])
                # print(f'1 {skipping_intervals}')
            elif self.dict_data_well["skm_depth"] > self.dict_data_well["depth_fond_paker_do"]["posle"]:
                skipping_intervals.append(
                    [float(self.dict_data_well["depth_fond_paker_do"]["posle"]) - 20, self.dict_data_well["skm_depth"]])
                # print(f'2 {skipping_intervals}')

        if self.dict_data_well["dict_leakiness"]:
            for nek in list(self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()):
                if int(float(nek.split('-')[1])) + 20 < self.dict_data_well["skm_depth"]:
                    skipping_intervals.append([int(float(nek.split('-')[0])) - 90, int(float(nek.split('-')[1])) + 20])
                else:
                    skipping_intervals.append([int(float(nek.split('-')[0])) - 90,
                                               self.dict_data_well["skm_depth"]])
        # print(f'глубина СКМ {self.dict_data_well["skm_depth"], skipping_intervals}')
        perforating_intervals = sorted(perforating_intervals, key=lambda x: x[0])

        for pvr in sorted(perforating_intervals, key=lambda x: x[0]):

            if pvr[1] + 40 < self.dict_data_well["skm_depth"]:
                skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                if self.dict_data_well["skm_depth"] >= pvr[1] + 40:
                    if [pvr[1] + 2, pvr[1] + 40] not in skipping_intervals:
                        skipping_intervals.append([pvr[1] + 2, pvr[1] + 40])
                else:
                    if [pvr[1] + 2, self.dict_data_well["skm_depth"]] not in skipping_intervals:
                        skipping_intervals.append([pvr[1] + 2, self.dict_data_well["skm_depth"]])
            elif pvr[1] + 40 > self.dict_data_well["skm_depth"]:
                if [pvr[0] - 90, pvr[0] - 2] not in skipping_intervals:
                    skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                if [pvr[1] + 1, self.dict_data_well["skm_depth"]] not in skipping_intervals:
                    skipping_intervals.append([pvr[1] + 1, self.dict_data_well["skm_depth"]])

        # print(f'СКМ на основе ПВР{sorted(skipping_intervals, key=lambda x: x[0])}')

        skipping_intervals = merge_overlapping_intervals(sorted(skipping_intervals, key=lambda x: x[0]))
        skipping_intervals_new = []
        for skm in sorted(skipping_intervals, key=lambda x: x[0]):
            kroly_skm = int(skm[0])
            pod_skm = int(skm[1])

            skm_range = list(range(kroly_skm, pod_skm))
            for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
                # print(int(pvr[0]) in skm_range, skm_range[0], int(pvr[0]))
                if int(pvr[0]) in skm_range and int(pvr[1]) in skm_range and skm_range[0] + 1 <= int(pvr[0]):
                    if skm_range[0] + 1 < int(pvr[0]) - 2:
                        skipping_intervals_new.append((skm_range[0] + 1, int(pvr[0] - 2)))
                        skm_range = skm_range[skm_range.index(int(pvr[1])):]
                    else:
                        skm_range = skm_range[skm_range.index(int(pvr[1]+1)):]

            skipping_intervals_new.append((skm_range[0], pod_skm))
    else:
        skipping_intervals_new = skm_interval

    return skipping_intervals_new


def raiding_interval(dict_data_well, ryber_key):
    str_raid = []
    crt = 0
    for plast in dict_data_well["plast_all"]:

        if dict_data_well["dict_perforation"][plast]['отрайбировано'] is False and \
                dict_data_well["dict_perforation"][plast]['кровля'] <= dict_data_well["current_bottom"]:

            for interval in dict_data_well["dict_perforation"][plast]['интервал']:
                if float(interval[1]) < dict_data_well["current_bottom"] and float(interval[0]) < float(interval[1]):
                    if dict_data_well["column_additional"] is False or \
                            (dict_data_well["column_additional"] and \
                             dict_data_well["head_column_additional"]._value > dict_data_well["current_bottom"]):

                        if float(interval[1]) + 20 <= dict_data_well["current_bottom"] and \
                                dict_data_well["shoe_column"]._value >= float(interval[1]) + 20:
                            crt = [float(interval[0]) - 20, float(interval[1]) + 20]
                        elif float(interval[1]) + 20 >= dict_data_well["shoe_column"]._value and \
                                dict_data_well["shoe_column"]._value > dict_data_well["current_bottom"]:
                            crt = [float(interval[0]) - 20, dict_data_well["shoe_column"]._value]
                        elif float(interval[1]) + 20 >= dict_data_well["shoe_column"]._value and \
                                dict_data_well["shoe_column"]._value <= dict_data_well["current_bottom"]:
                            crt = [float(interval[0]) - 20, dict_data_well["current_bottom"]]
                        elif float(interval[1]) + 20 < dict_data_well["shoe_column"]._value and \
                                float(interval[1] + 20) > dict_data_well["current_bottom"]:
                            crt = [float(interval[0]) - 20, dict_data_well["current_bottom"]]
                    else:
                        if float(interval[1]) + 20 <= dict_data_well["current_bottom"] and \
                                dict_data_well["shoe_column_additional"]._value >= float(interval[1]) + 20:
                            crt = [float(interval[0]) - 20, float(interval[1]) + 20]
                        elif float(interval[1]) + 20 >= dict_data_well["shoe_column_additional"]._value:
                            crt = [float(interval[0]) - 20, dict_data_well["shoe_column"]._value]
                        elif float(interval[1]) + 20 < dict_data_well["shoe_column_additional"]._value and \
                                float(interval[1] + 20) > dict_data_well["current_bottom"]:
                            crt = [float(interval[0]) - 20, dict_data_well["current_bottom"]]
                if crt != 0 and crt not in str_raid:
                    str_raid.append(crt)

    if len(dict_data_well["drilling_interval"]) != 0:
        for interval in dict_data_well["drilling_interval"]:
            if float(interval[1]) + 20 <= dict_data_well["current_bottom"] and interval[0] < interval[1]:
                str_raid.append((float(interval[0]) - 20, float(interval[1]) + 20))
            elif float(interval[1]) + 20 > dict_data_well["current_bottom"] and interval[0] < interval[1]:
                str_raid.append((float(interval[0]) - 20, dict_data_well["current_bottom"]))

    if len(dict_data_well["dict_leakiness"]) != 0:

        for nek in list(dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()):
            if dict_data_well["dict_leakiness"]['НЭК']['интервал'][nek]['отрайбировано'] is False:

                if float(nek.split('-')[1]) + 30 <= dict_data_well["current_bottom"] and float(
                        nek.split('-')[0]) + 30 <= dict_data_well["current_bottom"]:
                    crt = (float(nek.split('-')[0]) - 30, float(nek.split('-')[1]) + 30)
                else:
                    crt = (float(nek.split('-')[0]) - 30, dict_data_well["current_bottom"])
                str_raid.append(crt)

    merged_segments = merge_overlapping_intervals(str_raid)
    merged_segments_new = []
    if ryber_key == 'райбер в ЭК' and dict_data_well["column_additional"]:
        for str in merged_segments:
            if str[0] < dict_data_well["head_column_additional"]._value and str[0] < str[1]:
                merged_segments_new.append(str)

    elif ryber_key == 'райбер в ДП' and dict_data_well["column_additional"]:
        for str in merged_segments:
            if str[1] > dict_data_well["head_column_additional"]._value and str[0] < str[1]:
                merged_segments_new.append(str)
    else:
        for str in merged_segments:
            if str[0] < str[1]:
                merged_segments_new = merged_segments
    return merged_segments_new


def change_true_raid(self, str_raid):
    if self.dict_data_well["dict_leakiness"]:
        for nek in list(self.dict_data_well["dict_leakiness"]['НЭК']['интервал'].keys()):
            for str in str_raid:
                # print(str[0], list(nek)[0], str[1])
                if str[0] <= float(nek.split('-')[0]) <= str[1]:
                    self.dict_data_well["dict_leakiness"]['НЭК']['интервал'][nek]['отрайбировано'] = True
    if self.dict_data_well["plast_all"]:
        for plast in self.dict_data_well["plast_all"]:
            for interval in list((self.dict_data_well["dict_perforation"][plast]['интервал'])):
                for str in str_raid:
                    if str[0] <= list(interval)[0] <= str[1]:
                        self.dict_data_well["dict_perforation"][plast]['отрайбировано'] = True


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
        d = ''
        for i in list(string):
            d += f'{int(float(i[0]))} - {int(float(i[1]))}, '

    return d[:-2]


def definition_plast_work(self):
    from work_py.alone_oreration import calculation_fluid_work
    # Определение работающих пластов
    plast_work = set()
    perforation_roof = 5000
    perforation_sole = 0

    for plast, value in self.dict_data_well["dict_perforation"].items():
        for interval in value['интервал']:

            if self.dict_data_well["dict_perforation"][plast]["отключение"] is False:
                plast_work.add(plast)
            roof = min(list(map(lambda x: float(x[0]), list(self.dict_data_well["dict_perforation"][plast]['интервал']))))
            sole = max(list(map(lambda x: float(x[1]), list(self.dict_data_well["dict_perforation"][plast]['интервал']))))
            self.dict_data_well["dict_perforation"][plast]["кровля"] = roof
            self.dict_data_well["dict_perforation"][plast]["подошва"] = sole
            if self.dict_data_well["dict_perforation"][plast]["отключение"] is False:

                if perforation_roof >= roof and self.dict_data_well["current_bottom"] > roof:
                    perforation_roof = roof
                if perforation_sole < sole and self.dict_data_well["current_bottom"] > sole:
                    perforation_sole = sole
        zhgs = 1.01
        if "вертикаль" in list(self.dict_data_well["dict_perforation"][plast].keys()):
            vertical = min(self.dict_data_well["dict_perforation"][plast]["вертикаль"])
            pressuar = float(max(self.dict_data_well["dict_perforation"][plast]['давление']))
            if vertical and pressuar:
                zhgs = calculation_fluid_work(self.dict_data_well, vertical,pressuar)
                self.dict_data_well["dict_perforation"].setdefault(plast, {}).setdefault('рабочая жидкость',
                                                                                         []).append(zhgs)
            else:
                zhgs = 1.01
                self.dict_data_well["dict_perforation"].setdefault(plast, {}).setdefault('рабочая жидкость',
                                                                                         []).append(zhgs)

    self.dict_data_well["perforation_roof"] = perforation_roof
    self.dict_data_well["perforation_sole"] = perforation_sole
    self.dict_data_well["dict_perforation"] = dict(
        sorted(self.dict_data_well["dict_perforation"].items(), key=lambda item: (not item[1]['отключение'],
                                                                     item[0])))
    self.dict_data_well['plast_all'] = list(self.dict_data_well["dict_perforation"].keys())
    self.dict_data_well['plast_work'] = list(plast_work)
    self.dict_data_well["plast_all"] = list(self.dict_data_well["dict_perforation"].keys())
    data_list.plast_work = self.dict_data_well['plast_work']
    if len(self.dict_data_well["dict_perforation_project"]) != 0:
        self.dict_data_well["plast_project"] = list(self.dict_data_well["dict_perforation_project"].keys())




def count_row_height(self, wb2, ws, ws2, work_list, merged_cells_dict, ind_ins):
    from openpyxl.utils.cell import range_boundaries, get_column_letter
    from PIL import Image

    boundaries_dict = {}

    text_width_dict = {35: (0, 100), 50: (101, 200), 70: (201, 300), 95: (301, 400), 110: (401, 500),
                       150: (501, 600), 170: (601, 700), 190: (701, 800), 230: (801, 1000), 270: (1000, 1500)}

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

    head = plan.head_ind(0, ind_ins)

    plan.copy_true_ws(self.dict_data_well, ws, ws2, head)
    boundaries_dict_index = 1000
    stop_str = 1500
    for i in range(1, len(work_list) + 1):  # Добавлением работ
        a = work_list[i - 1]
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


    # try:
    #     # вставка сохраненных изображение по координатам ячеек
    #     if self.dict_data_well["image_list"]:
    #
    #         for img in self.dict_data_well["image_list"]:
    #             image_path = img[0]
    #             # logo = Image(image_path) # Используем open для открытия изображения
    #             # logo.width, logo.height = img[2][0] * 0.48, img[2][1] * 0.72
    #             ws2.add_image(image_path, img[1])
    # except TypeError as e:
    #     QMessageBox.warning(None, 'Ошибка', f'Ошибка Изменения размера изображения {type(e).__name__}\n\n{str(e)}')

    if self.dict_data_well["image_data"]:

        for image_info in self.dict_data_well["image_data"]:
            coord = image_info["coord"]
            width = image_info["width"]
            height = image_info["height"]
            image_base64 = image_info["data"]

            try:
                # Декодирование из Base64 и создание изображения:
                decoded_image_data = base64.b64decode(image_base64)

                # Создаем объект PIL Image из декодированных данных
                image = Image.open(BytesIO(decoded_image_data))
                print(image)
                # Проверка размеров изображения:
                print(f"Размеры изображения: {image.size}")

                file = f'{data_list.path_image}imageFiles/image_work/{coord}.png'

                # # Преобразуем изображение в режим RGB
                # image = image.convert('RGB')
                try:
                    image.save(file)
                except FileNotFoundError as f:
                    QMessageBox.warning(None, 'Ошибка', f'Не получилось вставить изображение {f}')
                    continue

                # Сохранение изображения в Excel файл:

                self.insert_image(ws2, file, coord, width * 0.72, height * 0.48)

            except ValueError as e:
                print(f"Ошибка при вставке изображения: {type(e).__name__}\n\n{str(e)}")

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