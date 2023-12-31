from PyQt5.QtWidgets import QInputDialog, QMessageBox

def gnkt_work(self):
    from open_pz import CreatePZ
    import H2S

    acid_true = True
    acid_V = 0
    acid_pr = 0
    acid = 0
    V_gntk = round(2327 * 0.74 / 1000, 1)

    try:
        expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                             f'Ожидаемая приемистость по пласту  ',
                                             list(CreatePZ.expected_pick_up.keys())[0], 0,
                                             1600)
        expected_P, ok = QInputDialog.getInt(self, 'Ожидаемое Давление закачки',
                                             f'Ожидаемое Давление закачки по пласту ',
                                             list(CreatePZ.expected_pick_up.values())[0], 0,
                                             250)
    except:
        expected_Q, ok = QInputDialog.getInt(self, 'Ожидаемая приемистость ',
                                             f'Ожидаемая приемистость по пласту  ',
                                             100, 0,
                                             1600)
        expected_P, ok = QInputDialog.getInt(self, 'Ожидаемое Давление закачки',
                                             'Ожидаемое Давление закачки по пласту {plast}',
                                             100, 0,
                                             250)


    acid_true_quest  = QMessageBox.question(self, 'Необходимость кислоты', 'Планировать кислоту?')
    if acid_true_quest == QMessageBox.StandardButton.Yes:
        acid_true_quest = True
    else:
        acid_true_quest = False
    fluid_work_insert, ok = QInputDialog.getDouble(self,'Рабочая жидкость', 'Введите удельный вес рабочей жидкости', 1.02, 0.87, 2, 2)


    if 2 in CreatePZ.cat_H2S_list or '2' in CreatePZ.cat_H2S_list:
        fluid_work = f'{fluid_work_insert}г/см3 с добавлением поглотителя сероводорода ХИМТЕХНО 101 Марка А из' \
                     f' расчета {H2S.calv_h2s(self,CreatePZ.cat_H2S_list[0], CreatePZ.H2S_mg[0], CreatePZ.H2S_pr[0])}кг/м3 '
    else:
        fluid_work = f'{fluid_work_insert}г/см3 '
    if acid_true_quest == False:
        V_rast, ok = QInputDialog.getDouble(self,'Растворитель', 'Введите объем растворителя', 2, 0.1, 30, 1)
        acid_true = False

    else:
        V_rast, ok  = QInputDialog.getDouble(self, 'Растворитель', 'Введите объем растворителя', 2, 0.1, 30, 1)
        acid_list = ['HCl', 'HF', 'ВТ']
        acid, ok = QInputDialog.getItem(self, 'Вид кислоты', 'Введите вид кислоты: HF, HCl', acid_list, 0, False)
        if ok and acid_list:
            self.le.setText(acid)
        acid_V, ok = QInputDialog.getDouble(self, 'Объем кислоты', 'Введите объем кислоты:', 10, 0.5, 300, 1)
        acid_pr, ok = QInputDialog.getInt(self, 'концентрация кислоты', 'Введите концентрацию кислоты', 15, 2, 24)
    acid_sel = 0
    if acid == 'HCl':
        acid_sel = f'Произвести  солянокислотную обработку {" ".join(CreatePZ.plast_work)}  в объеме  {acid_V}м3  ({acid} - {acid_pr} %) силами/' \
                   f' Крезол НС с протяжкой БДТ вдоль интервалов перфорации {CreatePZ.perforation_roof}-{CreatePZ.perforation_sole}м (снизу вверх) в ' \
                   f'присутствии представителя Заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.\n' \
                   f' (для приготовления соляной кислоты в объеме {acid_V}м3 - {acid_pr}% необходимо замешать {round(acid_V*acid_pr/24*1.118,1)}т HCL 24% и пресной воды {round(acid_V-acid_V*acid_pr/24*1.118,1)}м3)'
    elif acid == 'ВТ':
        vt, ok = QInputDialog.getText(None, 'Высокотехнологическая кислоты', 'Нужно расписать вид кислоты и объем')
        acid_sel = f'Произвести кислотную обработку пласта {" ".join(CreatePZ.plast_work)} {vt}  силами Крезол ' \
                   f'НС с протяжкой БДТ вдоль интервалов перфорации {CreatePZ.perforation_roof}-'\
           f'{CreatePZ.perforation_sole}м (снизу вверх) в присутствии представителя '\
           f'Заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.'
    elif acid == 'HF':
        acid_sel = f'Произвести  солянокислотную обработку пласта {" ".join(CreatePZ.plast_work)}  в объеме  {acid_V}м3  ({acid} - {acid_pr} %) силами Крезол '\
           f'НС с протяжкой БДТ вдоль интервалов перфорации {CreatePZ.perforation_roof}-'\
           f'{CreatePZ.perforation_sole}м (снизу вверх) в присутствии представителя '\
           f'Заказчика с составлением акта, не превышая давления закачки не более Р={CreatePZ.max_admissible_pressure}атм.'
    paker_opr = [None, 5, f'Опрессовать пакер на {CreatePZ.max_admissible_pressure}атм с выдержкой 30 мин с оформлением соответствующего акта в присутствии '\
    f'представителя представителя ЦДНГ',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады, представитель Заказчика', 1]
    if CreatePZ.H_F_paker_do["do"] == 0:
        print(25)
        H_F_paker_do = sum(list(CreatePZ.dict_nkt.values()))
        print(H_F_paker_do)
        if H_F_paker_do >= CreatePZ.current_bottom:
            H_F_paker_do, ok = QInputDialog.getDouble(self, 'глубина НКТ',
                                                        'Введите Глубины башмака НКТ',500 , 0, CreatePZ.current_bottom)
    else:
        H_F_paker_do = CreatePZ.H_F_paker_do['do']
    gnkt_opz =[
     [None,  None, 'Порядок работы', None, None, None, None, None, None, None, None, None],
        [None, 'п/п', 'Наименование работ', None, None, None, None, None, None, None,
         'Ответственный', 'Нормы'],
     [None,
      None, 'ВНИМАНИЕ: Перед спуском и вовремя проведения СПО бурильщикам и мастеру производить осмотр ГНКТ на наличие '
            '"меток" на г/трубы, установленных запрещённым способом.\nПри обнаружении - доложить руководству ООО "Ойл-Сервис" '
            'по согласованию произвести отрезание ГНКТ выше "метки" с составлением АКТа и указанием метража отрезанного участка ГНКТ. '
            'Установку меток на г/трубе производить ТОЛЬКО безопасным способом - (краской, лентой фум, шкемарём, и тд.) '
            'КАТЕГОРИЧЕСКИ ЗАПРЕЩАЕТСЯ устанавливать "метки" опасным способом - вальцевателем (труборезом) или другим инструментом - '
            'который причиняет механические повреждения на теле г/трубы и может привести к снижению прочностных характеристик ГНКТ.  '
            'Запросить у Заказчика внутренние диаметры спущенной компоновки для исключения заклинивания низа компоновки',
          None, None, None, None, None, None, None,
            'Мастер КРС,бурильщик', None],
        [None, None, 'Провести приемку скважины в ремонт у Заказчика с составлением акта. Переезд бригады КРС на скважину. '
                     'Подготовительные работы к КРС. Расставить технику и оборудование.Составить Акт .',
         None, None, None, None, None, None, None, 'Мастер КРС, представитель Заказчика', 'расчет нормы на переезд '],
    [None, None, 'Провести инструктаж по предупреждению ГНВП и ОФ при КРС, а также по плану ликвидации аварий при '
                 'производстве работ с записью в журнале (инструктаж, в обязательном порядке, проводить с обеими вахтами бригады).',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', None],
    [None, 3, 'Мастеру бригады - запретить бурильщикам оставлять устье скважины незагерметизированным независимо '
              'от продолжительности перерывов в работе.',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', None],
    [None, 4, 'Проводить замеры газовоздушной среды согласно утвержденного графика',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', None],

    [None, 6, 'Провести работы по монтажу колтюбинговой установки'
              ' в соответствии с технологической инструкцией, федеральных норм и правила в области промышленной безопасности'
              ' «Правила безопасности в нефтяной и газовой\
         промышленности»  РОСТЕХНАДЗОР Приказ №1 от 15.12.2020г и РД 153-39-023-97.',
     None, None, None, None, None, None, None,
        'Мастер ГНКТ, состав бригады ГНКТ', None],
    [None, 7, 'Все операции при производстве выполнять в соответствии с технологической инструкцией, федеральных норм и правила в'
              'области промышленной безопасности "Правила безопасности в нефтяной и газовой промышленности"  от 15.12.2020г '
              'и РД 153-39-023-97.',
     None, None, None, None, None, None, None,
        'Мастер ГНКТ, состав бригады', None],
    [None, 8, 'Произвести монтаж колтюбингового оборудования ПП4- 80х70 (при изменении тип и марку ПВО указывает мастер) '
              '______________________  (ПВО согласно утверждённой схемы № 5 от 14.10.2021г ("Обвязки устья при глушении '
              'скважин, после проведения гидроразрыва пласта и работы на скважинах ППД с оборудованием койлтюбинговых '
              'установок на месторождениях ООО "Башнефть-Добыча")',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, бур-к КРС, машинист подъёмника, пред. УСРСиСТ', 3.5],
        [None, 9, 'Пусковой комиссии в составе мастера и членов бригады согласно положения от 2015г.'
                  '"Положение о проведении пусковой комиссии при ТКРС" произвести проверку готовности бригады '
                  'для ремонта скважины с последующим составлением акта.',
         None, None, None, None, None, None, None,
            'Мастер ГНКТ, бур-к КРС, машинист подъёмника, пред. УСРСиСТ', 0.5],
    [None, 10, f'Перед началом опрессовки принять все требуемые меры безопасности.  Подготовиться к опрессовке.'
               f' Удостовериться в том, рабочая зона вокруг линий высокого давления обозначена знаками безопосности.'
               f' Запустить систему регистрации СОРП. Оповестить всех людей на кустовой площадке о проведении опрессовки.'
               f' Опрессовать все нагнетательные линии на {CreatePZ.max_admissible_pressure*1.5}атм. Опрессовать  выкидную линию '
               f'от устья скважины до желобной ёмкости на {round(CreatePZ.max_admissible_pressure*1.5,1)}атм '
               f'(надёжно закрепить, оборудовать дроссельными задвижками)',
         None, None, None, None, None, None, None,
            'Мастер ГНКТ, представ.БВО (вызов по телефонограмме при необходимости)', 'факт'],
    [None, 11, f'При закрытой центральной задвижке фондовой арматуры. Опрессовать превентор, глухие и трубные  плашки на '
               f'устье скважины на Р={CreatePZ.max_admissible_pressure}атм с выдержкой 30 мин (опрессовку ПВО зафиксировать'
               f' в вахтовом журнале). Оформить соответствующий акт в присутствии представителя Башкирского военизированного '
               f'отряда с выдачей разрешения на дальнейшее проведение работ (вызов представителя БВО по телефонограмме за 24 '
               f'часа).  Провести учебно-тренировочное занятие по сигналу "Выброс" с записью в журнале.',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, представ.БВО (вызов по телефонограмме при необходимости)', 0.47],
    [None, 12, f'Произвести спуск БДТ + насадка 5 каналов до {CreatePZ.current_bottom}м (забой) с промывкой скважины '
               f'мин.водой уд.веса {fluid_work} с фиксацией давления промывки, расход жидкости не менее 200л\\мин, объем '
               f'промывки не менее 1 цикла  со скоростью 5м/мин. Убедиться в наличии свободного прохода КНК-2 (при '
               f'прохождении насадкой лубрикаторной задвижки, пакера, воронки скорость спуска минимальная 2м/мин). При '
               f'посадке ГНКТ в колонне НКТ произвести закачку (на циркуляции) растворителя в объёме 0,2 м3 в ГНКТ. '
               f'Произвести продавку (на циркуляции) растворителя АСПО до башмака ГНКТ мин.водой уд.вес {fluid_work} '
               f'в объёме 2,0м3. Закрыть Кран на тройнике устьевого оборудования.  Стоянка на реакции 2 часа. Промывка колонны '
               f'НКТ - не менее1 цикла. Составить Акт. Промывка подвески ФНКТ по согласованию ПТО и ЦДНГ',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, представитель Заказчика', 2.04],
    [None, 13, f'Промыть НКТ и скважину с гл.{CreatePZ.current_bottom}м мин.водой уд.веса {fluid_work}  в 1 цикл'
               f' с добавлением 1т растворителя с составлением соответствующего акта. При появлении затяжек или '
               f'посадок при спуско-подъемных операциях произвести интенсивную промывку осложненного участка скважины. ',
        None, None, None, None, None, None, None,
             'Мастер ГНКТ, состав бригады, представит. Заказчика', 0.84],
    [None, 14, f'Произвести  обработку НКТ {V_rast}м3 растворителя в присутствии представителя Заказчика при открытом'
               f' малом затрубном пространстве на циркуляции.  Произвести продавку растворителя АСПО до башмака ГНКТ '
               f'мин.водой уд.вес {fluid_work} в объёме 2,2м3 не превышая давления закачки не более  Р={CreatePZ.max_admissible_pressure}атм. ',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ,  состав бригады, представитель Заказчика', 1.92],
    [None, 15, f'Приподнять БДТ до {int(H_F_paker_do) -20}м. Произвести круговую циркуляцию растворителя в течении 2часов. Составить Акт',
         None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', 2.06],

    [None, 22, f'Спустить БДТ до забоя. Промыть скважину от продуктов реакции кислоты мин.водой  {fluid_work}  с составлением'
               f'соответствующего акта. \n ПРИ ПОЯВЛЕНИИ ЗАТЯЖЕК ИЛИ ПОСАДОК ПРИ СПУСКО-ПОДЪЕМНЫХ ОПЕРАЦИЯХ ПРОИЗВЕСТИ '
               f'ИНТЕНСИВНУЮ ПРОМЫВКУ ОСЛОЖНЕННОГО УЧАСТКА СКВАЖИНЫ ',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады, представитель Заказчика', 0.93],
    [None, 23, f'Произвести гидросвабирование пласта в интервале {CreatePZ.perforation_roof}-'
               f'{CreatePZ.perforation_sole}м (закрыть затруб, произвести задавку в пласт '
               f'жидкости при не более Рзак={CreatePZ.max_admissible_pressure}атм при установленном герметичном пакере. '
               f'Операции по задавке и изливу произвести 3-4 раза в зависимости от приёмистости). ',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады, представитель Заказчика', 1],
    [None, 24, f'Исследовать скважину на приёмистость при Рзак={expected_P}атм с составлением акта в '
               f' в присутствии представителя ЦДНГ с составлением соответствующего акта (для вызова представителя давать '
               f'телефонограмму в ЦДНГ). Определение приёмистости производить после насыщения пласта не менее 6м3 или '
               f'при установившемся давлении закачки, но не более 1 часов. При недостижении запланированной приёмистости {expected_Q}м3/сут при Р= {expected_P}атм дальнейшие работы производить по согласованию с Заказчиком. Составить Акт ',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады, представитель Заказчика', 1.4],
    [None, 25, f'Вызвать телефонограммой представителя Заказчика для замера приёмистости  при '
               f'Рзак={expected_P}атм прибором "Панаметрикс".Перед запуском скважины '
               f'произвести сброс жидкости с водовода в объёме 3-5м3 в ЕДК в зависимости от наличия нефтяной эмульсии на '
               f'выходе в технологическую емкость для предупреждения повторной кольматации ПЗП шламом с водовода и '
               f'произвести замер приемистости переносным прибором после насыщения скважины в течении 1-2 часа от КНС. '
               f'При недостижении запланированной приёмистости дальнейшие работы производить по согласованию с  Заказчиком. '
               f'Составить Акт ',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады, представитель Заказчика УСРСиСТ' , 1.4],
    [None, 26, f'Поднять БДТ до устья с промывкой скважины мин.водой {fluid_work} . Составить Акт. Согласовать с '
               f'Заказчиком утилизацию жидкости в коллектор.',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', 1.56],
    [None, 27, 'Произвести демонтаж колтюбингового оборудования и линии обвязки желобной системы.',
         None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', 2.25],
    [None, 28, 'Запустить скважину под закачку. ',
         None, None, None, None, None, None, None,
         'Мастер ГНКТ, состав бригады', None],
    [None, 29, 'Сдать территорию скважину представителю Заказчика. Составить Акт.',
        None, None, None, None, None, None, None,
        'Мастер ГНКТ, состав бригады, представитель Заказчика', None],
    ]

    opz = [[None, 16, f'Допустить БДТ до забоя. Промыть скважину  мин.водой уд.веса {fluid_work}  с составлением '
                      f'соответствующего акта. При отсутствии циркуляции дальнейшие промывки исключить. Определить '
                      f'приемистость пласта в трубное пространство при давлении не более {CreatePZ.max_admissible_pressure}атм'
                      f'  (перед определением приемистости произвести закачку тех.воды не менее 6м3 или при установившемся '
                      f'давлении закачки, но не более 1 часа). Установить БДТ на гл.{CreatePZ.current_bottom}м.',
         None, None, None, None, None, None, None,
           'Мастер ГНКТ, состав бригады, представитель Заказчика', 1.33],
    [None, 17, acid_sel,
         None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады, подрядчик по ОПЗ', 2],
    [None, 18, f'Закачку {V_gntk}м3 кислоты производить при открытом малом затрубном пространстве на циркуляции. Закачку оставшейся '
               f'кислоты в объеме {acid_V-V_gntk}м3 производить при закрытом затрубном пространстве. Составить Акт.',
         None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', 2.88],
    [None, 19, f'Продавить кислоту в пласт мин.водой уд.веса {fluid_work} в объёме 3м3 при давлении не более '
               f'{CreatePZ.max_admissible_pressure}атм. Составить Акт',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', 1.11],
    [None, 20, f'Приподнять БДТ на {int(H_F_paker_do)-20}м. Стоянка на реакции 2 часа. В СЛУЧАЕ ОТСУТСТВИЯ ДАВЛЕНИЯ '
               f'ПРОДАВКИ ПРИ СКО, РАБОТЫ ПРОИЗВОДИМ БЕЗ РЕАГИРОВАНИЯ.СОСТАВИТЬ АКТ)',
        None, None, None, None, None, None, None,
        'Мастер ГНКТ, состав бригады', 3.06],
    [None, 21, 'Произвести разрядку скважины для извлечения продуктов реакции кислоты в объёме не менее объёма закаченной кислоты '
               '+ объём малого затрубного пространства (из расчета 1,88л на 1 м пространства между 73мм колонной НКТ и БДТ;'
               ' 0,46л между 60мм НКТ и БДТ; 3,38л между 89мм НКТ и БДТ) + 3м3. Разрядку производить до чистой промывочной '
               'жидкости (без признаков продуктов реакции кислоты), но не более 2 часов.  Зафиксировать избыточное давление '
               'на устье скважины, объём и описание скважинной жидкости на выходе с отражением их в акте, суточном рапорте'
               'работы бригад. Составить Акт.',
        None, None, None, None, None, None, None,
            'Мастер ГНКТ, состав бригады', 1]]



    n = 17
    if CreatePZ.H_F_paker_do['do'] != 0: # вставка строк при наличии пакера
        gnkt_opz.insert(7, paker_opr)
        n +=1

    if acid_true_quest == True: # Вставка строк при необходимости ОПЗ
        for i in opz:
            gnkt_opz.insert(n, i)
            n += 1
    else:
        pass

    for i in range(3, len(gnkt_opz)): # нумерация работ
        gnkt_opz[i][1] = i - 2

    return gnkt_opz

