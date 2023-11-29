from PyQt5.QtWidgets import QInputDialog, QMessageBox


def skm_interval():
    from open_pz import CreatePZ
    str_raid = []
    if all([CreatePZ.dict_work_pervorations[plast]['отрайбировано'] == False for plast in CreatePZ.plast_work]):
        str_raid.append([CreatePZ.perforation_roof - 90, CreatePZ.perforation_roof - 10])
        if CreatePZ.if_None(CreatePZ.paker_do["posle"]) != 'отсут' and CreatePZ.if_None(CreatePZ.H_F_paker_do["posle"]) != 'отсут' :
            str_raid.append([CreatePZ.H_F_paker_do["posle"] - 20, CreatePZ.H_F_paker_do["posle"] + 20])
        if CreatePZ.leakiness:

            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                print(f' наруш {nek}')
                if float(nek.split('-')[1]) + 20 < CreatePZ.current_bottom:
                    str_raid.append([int(float(nek.split('-')[0])) - 90, int(float(nek.split('-')[1])) + 20])
                else:
                    str_raid.append([int(float(nek.split('-')[0])) - 90,
                                     CreatePZ.CreatePZ.current_bottom - 2])
    else:
        if CreatePZ.paker_do["posle"] != 'отсут':
            str_raid.append([float(CreatePZ.H_F_paker_do["posle"]) - 20, float(CreatePZ.H_F_paker_do["posle"]) + 20])
        if CreatePZ.leakiness:
            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                if int(nek.split('-')[1]) + 20 < CreatePZ.current_bottom:
                    str_raid.append([int(nek.split('-')[0]) - 90, int(nek.split('-')[1]) + 20])
                else:
                    str_raid.append([int(nek.split('-')[0]) - 90,
                                     CreatePZ.CreatePZ.current_bottom - 2])

        for plast in CreatePZ.plast_all:
            intervalPvr = list(CreatePZ.dict_work_pervorations[plast]['интервал'])
            for pvr in intervalPvr:
                print(pvr)
                str_raid.append([pvr[0] - 90, pvr[1] - 10])
                if pvr[1] + 50 < CreatePZ.current_bottom:
                    str_raid.append([pvr[1] + 10, pvr[1] + 50])
                else:
                    str_raid.append([pvr[1] + 10, CreatePZ.current_bottom - 2])
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
            if ',' not in skm_column:
                a = []
                for i in skm_column.split('-'):
                    a.append(int(i))
                str_raid.append(a)
            else:
                for skm in skm_column.split(','):
                    a = []
                    for i in skm.split('-'):
                        a.append(int(i))
                    str_raid.append(a)

    print(f' Скрепер {str_raid}')
    merged_segments = merge_overlapping_intervals(str_raid)
    return merged_segments


def raiding_interval():
    from open_pz import CreatePZ
    str_raid = []
    if len(CreatePZ.dict_perforation) == 1 and CreatePZ.perforation_sole + 30 <= CreatePZ.current_bottom and CreatePZ.perforation_roof <= CreatePZ.current_bottom:
        str_raid.append([CreatePZ.perforation_roof - 30, CreatePZ.perforation_sole + 30])
    elif len(
            CreatePZ.dict_perforation) == 1 and CreatePZ.perforation_sole + 30 >= CreatePZ.current_bottom and CreatePZ.perforation_roof <= CreatePZ.current_bottom:

        str_raid.append([CreatePZ.perforation_roof - 30, CreatePZ.current_bottom])
    # print(str_raid)
    if len(CreatePZ.dict_perforation) > 1:
        for plast in CreatePZ.dict_perforation.keys():
            if plast in CreatePZ.plast_all:
                print(f' отрай {CreatePZ.dict_perforation[plast]["Прошаблонировано"]}')
                crt = []
                if CreatePZ.dict_perforation[plast]['отрайбировано'] == False:
                    for i in CreatePZ.dict_perforation[plast]['интервал']:
                        if float(i[1]) + 30 <= CreatePZ.current_bottom:
                            crt = [float(i[0]) - 30, float(i[1]) + 30]
                        else:
                            crt = [float(i[0]) - 30, CreatePZ.current_bottom]

                    if float(i[1]) < CreatePZ.current_bottom:
                        str_raid.append(crt)
                    # print(CreatePZ.dict_work_pervorations.keys())




    # try:
    if CreatePZ.leakiness == True:
        roof_leakiness = float(list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys())[0].split('-')[1])
        if len(CreatePZ.dict_leakiness['НЭК']['интервал']) == 1 and roof_leakiness + 30 <= CreatePZ.current_bottom:
            str_raid.append([roof_leakiness - 30, roof_leakiness + 30])
        elif len(
                CreatePZ.dict_leakiness['НЭК']['интервал']) == 1 and roof_leakiness + 30 >= CreatePZ.current_bottom:
            str_raid.append([roof_leakiness - 30, CreatePZ.current_bottom])

        for nek in CreatePZ.dict_leakiness['НЭК']['интервал'].keys():
            # print(CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отрайбировано'])
            if CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отрайбировано'] == False:
                i = nek.split('-')
                print(float(i[0])-30)

                if float(i[1]) + 30 <= CreatePZ.current_bottom:
                    crt = (float(i[0]) - 30, float(i[1]) + 30)
                else:
                    crt = (float(i[0]) - 30, CreatePZ.current_bottom)
                str_raid.append(crt)
    merged_segments = merge_overlapping_intervals(str_raid)
    for plast in CreatePZ.plast_work:
        for interval in list((CreatePZ.dict_work_pervorations[plast]['интервал'])):
            for str in str_raid:
                if str[0] <= list(interval)[0] <= str[1]:
                    CreatePZ.dict_work_pervorations[plast]['отрайбировано'] = True
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
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    print(merged)
    return merged


def raid(a):
    from open_pz import CreatePZ
    print(a, len(a))
    if len(a) < 2:
        return f'{int(a[0][0])} - {int(a[0][1])}'
    elif len(a) > 1 and CreatePZ.column_additional == True:
        d = ''
        for i in list(a):
            if CreatePZ.head_column_additional <= i[0]:
                d += f'{int(i[0])} - {int(i[1])}, '
    else:
        d = ''
        for i in list(a):
            d += f'{int(i[0])} - {int(i[1])}, '
    return d[:-2]
