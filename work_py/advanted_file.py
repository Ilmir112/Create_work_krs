from PyQt5.QtWidgets import QInputDialog


def raiding_interval():

    from open_pz import CreatePZ
    str_raid = []
    if len(CreatePZ.dict_perforation) == 1 and CreatePZ.perforation_sole + 30 <= CreatePZ.current_bottom:
        str_raid.append([CreatePZ.perforation_roof-30, CreatePZ.perforation_sole+30])
    elif len(CreatePZ.dict_perforation) == 1 and CreatePZ.perforation_sole + 30 >= CreatePZ.current_bottom:
        str_raid.append([CreatePZ.perforation_roof-30, CreatePZ.current_bottom])
    # print(str_raid)
    if len(CreatePZ.dict_perforation) > 1:
        for plast in CreatePZ.dict_perforation.keys():
            if plast in CreatePZ.plast_all:
                print(f' отрай {CreatePZ.dict_perforation[plast]["Прошаблонировано"]}')
                crt = []
                if CreatePZ.dict_perforation[plast]['отрайбировано'] == False:
                    for i in CreatePZ.dict_perforation[plast]['интервал']:
                        if int(i[1]) + 30 <= CreatePZ.current_bottom:
                            crt = [int(i[0]) - 30, int(i[1]) + 30]
                        else:
                            crt = [int(i[0]) - 30, CreatePZ.current_bottom]

                    if int(i[1]) < CreatePZ.current_bottom:
                        str_raid.append(crt)
                    print(CreatePZ.dict_work_pervorations.keys())

                    CreatePZ.dict_perforation[plast]['отрайбировано'] = True
                    if plast in CreatePZ.plast_work:
                        CreatePZ.dict_work_pervorations[plast]['отрайбировано'] = True

    try:
        roof_leakiness = int(list(CreatePZ.dict_leakiness.keys())[0].split('-')[0])
        if len(CreatePZ.dict_leakiness) == 1 and roof_leakiness + 30 <= CreatePZ.current_bottom:
            str_raid.append([roof_leakiness-30, roof_leakiness+30])
        elif len(CreatePZ.dict_leakiness) == 1 and roof_leakiness + 30 >= CreatePZ.current_bottom:
            str_raid.append([roof_leakiness-30, CreatePZ.current_bottom])

        if len(CreatePZ.dict_leakiness) >= 1:
            for nek in CreatePZ.dict_leakiness.keys():
                # print(CreatePZ.dict_leakiness[nek])
                if CreatePZ.dict_leakiness[nek]['отрайбировано'] == False:
                    i = nek.split('-')
                    print(i)

                    if int(i[1]) + 30 <= CreatePZ.current_bottom:
                        crt = [int(i[0]) - 30, int(i[1]) + 30]
                    else:
                        crt = [int(i[0]) - 30, CreatePZ.current_bottom]
                    str_raid.append(crt)
                CreatePZ.dict_leakiness[nek]['отрайбировано'] = True
    except:
        pass

    try:
        merged_segments=merge_overlapping_intervals(str_raid)
    except:
        str_raid1, ok = QInputDialog.getText(self, 'Райбирование ЭК',
                                             'Введите интервал райбирования через тире')
        str_raid = [str_raid1.split('-')]
        merged_segments = merge_overlapping_intervals(str_raid)
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
    print(a, len(a))
    if len(a) < 2:
        return f'{a[0][0]} - {a[0][1]}, '
    else:
        d = ''
        for i in list(a):
            d += f'{i[0]} - {i[1]}, '
    return d