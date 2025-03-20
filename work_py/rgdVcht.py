from PyQt5.QtWidgets import QMessageBox

import data_list
from work_py.descent_gno import GnoDescentWindow

def select_ovtr(self):
    ovtr = 'ОВТР 4ч' if self.data_well.region == 'ЧГМ' else 'ОВТР 6ч'
    return ovtr


def rgd_without_paker(self):
    rgd_list = [
        [f'СП НКТ 300м', None,
         f'Спустить с замером воронку на НКТ до глубины 300м с замером, шаблонированием шаблоном '
         f'{self.data_well.nkt_template}мм . '
         f'(При СПО первых десяти НКТ на спайдере дополнительно устанавливать элеватор ЭХЛ)',
         None, None, None, None, None, None, None,
         'мастер КРС', 1.3],
        [None, None,
         f'Произвести  монтаж ГИС согласно схемы  №8 при работе ГИС с утвержденной главным инженером  '
         f'{data_list.DICT_CONTRACTOR[data_list.contractor]["Дата ПВО"]}г '
         f'Обвязать устье скважины с ЕДК на жесткую линию. Опрессовать ПВО максимально допустимое давление '
         f'опрессовки э/колонны на '
         f'устье {self.data_well.max_admissible_pressure.get_value}атм, по невозможности на давление поглощения, но не'
         f' менее 30атм '
         f'в течении 30мин Провести практическое обучение вахт по сигналу "выброс" с записью в журнале проведения '
         f'учебных тревог',
         None, None, None, None, None, None, None,
         'мастер КРС', 0.75],
        [select_ovtr(self), None,
         select_ovtr(self),
         None, None, None, None, None, None, None,
         'мастер КРС', ''.join([i for i in select_ovtr(self) if i.isdigit()])],
        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". Составить'
         f' акт готовности скважины и передать его начальнику партии. При необходимости подготовить площадку'
         f' напротив мостков для постановки партии ГИС.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [f'РГД по колонне при закачке не менее {GnoDescentWindow.determination_injection_pressure(self)}атм',
         None,
         f'Произвести запись по тех.карте 2.3.1: Определение профиля приемистости скважины и оценка технического'
         f' состояния '
         f'эксплуатационной колонны при закачке (скважинная аппаратура на кабеле, НКТ подняты). '
         f'Давление закачки должно быть согласно ожидаемой закачки ППД. при закачке не менее '
         f'{GnoDescentWindow.determination_injection_pressure(self)}атм '
         f'при открытой затрубной задвижке',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 20]]
    ori = QMessageBox.question(None, 'ОРИ', 'Нужна ли интерпретация?')
    if ori == QMessageBox.StandardButton.Yes:

        ori = f'Интерпретация данных ГИС'
        rgd_list.append([f'ОРИ', None, ori,
                         None, None, None, None, None, None, None,
                         'Мастер КРС, подрядчик по ГИС', 8])
        rgd_list.append([None, None,
                         f'Поднять компоновку с доливом скважины в объеме 0.3м3 тех. жидкостью  уд.весом'
                         f' {self.data_well.fluid_work}',
                         None, None, None, None, None, None, None,
                         'Мастер КРС', 1.3])
    else:
        rgd_list.append([None, None,
                         f'Поднять компоновку с доливом скважины в объеме 0.3м3 тех. жидкостью  уд.весом '
                         f'{self.data_well.fluid_work}',
                         None, None, None, None, None, None, None,
                         'Мастер КРС', 1.3])
    return rgd_list


def rgd_with_paker(self):
    work_list = [
        [select_ovtr(self), None,
         select_ovtr(self),
         None, None, None, None, None, None, None,
         'мастер КРС', ''.join([i for i in select_ovtr(self) if i.isdigit()])],
        [None, None,
         f'Вызвать геофизическую партию. Заявку оформить за 16 часов через ЦИТС {data_list.contractor}". '
         f'Составить'
         ' акт готовности скважины и передать его начальнику партии. При необходимости подготовить площадку'
         ' напротив мостков для постановки партии ГИС.',
         None, None, None, None, None, None, None,
         'мастер КРС', None],
        [f'ГИС РГД', None,
         f'Произвести запись по тех.карте 2.3.2: определение профиля приемистости и оценку технического '
         f'состояния '
         f'эксплуатационной колонны и НКТ при закачке не менее {GnoDescentWindow.determination_injection_pressure(self)}атм '
         f'при открытой затрубной задвижке',
         None, None, None, None, None, None, None,
         'Мастер КРС, подрядчик по ГИС', 20],
        [None, None,
         f'Интерпретация данных ГИС',
         None, None, None, None, None, None, None,
         'мастер КРС, подрядчик по ГИС', 8]]
    return work_list
