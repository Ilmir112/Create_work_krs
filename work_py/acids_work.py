from PyQt5.QtWidgets import QInputDialog, QMessageBox


import well_data
from krs import well_volume
from selectPlast import CheckBoxDialog
from work_py.rationingKRS import well_volume_norm
from main import MyWindow



def acid_work(self):
    from work_py.swabbing import Swab_Window
    from work_py.opressovka import OpressovkaEK
    from work_py.alone_oreration import privyazkaNKT
    from work_py.acid_paker import AcidPakerWindow
    from work_py.rationingKRS import liftingNKT_norm, descentNKT_norm, well_volume_norm

    if len(well_data.plast_work) == 0:
        msc = QMessageBox.information(self, 'Внимание', 'Отсутствуют рабочие интервалы перфорации')
        return None
    else:
        # swabbing_true_quest1 = QMessageBox.question(self, 'Свабирование на данной компоновке',
        #                                            'Нужно ли Свабировать на данной компоновке?')
        #
        if self.acid_windowPaker is None:
            print(f' окно2 СКО ')
            self.acid_windowPaker = AcidPakerWindow()
            self.acid_windowPaker.setGeometry(200, 400, 300, 400)
            self.acid_windowPaker.show()
            MyWindow.pause_app()
            well_data.pause = True

        # if CreatePZswabbing_true_quest1 == QMessageBox.StandardButton.Yes:
        #     swabbing_true_quest = True
        # else:
        #     swabbing_true_quest = False


        # paker_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
        #                                       'Введите глубину посадки пакера', int(well_data.perforation_roof - 20), 0,
        #                                       5000)
        # paker_khost1 = int(well_data.perforation_sole - paker_depth)
        # print(f'хвостовик {paker_khost1}')
        # paker_khost, ok = QInputDialog.getInt(None, 'хвостовик',
        #                                       f'Введите длину хвостовика для подошвы ИП{well_data.perforation_sole} и глубины посадки пакера {paker_depth}',
        #                                       paker_khost1, 1, 4000)


        nkt_diam = ''.join(['73' if well_data.column_diametr._value > 110 else '60'])
        # print(f' 5 {well_data.column_additional == False, (well_data.column_additional == True and paker_depth < well_data.head_column_additional._value), swabbing_true_quest == False}')
        paker_diametr = OpressovkaEK.paker_diametr_select(well_data.paker_depth)
        if (well_data.column_additional == False and well_data.swabbing_true_quest == True) or (well_data.column_additional == True \
                and well_data.paker_depth < well_data.head_column_additional._value and well_data.swabbing_true_quest == True):
            paker_select = f'воронку + НКТ{nkt_diam}м {well_data.paker_khost}м + пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_diametr._value}мм х {well_data.column_wall_thickness._value}мм + НКТ 10м'
            dict_nkt = {73: well_data.paker_depth + well_data.paker_khost}

        elif well_data.column_additional == True and well_data.column_additional_diametr._value < 110 and \
                well_data.paker_depth > well_data.head_column_additional._value and well_data.swabbing_true_quest == True:
            paker_select = f'воронку + НКТ{60}мм {well_data.paker_khost}м + пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х {well_data.column_additional_wall_thickness._value}мм + НКТ60мм 10м '
            dict_nkt = {73: well_data.head_column_additional._value, 60: int(well_data.paker_depth - well_data.head_column_additional._value)}
        elif well_data.column_additional == True and well_data.column_additional_diametr._value > 110 and well_data.paker_depth > well_data.head_column_additional._value and well_data.swabbing_true_quest == True:
            paker_select = f'воронку + НКТ{well_data.nkt_diam}мм со снятыми фасками {well_data.paker_khost}м + пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х {well_data.column_additional_wall_thickness._value}мм + НКТ{well_data.nkt_diam}мм со снятыми фасками 10м'
            dict_nkt = {73: well_data.paker_depth + well_data.paker_khost}
        elif (well_data.column_additional == False and well_data.swabbing_true_quest == False) or (well_data.column_additional == True
                                                     and well_data.paker_depth < well_data.head_column_additional._value and well_data.swabbing_true_quest == False):

            dict_nkt = {73: well_data.paker_depth + well_data.paker_khost}
            # print(f' 5 {well_data.column_additional == False, (well_data.column_additional == True and paker_depth < well_data.head_column_additional._value), swabbing_true_quest == False}')
        elif well_data.column_additional == True or (well_data.column_additional_diametr._value < 110 and (well_data.paker_depth > well_data.head_column_additional._value) and well_data.swabbing_true_quest == False):
            paker_select = f'Заглушку + щелевой фильтр + НКТ{60}мм {well_data.paker_khost}м + пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х {well_data.column_additional_wall_thickness._value}мм + НКТ60мм 10м + сбивной клапан с ввертышем'
            dict_nkt = {73: well_data.head_column_additional._value, 60: int(well_data.paker_depth - well_data.head_column_additional._value)}
        elif well_data.column_additional == True and well_data.column_additional_diametr._value > 110 and well_data.paker_depth > well_data.head_column_additional._value \
                and well_data.swabbing_true_quest == False:
            paker_select = f'Заглушку + щелевой фильтр + НКТ{well_data.nkt_diam}мм со снятыми фасками {well_data.paker_khost}м + пакер ПРО-ЯМО-{paker_diametr}мм (либо аналог) ' \
                           f'для ЭК {well_data.column_additional_diametr._value}мм х {well_data.column_additional_wall_thickness._value}мм + НКТ{well_data.nkt_diam}мм со снятыми фасками 10м + сбивной клапан с ввертышем'
            dict_nkt = {73: well_data.paker_depth + well_data.paker_khost}

        elif nkt_diam == 60:
            dict_nkt = {60: well_data.paker_depth + well_data.paker_khost}

        paker_list = [
            [None, None,
             f'Спустить {paker_select} на НКТ{nkt_diam}м до глубины {well_data.paker_depth}м, воронкой до {well_data.paker_depth + well_data.well_data.paker_khost}м'
             f' с замером, шаблонированием шаблоном {well_data.nkt_template}мм. {("Произвести пробную посадку на глубине 50м" if well_data.column_additional == False else "")} '
             ,
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(well_data.paker_depth,1.2)],
            [None, None, f'Посадить пакер на глубине {well_data.paker_depth}м'
                ,
             None, None, None, None, None, None, None,
             'мастер КРС', 0.5],
            [None, None,
             f'Опрессовать эксплуатационную колонну в интервале {well_data.paker_depth}-0м на Р={well_data.max_admissible_pressure._value}атм'
             f' в течение 30 минут в присутствии представителя заказчика, составить акт. '
             f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', 0.83+0.58],
            [None, None,
             f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
             f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
             None, None, None, None, None, None, None,
             'мастер КРС', 0.7],
            [None, None,
             f'В случае негерметичности э/к, по согласованию с заказчиком произвести ОТСЭК для определения интервала '
             f'негерметичности эксплуатационной колонны с точностью до одного НКТ или запись РГД, ВЧТ с '
             f'целью определения места нарушения в присутствии представителя заказчика, составить акт. '
             f'Определить приемистость НЭК.',
             None, None, None, None, None, None, None,
             'мастер КРС', None],
            ]
        for plast in list(well_data.dict_perforation.keys()):
            for interval in well_data.dict_perforation[plast]['интервал']:
                if abs(float(interval[1] - well_data.paker_depth)) < 10 or abs(float(interval[0] - well_data.paker_depth)) < 10:
                    if privyazkaNKT(self) not in paker_list and well_data.privyazkaSKO == 0:
                        well_data.privyazkaSKO += 1
                        paker_list.insert(1, privyazkaNKT(self))
        if well_data.curator == 'ОР':
            definition_Q_quest = QMessageBox.question(self, 'Определение приемистости',
                                                       'Планировать опредение приемистости до СКО?')
            try:
                well_data.expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                     f'Ожидаемая приемистость по пласту {well_data.plast} ',
                                                     list(well_data.expected_pick_up.keys())[0], 0,
                                                     1600)
                well_data.expected_P, ok = QInputDialog.getInt(self, 'Ожидаемое Давление закачки',
                                                     f'Ожидаемое Давление закачки по пласту {plast}',
                                                     list(well_data.expected_pick_up.values())[0], 0,
                                                     250)
            except:
                well_data.expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                     f'Ожидаемая приемистость по пласту {well_data.plast} ',
                                                     100, 0,
                                                     1600)
                well_data.expected_P, ok = QInputDialog.getInt(self, f'Ожидаемое Давление закачки',
                                                     f'Ожидаемое Давление закачки по пласту {well_data.plast}',
                                                     100, 0,
                                                     250)

            if definition_Q_quest == QMessageBox.StandardButton.Yes:

                paker_list.insert(-2, [None, None,
                              f'Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
                              f'пласт {plast} на приемистость в трех режимах при Р={pressure_mode(well_data.expected_P, plast)}атм в присутствии представителя ЦДНГ. '
                              f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
                              f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {well_data.expected_Q}м3/сут при давлении {well_data.expected_P}атм '
                              f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                              None, None, None, None, None, None, None,
                              'мастер КРС', 0.17+0.52+0.2+0.2+0.2])

        for row in acid_work_list(self, well_data.paker_depth, well_data.paker_khost, dict_nkt, well_data.paker_layout):
            paker_list.append(row)

        reply_acid(self, well_data.paker_khost)
        paker_list.extend(acid_true_quest_list)

        if well_data.swabbing_true_quest:
            swabbing_with_paker = Swab_Window.swabbing_with_paker(self, well_data.paker_khost, 1)[1:]
            for row in swabbing_with_paker:
                paker_list.append(row)
        else:

            paker_list.append([None, None,
                                     f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {well_data.paker_depth}м с доливом скважины в '
                                     f'объеме {round(well_data.paker_depth * 1.12 / 1000, 1)}м3 удельным весом {well_data.fluid_work}',
                                     None, None, None, None, None, None, None,
                                     'мастер КРС',
                                     liftingNKT_norm(well_data.paker_depth, 1.2)])


    return paker_list

def open_checkbox_dialog():
    dialog = CheckBoxDialog()
    dialog.exec_()
def acid_work_list(self, paker_depth, paker_khost, dict_nkt, paker_layout):

    from krs import volume_vn_nkt
    from krs import well_volume
    from work_py.acid_paker import AcidPakerWindow

    open_checkbox_dialog()
    

    plast = well_data.plast_select
    # acid_true_quest_scv = QMessageBox.question(self, 'Необходимость кислотная ванна', 'Планировать кислотную ванну?')
    if well_data.acid_true_quest_scv == True:
        acid_true_scv = True
        # well_data.acid_V_scv, ok = QInputDialog.getDouble(self, 'Объем кислотной ванны', 'Введите объем кислоты:', 1, 0.2, 5, 1)
        # well_data.acid_pr_scv, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
        acid_work = [[None, None, f'Определить приемистость при Р-100атм в присутствии представителя заказчика.'
                                  f'при отсутствии приемистости произвести установку СКВ по согласованию с заказчиком',
     None, None, None, None, None, None, None,
     'мастер КРС, УСРСиСТ', 1.2],
                     [None, None, f'Произвести установку СКВ соляной кислотой {well_data.acid_pr_scv}% концентрации в объеме'
                                  f' {well_data.acid_V_scv}м3 (0,7т HCL 24%)(по спец. плану, составляет старший мастер)',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 1.2],
                     [None, None, f'закачать HCL-{well_data.acid_pr_scv}% в объеме V={well_data.acid_V_scv}м3; довести кислоту до пласта '
                                  f'тех.жидкостью в объеме {volume_vn_nkt(dict_nkt)}м3 . ',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 0.6],
                     [None, None, f'реагирование 2 часа.',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 2],
                     [None, None, f'Промыть скважину тех.жидкостью круговой циркуляцией обратной промывкой в 1,5 '
                                  f'кратном обьеме. Посадить пакер. Определить приемистость пласта в присутствии '
                                  f'представителя ЦДНГ (составить акт). Сорвать пакер. '
                                  f'При отсутствии приемистости СКВ повторить. При необходимости увеличить приемистость '
                                  f'методом дренирования.',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 0.83+0.2+0.83+0.5+0.5]]

    else:
        acid_work = []

    # well_data.acid_list = ['HCl', 'HF', 'ВТ', 'Нефтекислотка', 'Противогипсовая обработка']
    # well_data.acid, ok = QInputDialog.getItem(self, 'Вид кислоты', 'Введите вид кислоты:', well_data.acid_list, 0, False)
    # if ok and well_data.acid_list:
    #     self.le.setText(well_data.acid)








    if well_data.acid == 'HCl':
        # well_data.acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
        # well_data.acid_pr, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
        acid_sel = f'Произвести  солянокислотную обработку {plast}  в объеме  {well_data.acid_V}м3  ({well_data.acid} - {well_data.acid_pr} %) ' \
                   f' в ' \
                   f'присутствии представителя Заказчика с составлением акта, не превышая давления закачки не более Р={well_data.max_admissible_pressure._value}атм.\n' \
                   f'(для приготовления соляной кислоты в объеме {well_data.acid_V}м3 - {well_data.acid_pr}% необходимо замешать {round(well_data.acid_V * well_data.acid_pr / 24 * 1.118, 1)}т HCL 24% и' \
                   f' пресной воды {round(well_data.acid_V - well_data.acid_V * well_data.acid_pr / 24 * 1.118, 1)}м3)' \
                   f'Согласовать с Заказчиком проведение кислотной обработки силами ООО Крезол. '
    elif well_data.acid == 'ВТ':
        # acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
        vt, ok = QInputDialog.getText(None, 'Высокотехнологическая кислоты', 'Нужно расписать вид кислоты и объем')
        acid_sel = f'Произвести кислотную обработку {" ".join(well_data.plast_work)} {vt}  в присутствии представителя ' \
                   f'Заказчика с составлением акта, не превышая давления закачки не более Р={well_data.max_admissible_pressure._value}атм.'
    elif well_data.acid == 'HF':
        # well_data.acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
        # well_data.acid_pr, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
        well_data.acid_sel = f'Произвести кислотную обработку пласта {plast}  в объеме  {well_data.acid_V}м3  (концентрация в смеси HF 3% / HCl 13%) силами СК Крезол ' \
                   f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не более Р={well_data.max_admissible_pressure._value}атм.'
    elif well_data.acid == 'Нефтекислотка':
        # well_data.acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
        # well_data.acid_pr, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
        acid_oil, ok = QInputDialog.getInt(self, 'нефтекислотка', 'Введите объем нефти', 10, 0, 24)
        acid_sel = f'Произвести нефтекислотную обработку пласта{plast} в V=2тн товарной нефти + {well_data.acid_V}м3  (HCl - {well_data.acid_pr} %) + {well_data.acid_oil-2}т товарной нефти силами СК Крезол ' \
                   f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не более Р={well_data.max_admissible_pressure._value}атм.'
    elif well_data.acid == 'Противогипсовая обработка':

        # well_data.acid_V, ok = QInputDialog.getInt(self, 'противокислотная обработка', 'Введите объем едкого натрия', 10, 0, 24)
        well_data.acid_sel = f'Произвести противогипсовую обработку пласта{plast} в объеме {well_data.acid_V}м3 - {20}% раствором каустической соды' \
                   f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не ' \
                   f'более Р={well_data.max_admissible_pressure._value}атм.\n' \


    print(f'Ожидаемое показатели {well_data.expected_pick_up.values()}')
    acid_list_1 = [[None, None,
     f'{acid_sel}'
     f'ОБЕСПЕЧИТЬ НАЛИЧИЕ У СОСТАВА ВАХТЫ И СИЗ ПРИ КИСЛОТНОЙ ОБРАБОТКИ',
     None, None, None, None, None, None, None,
     'мастер КРС, УСРСиСТ', 8],
    [None, None,
     ''.join([f"Закачать кислоту в объеме V={round(volume_vn_nkt(dict_nkt), 1)}м3 (внутренний "
              f"объем НКТ)" if well_data.acid_V > volume_vn_nkt(dict_nkt) else f"Закачать кислоту в "
                                                                     f"объеме {round(well_data.acid_V, 1)}м3, "
                                                                     f"довести кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) - well_data.acid_V, 1)}м3 "]),
     None, None, None, None, None, None, None,
     'мастер КРС', None],
    [None, None,
     f'посадить пакер на глубине {paker_depth}м',
     None, None, None, None, None, None, None,
     'мастер КРС', None],
    [None, None,
     ''.join(
         [f'продавить  кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 при давлении не '
          f'более {well_data.max_admissible_pressure._value}атм. Увеличение давления согласовать'
          f' с заказчиком' if well_data.acid_V < volume_vn_nkt(
             dict_nkt) else f'продавить кислоту оставшейся кислотой в объеме {round(well_data.acid_V - volume_vn_nkt(dict_nkt), 1)}м3 и тех жидкостью '
                            f'в объеме {round(volume_vn_nkt(dict_nkt) * 1.5, 1)}м3 при давлении не более {well_data.max_admissible_pressure._value}атм. '
                            f'Увеличение давления согласовать с заказчиком']),
     None, None, None, None, None, None, None,
     'мастер КРС', None],
    [None, None,
     f'реагирование 2 часа.',
     None, None, None, None, None, None, None,
     'мастер КРС', 2],

    [None, None,
     f'Произвести срыв пакера с поэтапным увеличением нагрузки на 3-4т выше веса НКТ в течении 30мин и с '
     f'выдержкой 1ч для возврата резиновых элементов в исходное положение. ',
     None, None, None, None, None, None, None,
     'мастер КРС', 0.7],
    [None, None,
     flushingDownhole(self, paker_depth, paker_khost, paker_layout),
     None, None, None, None, None, None, None,
     'мастер КРС', well_volume_norm(well_volume(self, well_data.current_bottom))]]

    for row in acid_list_1:
        acid_work.append(row)

    if well_data.curator == 'ОР':
        acid_work.append([None, None,
                          f'Посадить пакер на {paker_depth}м. Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
                          f'пласт {plast} на приемистость в трех режимах при Р={pressure_mode(well_data.expected_P, plast)}атм в присутствии представителя ЦДНГ. '
                          f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
                          f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {well_data.expected_Q}м3/сут при давлении {well_data.expected_P}атм '
                          f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                          None, None, None, None, None, None, None,
                          'мастер КРС', 0.5 + 0.17 + 0.15+0.52+0.2+0.2+0.2])

    return acid_work

acid_true_quest_list = []
def reply_acid(self, paker_khost):

    from work_py.acid_paker import AcidPakerWindow
    acid_true_quest = QMessageBox.question(self, 'Необходимость кислоты',
                                           'Нужно ли планировать кислоту на следующий объет?')

    if acid_true_quest == QMessageBox.StandardButton.Yes:
        if self.acid_windowPaker is None:
            print(f' окно2 СКО ')
            self.acid_windowPaker = AcidPakerWindow()
            self.acid_windowPaker.setGeometry(200, 400, 300, 400)
            self.acid_windowPaker.show()
            MyWindow.pause_app()
            well_data.pause = True
        paker_layout = 2
        paker_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
                                          'Введите глубину посадки пакера', int(well_data.perforation_roof - 20), 0,
                                          int(well_data.current_bottom))

        acid_true_quest_list.append(
            [None, None, f'установить пакер на глубине {paker_depth}м', None, None, None, None, None, None, None,
             'мастер КРС', 1.2])

        for row in acid_work_list(self, paker_depth, paker_khost, well_data.dict_nkt, paker_layout):
            acid_true_quest_list.append(row)


        # print(reply_acid(self, difference_paker, paker_khost, dict_nkt, paker_select, nkt_diam, paker_depth_bottom))

        reply_acid(self, paker_khost)
    else:

        return acid_true_quest_list

# Определение трех режимов давлений при определении приемистости
def pressure_mode(mode, plast):


    mode = float(mode) / 10 * 10
    if mode > well_data.max_admissible_pressure._value and (plast != 'D2ps' or plast.lower() != 'дпаш'):
        mode_str = f'{float(mode)}, {float(mode)-10}, {float(mode)-20}'
    elif (plast == 'D2ps' or plast.lower() == 'дпаш') and well_data.region == 'ИГМ':
        mode_str = f'{120}, {140}, {160}'
    else:
        mode_str = f'{float(mode)-10}, {float(mode)}, {float(mode) + 10}'
    return mode_str


# промывка скважины после кислотной обработки в зависимости от интервала перфорации и комповноки и текущего забоя
def flushingDownhole(self, paker_depth, paker_khost, paker_layout):



    if paker_layout == 2:
        flushingDownhole_list = f'Только при наличии избыточного давления или когда при проведении ОПЗ получен технологический ""СТОП":' \
                                f'произвести промывку скважину обратной промывкой ' \
                                f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
                                f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
                                f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
    elif paker_depth + paker_khost >= well_data.current_bottom or (paker_depth + paker_khost < well_data.current_bottom):
        flushingDownhole_list = f'Допустить компоновку до глубины {well_data.current_bottom}м. Промыть скважину обратной промывкой ' \
                                f'по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не '\
                                f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth + paker_khost)*1.5,1)}м3 '\
                                f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
    elif paker_depth + paker_khost < well_data.current_bottom:
        flushingDownhole_list = f'Допустить пакер до глубины {int(well_data.perforation_roof-5)}м. (на 5м выше кровли интервала перфорации), ' \
                                f'низ НКТ до глубины {well_data.perforation_roof - 5 + paker_khost}м) ' \
                                f'Промыть скважину обратной промывкой по круговой циркуляции  жидкостью уд.весом {well_data.fluid_work} при расходе жидкости не ' \
                                f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'

    return flushingDownhole_list