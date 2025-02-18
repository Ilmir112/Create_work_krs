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
                interval_raid.append([interval[0] - 90, interval[0] - 2])
                if self.data_well.skm_depth >= interval[1] + 20:
                    if [interval[1] + 2, interval[1] + 20] not in interval_raid:
                        interval_raid.append([interval[1] + 2, interval[1] + 20])
                else:
                    if [interval[1] + 2, self.data_well.skm_depth] not in interval_raid:
                        interval_raid.append([interval[1] + 2, self.data_well.skm_depth])
                perforating_intervals.append(interval)
            else:
                interval_raid.append([interval[0] - 90, self.data_well.skm_depth])

    if self.data_well.plast_project:
        for plast in self.data_well.dict_perforation_project:
            for interval in self.data_well.dict_perforation_project[plast]['интервал']:
                if interval[1] + 20 < self.data_well.skm_depth:
                    interval_raid.append([interval[0] - 70, interval[1] + 20])
    if perforating_intervals:
        interval_raid = remove_overlapping_intervals(self, perforating_intervals, interval_raid)
    else:
        interval_raid = [[self.data_well.skm_depth - 70, self.data_well.skm_depth]] + interval_raid

    merged_segments = merge_overlapping_intervals(interval_raid)

    merged_segments_new = []

    for interval in merged_segments:

        if template in ['ПСШ ЭК', 'ПСШ без хвоста', 'ПСШ открытый ствол', 'СГМ ЭК', 'СГМ открытый ствол', 'ПСШ + пакер']:
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

                merged_segments_new.append(
                    (self.data_well.head_column_additional.get_value + 2, self.data_well.skm_depth))
            elif (interval[0] < float(self.data_well.head_column_additional.get_value) <
                  interval[1] <= self.data_well.skm_depth and interval[1] > interval[0]):

                merged_segments_new.append((self.data_well.head_column_additional.get_value + 2, interval[1]))
                # print(f'3 {interval, merged_segments}


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
    if skm_interval:
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
        assdw = sorted(perforating_intervals, key=lambda x: x[0])
        for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
            # print(int(pvr[0]) in skm_range, skm_range[0], int(pvr[0]))
            if int(pvr[0]) in skm_range and int(pvr[1]) in skm_range and skm_range[0] + 1 <= int(pvr[0]):
                if skm_range[1] < int(pvr[0]) - 1:
                    if (skm_range[1], int(pvr[0] - 2)) not in skipping_intervals_new:
                        skipping_intervals_new.append((skm_range[0] + 1, int(pvr[0] - 2)))
                        skm_range = skm_range[skm_range.index(int(pvr[1])):]
                else:
                    skm_range = skm_range[skm_range.index(int(pvr[1] + 1)):]

            elif int(pvr[0]) in skm_range and int(pvr[1]) not in skm_range and skm_range[0] + 1 <= int(pvr[0]):
                if (skm_range[2], skm_range[-1]) not in skipping_intervals_new:
                    skipping_intervals_new.append((skm_range[2], pvr[1]-2))
            elif int(pvr[0]) >= skm_range[0]:
                if (skm_range[2], skm_range[-1]) not in skipping_intervals_new:
                    skipping_intervals_new.append((skm_range[2], skm_range[-1]))


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
            for roof, sole in list((self.data_well.dict_perforation[plast]['интервал'])):
                for interval in interval_raid:
                    if interval[0] <= roof <= interval[1] and interval[0] <= sole <= interval[1]:
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

            vertical = min(
                filter(lambda x: type(x) in [float, int], self.data_well.dict_perforation[plast]["вертикаль"]))

            self.data_well.dict_perforation[plast]['давление'].append(0)
            pressure = float(
                max(filter(lambda x: type(x) in [float, int], self.data_well.dict_perforation[plast]['давление'])))

            if vertical and pressure:
                zhgs = calculation_fluid_work(self.data_well, vertical, pressure)
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


