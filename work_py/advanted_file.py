from PyQt5.QtWidgets import QInputDialog, QMessageBox


def skm_interval():
    from open_pz import CreatePZ
    str_raid = []
    if CreatePZ.paker_do["posle"] != '0':
        str_raid.append([float(CreatePZ.H_F_paker_do["posle"]) - 20, float(CreatePZ.H_F_paker_do["posle"]) + 20])

    if CreatePZ.leakiness:
        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            if int(float(nek.split('-')[1])) + 20 < CreatePZ.current_bottom:
                str_raid.append([int(float(nek.split('-')[0])) - 90, int(float(nek.split('-')[1])) + 20])
            else:
                str_raid.append([int(float(nek.split('-')[0])) - 90,
                                 CreatePZ.current_bottom - 2])
    if all([CreatePZ.dict_perforation[plast]['отрайбировано'] == False for plast in CreatePZ.plast_work]):
        str_raid.append([CreatePZ.perforation_roof - 90, CreatePZ.perforation_roof - 10])
        if CreatePZ.if_None(CreatePZ.paker_do["posle"]) != '0' and CreatePZ.if_None(
                CreatePZ.H_F_paker_do["posle"]) != '0':
            str_raid.append([float(CreatePZ.H_F_paker_do["posle"]) - 20, float(CreatePZ.H_F_paker_do["posle"]) + 20])
        if CreatePZ.leakiness:
            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                print(f' наруш {nek}')
                if float(nek.split('-')[1]) + 20 < CreatePZ.current_bottom:
                    str_raid.append([int(float(nek.split('-')[0])) - 90, int(float(nek.split('-')[1])) + 20])
                else:
                    str_raid.append([int(float(nek.split('-')[0])) - 90,
                                     CreatePZ.CreatePZ.current_bottom - 2])
    elif all(
            [CreatePZ.dict_perforation[plast]['отрайбировано'] == True for plast in CreatePZ.plast_work]):


        perforating_intervals = []

        for plast in CreatePZ.plast_all:
            for interval in CreatePZ.dict_perforation[plast]['интервал']:
                perforating_intervals.append(list(interval))
        print(f'ПВР {perforating_intervals}')
        print(f'скрепр2{str_raid}')

        str_raid.extend(remove_overlapping_intervals(perforating_intervals))
    print(f'скреперо {str_raid}')
    if CreatePZ.dict_perforation_project is None and any(
            [plast in CreatePZ.plast_all for plast in list(CreatePZ.dict_perforation_project.keys())]) == False:
        if CreatePZ.dict_perforation_project[plast]['интервал'][1] < CreatePZ.current_bottom:
            str_raid.append([CreatePZ.dict_perforation_project[plast]['интервал'][1] + 10,
                             CreatePZ.dict_perforation_project[plast]['интервал'][1] + 50])
        else:
            str_raid.append([CreatePZ.dict_perforation_project[plast]['интервал'][1] + 10,
                             CreatePZ.current_bottom - 2])
    else:
        pvlg_rir = QMessageBox.question(None, 'переход - приобщение',
                                        'Планируются ли достреливать новые интервалы перфорации')

        if pvlg_rir == QMessageBox.StandardButton.Yes:
            skm_column, ok = QInputDialog.getText(None, 'Скреперование',
                                                  'Введите интервал скреперования через тире')
            while '-' not in skm_column:
                skm_column, ok = QInputDialog.getText(None, 'Скреперование',
                                                      'Введите интервал скреперования через тире')

            if ',' not in skm_column:
                a = []
                for i in skm_column.split('-'):
                    a.append(int(float(i)))
                str_raid.append(a)
            else:
                for skm in skm_column.split(','):
                    a = []
                    for i in skm.split('-'):
                        a.append(int(float(i)))
                    str_raid.append(a)

    print(f' Скрепер {str_raid}')
    merged_segments = merge_overlapping_intervals(str_raid)
    return merged_segments


# Функция исключения из интервалов скреперования интервалов ПВР
def remove_overlapping_intervals(perforating_intervals):
    from open_pz import CreatePZ

    # print(f' перфорация_ {perforating_intervals}')
    skipping_intervals = []
    for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
        if pvr[1] <= CreatePZ.current_bottom - 3:
            if pvr[1] + 40 < CreatePZ.current_bottom and pvr[0] < CreatePZ.current_bottom:
                skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                skipping_intervals.append([pvr[1] + 2, pvr[1] + 40])

            elif pvr[1] + 40 > CreatePZ.current_bottom and pvr[0] < CreatePZ.current_bottom:
                skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                skipping_intervals.append([pvr[1] + 2, CreatePZ.current_bottom - 2])

    print(f'СКМ на основе ПВР{sorted(skipping_intervals, key=lambda x: x[0])}')
    skipping_intervals = merge_overlapping_intervals(sorted(skipping_intervals, key=lambda x: x[0]))
    lll = []
    for skm in sorted(skipping_intervals, key=lambda x: x[0]):
        kroly_skm = int(skm[0])
        pod_skm = int(skm[1])
        if CreatePZ.current_bottom > pod_skm:
            skm_range = list(range(kroly_skm, pod_skm + 1))

            for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
                print(int(pvr[0]) in skm_range, skm_range[0], int(pvr[0]))
                if int(pvr[0]) in skm_range and int(pvr[1]) in skm_range:
                    # print(skm_range)
                    lll.append((skm_range[0]+1, int(pvr[0] - 1)))
                    # print(lll, skm_range.index(int(pvr[0]-2)))
                    print(f' range {skm_range}')

                    skm_range = skm_range[skm_range.index(int(pvr[1])):]
                    print(f' range {skm_range}')
            lll.append((skm_range[0] + 2, pod_skm))

    print(f'после разделения {lll}')

    return lll


def raiding_interval(ryber_key):
    from open_pz import CreatePZ
    str_raid = []
    if len(CreatePZ.dict_perforation) == 1 and CreatePZ.perforation_sole + 30 <= CreatePZ.current_bottom and \
            CreatePZ.perforation_roof <= CreatePZ.current_bottom:
        str_raid.append([CreatePZ.perforation_roof - 30, CreatePZ.perforation_sole + 30])
    elif len(
            CreatePZ.dict_perforation) == 1 and CreatePZ.perforation_sole + 30 >= CreatePZ.current_bottom and \
            CreatePZ.perforation_roof <= CreatePZ.current_bottom:

        str_raid.append([CreatePZ.perforation_roof - 30, CreatePZ.current_bottom])
    # print(str_raid)
    elif len(CreatePZ.dict_perforation) > 1:
        for plast in CreatePZ.dict_perforation.keys():
            if plast in CreatePZ.plast_all:
                # print(f' отрай {CreatePZ.dict_perforation[plast]["Прошаблонировано"]}')
                crt = []
                if CreatePZ.dict_perforation[plast]['отрайбировано'] == False:
                    for i in CreatePZ.dict_perforation[plast]['интервал']:
                        if float(i[1]) <= CreatePZ.current_bottom and float(i[0]) <= CreatePZ.current_bottom:
                            if float(i[1]) + 20 <= CreatePZ.current_bottom:
                                crt = [float(i[0]) - 20, float(i[1]) + 20]
                            else:
                                crt = [float(i[0]) - 20, CreatePZ.current_bottom]
                            str_raid.append(crt)

    if len(CreatePZ.drilling_interval) != 0:
        # print(CreatePZ.drilling_interval)
        for interval in CreatePZ.drilling_interval:
            # print(interval)
            if float(interval[1]) + 20 <= CreatePZ.current_bottom:
                str_raid.append((float(interval[0]) - 20, float(interval[1]) + 20))
            else:
                str_raid.append((float(interval[0]) - 20, CreatePZ.current_bottom))

    if CreatePZ.leakiness == True:
        roof_leakiness = float(list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys())[0].split('-')[1])
        if len(CreatePZ.dict_leakiness['НЭК']['интервал']) == 1 and roof_leakiness + 30 <= CreatePZ.current_bottom:
            str_raid.append([roof_leakiness - 30, roof_leakiness + 30])
        elif len(
                CreatePZ.dict_leakiness['НЭК']['интервал']) == 1 and roof_leakiness + 30 >= CreatePZ.current_bottom:
            str_raid.append([roof_leakiness - 30, CreatePZ.current_bottom])

        for nek in CreatePZ.dict_leakiness['НЭК']['интервал'].keys():
            if CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отрайбировано'] == False:
                i = nek.split('-')

                if float(i[1]) + 30 <= CreatePZ.current_bottom and float(i[0]) + 30 <= CreatePZ.current_bottom:
                    crt = (float(i[0]) - 30, float(i[1]) + 30)
                else:
                    crt = (float(i[0]) - 30, CreatePZ.current_bottom)
                str_raid.append(crt)
    print(f' интервал райбире {str_raid}')
    if CreatePZ.column_additional == True and CreatePZ.current_bottom > CreatePZ.head_column_additional:
        if ryber_key == 'райбер в ЭК':
            print(ryber_key)
            for str in str_raid:
                if str[0] > CreatePZ.head_column_additional or str[1] > CreatePZ.head_column_additional:
                    str_raid.remove(str)
        else:
            print(ryber_key)
            for str in str_raid:
                print()
                if str[0] < CreatePZ.head_column_additional or str[1] < CreatePZ.head_column_additional:
                    str_raid.remove(str)

    merged_segments = merge_overlapping_intervals(str_raid)

    for plast in CreatePZ.plast_work:
        for interval in list((CreatePZ.dict_perforation[plast]['интервал'])):
            for str in str_raid:
                if str[0] <= list(interval)[0] <= str[1]:
                    CreatePZ.dict_perforation[plast]['отрайбировано'] = True
    for plast in CreatePZ.plast_all:
        for interval in list((CreatePZ.dict_perforation[plast]['интервал'])):
            for str in str_raid:
                if str[0] <= list(interval)[0] <= str[1]:
                    CreatePZ.dict_perforation[plast]['отрайбировано'] = True
    return merged_segments


def merge_overlapping_intervals(intervals):
    from open_pz import CreatePZ
    merged = []
    intervals = sorted(intervals, key=lambda x: x[0])
    for interval in intervals:
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    print(f'интервалы СКМ {merged}')
    CreatePZ.skm_interval = merged
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
            if CreatePZ.head_column_additional <= i[0]:
                d += f'{int(float(i[0]))} - {int(float(i[1]))}, '
    else:
        d = ''
        print(a)
        for i in list(a):
            print(i)
            d += f'{int(float(i[0]))} - {int(float(i[1]))}, '
    return d[:-2]
