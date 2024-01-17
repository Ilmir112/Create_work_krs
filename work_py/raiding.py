from PyQt5.QtWidgets import QInputDialog, QMessageBox

from work_py.alone_oreration import fluid_change
from work_py.rationingKRS import descentNKT_norm, liftingNKT_norm, well_volume_norm
from open_pz import CreatePZ
class Raid(CreatePZ):
    def __init__(self,  parent = None):
        super(CreatePZ, self).__init__(parent)
        
        CreatePZ.raidingColumn()
    def raidingColumn(self):

        from work_py.opressovka import paker_diametr_select
        from work_py.template_work import well_volume
        from work_py.advanted_file import raiding_interval,raid
        print(f'До отрайбирования {[CreatePZ.dict_perforation[plast]["отрайбировано"] for plast in CreatePZ.plast_work]}')

        ryber_diam = paker_diametr_select(CreatePZ.current_bottom) + 3
        if 'ПОМ' in str(CreatePZ.paker_do["posle"]).upper() and '122' in str(CreatePZ.paker_do["posle"]):
            ryber_diam = 126
        ryber_diam, ok = QInputDialog.getInt(None, 'Диаметр райбера',
                                                  f'Введите диаметр райбера',
                                                  int(ryber_diam), 70,
                                                  200)
        nkt_pod = 0
        if CreatePZ.column_additional == True:
            nkt_pod = ['60мм' if CreatePZ.column_additional_diametr <110 else '73мм со снятыми фасками']
            nkt_pod = ''.join(nkt_pod)

        nkt_diam = ''.join(['73мм' if CreatePZ.column_diametr > 110 else '60мм'])

        ryber_str_EK = f'райбер-{ryber_diam} для ЭК {CreatePZ.column_diametr}мм х {CreatePZ.column_wall_thickness}мм +' \
                       f' забойный двигатель Д-106 +НКТ{nkt_diam}м 20м + репер '
        ryber_str_DP = f'райбер-{ryber_diam} для ЭК {CreatePZ.column_additional_diametr}мм х ' \
                    f'{CreatePZ.column_additional_wall_thickness}мм + забойный двигатель Д-76 +НКТ{nkt_pod}мм 20м + репер + ' \
                    f'НКТ{nkt_pod} {round(CreatePZ.current_bottom - float(CreatePZ.head_column_additional))}м'

        if CreatePZ.column_additional == False or (CreatePZ.column_additional == True and CreatePZ.head_column_additional >= CreatePZ.current_bottom):
            ryber_key = 'райбер в ЭК'
            ryber_str = ryber_str_EK
        elif CreatePZ.column_additional == True:
            ryber_key = 'райбер в ДП'
            ryber_str = ryber_str_DP

        rayber_sel = ['райбер в ЭК', 'райбер в ДП']
        rayber_dict = {'райбер в ЭК': ryber_str_EK, 'райбер в ДП': ryber_str_DP}

        rayber, ok = QInputDialog.getItem(self, 'Спуcкаемое  оборудование', 'выбор спуcкаемого оборудования',
                                            rayber_sel, rayber_sel.index(ryber_key), False)

        if ok and rayber_sel:
            self.le.setText(ryber_str)

        ryber_str = rayber_dict[rayber]
        result = {}
        for key, value in rayber_dict.items():
            result[value] = key
        ryber_key = result[ryber_str]
        raiding_interval_tuple = raiding_interval(ryber_key)
        print(f' интервал райбирования {raiding_interval_tuple, len(raiding_interval_tuple)}')
        if raiding_interval_tuple == '':
            while raiding_interval_tuple != '':
                raiding_interval_tuple, ok = QInputDialog.getText(self,'интервал райбирование', 'Введите интервал райбирования')
            raiding_interval_tuple = [raiding_interval_tuple.split('-')]
        if len(raiding_interval_tuple) != 0:
            krovly_raiding = int(raiding_interval_tuple[0][0])
        else:
            krovly_raiding = CreatePZ.perforation_roof

        raiding_interval = raid(raiding_interval_tuple)
        ryber_list = [
            [None, None,
             f'Спустить {ryber_str}  на НКТ{nkt_diam} до Н={krovly_raiding}м с замером, '
             f'шаблонированием шаблоном 59,6мм (При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ). '
             f'В случае разгрузки инструмента  при спуске, проработать место посадки с промывкой скв., составить акт.'
             f'СКОРОСТЬ СПУСКА НЕ БОЛЕЕ 1 М/С (НЕ ДОХОДЯ 40 - 50 М ДО ПЛАНОВОГО ИНТЕРВАЛА СКОРОСТЬ СПУСКА СНИЗИТЬ ДО 0,25 М/С). '
             f'ЗА 20 М ДО ЗАБОЯ СПУСК ПРОИЗВОДИТЬ С ПРОМЫВКОЙ',
             None, None, None, None, None, None, None,
             'мастер КРС', descentNKT_norm(krovly_raiding, 1.2)],
            [None, None, f'Собрать промывочное оборудование: вертлюг, ведущая труба (установить вставной фильтр под ведущей трубой), '
                         f'буровой рукав, устьевой герметизатор, нагнетательная линия. Застраховать буровой рукав за вертлюг. ',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 0.6],
            [None, None,
             f'Произвести райбирование ЭК в инт. {raiding_interval}м с наращиванием, с промывкой и проработкой 5 раз каждого наращивания. '
             f'Составить акт. (Вызов представителя осуществлять телефонограммой за 12 часов, с подтверждением за 2 часа '
             f'до начала работ) Работы производить согласно сборника технологических регламентов и инструкций в присутствии'
             f' представителя заказчика. Допустить до текущего забоя {CreatePZ.current_bottom}м.',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', 8],
            [None, None,
             f'ПРИМЕЧАНИЕ: РАСХОД РАБОЧЕЙ ЖИДКОСТИ 8-10 Л/С;'
             f' ОСЕВАЯ НАГРУЗКА НЕ БОЛЕЕ 75% ОТ ДОПУСТИМОЙ НАГРУЗКИ (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ГЗД И ДОЛОТА);'
             f' РАБОЧЕЕ ДАВЛЕНИЕ 4-10 МПА (УТОЧНИТЬ ПО ПАСПОРТУ ЗАВЕЗЁННОГО ВЗД);'
             f' ПРЕДУСМОТРЕТЬ КОМПЕНСАЦИЮ РЕАКТИВНОГО МОМЕНТА НА ВЕДУЩЕЙ ТРУБЕ))',
             None, None, None, None, None, None, None,
             'Мастер КРС, УСРСиСТ', None],
            [None, None,
             f'Промыть скважину круговой циркуляцией  тех жидкостью уд.весом {CreatePZ.fluid_work}  '
             f'в присутствии представителя заказчика в объеме {round(well_volume()*2,1)}м3. Составить акт.',
             None, None, None, None, None, None, None,
             'мастер КРС, предст. заказчика', well_volume_norm(well_volume())],
            [None, None,
             f'Поднять  {ryber_str} на НКТ{nkt_diam}мм с глубины {CreatePZ.current_bottom}м с доливом скважины в '
             f'объеме {round(CreatePZ.current_bottom*1.12/1000, 1)}м3 тех. жидкостью  уд.весом {CreatePZ.fluid_work}',
             None, None, None, None, None, None, None,
             'мастер КРС', liftingNKT_norm(CreatePZ.current_bottom,1.2)]]

        print(f' после отрайбирования {[CreatePZ.dict_perforation[plast]["отрайбировано"] for plast in CreatePZ.plast_work]}')
        if len(CreatePZ.plast_work) == 0:
            acid_true_quest = QMessageBox.question(self, 'Необходимость смены объема',
                                                   'Нужно ли изменять удельный вес?')
            if acid_true_quest == QMessageBox.StandardButton.Yes:
                for row in fluid_change(self):
                    ryber_list.insert(-2, row)
        return ryber_list



