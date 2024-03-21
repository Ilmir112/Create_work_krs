from PyQt5.QtWidgets import QInputDialog, QMessageBox


def skm_interval(self, template):
    from open_pz import CreatePZ

    str_raid = []
    if CreatePZ.paker_do["posle"] != 0:
        str_raid.append([float(CreatePZ.depth_fond_paker_do["posle"]) - 20, float(CreatePZ.depth_fond_paker_do["posle"]) + 20])

    if CreatePZ.leakiness:
        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            if int(float(nek[1])) + 20 < CreatePZ.current_bottom:
                str_raid.append([int(float(nek[0])) - 90, int(float(nek[1])) + 20])
            else:
                str_raid.append([int(float(nek[0])) - 90,
                                 CreatePZ.current_bottom - 2])
    if all([CreatePZ.dict_perforation[plast]['отрайбировано'] is False for plast in CreatePZ.plast_work]):
        str_raid.append([CreatePZ.perforation_roof - 90, CreatePZ.skm_depth])
        if CreatePZ.leakiness:
            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                # print(f' наруш {nek}')
                if float(nek[1]) + 20 < CreatePZ.current_bottom:
                    str_raid.append([int(float(nek[0])) - 90, int(float(nek[1])) + 20])
                else:
                    str_raid.append([int(float(nek[0])) - 90,
                                     CreatePZ.current_bottom - 2])
        print(f'ПВР не отрайбированы {str_raid}')
    elif all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] is True for plast in CreatePZ.plast_work]):
        str_raid = []

        perforating_intervals = []

        for plast in CreatePZ.plast_all:
            for interval in CreatePZ.dict_perforation[plast]['интервал']:
                perforating_intervals.append(list(interval))


        str_raid.extend(remove_overlapping_intervals(perforating_intervals))

    if CreatePZ.dict_perforation_project is None and any(
            [plast in CreatePZ.plast_all for plast in list(CreatePZ.dict_perforation_project.keys())]) == False:
        if CreatePZ.dict_perforation_project[plast]['интервал'][1] < CreatePZ.current_bottom:
            str_raid.append([CreatePZ.dict_perforation_project[plast]['интервал'][1] + 10,
                             CreatePZ.dict_perforation_project[plast]['интервал'][1] + 50])
        else:
            str_raid.append([CreatePZ.dict_perforation_project[plast]['интервал'][1] + 10,
                             CreatePZ.current_bottom - 2])



    # print(f'скреперо {str_raid}')
    merged_segments = merge_overlapping_intervals(str_raid)
    # print(f'скреперо после {str_raid}')
    merged_segments_new = []
    # print(template)

    for interval in merged_segments:
        if template in ['ПСШ ЭК', 'ПСШ без хвоста', 'ПСШ открытый ствол']:
            if CreatePZ.skm_depth >= interval[1] and interval[1] > interval[0]:
                merged_segments_new.append(interval)
            elif CreatePZ.skm_depth <= interval[1] and CreatePZ.skm_depth >= interval[0] and interval[1] > interval[0]:
                merged_segments_new.append([interval[0], CreatePZ.skm_depth])


        elif template in ['ПСШ СКМ в доп колонне c хвостом', 'ПСШ СКМ в доп колонне без хвоста',
                          'ПСШ СКМ в доп колонне + открытый ствол'] and CreatePZ.skm_depth > interval[1]:
            if interval[0] > float(CreatePZ.head_column_additional._value) and interval[1] > float(
                    CreatePZ.head_column_additional._value) and CreatePZ.skm_depth >= interval[1] \
                    and interval[1] > interval[0]:
                merged_segments_new.append(interval)

            elif interval[0] < float(CreatePZ.head_column_additional._value) and interval[1] > float(
                    CreatePZ.head_column_additional._value) and CreatePZ.skm_depth <= interval[1] \
                    and CreatePZ.skm_depth >= interval[0] and interval[1] > interval[0]:

                merged_segments_new.append((CreatePZ.head_column_additional._value + 2, CreatePZ.skm_depth))
            elif interval[0] < float(CreatePZ.head_column_additional._value) and interval[1] > float(
                CreatePZ.head_column_additional._value) and CreatePZ.skm_depth >= interval[1] and interval[1] > interval[0]:

                merged_segments_new.append((CreatePZ.head_column_additional._value + 2, interval[1]))
                # print(f'2 {interval, merged_segments}')
        elif template in ['ПСШ Доп колонна СКМ в основной колонне']:
            if interval[0] < float(CreatePZ.head_column_additional._value) and interval[1] < float(
                    CreatePZ.head_column_additional._value) and CreatePZ.skm_depth >= interval[1] and interval[1] > interval[0]:
                merged_segments_new.append(interval)

            elif interval[0] < float(CreatePZ.head_column_additional._value) and interval[1] > float(
                    CreatePZ.head_column_additional._value) and CreatePZ.skm_depth <= interval[1] \
                    and CreatePZ.skm_depth >= interval[0] and interval[1] > interval[0]:
                # merged_segments.remove(interval)
                merged_segments_new.append((interval[0], CreatePZ.skm_depth))

    CreatePZ.skm_interval = merged_segments_new
    return merged_segments_new


# Функция исключения из интервалов скреперования интервалов ПВР
def remove_overlapping_intervals(perforating_intervals, skm_interval = None):
    from open_pz import CreatePZ

    if skm_interval is None:
        # print(f' перфорация_ {perforating_intervals}')
        skipping_intervals = []
        if CreatePZ.paker_do["posle"] != 0:
            if CreatePZ.skm_depth > CreatePZ.depth_fond_paker_do["posle"] + 20:
                skipping_intervals.append(
                    [float(CreatePZ.depth_fond_paker_do["posle"]) - 20, float(CreatePZ.depth_fond_paker_do["posle"]) + 20])
                # print(f'1 {skipping_intervals}')
            elif CreatePZ.skm_depth > CreatePZ.depth_fond_paker_do["posle"]:
                skipping_intervals.append(
                    [float(CreatePZ.depth_fond_paker_do["posle"]) - 20, CreatePZ.skm_depth])
                # print(f'2 {skipping_intervals}')

        if CreatePZ.leakiness:
            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                if int(float(nek[1])) + 20 < CreatePZ.skm_depth:
                    skipping_intervals.append([int(float(nek[0])) - 90, int(float(nek[1])) + 20])
                else:
                    skipping_intervals.append([int(float(nek[0])) - 90,
                                     CreatePZ.skm_depth])
        print(f'глубина СКМ {CreatePZ.skm_depth, skipping_intervals}')
        print(perforating_intervals)
        for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
            if pvr[1] <= CreatePZ.skm_depth:
                print(pvr, CreatePZ.skm_depth)
                if pvr[1] + 40 < CreatePZ.skm_depth and pvr[0] < CreatePZ.skm_depth:
                    skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                    if CreatePZ.skm_depth >= pvr[1] + 40:
                        if [pvr[1] + 2, pvr[1] + 40] not in skipping_intervals:
                            skipping_intervals.append([pvr[1] + 2, pvr[1] + 40])
                    else:
                        if [pvr[1] + 2, CreatePZ.skm_depth] not in skipping_intervals:
                            skipping_intervals.append([pvr[1] + 2, CreatePZ.skm_depth])
                elif pvr[1] + 40 > CreatePZ.skm_depth and pvr[0] < CreatePZ.skm_depth:
                    if [pvr[0] - 90, pvr[0] - 2] not in skipping_intervals:
                        skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                    if [pvr[1] + 1, CreatePZ.skm_depth] not in skipping_intervals:
                        skipping_intervals.append([pvr[1] + 1, CreatePZ.skm_depth])

        print(f'СКМ на основе ПВР{sorted(skipping_intervals, key=lambda x: x[0])}')

        skipping_intervals = merge_overlapping_intervals(sorted(skipping_intervals, key=lambda x: x[0]))
        skipping_intervals_new = []
        for skm in sorted(skipping_intervals, key=lambda x: x[0]):
            kroly_skm = int(skm[0])
            pod_skm = int(skm[1])

            skm_range = list(range(kroly_skm, pod_skm + 1))
            for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
                # print(int(pvr[0]) in skm_range, skm_range[0], int(pvr[0]))
                if int(pvr[0]) in skm_range and int(pvr[1]) in skm_range and skm_range[0]+1 <= int(pvr[0] - 1):
                    if skm_range[0]+1 < int(pvr[0]) - 2:
                        skipping_intervals_new.append((skm_range[0]+1, int(pvr[0] - 2)))
                        skm_range = skm_range[skm_range.index(int(pvr[1])):]



            skipping_intervals_new.append((skm_range[0], pod_skm))
    else:
        skipping_intervals_new = skm_interval

    print(f'после разделения {skipping_intervals_new}')



    return skipping_intervals_new


def raiding_interval(ryber_key):
    from open_pz import CreatePZ
    str_raid = []

    for plast in CreatePZ.dict_perforation.keys():
        if plast in CreatePZ.plast_all:

            if CreatePZ.dict_perforation[plast]['отрайбировано'] == False:
                for interval in CreatePZ.dict_perforation[plast]['интервал']:
                    if float(interval[1]) <= CreatePZ.current_bottom and float(interval[0]) <= CreatePZ.current_bottom:
                        if int(interval[0]) == int(CreatePZ.shoe_column._value) and CreatePZ.column_additional is False:
                            crt = [float(interval[0]) - 20, CreatePZ.shoe_column._value]
                            print(f'4 {crt}')
                        elif int(interval[1]) == int(CreatePZ.shoe_column_additional._value) and CreatePZ.column_additional:
                            crt = [float(interval[1]) - 20, CreatePZ.shoe_column_additional._value]
                            print(f'5 {crt}')
                        elif float(interval[1]) + 20 <= CreatePZ.current_bottom and \
                                CreatePZ.shoe_column._value >= float(interval[1]) + 20:
                            crt = [float(interval[0]) - 20, float(interval[1]) + 20]
                            print(f'1 {crt}')
                        elif float(interval[1]) + 20 >= CreatePZ.shoe_column._value and CreatePZ.column_additional is False:
                            crt = [float(interval[1]) - 20, CreatePZ.shoe_column._value]
                            print(f'2 {crt}')
                        elif float(interval[1]) - 20 >= CreatePZ.shoe_column_additional._value and CreatePZ.column_additional:
                            crt = [float(interval[0]), CreatePZ.shoe_column._value]
                            print(f'3 {crt}')
                        elif int(interval[0]) == int(CreatePZ.shoe_column._value) and CreatePZ.column_additional is False:
                            crt = [float(interval[0]) - 20, CreatePZ.shoe_column._value]
                            print(f'4 {crt}')
                        elif int(interval[1]) == int(CreatePZ.shoe_column_additional._value) and CreatePZ.column_additional:
                            crt = [float(interval[1]) - 20, CreatePZ.shoe_column_additional._value]
                            print(f'5 {crt}')
                        else:
                            crt = [float(interval[0]) - 20, CreatePZ.current_bottom]
                        str_raid.append(crt)

    if len(CreatePZ.drilling_interval) != 0:
        # print(CreatePZ.drilling_interval)
        for interval in CreatePZ.drilling_interval:
            # print(interval)
            if float(interval[1]) + 20 <= CreatePZ.current_bottom:
                str_raid.append((float(interval[0]) - 20, float(interval[1]) + 20))
            else:
                str_raid.append((float(interval[0]) - 20, CreatePZ.current_bottom))
  # print(CreatePZ.leakiness)
    if len(CreatePZ.dict_leakiness) != 0:

        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            if CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отрайбировано'] is False:

                if float(nek[1]) + 30 <= CreatePZ.current_bottom and float(nek[0]) + 30 <= CreatePZ.current_bottom:
                    crt = (float(nek[0]) - 30, float(nek[1]) + 30)
                else:
                    crt = (float(nek[0]) - 30, CreatePZ.current_bottom)
                str_raid.append(crt)
    # print(f' интервал райбире {str_raid}')
    if CreatePZ.column_additional is True and CreatePZ.current_bottom > CreatePZ.head_column_additional._value:
        if ryber_key == 'райбер в ЭК':
            # print(ryber_key)
            for str in str_raid:
                if str[0] > CreatePZ.head_column_additional._value or str[1] > CreatePZ.head_column_additional._value:
                    str_raid.remove(str)
        else:
            # print(ryber_key)
            for str in str_raid:

                if str[0] < CreatePZ.head_column_additional._value or str[1] < CreatePZ.head_column_additional._value:
                    str_raid.remove(str)

    merged_segments = merge_overlapping_intervals(str_raid)

    if CreatePZ.dict_leakiness:
        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            for str in str_raid:
                # print(str[0], list(nek)[0], str[1])
                if str[0] <= list(nek)[0] <= str[1]:
                    CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отрайбировано'] = True
    if CreatePZ.plast_all:
        for plast in CreatePZ.plast_all:
            for interval in list((CreatePZ.dict_perforation[plast]['интервал'])):
                for str in str_raid:
                    if str[0] <= list(interval)[0] <= str[1]:
                        CreatePZ.dict_perforation[plast]['отрайбировано'] = True


    return merged_segments


def merge_overlapping_intervals(intervals):

    merged = []

    intervals = sorted(intervals, key=lambda x: x[0])
    for interval in intervals:
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            if interval[0] < interval[1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    print(f'интервалы СКМ {merged}')

    return merged


def raid(a):
    from open_pz import CreatePZ


    if len(a) == 1:
        return f'{int(float(a[0][0]))} - {int(float(a[0][1]))}'
    if len(a) == 0:
        return 'разбуренного цем моста'
    elif len(a) > 1 and CreatePZ.column_additional == True:
        d = ''
        for i in list(a):
            if CreatePZ.head_column_additional._value <= i[0]:
                d += f'{int(float(i[0]))} - {int(float(i[1]))}, '
    else:
        d = ''
        print(a)
        for i in list(a):
            print(i)
            d += f'{int(float(i[0]))} - {int(float(i[1]))}, '



    return d[:-2]