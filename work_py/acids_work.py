from PyQt5.QtWidgets import QInputDialog, QMessageBox


def acid_work(self):
    from work_py.opressovka import paker_diametr_select
    from work_py.swabbing import swabbing_with_paker
    from open_pz import CreatePZ

    swabbing_true_quest = QMessageBox.question(self, 'Свабирование на данной компоновке',
                                               'Нужно ли Свабировать на данной компоновке?')

    if swabbing_true_quest == QMessageBox.StandardButton.Yes:
        swabbing_true_quest = True
    else:
        swabbing_true_quest = False


    paker_depth, ok = QInputDialog.getInt(None, 'посадка пакера',
                                          'Введите глубину посадки пакера', int(CreatePZ.perforation_roof - 20), 0,
                                          5000)
    paker_khost1 = int(CreatePZ.perforation_sole - paker_depth)
    print(f'хвостовик {paker_khost1}')
    paker_khost, ok = QInputDialog.getInt(None, 'хвостовик',
                                          f'Введите длину хвостовика для подошвы ИП{CreatePZ.perforation_sole} и глубины посадки пакера {paker_depth}',
                                          paker_khost1, 1, 4000)


    nkt_diam = ''.join(['73' if CreatePZ.column_diametr > 110 else '60'])
    print(f' 5 {CreatePZ.column_additional == False, (CreatePZ.column_additional == True and paker_depth < CreatePZ.head_column_additional), swabbing_true_quest == False}')

    if (CreatePZ.column_additional == False and swabbing_true_quest == True) or (CreatePZ.column_additional == True \
            and paker_depth < CreatePZ.head_column_additiona and swabbing_true_quest == True):
        paker_select = f'воронку + НКТ{nkt_diam}м {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + НКТ 10м'
        dict_nkt = {73: paker_depth + paker_khost}

    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr < 110 and \
            paker_depth > CreatePZ.head_column_additional and swabbing_true_quest == True:
        paker_select = f'воронку + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ60мм 10м '
        dict_nkt = {73: CreatePZ.head_column_additional, 60: int(paker_depth - CreatePZ.head_column_additional)}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth > CreatePZ.head_column_additional and swabbing_true_quest == True:
        paker_select = f'воронку + НКТ73мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ73мм со снятыми фасками 10м'
        dict_nkt = {73: paker_depth + paker_khost}
    elif (CreatePZ.column_additional == False and swabbing_true_quest == False) or (CreatePZ.column_additional == True
                                                 and paker_depth < CreatePZ.head_column_additional and swabbing_true_quest == False):
        paker_select = f'Заглушку + щелевой фильтр + НКТ{nkt_diam}м {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм + НКТ 10м + сбивной клапан с ввертышем'
        dict_nkt = {73: paker_depth + paker_khost}
        # print(f' 5 {CreatePZ.column_additional == False, (CreatePZ.column_additional == True and paker_depth < CreatePZ.head_column_additional), swabbing_true_quest == False}')
    elif CreatePZ.column_additional == True or (CreatePZ.column_additional_diametr < 110 and (paker_depth > CreatePZ.head_column_additional) and swabbing_true_quest == False):
        paker_select = f'Заглушку + щелевой фильтр + НКТ{60}мм {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ60мм 10м + сбивной клапан с ввертышем'
        dict_nkt = {73: CreatePZ.head_column_additional, 60: int(paker_depth - CreatePZ.head_column_additional)}
    elif CreatePZ.column_additional == True and CreatePZ.column_additional_diametr > 110 and paker_depth > CreatePZ.head_column_additional \
            and swabbing_true_quest == False:
        paker_select = f'Заглушку + щелевой фильтр + НКТ73мм со снятыми фасками {paker_khost}м + пакер ПРО-ЯМО-{paker_diametr_select(paker_depth)}мм (либо аналог) ' \
                       f'для ЭК {CreatePZ.column_additional_diametr}мм х {CreatePZ.column_additional_wall_thickness}мм + НКТ73мм со снятыми фасками 10м + сбивной клапан с ввертышем'
        dict_nkt = {73: paker_depth + paker_khost}

    elif nkt_diam == 60:
        dict_nkt = {60: paker_depth + paker_khost}

    paker_list = [
        [None, None,
         f'Спустить {paker_select} на НКТ{nkt_diam}мм до глубины {paker_depth}м, воронкой до {paker_depth + paker_khost}м'
         f' с замером, шаблонированием шаблоном. {("Произвести пробную посадку на глубине 50м" if CreatePZ.column_additional == False else "")} '
         ,
         None, None, None, None, None, None, None,
         'мастер КРС', round(
            CreatePZ.current_bottom / 9.52 * 1.51 / 60 * 1.2 * 1.2 * 1.04 + 0.18 + 0.008 * CreatePZ.current_bottom / 9.52 + 0.003 * CreatePZ.current_bottom / 9.52,
            2)],
        [None, None, f'Посадить пакер на глубине {paker_depth}м'
            ,
         None, None, None, None, None, None, None,
         'мастер КРС', 0.4],
        [None, None,
         f'Опрессовать эксплуатационную колонну в интервале {paker_depth}-0м на Р={CreatePZ.max_admissible_pressure}атм'
         f' в течение 30 минут {"".join(["на наличие перетоков " if len(CreatePZ.leakiness) != 0 and min(CreatePZ.leakiness[0]) <= paker_depth else " "])} в присутствии представителя заказчика, составить акт.  '
         f'(Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до начала работ)',
         None, None, None, None, None, None, None,
         'мастер КРС, предст. заказчика', 1.],
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
         'мастер КРС', 0.4],

        ]


    for row in acid_work_list(self, paker_depth, paker_khost, dict_nkt, CreatePZ.paker_layout):
        paker_list.append(row)

    if swabbing_true_quest:
        swabbing_with_paker = swabbing_with_paker(self)[1:]
        for row in swabbing_with_paker:
            paker_list.append(row)
    else:
        paker_list.append([None, None,
                                 f'Поднять {paker_select} на НКТ{nkt_diam} c глубины {paker_depth}м с доливом скважины в '
                                 f'объеме {round(paker_depth * 1.12 / 1000, 1)}м3 удельным весом {CreatePZ.fluid_work}',
                                 None, None, None, None, None, None, None,
                                 'мастер КРС',
                                 round(0.25 + 0.033 * 1.2 * (paker_depth + paker_khost) / 9.5 * 1.04, 1)])


    return paker_list
def acid_work_list(self, paker_depth, paker_khost, dict_nkt, paker_layout):
    from open_pz import CreatePZ
    from krs import volume_vn_nkt
    # print(f'пласты {CreatePZ.plast}')
    plast, ok = QInputDialog.getItem(self, 'выбор пласта для ОПЗ ', 'выберете пласта дл перфорации',
                                     CreatePZ.plast_work, 0, False)
    if ok and plast:
        self.le.setText(plast)

    acid_true_quest_scv = QMessageBox.question(self, 'Необходимость кислотная ванна', 'Планировать кислотную ванну?')
    if acid_true_quest_scv == QMessageBox.StandardButton.Yes:
        acid_true_scv = True
        acid_V_scv, ok = QInputDialog.getDouble(self, 'Объем кислотной ванны', 'Введите объем кислоты:', 1, 0.2, 5, 1)
        acid_pr_scv, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
        acid_work = [[None, None, f'Определить приемистость при Р-100атм в присутствии представителя заказчика.'
                                  f'при отсутствии приемистости произвести установку СКВ по согласованию с заказчиком',
     None, None, None, None, None, None, None,
     'мастер КРС, УСРСиСТ', 1.2],
                     [None, None, f'Произвести установку СКВ соляной кислотой {acid_pr_scv}% концентрации в объеме'
                                  f' {acid_V_scv}м3 (0,7т HCL 24%)(по спец. плану, составляет старший мастер)',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 1.2],
                     [None, None, f'закачать HCL-{acid_pr_scv}% в объеме V={acid_V_scv}м3; довести кислоту до пласта '
                                  f'тех.жидкостью в объеме {volume_vn_nkt(dict_nkt)}м3 . ',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 0.6],
                     [None, None, f'реагирование 2 часа.',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 2],
                     [None, None, f'Промыть скважину тех.жидкостью круговой циркуляцией обратной промывкой в 1,5 '
                                  f'кратном обьеме. Посадить пакер на Н=2310м. Определить приемистость пласта в присутствии '
                                  f'представителя ЦДНГ (составить акт). Сорвать пакер. '
                                  f'При отсутствии приемистости СКВ повторить. При необходимости увеличить приемистость '
                                  f'методом дренирования.',
                      None, None, None, None, None, None, None,
                      'мастер КРС, УСРСиСТ', 2]]



    else:
        acid_work = []

    acid_list = ['HCl', 'HF', 'ВТ', 'Нефтекислотка']
    acid, ok = QInputDialog.getItem(self, 'Вид кислоты', 'Введите вид кислоты:', acid_list, 0, False)
    if ok and acid_list:
        self.le.setText(acid)
    acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
    acid_pr, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)





    if acid == 'HCl':
        acid_sel = f'Произвести  солянокислотную обработку {plast}  в объеме  {acid_V}м3  ({acid} - {acid_pr} %) ' \
                   f'с добавлением стабилизатора железа HiRon в объеме 70кг и деэмульгатора в объеме 50л. в ' \
                   f'присутствии представителя Заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.\n' \
                   f'(для приготовления соляной кислоты в объеме {acid_V}м3 - {acid_pr}% необходимо замешать {round(acid_V * acid_pr / 24 * 1.118, 1)}т HCL 24% и' \
                   f' пресной воды {round(acid_V - acid_V * acid_pr / 24 * 1.118, 1)}м3)' \
                   f'Согласовать с Заказчиком проведение кислотной обработки силами ООО Крезол. '
    elif acid == 'ВТ':
        vt, ok = QInputDialog.getText(None, 'Высокотехнологическая кислоты', 'Нужно расписать вид кислоты и объем')
        acid_sel = f'Произвести кислотную обработку {" ".join(CreatePZ.plast_work)} {vt}  в присутствии представителя ' \
                   f'Заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.'
    elif acid == 'HF':
        acid_sel = f'Произвести кислотную обработку пласта {plast}  в объеме  {acid_V}м3  ({acid} - {acid_pr} %) силами СК Крезол ' \
                   f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.'
    elif acid == 'Нефтекислотка':
        acid_oil, ok = QInputDialog.getInt(self, 'нефтекислотка', 'Введите объем нефти', 10, 0, 24)
        acid_sel = f'Произвести нефтекислотную обработку пласта{plast} в V=2тн товарной нефти + {acid_V}м3  (HCl - {acid_pr} %) + {acid_oil-2}т товарной нефти силами СК Крезол ' \
                   f'в присутствии представителя заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.'

    print(f'Ожидаемое показатели {CreatePZ.expected_pick_up.values()}')
    acid_list_1 = [[None, None,
     f'{acid_sel}'
     f'ОБЕСПЕЧИТЬ НАЛИЧИЕ У СОСТАВА ВАХТЫ И СИЗ ПРИ КИСЛОТНОЙ ОБРАБОТКИ',
     None, None, None, None, None, None, None,
     'мастер КРС, УСРСиСТ', 8],
    [None, None,
     ''.join([f"Закачать кислоту в объеме V={round(volume_vn_nkt(dict_nkt), 1)}м3 (внутренний "
              f"объем НКТ)" if acid_V > volume_vn_nkt(dict_nkt) else f"Закачать кислоту в "
                                                                     f"объеме {round(acid_V, 1)}м3, "
                                                                     f"довести кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) - acid_V, 1)}м3 "]),
     None, None, None, None, None, None, None,
     'мастер КРС', None],
    [None, None,
     f'посадить пакер на глубине {paker_depth}м',
     None, None, None, None, None, None, None,
     'мастер КРС', None],
    [None, None,
     ''.join(
         [f'продавить  кислоту тех жидкостью в объеме {round(volume_vn_nkt(dict_nkt) + 0.5, 1)}м3 при давлении не '
          f'более {CreatePZ.max_admissible_pressure}атм. Увеличение давления согласовать'
          f' с заказчиком' if acid_V < volume_vn_nkt(
             dict_nkt) else f'продавить кислоту оставшейся кислотой в объеме {round(acid_V - volume_vn_nkt(dict_nkt), 1)}м3 и тех жидкостью '
                            f'в объеме {round(volume_vn_nkt(dict_nkt) + 0.5, 1)}м3 при давлении не более {CreatePZ.max_admissible_pressure}атм. '
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
     'мастер КРС', 1.5]]
    if CreatePZ.curator == 'ОР':
        try:
            expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                             f'Ожидаемая приемистость по пласту {plast} ', list(CreatePZ.expected_pick_up.keys())[0], 0,
                                             1600)
            expected_P, ok = QInputDialog.getInt(self, 'Ожидаемое Давление закачки',
                                             f'Ожидаемое Давление закачки по пласту {plast}', list(CreatePZ.expected_pick_up.values())[0], 0,
                                             250)
        except:
            expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                                 f'Ожидаемая приемистость по пласту {plast} ',
                                                 100, 0,
                                                 1600)
            expected_P, ok = QInputDialog.getInt(self, f'Ожидаемое Давление закачки',
                                                 f'Ожидаемое Давление закачки по пласту {plast}',
                                                 100, 0,
                                                 250)




    for row in acid_list_1:
        acid_work.append(row)

    if CreatePZ.curator == 'ОР':
        acid_work.append([None, None,
                          f'Посадить пакер на {paker_depth}м. Произвести насыщение скважины до стабилизации давления закачки не менее 5м3. Опробовать  '
                          f'пласт {plast} на приемистость в трех режимах при Р={pressure_mode(expected_P, plast)}атм в присутствии представителя ЦДНГ. '
                          f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа до '
                          f'начала работ). В СЛУЧАЕ ПРИЕМИСТОСТИ НИЖЕ {expected_Q}м3/сут при давлении {expected_P}атм '
                          f'ДАЛЬНЕЙШИЕ РАБОТЫ СОГЛАСОВАТЬ С ЗАКАЗЧИКОМ',
                          None, None, None, None, None, None, None,
                          'мастер КРС', 2.25])
    return acid_work

# Определение трех режимов давлений при определении приемистости
def pressure_mode(mode, plast):
    from open_pz import CreatePZ

    mode = int(mode / 10) * 10
    if mode > CreatePZ.max_admissible_pressure and (plast != 'D2ps' or plast.lower() != 'дпаш'):
        mode_str = f'{mode}, {mode-10}, {mode-20}'
    elif (plast == 'D2ps' or plast.lower() == 'дпаш') and CreatePZ.region == 'ИГМ':
        mode_str = f'{120}, {140}, {160}'
    else:
        mode_str = f'{mode-10}, {mode}, {mode + 10}'
    return mode_str


# промывка скважины после кислотной обработки в зависимости от интервала перфорации и комповноки и текущего забоя
def flushingDownhole(self, paker_depth, paker_khost, paker_layout):
    from open_pz import CreatePZ
    from krs import well_volume

    if paker_layout == 2:
        flushingDownhole_list = f'Только при наличии избыточного давления или когда при проведении ОПЗ получен технологический ""СТОП":' \
                                f'произвести промывку скважину обратной промывкой ' \
                                f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
                                f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth) * 1.5, 1)}м3 ' \
                                f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
    elif paker_depth + paker_khost >= CreatePZ.current_bottom or (paker_depth + paker_khost < CreatePZ.current_bottom and CreatePZ.work_pervorations_approved == True):
        flushingDownhole_list = f'Допустить компоновку до глубины {CreatePZ.current_bottom}м. Промыть скважину обратной промывкой ' \
                                f'по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не '\
                                f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth + paker_khost)*1.5,1)}м3 '\
                                f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'
    elif paker_depth + paker_khost < CreatePZ.current_bottom and CreatePZ.work_pervorations_approved == False:
        flushingDownhole_list = f'Допустить пакер до глубины {int(CreatePZ.perforation_roof-5)}м. (на 5м выше кровли интервала перфорации), ' \
                                f'низ НКТ до глубины {CreatePZ.perforation_roof - 5 + paker_khost}м) ' \
                                f'Промыть скважину обратной промывкой по круговой циркуляции  жидкостью уд.весом {CreatePZ.fluid_work} при расходе жидкости не ' \
                                f'менее 6-8 л/сек в объеме не менее {round(well_volume(self, paker_depth + paker_khost) * 1.5, 1)}м3 ' \
                                f'в присутствии представителя заказчика ДО ЧИСТОЙ ВОДЫ.'

    return flushingDownhole_list