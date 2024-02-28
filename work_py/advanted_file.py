from PyQt5.QtWidgets import QInputDialog, QMessageBox


def skm_interval(self, template):
    from open_pz import CreatePZ

    str_raid = []
    if CreatePZ.paker_do["posle"] != 0:
        str_raid.append([float(CreatePZ.H_F_paker_do["posle"]) - 20, float(CreatePZ.H_F_paker_do["posle"]) + 20])

    if CreatePZ.leakiness:
        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            if int(float(nek[1])) + 20 < CreatePZ.current_bottom:
                str_raid.append([int(float(nek[0])) - 90, int(float(nek[1])) + 20])
            else:
                str_raid.append([int(float(nek[0])) - 90,
                                 CreatePZ.current_bottom - 2])
    if all([CreatePZ.dict_perforation[plast]['отрайбировано'] is False for plast in CreatePZ.plast_work]):
        str_raid.append([CreatePZ.perforation_roof - 90, CreatePZ.perforation_roof - 10])

        if CreatePZ.leakiness:
            for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
                print(f' наруш {nek}')
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
    else:
        pvlg_rir = QMessageBox.question(None, 'переход - приобщение',
                                        'Планируются ли достреливать новые интервалы перфорации')

        if pvlg_rir == QMessageBox.StandardButton.Yes:

            skm_column, ok = QInputDialog.getText(None, 'Скреперование',
                                                      'Введите интервал скреперования через тире')


            while '-' not in skm_column:
                mes = QMessageBox.warning(None, 'Введены не корректные данные')
                skm_column, ok = QInputDialog.getText(None, 'Скреперование',
                                                      'Введите интервал скреперования через тире')
                while skm_column.split('-')[0] >= skm_column.split('-')[1]:
                    mes = QMessageBox.warning(None, 'Введенны не корректные данные')
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

    # print(f'скреперо {str_raid}')
    merged_segments = merge_overlapping_intervals(str_raid)
    # print(f'скреперо после {str_raid}')
    merged_segments_new = []
    # print(template)

    for interval in merged_segments:
        if template in ['ПСШ ЭК', 'ПСШ без хвоста', 'ПСШ открытый ствол']:
            merged_segments_new = merged_segments
        elif template in ['ПСШ открытый ствол']:
            if interval[0] < float(CreatePZ.shoe_column) and interval[1] < float(
                    CreatePZ.shoe_column):
                merged_segments_new.append(interval)

            elif interval[0] < float(CreatePZ.shoe_column) and interval[1] > float(
                    CreatePZ.shoe_column):

                merged_segments_new.append((interval[1], float(CreatePZ.shoe_column) -1))

        elif template in ['ПСШ СКМ в доп колонне c хвостом', 'ПСШ СКМ в доп колонне без хвоста',
                          'ПСШ СКМ в доп колонне + открытый ствол']:
            if interval[0] > float(CreatePZ.head_column_additional) and interval[1] > float(
                    CreatePZ.head_column_additional):
                merged_segments_new.append(interval)

            elif interval[0] < float(CreatePZ.head_column_additional) and interval[1] > float(
                    CreatePZ.head_column_additional):

                merged_segments_new.append((CreatePZ.head_column_additional + 2, interval[1]))
                # print(f'2 {interval, merged_segments}')
        elif template in ['ПСШ Доп колонна СКМ в основной колонне']:
            if interval[0] < float(CreatePZ.head_column_additional) and interval[1] < float(
                    CreatePZ.head_column_additional):
                merged_segments_new.append(interval)

            elif interval[0] < float(CreatePZ.head_column_additional) and interval[1] > float(
                    CreatePZ.head_column_additional):
                # merged_segments.remove(interval)
                merged_segments_new.append((interval[0], CreatePZ.head_column_additional - 2))
        elif template in ['ПСШ СКМ в доп колонне + открытый ствол']:
            if interval[0] < float(CreatePZ.shoe_column_additional) and interval[1] < float(
                    CreatePZ.shoe_column_additional):
                merged_segments_new.append(interval)
                # print(f'4 {interval, merged_segments}')
    # print(f'Новые интервалы {merged_segments_new}')
    for skip in merged_segments_new:
        skip_question = QMessageBox.question(None, 'Скреперование интервалов посадки',
                                             f'Нужно ли скреперованить интервал {skip}?')
        if skip_question == QMessageBox.StandardButton.No:
            merged_segments_new.pop(merged_segments_new.index(skip))

    CreatePZ.skm_interval.extend(merged_segments_new)
    return merged_segments_new


# Функция исключения из интервалов скреперования интервалов ПВР
def remove_overlapping_intervals(perforating_intervals):
    from open_pz import CreatePZ

    # print(f' перфорация_ {perforating_intervals}')
    skipping_intervals = []
    if CreatePZ.paker_do["posle"] != 0:
        if CreatePZ.skm_depth > CreatePZ.H_F_paker_do["posle"] + 20:
            skipping_intervals.append(
                [float(CreatePZ.H_F_paker_do["posle"]) - 20, float(CreatePZ.H_F_paker_do["posle"]) + 20])
            print(f'1 {skipping_intervals}')
        else:
            skipping_intervals.append(
                [float(CreatePZ.H_F_paker_do["posle"]) - 20, CreatePZ.skm_depth])
            print(f'2 {skipping_intervals}')
    if CreatePZ.paker2_do["posle"] != 0:
        if CreatePZ.skm_depth > CreatePZ.H_F_paker_do["posle"] + 20:
            skipping_intervals.append(
                [float(CreatePZ.H_F_paker_do["posle"]) - 20, float(CreatePZ.H_F_paker_do["posle"]) + 20])
            print(f'3 {skipping_intervals}')
        else:
            skipping_intervals.append(
                [float(CreatePZ.H_F_paker_do["posle"]) - 20, CreatePZ.skm_depth])
            print(f'4 {skipping_intervals}')
    if CreatePZ.leakiness:
        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            if int(float(nek[1])) + 20 < CreatePZ.skm_depth:
                skipping_intervals.append([int(float(nek[0])) - 90, int(float(nek[1])) + 20])
            else:
                skipping_intervals.append([int(float(nek[0])) - 90,
                                 CreatePZ.skm_depth])

    for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
        if pvr[1] <= CreatePZ.current_bottom:
            if pvr[1] + 40 < CreatePZ.current_bottom and pvr[0] < CreatePZ.current_bottom:
                skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                print(f'5 {skipping_intervals}')
                if CreatePZ.skm_depth >= pvr[1] + 40:
                    skipping_intervals.append([pvr[1] + 2, pvr[1] + 40])
                    print(f'6 {skipping_intervals}')
                else:
                    skipping_intervals.append([pvr[1] + 2, CreatePZ.skm_depth])
                    print(f'7 {skipping_intervals}')

            elif pvr[1] + 40 > CreatePZ.skm_depth and pvr[0] < CreatePZ.skm_depth:
                skipping_intervals.append([pvr[0] - 90, pvr[0] - 2])
                print(f'8 {skipping_intervals}')
                skipping_intervals.append([pvr[1] + 1, CreatePZ.skm_depth])
                print(f'9 {skipping_intervals}')


    print(f'СКМ на основе ПВР{sorted(skipping_intervals, key=lambda x: x[0])}')
    skipping_intervals = merge_overlapping_intervals(sorted(skipping_intervals, key=lambda x: x[0]))
    skipping_intervals_new = []
    for skm in sorted(skipping_intervals, key=lambda x: x[0]):
        kroly_skm = int(skm[0])
        pod_skm = int(skm[1])
        if CreatePZ.current_bottom >= pod_skm:
            skm_range = list(range(kroly_skm, pod_skm + 1))

            for pvr in sorted(perforating_intervals, key=lambda x: x[0]):
                # print(int(pvr[0]) in skm_range, skm_range[0], int(pvr[0]))
                if int(pvr[0]) in skm_range and int(pvr[1]) in skm_range and skm_range[0]+1 <= int(pvr[0] - 1):
                    # print(skm_range)
                    skipping_intervals_new.append((skm_range[0]+1, int(pvr[0] - 1)))
                    # print(skipping_intervals_new, skm_range.index(int(pvr[0]-2)))
                    # print(f' range {skm_range}')

                    skm_range = skm_range[skm_range.index(int(pvr[1])):]
            print(f' range {skm_range}')
            skipping_intervals_new.append((skm_range[0] + 2, pod_skm))

    print(f'после разделения {skipping_intervals_new}')



    return skipping_intervals_new


def raiding_interval(ryber_key):
    from open_pz import CreatePZ
    str_raid = []
    # if len(CreatePZ.dict_perforation) == 1 and CreatePZ.perforation_sole + 30 <= CreatePZ.current_bottom and \
    #         CreatePZ.perforation_roof <= CreatePZ.current_bottom:
    #     str_raid.append([CreatePZ.perforation_roof - 30, CreatePZ.perforation_sole + 30])
    #     print(f' кровля {str_raid, CreatePZ.perforation_sole}')
    # elif len(
    #         CreatePZ.dict_perforation) == 1 and CreatePZ.perforation_sole + 30 >= CreatePZ.current_bottom and \
    #         CreatePZ.perforation_roof <= CreatePZ.current_bottom:
    #
    #     str_raid.append([CreatePZ.perforation_roof - 30, CreatePZ.current_bottom])

    # if len(CreatePZ.dict_perforation) > 1:
    for plast in CreatePZ.dict_perforation.keys():
        if plast in CreatePZ.plast_all:

            if CreatePZ.dict_perforation[plast]['отрайбировано'] == False:
                for interval in CreatePZ.dict_perforation[plast]['интервал']:
                    if float(interval[1]) <= CreatePZ.current_bottom and float(interval[0]) <= CreatePZ.current_bottom:
                        if int(interval[0]) == int(CreatePZ.shoe_column) and CreatePZ.column_additional is False:
                            crt = [float(interval[0]) - 20, CreatePZ.shoe_column]
                            print(f'4 {crt}')
                        elif int(interval[1]) == int(CreatePZ.shoe_column_additional) and CreatePZ.column_additional:
                            crt = [float(interval[1]) - 20, CreatePZ.shoe_column_additional]
                            print(f'5 {crt}')
                        elif float(interval[1]) + 20 <= CreatePZ.current_bottom and \
                                CreatePZ.shoe_column >= float(interval[1]) + 20:
                            crt = [float(interval[0]) - 20, float(interval[1]) + 20]
                            print(f'1 {crt}')
                        elif float(interval[1]) + 20 >= CreatePZ.shoe_column and CreatePZ.column_additional is False:
                            crt = [float(interval[1]) - 20, CreatePZ.shoe_column]
                            print(f'2 {crt}')
                        elif float(interval[1]) - 20 >= CreatePZ.shoe_column_additional and CreatePZ.column_additional:
                            crt = [float(interval[0]), CreatePZ.shoe_column]
                            print(f'3 {crt}')
                        elif int(interval[0]) == int(CreatePZ.shoe_column) and CreatePZ.column_additional is False:
                            crt = [float(interval[0]) - 20, CreatePZ.shoe_column]
                            print(f'4 {crt}')
                        elif int(interval[1]) == int(CreatePZ.shoe_column_additional) and CreatePZ.column_additional:
                            crt = [float(interval[1]) - 20, CreatePZ.shoe_column_additional]
                            print(f'5 {crt}')
                        else:
                            crt = [float(interval[0]) - 20, CreatePZ.current_bottom]
                        str_raid.append(crt)
    print(f'интерва hfq {str_raid}')
    if len(CreatePZ.drilling_interval) != 0:
        # print(CreatePZ.drilling_interval)
        for interval in CreatePZ.drilling_interval:
            # print(interval)
            if float(interval[1]) + 20 <= CreatePZ.current_bottom:
                str_raid.append((float(interval[0]) - 20, float(interval[1]) + 20))
            else:
                str_raid.append((float(interval[0]) - 20, CreatePZ.current_bottom))

    if CreatePZ.leakiness == True:
        roof_leakiness = float(list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys())[0][0])


        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            if CreatePZ.dict_leakiness['НЭК']['интервал'][nek]['отрайбировано'] is False:

                if float(nek[1]) + 30 <= CreatePZ.current_bottom and float(nek[0]) + 30 <= CreatePZ.current_bottom:
                    crt = (float(nek[0]) - 30, float(nek[1]) + 30)
                else:
                    crt = (float(nek[0]) - 30, CreatePZ.current_bottom)
                str_raid.append(crt)
    # print(f' интервал райбире {str_raid}')
    if CreatePZ.column_additional == True and CreatePZ.current_bottom > CreatePZ.head_column_additional:
        if ryber_key == 'райбер в ЭК':
            # print(ryber_key)
            for str in str_raid:
                if str[0] > CreatePZ.head_column_additional or str[1] > CreatePZ.head_column_additional:
                    str_raid.remove(str)
        else:
            # print(ryber_key)
            for str in str_raid:

                if str[0] < CreatePZ.head_column_additional or str[1] < CreatePZ.head_column_additional:
                    str_raid.remove(str)
    pvlg_rir = QMessageBox.question(None, 'дополнительный интервал',
                                    'Нужно ли дополнительно интервал прорабатывать?')

    if pvlg_rir == QMessageBox.StandardButton.Yes:

        skm_column, ok = QInputDialog.getText(None, 'Райбирование',
                                              'Введите интервал райбирования через тире')

        while '-' not in skm_column:
            mes = QMessageBox.warning(None, 'Введены не корректные данные', 'Введены не корректные данные')
            skm_column, ok = QInputDialog.getText(None, 'Райбирование',
                                                  'Введите интервал райбирования через тире')
            while skm_column.split('-')[0] >= skm_column.split('-')[1]:
                mes = QMessageBox.warning(None, 'Введенны не корректные данные')
                skm_column, ok = QInputDialog.getText(None, 'Райбирование',
                                                      'Введите интервал райбирования через тире')
        str_raid.append((int(skm_column.split('-')[0]), int(skm_column.split('-')[1])))

    merged_segments = merge_overlapping_intervals(str_raid)
    if CreatePZ.dict_leakiness:
        for nek in list(CreatePZ.dict_leakiness['НЭК']['интервал'].keys()):
            for str in str_raid:
                print(str[0], list(nek)[0], str[1])
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
    from open_pz import CreatePZ
    merged = []
    print(intervals)
    intervals = sorted(intervals, key=lambda x: x[0])
    for interval in intervals:
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
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
            if CreatePZ.head_column_additional <= i[0]:
                d += f'{int(float(i[0]))} - {int(float(i[1]))}, '
    else:
        d = ''
        print(a)
        for i in list(a):
            print(i)
            d += f'{int(float(i[0]))} - {int(float(i[1]))}, '



    return d[:-2]